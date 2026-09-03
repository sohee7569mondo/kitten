"""흐름 조립 — 새 프로젝트 만들기, 음성 다시 만들기, 컷 다시 굽기.

시연 프로그램의 4단계(주제 → 옵션 → 생성 → 리터치)에서
'생성'까지를 make_project()가 한 번에 처리합니다. 그 다음부터가 리터치입니다.
"""

from __future__ import annotations

from pathlib import Path

from . import ai, source, tts
from .project import Project, Scene, folders
from .render import render, render_cut


def make_project(
    folder: str | Path,
    *,
    keyword: str,
    sources: list[str] | None = None,
    scenes: int = 8,
    style: str = "정보 전달 (뉴스형)",
    voice: str = "ko-KR-SunHiNeural",
    analyze: bool = True,
    tts_provider: str = "edge",
    log=print,
) -> Project:
    """소재와 키워드로 프로젝트 하나를 세웁니다. 대본·음성까지 채워서 돌려줍니다."""
    fs = folders(folder)
    sources = sources or []

    # 1) 소재 가져오기
    grabbed: list[Path] = []
    for s in sources:
        log(f"소재 가져오는 중: {s}")
        grabbed.append(source.fetch(s, folder))

    # 2) 소재 훑어보기 (키가 있을 때만)
    brief = None
    if analyze and grabbed and ai.have_api_key():
        look: list[Path] = []
        for g in grabbed[:3]:
            if source.kind_of(g) == "video":
                look += source.frames(g, fs["media"] / "frames", count=4)
            else:
                look.append(g)
        if look:
            log("소재 분석 중…")
            try:
                brief = ai.analyze_media(look, hint=keyword)
                keyword = keyword or brief.get("keyword", "")
                log(f"  → {brief.get('product', '')}")
            except ai.AIError as exc:
                log(f"  분석을 건너뜁니다: {exc}")

    # 3) 대본
    log("대본 쓰는 중…" + ("" if ai.have_api_key() else " (키가 없어 기본 틀로 만듭니다)"))
    data = ai.write_script(keyword, scenes=scenes, style=style, brief=brief)

    project = Project(
        title=data.get("title") or keyword,
        keyword=keyword,
        style=style,
        voice=voice,
        scenes=ai.to_scenes(data),
    )
    project.renumber()

    # 4) 소재를 장면에 배분
    if grabbed:
        source.auto_assign(project, grabbed, folder)

    # 5) 음성 → 컷 길이 자동 맞춤
    log(f"음성 만드는 중… ({len(project.scenes)}컷)")
    tts.apply_voice(project, folder, provider=tts_provider)

    project.save(folder)
    log(f"대본 준비 완료 — 총 {project.total_duration:.1f}초")
    return project


def revoice(
    folder: str | Path, *, only: int | None = None, tts_provider: str = "edge",
    fit_duration: bool = True,
) -> Project:
    """대본을 고친 뒤 음성만 다시 만듭니다."""
    project = Project.load(folder)
    tts.apply_voice(project, folder, provider=tts_provider, only=only, fit_duration=fit_duration)
    project.save(folder)
    return project


def rebuild_cut(folder: str | Path, index: int) -> Path:
    project = Project.load(folder)
    scene = next((s for s in project.scenes if s.index == index), None)
    if scene is None:
        raise ValueError(f"{index}번 장면이 없습니다.")
    return render_cut(project, scene, folder)


def finish(folder: str | Path, *, progress=None, out_name: str = "out.mp4") -> Path:
    project = Project.load(folder)
    return render(project, folder, progress=progress, out_name=out_name)
