# -*- coding: utf-8 -*-
"""원고에서 되풀이되는 문장과 말버릇을 찾습니다.

소희 님 : 「지금 리뷰 받았는데 반복되는 부분이 많다고 신년운세에서」

사람 눈으로는 열 장을 한꺼번에 못 봅니다. 기계가 대신 셉니다.

    python3 wordpress/tools/find_repeat.py 2026
    python3 wordpress/tools/find_repeat.py 2027

세 가지를 봅니다
  ① 똑같은 문장이 여러 장에 나오는가
  ② 말버릇 — 같은 꼴이 몇 번 나오는가 (「어떤 해는 ~」 같은 것)
  ③ 장마다 되풀이되는 낱말
"""
import io, os, re, sys, glob
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
YEAR = sys.argv[1] if len(sys.argv) > 1 else '2026'

files = sorted(glob.glob(os.path.join(HERE, '..', 'drafts', '%s년운세-*.md' % YEAR)))
files = [f for f in files if '-00-' not in f and '보관' not in f and '설계' not in f
         and '문장설계표' not in f]
if not files:
    raise SystemExit('원고를 못 찾았습니다')


def clean(t):
    t = re.sub(r'<[^>]+>', '', t)
    t = t.replace('**', '').replace('*', '')
    t = t.replace('{이름}', '').replace('님', '')
    t = t.replace('{올해이름}', '').replace('{대운이름}', '')
    return t


def sentences(t):
    """문장으로 자릅니다. 마침표·물음표·느낌표 뒤에서."""
    out = []
    for line in t.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        if line.startswith('☞') or line.startswith('★'):
            continue      # 제 메모는 셈에서 뺍니다
        if line.startswith('|') or line.startswith('---'):
            continue
        for s in re.split(r'(?<=[.?!])\s+', clean(line)):
            s = s.strip()
            if len(s) >= 12:
                out.append(s)
    return out


docs = {}
for f in files:
    name = os.path.basename(f)
    m = re.search(r'-(\d\d)-', name)
    no = m.group(1) if m else '??'
    docs[no + ' ' + re.sub(r'^\d+년운세-\d\d-|\.md$', '', name)] = \
        sentences(io.open(f, encoding='utf-8').read())

print('═══ %s년 신년운세 — 되풀이 찾기 ═══' % YEAR)
print('   장 %d개 · 문장 %d개' % (len(docs), sum(len(v) for v in docs.values())))
print('')

# ① 똑같은 문장
print('── ① 똑같은 문장이 두 곳 이상 ──────────────')
where = defaultdict(list)
for ch, ss in docs.items():
    for s in ss:
        where[s].append(ch)
dup = [(s, w) for s, w in where.items() if len(set(w)) > 1]
dup.sort(key=lambda x: -len(x[1]))
if not dup:
    print('   없습니다.')
for s, w in dup[:12]:
    print('   [%s]' % ' · '.join(sorted(set(w))))
    print('     %s' % (s[:78] + (' …' if len(s) > 78 else '')))
print('')

# ② 말버릇 — 앞 열 글자가 같은 문장
print('── ② 같은 꼴로 시작하는 문장 (말버릇) ───────')
head = defaultdict(list)
for ch, ss in docs.items():
    for s in ss:
        k = s[:10].replace(' ', '')
        if len(k) >= 8:
            head[k].append((ch, s))
rows = [(k, v) for k, v in head.items() if len(v) >= 3]
rows.sort(key=lambda x: -len(x[1]))
if not rows:
    print('   없습니다.')
for k, v in rows[:10]:
    chs = sorted(set(c for c, _ in v))
    print('   「%s…」 %d번   [%s]' % (k, len(v), ' · '.join(chs)))
    for c, s in v[:3]:
        print('      %s  %s' % (c.split()[0], s[:66] + (' …' if len(s) > 66 else '')))
print('')

# ③ 장을 넘나드는 낱말
print('── ③ 여러 장에 걸쳐 자주 나오는 말 ──────────')
STOP = set('그리고 그런데 하지만 그래서 그러나 이것 그것 저것 무엇 사람 시간 마음 생각 자리 경우 정도 지금 올해 한번 우리 당신'.split())
cnt = Counter()
chs = defaultdict(set)
for ch, ss in docs.items():
    for s in ss:
        for w in re.findall(r'[가-힣]{2,6}', s):
            if w in STOP:
                continue
            cnt[w] += 1
            chs[w].add(ch.split()[0])
rows = [(w, n, len(chs[w])) for w, n in cnt.items() if n >= 12 and len(chs[w]) >= 5]
rows.sort(key=lambda x: -x[1])
for w, n, c in rows[:20]:
    print('   %-8s %3d번   %d장에 걸쳐' % (w, n, c))
