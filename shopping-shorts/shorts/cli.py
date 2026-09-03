"""명령줄 진입점.

    python -m shorts new  <폴더> --keyword "녹 제거 페인트" --source 영상.mp4
    python -m shorts voice <폴더> [--scene 3]
    python -m shorts cut   <폴더> --scene 3
    python -m shorts render <폴더>
    python -m shorts voices
    python -m shorts web
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import pipeline
from .project import Project
from .tts import KO_VOICES, list_voices


def _print_scenes(project: Project) -> None:
    print(f"\n[{project.title}] 총 {len(project.scenes)}컷 / {project.total_duration:.1f}초")
    for s in project.scenes:
        cap = s.caption.replace("\n", " / ")
        print(f"  {s.index:2d}. ({s.duration:4.1f}초) {cap}")
        print(f"       읽기: {s.narration}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="shorts", description="쇼핑 쇼츠 자동 제작기")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="새 프로젝트 만들기 (대본+음성까지)")
    p_new.add_argument("folder")
    p_new.add_argument("--keyword", required=True, help="영상 주제")
    p_new.add_argument("--source", action="append", default=[], help="소재 파일/주소 (여러 번 가능)")
    p_new.add_argument("--scenes", type=int, default=8)
    p_new.add_argument("--style", default="정보 전달 (뉴스형)")
    p_new.add_argument("--voice", default="ko-KR-SunHiNeural")
    p_new.add_argument("--no-analyze", action="store_true")
    p_new.add_argument("--no-tts", action="store_true", help="음성 없이 자리만 잡기")
    p_new.add_argument("--render", action="store_true", help="만든 뒤 바로 렌더까지")

    p_voice = sub.add_parser("voice", help="대본 고친 뒤 음성 다시 만들기")
    p_voice.add_argument("folder")
    p_voice.add_argument("--scene", type=int, default=None)
    p_voice.add_argument("--keep-duration", action="store_true", help="컷 길이는 그대로 두기")

    p_cut = sub.add_parser("cut", help="컷 하나만 다시 굽기")
    p_cut.add_argument("folder")
    p_cut.add_argument("--scene", type=int, required=True)

    p_render = sub.add_parser("render", help="전체 렌더")
    p_render.add_argument("folder")
    p_render.add_argument("--out", default="out.mp4")

    p_show = sub.add_parser("show", help="대본 보기")
    p_show.add_argument("folder")

    sub.add_parser("voices", help="쓸 수 있는 한국어 목소리 목록")

    p_web = sub.add_parser("web", help="브라우저 편집 화면 켜기")
    p_web.add_argument("--port", type=int, default=8765)
    p_web.add_argument("--workspace", default="projects", help="프로젝트를 모아둘 폴더")

    args = ap.parse_args(argv)

    if args.cmd == "new":
        project = pipeline.make_project(
            args.folder,
            keyword=args.keyword,
            sources=args.source,
            scenes=args.scenes,
            style=args.style,
            voice=args.voice,
            analyze=not args.no_analyze,
            tts_provider="none" if args.no_tts else "edge",
        )
        _print_scenes(project)
        print(f"\n대본 파일: {Path(args.folder) / 'project.json'}")
        if args.render:
            out = pipeline.finish(args.folder, progress=lambda i, n, m: print(f"  [{i}/{n}] {m}"))
            print(f"완성: {out}")
        else:
            print("고칠 곳을 고친 뒤:  python -m shorts voice " + args.folder)
            print("바로 뽑으려면:      python -m shorts render " + args.folder)
        return 0

    if args.cmd == "voice":
        project = pipeline.revoice(
            args.folder, only=args.scene, fit_duration=not args.keep_duration
        )
        _print_scenes(project)
        return 0

    if args.cmd == "cut":
        out = pipeline.rebuild_cut(args.folder, args.scene)
        print(f"다시 구웠습니다: {out}")
        return 0

    if args.cmd == "render":
        out = pipeline.finish(
            args.folder, progress=lambda i, n, m: print(f"  [{i}/{n}] {m}"), out_name=args.out
        )
        print(f"완성: {out}")
        return 0

    if args.cmd == "show":
        _print_scenes(Project.load(args.folder))
        return 0

    if args.cmd == "voices":
        print("자주 쓰는 목소리:")
        for k, v in KO_VOICES.items():
            print(f"  {k}\n      {v}")
        try:
            print("\n전체 목록:")
            for v in list_voices("ko"):
                print(f"  {v['ShortName']}  ({v.get('Gender', '')})")
        except Exception as exc:
            print(f"  (목록을 가져오지 못했습니다: {exc})")
        return 0

    if args.cmd == "web":
        from .web.app import serve

        serve(port=args.port, workspace=args.workspace)
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
