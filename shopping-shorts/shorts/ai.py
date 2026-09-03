"""대본 쓰기 — Claude로 쓰거나, 키가 없으면 틀로 찍어냅니다.

키가 없어도 프로그램이 끝까지 돌아가야 한다고 봤습니다. 그래서 두 갈래입니다.
 - ANTHROPIC_API_KEY 가 있으면: 소재 화면까지 눈으로 보고 대본을 씁니다
 - 없으면: 훅-전개-CTA 틀에 키워드를 끼워 넣습니다 (품질은 당연히 덜하지만 돕니다)
"""

from __future__ import annotations

import base64
import json
import os
import re
from pathlib import Path

from .project import Scene

MODEL = "claude-opus-5"

# 쇼핑 쇼츠 대본의 뼈대. 시연 프로그램이 뽑아내던 훅·전개·CTA 구성입니다.
SYSTEM = """당신은 한국 쇼핑 쇼츠(제휴마케팅 숏폼) 대본 작가입니다.

지켜야 할 것:
- 구성은 훅(1~2컷) → 전개(중간) → CTA(마지막 1컷).
- 첫 컷은 3초 안에 손가락을 멈추게 하는 문제 제기나 결과 장면.
- narration은 실제로 사람이 읽는 문장. 구어체 반말 금지, 친근한 존댓말.
- narration에는 이모지·특수문자·괄호를 쓰지 마세요. 소리내어 읽을 수 없는 것은 넣지 않습니다.
- caption은 화면에 박히는 자막. 한 컷당 두 줄, 각 줄 12자 이내, 줄바꿈은 \\n.
- caption은 narration의 요약이지 그대로 옮긴 것이 아닙니다.
- 한 컷의 narration은 2~4초 분량(한국어 기준 12~28자)으로 짧게 끊으세요.
- 의학적 효능, 최저가, 1위 같은 검증 불가한 단정은 쓰지 마세요.
- 과장 광고로 문제가 될 표현(완치, 100% 보장) 금지."""


class AIError(RuntimeError):
    pass


def have_api_key() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))


def _client():
    try:
        import anthropic
    except ImportError as exc:
        raise AIError("`pip install anthropic` 이 필요합니다.") from exc
    return anthropic.Anthropic()


def _text_of(response) -> str:
    if getattr(response, "stop_reason", None) == "refusal":
        raise AIError("모델이 이 요청을 거절했습니다. 주제나 표현을 바꿔서 다시 시도해주세요.")
    for block in response.content:
        if block.type == "text":
            return block.text
    raise AIError("응답에서 글을 찾지 못했습니다.")


def _image_block(path: Path) -> dict:
    ext = path.suffix.lower()
    media = {".png": "image/png", ".webp": "image/webp", ".gif": "image/gif"}.get(ext, "image/jpeg")
    data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    return {"type": "image", "source": {"type": "base64", "media_type": media, "data": data}}


# --- 1단계: 소재 분석 -------------------------------------------------
ANALYZE_SCHEMA = {
    "type": "object",
    "properties": {
        "product": {"type": "string", "description": "화면에 보이는 상품이 무엇인지"},
        "keyword": {"type": "string", "description": "영상 주제 키워드 한 줄"},
        "problem": {"type": "string", "description": "이 상품이 풀어주는 불편"},
        "selling_points": {"type": "array", "items": {"type": "string"}},
        "hashtags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["product", "keyword", "problem", "selling_points", "hashtags"],
    "additionalProperties": False,
}


def analyze_media(images: list[str | Path], hint: str = "") -> dict:
    """소재 화면 몇 장을 보고 상품·주제·팔 거리를 뽑습니다."""
    if not have_api_key():
        raise AIError("분석에는 ANTHROPIC_API_KEY 가 필요합니다.")
    paths = [Path(p) for p in images][:8]
    if not paths:
        raise AIError("분석할 이미지가 없습니다.")

    content: list[dict] = [_image_block(p) for p in paths]
    content.append({
        "type": "text",
        "text": (
            f"이 장면들은 한 상품의 홍보 영상에서 뽑은 것입니다."
            f"{(' 참고: ' + hint) if hint else ''}\n"
            "무슨 상품이고, 어떤 불편을 풀어주는지, 쇼츠에서 내세울 만한 점을 정리해주세요."
        ),
    })

    resp = _client().messages.create(
        model=MODEL,
        max_tokens=16000,
        system="당신은 한국 이커머스 상품 분석가입니다. 화면에 실제로 보이는 것만 근거로 판단하세요.",
        messages=[{"role": "user", "content": content}],
        output_config={"format": {"type": "json_schema", "schema": ANALYZE_SCHEMA}},
    )
    return json.loads(_text_of(resp))


# --- 2단계: 대본 -------------------------------------------------------
SCRIPT_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "hashtags": {"type": "array", "items": {"type": "string"}},
        "scenes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "role": {"type": "string", "enum": ["훅", "전개", "CTA"]},
                    "caption": {"type": "string"},
                    "narration": {"type": "string"},
                },
                "required": ["role", "caption", "narration"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["title", "hashtags", "scenes"],
    "additionalProperties": False,
}


def write_script(
    keyword: str,
    *,
    scenes: int = 8,
    style: str = "정보 전달 (뉴스형)",
    brief: dict | None = None,
) -> dict:
    """대본을 씁니다. 키가 없으면 틀로 찍어냅니다."""
    if not have_api_key():
        return template_script(keyword, scenes=scenes)

    lines = [
        f"주제 키워드: {keyword}",
        f"영상 스타일: {style}",
        f"컷 수: 정확히 {scenes}컷",
    ]
    if brief:
        lines.append("소재 분석 결과:\n" + json.dumps(brief, ensure_ascii=False, indent=2))
    lines.append("위 조건으로 세로 쇼츠 대본을 써주세요.")

    resp = _client().messages.create(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": "\n".join(lines)}],
        output_config={"format": {"type": "json_schema", "schema": SCRIPT_SCHEMA}},
    )
    data = json.loads(_text_of(resp))
    data["scenes"] = data.get("scenes", [])[:scenes] or template_script(keyword, scenes=scenes)["scenes"]
    return data


def template_script(keyword: str, *, scenes: int = 8) -> dict:
    """키 없이 쓰는 기본 틀. 손볼 것을 전제로 한 초안입니다."""
    kw = (keyword or "이 상품").strip()
    short = kw if len(kw) <= 10 else kw[:10]
    beats = [
        ("훅", f"{short}\n고민이셨죠?", f"{kw} 때문에 고민이셨죠?"),
        ("훅", "이거 하나면\n끝납니다", "그런데 이거 하나면 끝납니다."),
        ("전개", "복잡한 준비\n필요 없어요", "복잡한 준비 과정이 필요 없어요."),
        ("전개", "그냥 이대로\n쓰시면 돼요", "그냥 이대로 쓰시면 됩니다."),
        ("전개", "결과는\n보시는 대로", "결과는 보시는 그대로입니다."),
        ("전개", "한 번 쓰면\n오래갑니다", "한 번 쓰면 꽤 오래갑니다."),
        ("전개", "가격도\n부담 없어요", "가격도 생각보다 부담이 없습니다."),
        ("CTA", "지금 아래\n링크 확인!", "지금 아래 링크에서 확인해보세요."),
    ]
    out = []
    for i in range(scenes):
        role, cap, nar = beats[i] if i < len(beats) else beats[-2]
        out.append({"role": role, "caption": cap, "narration": nar})
    if out:
        out[-1] = {"role": "CTA", "caption": "지금 아래\n링크 확인!", "narration": "지금 아래 링크에서 확인해보세요."}
    return {"title": kw, "hashtags": [f"#{re.sub(r'[^가-힣A-Za-z0-9]', '', kw)}"], "scenes": out}


def to_scenes(data: dict) -> list[Scene]:
    out = []
    for i, s in enumerate(data.get("scenes", []), start=1):
        out.append(
            Scene(
                index=i,
                caption=(s.get("caption") or "").replace("\\n", "\n").strip(),
                narration=(s.get("narration") or "").strip(),
                group=s.get("role", ""),
            )
        )
    return out
