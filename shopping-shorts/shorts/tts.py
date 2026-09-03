"""음성 만들기.

기본은 edge-tts입니다. 키도 없고 돈도 안 드는데 한국어 품질이 쓸 만해서
처음 시작하기에 가장 좋습니다. 나중에 클로바보이스·일레븐랩스로 바꾸고
싶으면 synthesize() 하나만 갈아끼우면 됩니다.

시연 프로그램의 '음성 길이에 맞춰 컷 자동조정'은 apply_voice()가 합니다.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from .ffmpeg_tools import probe_duration, run
from .project import Project, folders

# 자주 쓰는 한국어 화자. `python -m shorts voices` 로 전체 목록을 볼 수 있습니다.
KO_VOICES = {
    "ko-KR-SunHiNeural": "선히 — 여성, 밝고 또렷함 (기본값. 쇼핑 쇼츠에 무난)",
    "ko-KR-InJoonNeural": "인준 — 남성, 차분한 뉴스 톤",
    "ko-KR-HyunsuMultilingualNeural": "현수 — 남성, 자연스러운 최신 음성",
}


class TTSError(RuntimeError):
    pass


def _silence(path: Path, seconds: float = 2.0) -> None:
    run([
        "-f", "lavfi",
        "-i", f"anullsrc=channel_layout=stereo:sample_rate=48000:d={seconds:.3f}",
        "-c:a", "libmp3lame", str(path),
    ])


def synthesize(
    text: str,
    out_path: str | Path,
    *,
    voice: str = "ko-KR-SunHiNeural",
    rate: str = "+0%",
    provider: str = "edge",
) -> float:
    """문장 하나를 음성 파일로. 만들어진 길이(초)를 돌려줍니다."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    text = (text or "").strip()

    if not text or provider == "none":
        # 대본이 비었거나 음성을 끈 경우 — 자리만 채웁니다.
        _silence(out_path, 1.5)
        return probe_duration(out_path)

    if provider != "edge":
        raise TTSError(f"아직 붙이지 않은 음성 엔진입니다: {provider}")

    try:
        import edge_tts
    except ImportError as exc:
        raise TTSError("edge-tts가 없습니다. `pip install edge-tts` 를 실행해주세요.") from exc

    async def _go() -> None:
        comm = edge_tts.Communicate(text, voice, rate=rate)
        await comm.save(str(out_path))

    try:
        asyncio.run(_go())
    except Exception as exc:
        raise TTSError(
            f"음성 생성 실패({voice}): {exc}\n"
            "인터넷 연결을 확인해주세요. edge-tts는 마이크로소프트 서버를 씁니다."
        ) from exc

    if not out_path.exists() or out_path.stat().st_size == 0:
        raise TTSError("음성 파일이 비어 있습니다. 화자 이름이 맞는지 확인해주세요.")
    return probe_duration(out_path)


def apply_voice(
    project: Project,
    folder: str | Path,
    *,
    provider: str = "edge",
    only: int | None = None,
    fit_duration: bool = True,
) -> Project:
    """장면마다 음성을 만들고, 컷 길이를 그 음성 길이에 맞춥니다.

    fit_duration=False로 두면 길이는 손대지 않고 음성만 새로 만듭니다.
    """
    fs = folders(folder)
    for scene in project.scenes:
        if only is not None and scene.index != only:
            continue
        rel = f"audio/scene_{scene.index:03d}.mp3"
        dur = synthesize(
            scene.narration,
            fs["root"] / rel,
            voice=project.voice,
            rate=project.speed,
            provider=provider,
        )
        scene.audio = rel
        scene.audio_duration = round(dur, 3)
        if fit_duration:
            scene.duration = round(max(1.0, dur + project.pad), 2)
    return project


def list_voices(lang: str = "ko") -> list[dict]:
    try:
        import edge_tts
    except ImportError as exc:
        raise TTSError("edge-tts가 없습니다. `pip install edge-tts` 를 실행해주세요.") from exc

    voices = asyncio.run(edge_tts.list_voices())
    return [v for v in voices if v.get("Locale", "").startswith(lang)]
