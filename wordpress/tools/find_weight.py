# -*- coding: utf-8 -*-
"""장마다 「힘을 얼마나 줬는지」를 잽니다.

소희 님 : 「우리가 10장을 만드는데 전부 힘을 준 건 아닌가 생각중.
          힘을 뺄 땐 뺐어야 하는데」

되풀이가 아니라 **강약이 없는 것**일 수 있습니다. 열 장이 다 같은
무게로 밀어붙이면 읽는 사람은 「또 그 소리」로 느낍니다.
힘을 준 표시를 장마다 세어 봅니다.

    python3 wordpress/tools/find_weight.py 2026 인성 관성
"""
import io, os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
YEAR = sys.argv[1] if len(sys.argv) > 1 else '2026'
SP   = sys.argv[2] if len(sys.argv) > 2 else '인성'
DAE  = sys.argv[3] if len(sys.argv) > 3 else '관성'
NY = json.load(io.open(os.path.join(HERE, 'NY%s.json' % YEAR), encoding='utf-8'))
CH = ['01','02','03','04','05','06','07','08','09','10']

TITLE = {}
pages = {}
for ch in CH:
    buf = []
    for b in NY.get(ch, []):
        k = b.get('kind')
        if k == 'title':
            TITLE[ch] = re.sub(r'<[^>]+>', '', str(b.get('t', '')))
            buf.append(str(b.get('h', '')))
        elif k == 'always':
            buf.append(str(b.get('t', '')) + str(b.get('h', '')))
        elif k == 'group':
            if b.get('key') == SP:
                buf.append(str(b.get('t', '')) + str(b.get('h', '')))
        elif k == 'branch':
            if b.get('group') == SP and b.get('key') == DAE:
                buf.append(str(b.get('t', '')) + str(b.get('h', '')))
    pages[ch] = ' '.join(buf)


def plain(h):
    s = re.sub(r'<[^>]+>', ' ', h)
    return re.sub(r'\s+', ' ', s).strip()


print('═══ %s년 — 장마다 힘을 얼마나 줬나 (세운 %s × 대운 %s) ═══'
      % (YEAR, SP, DAE))
print('')
print('  장                     글자   문단  굵게  「」  소제목  ~하세요  힘')
print('  ' + '─' * 74)

rows = []
for ch in CH:
    h = pages[ch]
    t = plain(h)
    chars = len(t)
    paras = h.count('<p')
    bold  = h.count('<strong>')
    quote = t.count('「')
    h3    = h.count('<h3')
    order = len(re.findall(r'(하세요|보세요|마세요|두세요|주세요)', t))
    per = (bold + quote + order) / max(chars / 1000.0, 1)   # 천 자당 힘 준 횟수
    rows.append((ch, chars, paras, bold, quote, h3, order, per))

for ch, chars, paras, bold, quote, h3, order, per in rows:
    name = TITLE.get(ch, '')[:16]
    bar = '█' * int(round(per / 2.0))
    print('  %-2s %-18s %5s  %4d  %4d  %4d  %5d  %6d  %s %.0f'
          % (ch, name, format(chars, ','), paras, bold, quote, h3, order, bar, per))

print('')
tot = sum(r[1] for r in rows)
print('  모두 %s자 · 한 장 평균 %s자' % (format(tot, ','), format(tot // 10, ',')))
lo = min(rows, key=lambda r: r[1])
hi = max(rows, key=lambda r: r[1])
print('  가장 긴 장 %s(%s자) · 가장 짧은 장 %s(%s자) — 차이 %.1f배'
      % (hi[0], format(hi[1], ','), lo[0], format(lo[1], ','), hi[1] / float(lo[1])))
print('')
print('  ★ 힘(맨 오른쪽)은 천 자마다 굵게 · 「」 · 시키는 말이 몇 번 나오는가입니다.')
print('    책은 큰 장과 쉬어가는 장이 번갈아야 읽힙니다. 막대가 고르면')
print('    열 장이 다 같은 목소리로 말하고 있다는 뜻입니다.')
