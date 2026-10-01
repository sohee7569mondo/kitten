# -*- coding: utf-8 -*-
"""장마다 「모두에게 나가는 글(always)」을 셉니다.

2026-09-14 · 소희 님 : 「다른데도 그런지 체크 해야 할듯」
②장에서 남의 이야기가 모두에게 나가던 것을 고쳤습니다. 같은 일이
다른 장에도 있는지 봅니다. 짐작하지 않고 JSON 을 직접 셉니다.

의심 표시(★)를 다는 기준 —
  · 다섯 갈래 이름(비겁…)이 둘 이상 나오는 always
  · 대운 이름(나를 세우는 십 년…)이 나오는 always
  · 나란한 always 가 셋 이상 이어지고 길이가 비슷한 것 (갈래별 글의 냄새)
"""
import io, json, re, sys, os

HERE = '/home/user/kitten/wordpress/tools'
FIVE = ['비겁', '식상', '재성', '관성', '인성']
DAENAMES = ['나를 세우는 십 년', '밖으로 펼치는 십 년', '거두고 쌓는 십 년',
            '자리를 만드는 십 년', '배우고 채우는 십 년']

def txt(h):
    return re.sub(r'<[^>]+>', '', str(h or ''))

for year in (sys.argv[1:] or ['2026', '2027']):
    doc = json.loads(io.open(os.path.join(HERE, 'NY%s.json' % year), encoding='utf-8').read())
    print('\n' + '═' * 62)
    print('  %s년 — 모두에게 나가는 글' % year)
    print('═' * 62)
    tot_all, tot_pick = 0, 0
    for no in sorted(k for k in doc if k.isdigit()):
        bs = doc[no]
        a_chars = sum(len(txt(b['h'])) for b in bs if b['kind'] in ('always', 'title'))
        # 한 손님이 실제로 받는 고른 글 — 갈래마다 하나씩만
        sel = {}
        for b in bs:
            if b['kind'] in ('always', 'title'):
                continue
            k = (b['kind'], b.get('axis') or '', b.get('group') or '')
            sel.setdefault(k, []).append(len(txt(b['h'])))
        p_chars = sum(sum(v) // max(1, len(v)) for v in sel.values())
        tot_all += a_chars; tot_pick += p_chars
        flags = []
        run, runlen = 0, []
        for b in bs:
            if b['kind'] != 'always':
                if run >= 3: flags.append('나란한 always %d개' % run)
                run = 0; continue
            run += 1
            t = txt(b['h']) + ' ' + txt(b.get('t'))
            hit = [g for g in FIVE if g in t]
            if len(hit) >= 2:
                flags.append('갈래말 %s · %s' % ('/'.join(hit[:3]), (txt(b.get('t')) or '(제목없음)')[:24]))
            for d in DAENAMES:
                if d in t:
                    flags.append('대운말 「%s」 · %s' % (d, (txt(b.get('t')) or '(제목없음)')[:20]))
                    break
        if run >= 3: flags.append('나란한 always %d개' % run)
        mark = '★' if flags else '  '
        print('%s %s  모두 %6d자  ·  고른 것 %6d자' % (mark, no, a_chars, p_chars))
        seen = set()
        for f in flags:
            if f in seen: continue
            seen.add(f)
            print('        - ' + f)
    print('  ' + '-' * 58)
    print('   합계  모두 %6d자  ·  고른 것 %6d자  ·  한 손님 %6d자'
          % (tot_all, tot_pick, tot_all + tot_pick))
