# -*- coding: utf-8 -*-
"""낱말표를 소희 님이 고치실 원고로 뽑습니다.

    python3 dump_words.py    →  wordpress/drafts/유앤미-낱말표.md

  이 원고가 **원본**입니다. 여기만 고치고 emit_uandme_words.py 를
  돌리면 조각 둘(자바스크립트·PHP)에 같이 들어갑니다.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uandme_words as W

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', 'drafts', '유앤미-낱말표.md')

HEAD = '''# 유앤미 낱말표

소희 님 2026-09-15
  「똑같은 실과 바늘의 관계라 써도 해설이 틀리면 되지?」

맞습니다. 그래서 두 층으로 나눴습니다.

    이름 (스무 칸)    점수가 맡습니다. 관계를 안 가립니다.
                      요약 · 이모지 · 별명 · 본문 두 문장 — **카드는 여기만 씁니다**
    해설 (서른다섯)   관계가 맡습니다.
                      훅 한 줄 — 결과 화면과 카톡 설명글에 나갑니다

합쳐서 **쉰다섯 칸**입니다. 일흔 칸이던 것보다 적으면서,
이름은 스무 가지로 늘어 겹칠 일이 줄었습니다.

카드에 나가는 모양 —

    연인 궁합 · 72점
    자꾸 신경 쓰이는 사이            ← 이름 칸의 「요약」
    톰과 제리 같은 사이              ← 이름 칸의 「별명」
    만나면 싸우고, 안 만나면 …        ← 해설 칸의 「본문」
    나도 해보기 · stellasaju.com/uandme

## 지킬 것 — 안 지키면 글자가 네모(□)로 나옵니다

  · **한자를 쓰지 않습니다.** 情 · 中 같은 글자는 카드 글꼴에 없습니다.
  · **따옴표와 앰퍼샌드를 쓰지 않습니다.**
  · **이름 칸에는 관계를 가리는 낱말을 쓰지 않습니다.**
    연애 · 밀당 · 콩깍지 · 부부 · 남매 · 회사 … 는 한쪽에만 맞습니다.
    「실과 바늘」처럼 어느 사이에나 맞는 말로 씁니다.
    (만들 때마다 제가 검사합니다.)
  · 별명·요약은 **열여섯 자 안쪽**, 훅은 **스물네 자 안쪽**,
    본문은 한 문장이 **스물네 자 안쪽**으로 세 문장.
  · 실존 인물 이름은 쓰지 않습니다 (초상권). 옛이야기·고전은 괜찮습니다 —
    실과 바늘 · 톰과 제리 · 흥부와 놀부 · 관중과 포숙아.
  · 이모지는 **카톡 글머리에만** 나갑니다. 카드 그림에는 안 들어갑니다.

'''

FOOT = '''
---

## 고친 뒤에

저에게 「낱말표 고쳤어」라고만 알려주세요.
제가 `emit_uandme_words.py` 를 돌려 조각에 넣고, 규칙에 어긋난 곳이
있으면 어디가 걸렸는지 찍어 드립니다.
'''


def main():
    L = [HEAD]
    L.append('# 이름 — 점수 구간 스무 칸')
    L.append('')
    L.append('관계를 안 가립니다. 연인에게도 친구에게도 동업자에게도 같은 말이 갑니다.')
    L.append('**카드에 나가는 글은 전부 여기 있습니다** — 요약 · 별명 · 본문 두 문장.')
    for i, row in enumerate(W.BAND):
        sum_, em, nick = row[0], row[1], row[2]
        body = row[3] if len(row) > 3 else ['', '']
        lo = W.BAND_MIN[i]
        hi = 99 if i == 0 else W.BAND_MIN[i - 1] - 1
        L.append('')
        L.append('## ' + str(lo) + '~' + str(hi) + '점')
        L.append('이모지 ' + em)
        L.append('요약   ' + sum_)
        L.append('별명   ' + nick)
        L.append('본문   ' + body[0])
        L.append('       ' + (body[1] if len(body) > 1 else ''))
    L.append('')
    L.append('')
    L.append('# 해설 — 관계 일곱 × 큰 칸 다섯')
    L.append('')
    L.append('여기가 관계를 맡습니다. 훅은 결과 화면과 카톡 설명글에,')
    L.append('본문 세 문장은 카드에 나갑니다.')
    for rel in W.RELS:
        L.append('')
        L.append('# ' + W.RELKO[rel] + ' [' + rel + ']')
        for i, (hook, lines) in enumerate(W.TALK[rel]):
            lo = W.STEP_MIN[i]
            hi = 99 if i == 0 else W.STEP_MIN[i - 1] - 1
            L.append('')
            L.append('## ' + str(lo) + '~' + str(hi) + '점')
            L.append('훅     ' + hook)
            L.append('본문   ' + lines[0])
            L.append('       ' + lines[1])
            L.append('       ' + lines[2])
    L.append(FOOT)
    io.open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(os.path.abspath(OUT))
    print('이름 ' + str(len(W.BAND)) + '칸 · 해설 ' +
          str(len(W.RELS) * len(W.STEP_MIN)) + '칸')


main()
