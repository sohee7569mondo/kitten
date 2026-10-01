# -*- coding: utf-8 -*-
"""한 손님이 **실제로 받는 책** 안에서 되풀이를 찾습니다.

소희 님 : 「리뷰 받았는데 반복되는 부분이 많다고 신년운세에서」

원고 전체를 통째로 대조하면 안 됩니다. 갈래별 글은 **한 손님이
하나만** 봅니다. ②장의 다섯 갈래가 서로 닮은 것은 자연스러워요.
진짜 문제는 **같은 사람이 열 장을 넘기며 같은 말을 다시 만나는 것**
입니다. 그래서 조각이 만든 JSON 에서 한 손님 몫만 뽑아 이어붙입니다.

    python3 wordpress/tools/find_repeat2.py 2026
    python3 wordpress/tools/find_repeat2.py 2026 재성 관성   (세운·대운 지정)

스물다섯 가지(세운 다섯 × 대운 다섯)를 다 돌려 가장 많이 겹치는
짝을 보여줍니다.
"""
import io, os, re, sys, json, itertools
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
YEAR = sys.argv[1] if len(sys.argv) > 1 else '2026'
NY = json.load(io.open(os.path.join(HERE, 'NY%s.json' % YEAR), encoding='utf-8'))
G = ['비겁', '식상', '재성', '관성', '인성']
CH = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']


def strip(t):
    t = re.sub(r'<[^>]+>', ' ', str(t))
    t = t.replace('{이름}', '').replace('{올해이름}', '').replace('{대운이름}', '')
    t = t.replace('님', '').replace('&nbsp;', ' ')
    return re.sub(r'\s+', ' ', t).strip()


def book(sp, dae):
    """세운 sp · 대운 dae 인 한 분이 받는 글을 장별로 모읍니다."""
    out = []
    for ch in CH:
        buf = []
        for b in NY.get(ch, []):
            k = b.get('kind')
            if k == 'title':
                buf.append(strip(b.get('h', '')))
            elif k == 'always':
                buf.append(strip(b.get('t', '')) + ' ' + strip(b.get('h', '')))
            elif k == 'group':
                if b.get('key') == sp:
                    buf.append(strip(b.get('t', '')) + ' ' + strip(b.get('h', '')))
            elif k == 'branch':
                if b.get('group') == sp:
                    if b.get('key') == dae:
                        buf.append(strip(b.get('t', '')) + ' ' + strip(b.get('h', '')))
        out.append((ch, ' '.join(buf)))
    return out


def sents(t):
    out = []
    for s in re.split(r'(?<=[.?!])\s+', t):
        s = s.strip()
        if len(s) >= 14:
            out.append(s)
    return out


def dups(pages):
    where = defaultdict(list)
    for ch, t in pages:
        for s in sents(t):
            where[s].append(ch)
    return [(s, sorted(set(w))) for s, w in where.items() if len(set(w)) > 1]


if len(sys.argv) > 3:
    pairs = [(sys.argv[2], sys.argv[3])]
else:
    pairs = list(itertools.product(G, G))

print('═══ %s년 — 한 손님이 받는 책 안의 되풀이 ═══' % YEAR)
print('')

score = []
for sp, dae in pairs:
    pages = book(sp, dae)
    d = dups(pages)
    chars = sum(len(t) for _, t in pages)
    score.append((len(d), sp, dae, d, chars))

score.sort(key=lambda x: -x[0])

print('── 스물다섯 가지 가운데 겹침이 많은 차례 ──────')
for n, sp, dae, d, chars in score[:8]:
    print('   세운 %s × 대운 %s   겹친 문장 %d개 · 책 %s자'
          % (sp, dae, n, format(chars, ',')))
print('')

n, sp, dae, d, chars = score[0]
print('── 가장 심한 짝: 세운 %s × 대운 %s ────────────' % (sp, dae))
if not d:
    print('   똑같은 문장은 없습니다.')
d.sort(key=lambda x: -len(x[0]))
for s, w in d[:14]:
    print('   [%s]' % ' · '.join(w))
    print('     %s' % (s[:88] + (' …' if len(s) > 88 else '')))
print('')

# ── 비슷한 문장 ─────────────────────────────────
# 똑같지는 않은데 읽는 사람에게는 「또 그 소리」로 들리는 것들입니다.
# 낱말을 견주어 열에 예닐곱이 같으면 비슷한 것으로 봅니다.
def words(s):
    return set(w for w in re.findall(r'[가-힣]{2,}', s) if len(w) >= 2)

def near(pages, lo=0.62):
    rows = []
    flat = []
    for ch, t in pages:
        for s in sents(t):
            flat.append((ch, s, words(s)))
    n = len(flat)
    for i in range(n):
        for j in range(i + 1, n):
            if flat[i][0] == flat[j][0]:
                continue            # 같은 장 안은 넘어갑니다
            a, b = flat[i][2], flat[j][2]
            if len(a) < 5 or len(b) < 5:
                continue
            same = len(a & b)
            r = same / float(min(len(a), len(b)))
            if r >= lo:
                rows.append((r, flat[i][0], flat[i][1], flat[j][0], flat[j][1]))
    rows.sort(key=lambda x: -x[0])
    return rows

print('── 비슷한 문장 (똑같지는 않지만 「또 그 소리」) ──')
print('   세운 %s × 대운 %s 로 봅니다' % (sp, dae))
nd = near(book(sp, dae))
seen = set()
shown = 0
for r, c1, s1, c2, s2 in nd:
    k = (s1[:20], s2[:20])
    if k in seen:
        continue
    seen.add(k)
    print('   %d%%  [%s → %s]' % (int(r * 100), c1, c2))
    print('      %s' % (s1[:76] + (' …' if len(s1) > 76 else '')))
    print('      %s' % (s2[:76] + (' …' if len(s2) > 76 else '')))
    shown += 1
    if shown >= 12:
        break
if shown == 0:
    print('   없습니다.')
print('')

print('── 모든 짝에서 한 번이라도 겹친 문장 (잦은 차례) ──')
allw = defaultdict(set)
for _, sp2, dae2, d2, _ in score:
    for s, w in d2:
        allw[s].add((sp2, dae2))
rows = sorted(allw.items(), key=lambda x: -len(x[1]))
for s, ps in rows[:14]:
    print('   %d/25 가지에서   %s' % (len(ps), s[:76] + (' …' if len(s) > 76 else '')))
