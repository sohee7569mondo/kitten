"""화면 소재 가져오기 — 로컬 파일 / 직링크 / 영상 플랫폼.

세 갈래를 한 함수(fetch)로 받습니다.
 - 내 컴퓨터의 파일 경로
 - .mp4 / .jpg 직링크 (타오바오·알리 상세페이지 영상이 대개 이 형태입니다)
 - 유튜브 같은 플랫폼 주소 → yt-dlp가 깔려 있을 때만

auto_assign()이 가져온 소재를 장면마다 배분합니다. 영상이 하나뿐이면
장면마다 다른 구간을 잘라 쓰기 때문에, 같은 화면이 반복되지 않습니다.
"""

from __future__ import annotations

import mimetypes
import re
import shutil
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from .ffmpeg_tools import has_video_stream, probe_duration, run
from .project import Media, Project, folders

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
_IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
_VID_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}
_DIRECT_RE = re.compile(r"\.(mp4|mov|webm|m4v|jpe?g|png|webp)(\?|$)", re.I)


class SourceError(RuntimeError):
    pass


def kind_of(path: str | Path) -> str:
    ext = Path(path).suffix.lower()
    if ext in _IMG_EXT:
        return "image"
    if ext in _VID_EXT:
        return "video"
    return "video" if has_video_stream(path) else "image"


def _safe_name(name: str) -> str:
    name = re.sub(r"[^\w.\-]+", "_", name).strip("_")
    return name[:80] or "media"


def _download(url: str, dest_dir: Path) -> Path:
    parsed = urlparse(url)
    base = _safe_name(Path(parsed.path).name or "download")
    if not Path(base).suffix:
        base += ".mp4"
    out = dest_dir / base
    req = urllib.request.Request(url, headers={"User-Agent": _UA, "Referer": f"{parsed.scheme}://{parsed.netloc}/"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp, open(out, "wb") as fh:
            ctype = resp.headers.get("Content-Type", "")
            ext = mimetypes.guess_extension(ctype.split(";")[0].strip() or "") or ""
            if ext and not out.suffix:
                out = out.with_suffix(ext)
                fh.close()
            shutil.copyfileobj(resp, fh)
    except Exception as exc:
        raise SourceError(f"내려받기 실패: {url}\n{exc}") from exc
    if out.stat().st_size == 0:
        raise SourceError(f"빈 파일을 받았습니다: {url}")
    return out


def _ytdlp(url: str, dest_dir: Path) -> Path:
    try:
        import yt_dlp
    except ImportError as exc:
        raise SourceError(
            "이 주소는 yt-dlp가 있어야 받을 수 있습니다. `pip install yt-dlp` 를 실행해주세요.\n"
            "(내 컴퓨터에 이미 받아둔 영상 파일 경로를 넣어도 됩니다.)"
        ) from exc

    opts = {
        "outtmpl": str(dest_dir / "%(id)s.%(ext)s"),
        "format": "bv*[height<=1920][ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
        "quiet": True,
        "noprogress": True,
        "merge_output_format": "mp4",
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return Path(ydl.prepare_filename(info)).with_suffix(".mp4")


def fetch(src: str, folder: str | Path) -> Path:
    """소재 하나를 프로젝트의 media 폴더로 가져옵니다. 가져온 경로를 돌려줍니다."""
    fs = folders(folder)
    dest = fs["media"]

    local = Path(src).expanduser()
    if local.exists():
        out = dest / _safe_name(local.name)
        if local.resolve() != out.resolve():
            shutil.copyfile(local, out)
        return out

    if not src.lower().startswith(("http://", "https://")):
        raise SourceError(f"파일도 아니고 주소도 아닙니다: {src}")

    if _DIRECT_RE.search(urlparse(src).path):
        return _download(src, dest)
    return _ytdlp(src, dest)


def frames(video: str | Path, dest_dir: str | Path, count: int = 6) -> list[Path]:
    """영상에서 고르게 몇 장 뽑습니다. 소재로도 쓰고, 분석에도 씁니다."""
    video = Path(video)
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dur = probe_duration(video)
    if dur <= 0:
        raise SourceError(f"길이를 읽지 못했습니다: {video}")
    out: list[Path] = []
    for i in range(count):
        # 맨 앞뒤는 로고·암전인 경우가 많아 안쪽에서 뽑습니다.
        t = dur * (i + 0.5) / count
        p = dest_dir / f"{video.stem}_f{i+1:02d}.jpg"
        run(["-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-q:v", "3", str(p)])
        out.append(p)
    return out


def auto_assign(project: Project, sources: list[str | Path], folder: str | Path) -> Project:
    """소재를 장면에 배분합니다.

    - 소재가 장면보다 적으면 번갈아 돌려 씁니다 (시연 프로그램과 같은 방식)
    - 영상 소재는 장면마다 다른 구간을 잡아서, 같은 그림이 반복되지 않게 합니다
    """
    fs = folders(folder)
    root = fs["root"]
    if not sources:
        return project

    resolved: list[tuple[str, Path, float]] = []
    for s in sources:
        p = Path(s)
        if not p.is_absolute():
            p = root / p
        k = kind_of(p)
        resolved.append((k, p, probe_duration(p) if k == "video" else 0.0))

    # 같은 영상이 여러 장면에 걸릴 때 구간을 나눠주기 위한 카운터
    used: dict[str, int] = {}
    total_by_src: dict[str, int] = {}
    for i, scene in enumerate(project.scenes):
        key = str(resolved[i % len(resolved)][1])
        total_by_src[key] = total_by_src.get(key, 0) + 1

    for i, scene in enumerate(project.scenes):
        kind, path, dur = resolved[i % len(resolved)]
        rel = str(path.relative_to(root)) if root in path.parents else str(path)
        if kind == "video":
            key = str(path)
            n = used.get(key, 0)
            used[key] = n + 1
            slots = max(1, total_by_src.get(key, 1))
            span = max(0.0, dur - scene.duration)
            start = span * n / slots if slots > 1 else 0.0
            scene.media = Media(type="video", path=rel, start=round(start, 2))
        else:
            motion = "zoom_in" if i % 2 == 0 else "zoom_out"
            scene.media = Media(type="image", path=rel, motion=motion)
    return project
