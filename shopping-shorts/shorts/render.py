"""렌더링 — 장면 하나를 mp4 한 컷으로 굽고, 컷들을 이어붙입니다.

설계 하나만 짚어두면:
컷을 구울 때 그 장면의 자막과 음성까지 함께 넣습니다. 그래서
 (1) 영상 인코딩이 한 번만 돌고 (자막을 나중에 태우면 두 번 돌아야 합니다)
 (2) 구워진 컷 파일이 그대로 '장면별 미리보기'가 됩니다
 (3) 마지막 이어붙이기는 재인코딩 없이 복사로 끝납니다
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Callable

from .ffmpeg_tools import probe_duration, run
from .project import Project, Scene, folders
from .subtitle import write_ass

Progress = Callable[[int, int, str], None]


def _video_filters(project: Project, scene: Scene) -> str:
    w, h, fps = project.width, project.height, project.fps
    m = scene.media
    dur = max(0.2, scene.duration)

    if m.type == "image":
        if m.motion in ("zoom_in", "zoom_out"):
            frames = max(2, int(round(dur * fps)))
            # 큰 판으로 키워 놓고 zoompan으로 훑어야 덜 떨립니다.
            base = f"scale={w*2}:{h*2}:force_original_aspect_ratio=increase,crop={w*2}:{h*2}"
            if m.motion == "zoom_in":
                z = "min(zoom+0.0012,1.25)"
            else:
                z = "if(lte(zoom,1.0),1.25,max(1.0,zoom-0.0012))"
            zp = (
                f"zoompan=z='{z}':d={frames}"
                f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}"
            )
            chain = f"{base},{zp}"
        else:
            chain = (
                f"scale={w}:{h}:force_original_aspect_ratio=increase,"
                f"crop={w}:{h},fps={fps}"
            )
    elif m.type == "video":
        chain = (
            f"fps={fps},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
        )
    else:  # color
        chain = f"fps={fps}"

    return f"{chain},setsar=1,format=yuv420p"


def _video_input(project: Project, scene: Scene, root: Path) -> list[str]:
    """장면의 화면 소재를 ffmpeg 입력 인자로."""
    m = scene.media
    dur = max(0.2, scene.duration)

    if m.type == "image":
        path = _resolve(m.path, root)
        return ["-loop", "1", "-t", f"{dur:.3f}", "-i", path]

    if m.type == "video":
        path = _resolve(m.path, root)
        src = probe_duration(path)
        start = max(0.0, m.start)
        if src and src >= dur:
            # 끝을 넘어가면 뒤로 물러서서 잘라옵니다.
            start = min(start, max(0.0, src - dur))
            return ["-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", path]
        # 소재가 컷보다 짧으면 이어 돌려서 채웁니다.
        return ["-stream_loop", "-1", "-t", f"{dur:.3f}", "-i", path]

    color = m.color or "0x101820"
    return [
        "-f", "lavfi",
        "-i", f"color=c={color}:s={project.width}x{project.height}:d={dur:.3f}:r={project.fps}",
    ]


def _resolve(path: str, root: Path) -> str:
    p = Path(path)
    if not p.is_absolute():
        p = root / p
    if not p.exists():
        raise FileNotFoundError(f"소재 파일이 없습니다: {p}")
    return str(p)


def render_cut(project: Project, scene: Scene, folder: str | Path) -> Path:
    """장면 하나 → cuts/cut_XXX.mp4 (자막·음성 포함, 그대로 재생 가능)."""
    fs = folders(folder)
    root = fs["root"]
    dur = max(0.2, scene.duration)

    subs_dir = root / "subs"
    subs_dir.mkdir(exist_ok=True)
    ass_rel = f"subs/cut_{scene.index:03d}.ass"
    write_ass(project, root / ass_rel, only_scene=scene.index)

    args: list[str] = []
    args += _video_input(project, scene, root)

    # 음성: 없으면 무음으로 채워 컷 길이를 맞춥니다.
    if scene.audio and (root / scene.audio).exists():
        args += ["-i", str(root / scene.audio)]
    else:
        args += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]

    # 효과음(선택): 컷 앞머리에 한 번 겹쳐 깔립니다.
    sfx = None
    if scene.sfx:
        cand = Path(scene.sfx)
        if not cand.is_absolute():
            cand = root / cand
        if cand.exists():
            sfx = cand
            args += ["-i", str(cand)]

    vf = _video_filters(project, scene)
    fontsdir = os.environ.get("SHORTS_FONTSDIR", "")
    ass = f"ass=filename={ass_rel}"
    if fontsdir:
        ass += f":fontsdir={fontsdir}"
    vf = f"{vf},{ass}"

    out_rel = f"cuts/cut_{scene.index:03d}.mp4"
    afmt = "aformat=sample_rates=48000:channel_layouts=stereo"
    if sfx is not None:
        vol = max(0.0, min(1.0, scene.sfx_volume))
        args += [
            "-filter_complex",
            f"[0:v]{vf}[v];"
            f"[1:a]{afmt},apad[a0];"
            f"[2:a]{afmt},volume={vol:.3f}[a1];"
            f"[a0][a1]amix=inputs=2:duration=first:dropout_transition=0,{afmt}[a]",
            "-map", "[v]", "-map", "[a]",
        ]
    else:
        args += [
            "-map", "0:v:0", "-map", "1:a:0",
            "-vf", vf,
            "-af", f"{afmt},apad",
        ]
    args += [
        "-t", f"{dur:.3f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", str(project.fps),
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-movflags", "+faststart",
        out_rel,
    ]
    run(args, cwd=root)
    return root / out_rel


def concat_cuts(project: Project, folder: str | Path, out_name: str = "out.mp4") -> Path:
    """구운 컷들을 재인코딩 없이 이어붙입니다."""
    fs = folders(folder)
    root = fs["root"]
    cuts = [root / f"cuts/cut_{s.index:03d}.mp4" for s in project.scenes]
    missing = [c.name for c in cuts if not c.exists()]
    if missing:
        raise FileNotFoundError(f"아직 굽지 않은 컷이 있습니다: {', '.join(missing)}")

    if len(cuts) == 1:
        shutil.copyfile(cuts[0], root / out_name)
        return root / out_name

    list_path = root / "cuts" / "concat.txt"
    list_path.write_text(
        "".join(f"file '{c.name}'\n" for c in cuts), encoding="utf-8"
    )
    run(
        ["-f", "concat", "-safe", "0", "-i", "cuts/concat.txt",
         "-c", "copy", "-movflags", "+faststart", out_name],
        cwd=root,
    )
    return root / out_name


def mix_bgm(project: Project, folder: str | Path, target: str = "out.mp4") -> Path:
    """배경음 깔기. 영상은 건드리지 않고 소리만 다시 씁니다."""
    root = Path(folder)
    bgm = _resolve(project.bgm, root)
    tmp = root / "_bgm_tmp.mp4"
    vol = max(0.0, min(1.0, project.bgm_volume))
    run(
        [
            "-i", target, "-stream_loop", "-1", "-i", bgm,
            "-filter_complex",
            f"[1:a]volume={vol:.3f}[b];[0:a][b]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
            tmp.name,
        ],
        cwd=root,
    )
    tmp.replace(root / target)
    return root / target


def render(
    project: Project,
    folder: str | Path,
    *,
    progress: Progress | None = None,
    out_name: str = "out.mp4",
) -> Path:
    """전체 렌더. progress(현재, 전체, 메시지)로 진행률을 흘려보냅니다."""
    total = len(project.scenes)
    if not total:
        raise ValueError("장면이 하나도 없습니다.")
    for i, scene in enumerate(project.scenes, start=1):
        if progress:
            progress(i - 1, total, f"장면 {scene.index} 굽는 중")
        render_cut(project, scene, folder)
    if progress:
        progress(total, total, "이어붙이는 중")
    out = concat_cuts(project, folder, out_name)
    if project.bgm:
        if progress:
            progress(total, total, "배경음 넣는 중")
        out = mix_bgm(project, folder, out_name)
    if progress:
        progress(total, total, "완료")
    return out
