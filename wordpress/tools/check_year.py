# -*- coding: utf-8 -*-
"""원고에 해·오행이 박혀 있는지 찾습니다.

2026-09-14 · 소희 님 : 「2026년이라는 표현은 문장에서 빼세요」
                       「{연도} 또는 올해를 쓰세요」

박혀 있으면 다음 해에 그 문장을 못 씁니다. 조각을 만들기 전에 이것을
돌려 0 이 나오는지 봅니다. 「올해」는 얼마든지 써도 됩니다 —
책이 그려질 때 그 해를 뜻하니까요.

    python3 check_year.py 2026
"""
import io, json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
# 해마다 달라지는 것 — 이것이 글에 박혀 있으면 안 됩니다
BAD = [
    (r'20\d\d\s*년', '해 (→ {연도}년 · {다음해}년 · {지난해}년)'),
    (r'(갑자|을축|병인|정묘|무진|기사|경오|신미|임신|계유|갑술|을해|병자|정축|무인|기묘'
     r'|경진|신사|임오|계미|갑신|을유|병술|정해|무자|기축|경인|신묘|임진|계사|갑오|을미'
     r'|병신|정유|무술|기해|경자|신축|임인|계묘|갑진|을사|병오|정미|무신|기유|경술|신해)\s*년',
     '간지 (→ {간지})'),
    (r'(?<![변조변]) ?(목|화|토|금|수)의 (기운|움직임|해|성질)', '오행 (→ {올해오행})'),
]


def run(year):
    doc = json.loads(io.open(os.path.join(HERE, 'NY%s.json' % year),
                             encoding='utf-8').read())
    hits = []
    for no in sorted(k for k in doc if k.isdigit()):
        for b in doc[no]:
            s = re.sub(r'<[^>]+>', '', str(b.get('t') or '') + ' ' + str(b.get('h') or ''))
            for pat, why in BAD:
                for m in re.finditer(pat, s):
                    a = max(0, m.start() - 18)
                    hits.append((no, why, s[a:m.end() + 22].replace('\n', ' ')))
    print('%s년 원고 — 해가 박힌 자리 %d곳' % (year, len(hits)))
    for no, why, t in hits:
        print('  ★ %s장 · %s\n       …%s…' % (no, why, t))
    if not hits:
        print('  모두 빈칸입니다 — 다음 해에도 그대로 쓸 수 있습니다.')
    return len(hits)


if __name__ == '__main__':
    sys.exit(1 if run(sys.argv[1] if len(sys.argv) > 1 else '2026') else 0)
