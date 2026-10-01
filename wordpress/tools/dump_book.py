# -*- coding: utf-8 -*-
"""한 손님이 받는 책을 글로 뽑습니다.

    python3 wordpress/tools/dump_book.py 2026 인성 관성 > 소희님책.md

사이트가 깨져 있어도 내용은 읽고 판단하실 수 있습니다.
"""
import io, os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
YEAR = sys.argv[1] if len(sys.argv) > 1 else '2026'
SP   = sys.argv[2] if len(sys.argv) > 2 else '인성'
DAE  = sys.argv[3] if len(sys.argv) > 3 else '관성'
NAME = sys.argv[4] if len(sys.argv) > 4 else '소희'

NY = json.load(io.open(os.path.join(HERE, 'NY%s.json' % YEAR), encoding='utf-8'))
CH = ['01','02','03','04','05','06','07','08','09','10']


def txt(h):
    s = str(h)
    s = re.sub(r'</p>\s*<p[^>]*>', '\n\n', s)
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'<h3[^>]*>', '\n### ', s)
    s = re.sub(r'</h3>', '\n', s)
    s = re.sub(r'<strong>|</strong>', '**', s)
    s = re.sub(r'<em>|</em>', '*', s)
    s = re.sub(r'<li[^>]*>', '\n- ', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('&nbsp;', ' ').replace('&amp;', '+')
    s = s.replace('{이름}', NAME).replace('{올해이름}', '채우고 다음을 준비하는 해')
    s = s.replace('{대운이름}', DAE + ' 흐름')
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()


print('# %s년 신년운세 — %s님' % (YEAR, NAME))
print('')
print('> 세운 **%s** · 대운 **%s** 로 뽑은 것입니다.' % (SP, DAE))
print('> 조각(patch160_ny%s)이 만드는 것과 같은 글입니다.' % YEAR)
print('')

total = 0
for ch in CH:
    for b in NY.get(ch, []):
        k = b.get('kind')
        use = False
        if k == 'title':
            print('\n---\n')
            print('# ' + txt(b.get('t', '')).replace('**', ''))
            print('')
            print(txt(b.get('h', '')))
            total += len(txt(b.get('h', '')))
            continue
        if k == 'always':
            use = True
        elif k == 'group':
            use = (b.get('key') == SP)
        elif k == 'branch':
            use = (b.get('group') == SP and b.get('key') == DAE)
        if not use:
            continue
        t = txt(b.get('t', ''))
        if t:
            print('\n## ' + t.replace('**', ''))
        h = txt(b.get('h', ''))
        if h:
            print('')
            print(h)
        total += len(h)

sys.stderr.write('글자 %s자\n' % format(total, ','))
