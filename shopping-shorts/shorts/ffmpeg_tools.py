"""ffmpeg 실행기.

ffmpeg를 따로 설치하지 않아도 되게, pip로 깔리는 imageio-ffmpeg가 들고 오는
실행파일을 먼저 찾습니다. 시스템에 ffmpeg가 이미 있으면 그걸 씁니다.
ffprobe는 없는 환경이 많아 쓰지 않고, ffmpeg가 뱉는 Duration 줄을 읽습니다.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

_DURATION_RE = re.compile(r"Duration:\s*(\d+):(\d\d):(\d\d(?:\.\d+)?)")


class FFmpegError(RuntimeError):
    pass


def ffmpeg_path() -> str:
    env = os.environ.get("SHORTS_FFMPEG")
    if env and Path(env).exists():
        return env
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:  # pragma: no cover - 설치 안내용
        raise FFmpegError(
            "ffmpeg를 찾지 못했습니다. `pip install imageio-ffmpeg` 를 실행하거나 "
            "ffmpeg를 설치한 뒤 SHORTS_FFMPEG 환경변수에 경로를 넣어주세요."
        ) from exc


def run(
    args: list[str], *, quiet: bool = True, cwd: str | Path | None = None
) -> subprocess.CompletedProcess:
    """ffmpeg 한 번 실행. 실패하면 stderr 끝부분을 붙여서 올립니다.

    cwd를 주면 그 폴더에서 실행합니다. 자막 필터(ass=)에 상대경로를 넘기기
    위해서인데, 윈도우의 ``C:\경로`` 는 필터 문법의 콜론과 부딪혀서
    절대경로를 그대로 넘기면 깨집니다.
    """
    cmd = [ffmpeg_path(), "-hide_banner", "-nostdin", "-y", *args]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, errors="replace",
        cwd=str(cwd) if cwd else None,
    )
    if proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-15:])
        raise FFmpegError(f"ffmpeg 실패 (코드 {proc.returncode})\n{tail}")
    if not quiet and proc.stderr:
        print(proc.stderr[-2000:])
    return proc


def probe_duration(path: str | Path) -> float:
    """미디어 길이(초). 못 읽으면 0.0."""
    proc = subprocess.run(
        [ffmpeg_path(), "-hide_banner", "-nostdin", "-i", str(path)],
        capture_output=True,
        text=True,
        errors="replace",
    )
    m = _DURATION_RE.search(proc.stderr)
    if not m:
        return 0.0
    h, mnt, sec = m.groups()
    return int(h) * 3600 + int(mnt) * 60 + float(sec)


def has_video_stream(path: str | Path) -> bool:
    proc = subprocess.run(
        [ffmpeg_path(), "-hide_banner", "-nostdin", "-i", str(path)],
        capture_output=True,
        text=True,
        errors="replace",
    )
    return bool(re.search(r"Stream #\d+:\d+.*: Video:", proc.stderr))
