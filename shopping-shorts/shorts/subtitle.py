"""자막(ASS) 만들기.

ffmpeg에 자막을 태우는 방법은 여러 가지지만, 시연 화면에 있는 항목
(폰트·크기·색·외곽선·그림자·위치)을 그대로 다루려면 ASS가 가장 잘 맞습니다.
drawtext로는 외곽선/그림자/줄바꿈을 이만큼 다루기 어렵습니다.
"""

from __future__ import annotations

import platform
from pathlib import Path

from .project import Project, SubtitleStyle

# 위치·정렬 → ASS Alignment(숫자패드 배치)
_ALIGN = {
    ("bottom", "left"): 1, ("bottom", "center"): 2, ("bottom", "right"): 3,
    ("middle", "left"): 4, ("middle", "center"): 5, ("middle", "right"): 6,
    ("top", "left"): 7, ("top", "center"): 8, ("top", "right"): 9,
}

_DEFAULT_FONTS = {
    "Windows": "Malgun Gothic",
    "Darwin": "Apple SD Gothic Neo",
    "Linux": "NanumGothic",
}


def default_font() -> str:
    return _DEFAULT_FONTS.get(platform.system(), "NanumGothic")


def _ass_color(rrggbb: str) -> str:
    """RRGGBB → ASS의 &HAABBGGRR. ASS는 색 순서가 거꾸로입니다."""
    h = rrggbb.strip().lstrip("#").upper()
    if len(h) != 6:
        h = "FFFFFF"
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}"


def _ts(sec: float) -> str:
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int(sec % 3600 // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def _escape(text: str) -> str:
    """ASS 한 줄로 밀어넣기. 사용자가 친 줄바꿈은 \\N으로 살립니다."""
    text = text.replace("\\", "\\\\").replace("{", "(").replace("}", ")")
    lines = [ln.strip() for ln in text.splitlines()]
    return "\\N".join(ln for ln in lines if ln) or " "


def style_line(st: SubtitleStyle, project: Project) -> str:
    font = st.font.strip() or default_font()
    align = _ALIGN.get((st.position, st.align), 5)
    # 화면 세로 가운데면 MarginV는 무시되므로 0으로 둡니다.
    margin_v = 0 if st.position == "middle" else max(0, st.margin_v)
    side = int(project.width * (100 - min(100, max(20, st.max_width_pct))) / 200)
    return (
        f"Style: Default,{font},{st.size},"
        f"{_ass_color(st.color)},&H000000FF,{_ass_color(st.outline_color)},&H80000000,"
        f"1,0,0,0,100,100,0,0,1,{st.outline},{st.shadow},{align},"
        f"{side},{side},{margin_v},1"
    )


def build_ass(project: Project, *, only_scene: int | None = None) -> str:
    """프로젝트 전체(또는 장면 하나)의 자막 파일 내용을 만듭니다."""
    head = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {project.width}",
        f"PlayResY: {project.height}",
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        "YCbCr Matrix: TV.709",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,"
        " BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
        " BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        style_line(project.subtitle, project),
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    events = []
    t = 0.0
    for scene in project.scenes:
        dur = max(0.2, scene.duration)
        if only_scene is None or scene.index == only_scene:
            start = 0.0 if only_scene is not None else t
            if scene.caption.strip():
                events.append(
                    f"Dialogue: 0,{_ts(start)},{_ts(start + dur)},Default,,0,0,0,,"
                    f"{_escape(scene.caption)}"
                )
        t += dur
    return "\n".join(head + events) + "\n"


def write_ass(project: Project, path: str | Path, *, only_scene: int | None = None) -> Path:
    path = Path(path)
    path.write_text(build_ass(project, only_scene=only_scene), encoding="utf-8")
    return path
