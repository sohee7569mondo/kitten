"""내 컴퓨터에서만 도는 작은 편집 서버.

바깥에 열지 않습니다(127.0.0.1). 라이브러리를 더 깔지 않으려고
파이썬에 들어 있는 http.server로 만들었습니다.
"""

from __future__ import annotations

import json
import mimetypes
import threading
import traceback
import webbrowser
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .. import pipeline, source, tts
from ..project import Project, Scene, folders
from ..render import render_cut

STATIC = Path(__file__).parent / "static"


class Job:
    """한 번에 하나만 도는 작업(대본 만들기 / 렌더)."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.running = False
        self.done = 0
        self.total = 0
        self.message = ""
        self.error = ""
        self.log: list[str] = []

    def snapshot(self) -> dict:
        return {
            "running": self.running,
            "done": self.done,
            "total": self.total,
            "message": self.message,
            "error": self.error,
            "log": self.log[-40:],
        }

    def start(self, fn) -> bool:
        with self.lock:
            if self.running:
                return False
            self.running = True
            self.done = 0
            self.total = 0
            self.message = "시작합니다"
            self.error = ""
            self.log = []

        def run() -> None:
            try:
                fn(self)
                self.message = "완료"
            except Exception as exc:  # 사용자에게 그대로 보여줍니다
                self.error = str(exc)
                self.log.append("오류: " + str(exc))
                traceback.print_exc()
            finally:
                self.running = False

        threading.Thread(target=run, daemon=True).start()
        return True

    def say(self, text: str) -> None:
        self.message = text
        self.log.append(text)

    def progress(self, done: int, total: int, message: str) -> None:
        self.done, self.total = done, total
        self.say(message)


JOB = Job()


class Handler(BaseHTTPRequestHandler):
    workspace: Path = Path("projects")

    # --- 뼈대 ---------------------------------------------------------
    def log_message(self, fmt, *args):  # 콘솔을 조용하게
        pass

    def _send(self, code: int, body: bytes, ctype: str, extra: dict | None = None) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, data, code: int = 200) -> None:
        self._send(code, json.dumps(data, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8")

    def _fail(self, exc: Exception, code: int = 400) -> None:
        self._json({"error": str(exc)}, code)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def _dir(self, name: str) -> Path:
        """작업 폴더 밖으로 못 나가게 묶어둡니다."""
        p = (self.workspace / name).resolve()
        root = self.workspace.resolve()
        if root != p and root not in p.parents:
            raise ValueError("작업 폴더 밖입니다.")
        return p

    # --- GET ----------------------------------------------------------
    def do_GET(self) -> None:
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path in ("/", "/index.html"):
                body = (STATIC / "index.html").read_bytes()
                return self._send(200, body, "text/html; charset=utf-8")

            if u.path == "/api/projects":
                self.workspace.mkdir(parents=True, exist_ok=True)
                names = sorted(
                    p.name for p in self.workspace.iterdir()
                    if p.is_dir() and (p / "project.json").exists()
                )
                return self._json({"projects": names, "workspace": str(self.workspace.resolve())})

            if u.path == "/api/state":
                folder = self._dir(q["dir"][0])
                project = Project.load(folder)
                data = asdict(project)
                data["_cuts"] = {
                    s.index: (folder / f"cuts/cut_{s.index:03d}.mp4").exists()
                    for s in project.scenes
                }
                data["_out"] = (folder / "out.mp4").exists()
                data["_dir"] = str(folder)
                return self._json(data)

            if u.path == "/api/job":
                return self._json(JOB.snapshot())

            if u.path == "/api/voices":
                return self._json({"voices": tts.KO_VOICES})

            if u.path == "/media":
                folder = self._dir(q["dir"][0])
                rel = q["path"][0].lstrip("/")
                target = (folder / rel).resolve()
                if folder != target and folder not in target.parents:
                    raise ValueError("폴더 밖입니다.")
                if not target.exists():
                    return self._json({"error": "파일이 없습니다"}, 404)
                return self._serve_file(target)

            return self._json({"error": "없는 주소"}, 404)
        except Exception as exc:
            self._fail(exc)

    def _serve_file(self, path: Path) -> None:
        """영상 재생용. 브라우저가 구간 요청을 하면 그 부분만 보냅니다."""
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        size = path.stat().st_size
        rng = self.headers.get("Range")
        if rng and rng.startswith("bytes="):
            first, _, last = rng[6:].partition("-")
            start = int(first or 0)
            end = int(last) if last else size - 1
            end = min(end, size - 1)
            with open(path, "rb") as fh:
                fh.seek(start)
                chunk = fh.read(end - start + 1)
            self.send_response(206)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(len(chunk)))
            self.end_headers()
            self.wfile.write(chunk)
            return
        self._send(200, path.read_bytes(), ctype, {"Accept-Ranges": "bytes"})

    # --- POST ---------------------------------------------------------
    def do_POST(self) -> None:
        u = urlparse(self.path)
        try:
            body = self._body()

            if u.path == "/api/new":
                name = (body.get("name") or "").strip()
                if not name:
                    raise ValueError("프로젝트 이름을 적어주세요.")
                folder = self._dir(name)
                srcs = [s.strip() for s in (body.get("sources") or []) if s.strip()]
                opts = dict(
                    keyword=body.get("keyword", "").strip(),
                    sources=srcs,
                    scenes=int(body.get("scene_count") or 8),
                    style=body.get("style") or "정보 전달 (뉴스형)",
                    voice=body.get("voice") or "ko-KR-SunHiNeural",
                    tts_provider="edge" if body.get("tts", True) else "none",
                )
                if not opts["keyword"] and not srcs:
                    raise ValueError("주제 키워드나 소재 중 하나는 있어야 합니다.")

                def work(job: Job) -> None:
                    job.total = 4
                    pipeline.make_project(folder, log=job.say, **opts)
                    job.done = 4

                if not JOB.start(work):
                    raise RuntimeError("이미 다른 작업이 돌고 있습니다.")
                return self._json({"ok": True, "dir": name})

            if u.path == "/api/save":
                folder = self._dir(body["dir"])
                project = Project.from_dict(body["project"])
                project.renumber()
                project.save(folder)
                return self._json({"ok": True})

            if u.path == "/api/voice":
                folder = self._dir(body["dir"])
                only = body.get("scene")
                fit = bool(body.get("fit", True))
                project = pipeline.revoice(
                    folder, only=int(only) if only else None, fit_duration=fit
                )
                return self._json({"ok": True, "project": asdict(project)})

            if u.path == "/api/cut":
                folder = self._dir(body["dir"])
                out = pipeline.rebuild_cut(folder, int(body["scene"]))
                return self._json({"ok": True, "path": out.name})

            if u.path == "/api/render":
                folder = self._dir(body["dir"])

                def work(job: Job) -> None:
                    pipeline.finish(folder, progress=job.progress)

                if not JOB.start(work):
                    raise RuntimeError("이미 다른 작업이 돌고 있습니다.")
                return self._json({"ok": True})

            if u.path == "/api/media":
                # 컷 하나에 소재를 새로 지정
                folder = self._dir(body["dir"])
                project = Project.load(folder)
                got = source.fetch(body["source"], folder)
                idx = int(body["scene"])
                scene = next(s for s in project.scenes if s.index == idx)
                kind = source.kind_of(got)
                scene.media.type = kind
                scene.media.path = str(got.relative_to(folder))
                scene.media.start = 0.0
                project.save(folder)
                return self._json({"ok": True, "project": asdict(project)})

            if u.path == "/api/scene":
                # 컷 추가 / 삭제
                folder = self._dir(body["dir"])
                project = Project.load(folder)
                action = body.get("action")
                if action == "add":
                    at = int(body.get("after") or len(project.scenes))
                    project.scenes.insert(at, Scene(index=at + 1, caption="새 자막", narration="새 문장입니다."))
                elif action == "delete":
                    idx = int(body["scene"])
                    project.scenes = [s for s in project.scenes if s.index != idx]
                project.renumber()
                project.save(folder)
                return self._json({"ok": True, "project": asdict(project)})

            return self._json({"error": "없는 주소"}, 404)
        except Exception as exc:
            traceback.print_exc()
            self._fail(exc)


def serve(port: int = 8765, workspace: str = "projects", open_browser: bool = True) -> None:
    ws = Path(workspace)
    ws.mkdir(parents=True, exist_ok=True)
    Handler.workspace = ws
    url = f"http://127.0.0.1:{port}/"
    print(f"편집 화면: {url}")
    print(f"프로젝트 폴더: {ws.resolve()}")
    print("끄려면 이 창에서 Ctrl+C 를 누르세요.")
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n껐습니다.")
