"""프로젝트 파일(project.json) — 시연 프로그램의 '임시저장 / 대본 확정'에 해당합니다.

한 프로젝트 = 한 편의 쇼츠. 폴더 하나에 대본·음성·소재·결과물이 모두 들어갑니다.

    프로젝트폴더/
      project.json     ← 대본과 설정 (사람이 열어서 고쳐도 됩니다)
      media/           ← 내려받거나 복사해 온 소재
      audio/           ← 장면별 TTS mp3
      cuts/            ← 장면별 렌더 결과
      out.mp4          ← 최종 결과물
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

SCHEMA_VERSION = 1


@dataclass
class SubtitleStyle:
    """시연 화면의 '자막 스타일' 패널과 같은 항목들."""

    font: str = ""          # 비우면 OS별 기본 한글 폰트를 자동으로 찾습니다
    size: int = 80          # 1080 너비 기준
    color: str = "FFFFFF"   # RRGGBB
    outline_color: str = "000000"
    outline: int = 5
    shadow: int = 10
    position: str = "middle"  # top / middle / bottom
    align: str = "center"     # left / center / right
    margin_v: int = 260       # position=bottom/top 일 때 화면 끝에서 띄우는 픽셀
    max_width_pct: int = 100  # 자막 줄 최대 너비(%)


@dataclass
class Media:
    """장면에 깔릴 화면 소재. 영상이면 start부터 잘라 씁니다."""

    type: str = "color"           # image / video / color
    path: str = ""
    start: float = 0.0            # video일 때 잘라내기 시작 지점(초)
    color: str = "0x101820"       # type=color 일 때 배경색
    motion: str = "zoom_in"       # image일 때: zoom_in / zoom_out / none


@dataclass
class Scene:
    index: int = 0
    caption: str = ""             # 화면에 박히는 자막 (줄바꿈 그대로 반영)
    narration: str = ""           # 실제로 읽는 문장 (TTS 대본)
    duration: float = 2.0         # 컷 길이(초). 음성 생성 후 자동으로 맞춰집니다
    media: Media = field(default_factory=Media)
    audio: str = ""               # 프로젝트 폴더 기준 상대경로
    audio_duration: float = 0.0
    sfx: str = ""                 # 컷에 깔 효과음 파일(선택)
    sfx_volume: float = 0.6
    group: str = ""               # 시연 화면의 G1/G2 같은 묶음 표시(선택)


@dataclass
class Project:
    title: str = "제목 없음"
    keyword: str = ""
    style: str = "정보 전달 (뉴스형)"
    voice: str = "ko-KR-SunHiNeural"
    speed: str = "+0%"            # edge-tts 말하기 속도
    width: int = 1080
    height: int = 1920
    fps: int = 30
    bgm: str = ""                 # 배경음 파일 경로(선택)
    bgm_volume: float = 0.12
    pad: float = 0.25             # 컷마다 음성 뒤에 붙이는 여유(초)
    subtitle: SubtitleStyle = field(default_factory=SubtitleStyle)
    scenes: list[Scene] = field(default_factory=list)
    version: int = SCHEMA_VERSION

    # --- 저장/불러오기 -------------------------------------------------
    @staticmethod
    def path_for(folder: str | Path) -> Path:
        return Path(folder) / "project.json"

    def save(self, folder: str | Path) -> Path:
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        p = self.path_for(folder)
        p.write_text(
            json.dumps(asdict(self), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return p

    @classmethod
    def load(cls, folder: str | Path) -> "Project":
        raw = json.loads(cls.path_for(folder).read_text(encoding="utf-8"))
        return cls.from_dict(raw)

    @classmethod
    def from_dict(cls, raw: dict) -> "Project":
        scenes = []
        for i, s in enumerate(raw.get("scenes", []), start=1):
            media = Media(**{**asdict(Media()), **(s.get("media") or {})})
            s = {k: v for k, v in s.items() if k != "media"}
            base = asdict(Scene())
            base.pop("media")
            scene = Scene(**{**base, **s}, media=media)
            scene.index = scene.index or i
            scenes.append(scene)
        sub = SubtitleStyle(**{**asdict(SubtitleStyle()), **(raw.get("subtitle") or {})})
        body = {
            k: v
            for k, v in raw.items()
            if k not in {"scenes", "subtitle"} and k in asdict(cls())
        }
        return cls(**body, subtitle=sub, scenes=scenes)

    # --- 편의 ----------------------------------------------------------
    def renumber(self) -> None:
        for i, s in enumerate(self.scenes, start=1):
            s.index = i

    @property
    def total_duration(self) -> float:
        return round(sum(s.duration for s in self.scenes), 3)


def folders(folder: str | Path) -> dict[str, Path]:
    folder = Path(folder)
    out = {
        "root": folder,
        "media": folder / "media",
        "audio": folder / "audio",
        "cuts": folder / "cuts",
    }
    for p in out.values():
        p.mkdir(parents=True, exist_ok=True)
    return out
