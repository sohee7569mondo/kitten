# -*- coding: utf-8 -*-
"""별명표를 소희 님이 고치실 원고로 뽑습니다.

    python3 dump_nick.py          →  wordpress/drafts/유앤미-별명표.md

  이 원고가 앞으로 **원본**입니다. 여기만 고치고 emit_uandme_nick.py 를
  돌리면 조각 둘(자바스크립트·PHP)에 같이 들어갑니다.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uandme_nick import NICK, BODY, EMOJI, RELS, RELKO, MINS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', 'drafts', '유앤미-별명표.md')

HEAD = '''# 유앤미 별명표 — 카톡에 뜰 이름

소희 님 2026-09-15
  「공유되는 이미지 판은 무조건 이쁘고 바이럴되게
    서로를 키우는 사이를 유머스럽게나 드라마 주인공이름을 빗댄 이름으로?」
  「점수별로 보고 관계를 짓는 이름을 줘야겟네 … 경우의 표만 주면 이름 짓지 뭐」

관계 일곱 × 점수 열 구간 = **일흔 칸**입니다.
아래 초안을 **덮어 쓰시면** 됩니다. 빈칸으로 두면 초안이 그대로 갑니다.

카드에 나가는 모양 —

    연인 궁합 · 78점
    좋아하는데 왜 자꾸 엇갈릴까?        ← 훅
    갑돌이와 갑순이 같은 사이            ← 별명
    끌리는 힘은 분명합니다. …            ← 본문 세 문장
    나도 해보기 · stellasaju.com/uandme

## 지킬 것 — 안 지키면 글자가 네모(□)로 나옵니다

  · **한자를 쓰지 않습니다.** 情 · 中 같은 글자는 카드 글꼴에 없습니다.
  · **이모지는 본문에 쓰지 않습니다.** 구간마다 하나씩 따로 있습니다
    (카톡 글머리에만 씁니다. 그림에는 안 들어갑니다).
  · **따옴표와 앰퍼샌드(그리고 기호)를 쓰지 않습니다.**
  · 별명은 **열한 자 안쪽** · 훅은 **스물네 자 안쪽** ·
    본문은 한 문장이 **스물네 자 안쪽**, 세 문장.
  · 실존 인물 이름은 쓰지 않습니다 (초상권). 옛이야기·고전은 괜찮습니다 —
    춘향이와 몽룡 · 견우직녀 · 흥부와 놀부 · 관중과 포숙아 · 톰과 제리.

## 점수 구간이 열 개입니다

지금은 이렇게 끊습니다. 소희 님이 보내주신 「70~74점」처럼 더 잘게
나누고 싶으시면 말씀만 주세요 — 스무 칸(5점 단위)으로 늘리면
별명이 140개가 됩니다. 이름이 겹칠 일이 줄어 자랑할 맛은 더 납니다.

'''


def band(i):
    lo = MINS[i]
    hi = 100 if i == 0 else MINS[i - 1] - 1
    return str(lo) + '~' + str(hi) + '점'


def main():
    L = [HEAD]
    L.append('| 구간 | 이모지 |')
    L.append('|---|---|')
    for i in range(len(MINS)):
        L.append('| ' + band(i) + ' | ' + EMOJI[i] + ' |')
    L.append('')
    for rel in RELS:
        L.append('')
        L.append('# ' + RELKO[rel] + ' [' + rel + ']')
        for i in range(len(MINS)):
            name, hook = NICK[rel][i]
            b = BODY[rel][i]
            L.append('')
            L.append('## ' + band(i))
            L.append('별명   ' + name)
            L.append('훅     ' + hook)
            L.append('본문   ' + b[0])
            L.append('       ' + b[1])
            L.append('       ' + b[2])
        L.append('')
    io.open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(os.path.abspath(OUT))
    print('칸 ' + str(len(RELS) * len(MINS)))


main()
