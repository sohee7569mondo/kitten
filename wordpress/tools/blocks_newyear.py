# -*- coding: utf-8 -*-
"""원천 문장 — 갈래별로 모아서 봅니다.

2026-09-14 · 소희 님 :
  「2026년 문장을 바로 2027년용으로 복사하는 것이 아니라, 지금 만든
   1~9장의 문장을 한 번 '원천 문장'으로 정리해야 합니다.」
  「[세운 의미] + [대운 의미] + [장별 의미] + [실천 문장] 으로 분해」

지금 원고는 이미 그 꼴로 나뉘어 있습니다 — 다만 장별로 흩어져 있어
한눈에 안 보입니다. 이 도구가 그것을 **갈래 기준으로 세로로 모읍니다.**

    python3 blocks_newyear.py 2026 세운    비겁의 아홉 장을 한자리에
    python3 blocks_newyear.py 2026 대운    나를 세우는 십 년의 아홉 장을
    python3 blocks_newyear.py 2026 조합    비겁 × 나를 세우는 십 년 …

이렇게 보면 「채우는 흐름의 핵심」이 장마다 어떻게 변주되는지 보이고,
다음 해에는 그 핵심만 가져다 새 해의 표현으로 갈아입히면 됩니다.
"""
import io, json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ['비겁', '식상', '재성', '관성', '인성']
DAE = {'비겁': '나를 세우는 십 년', '식상': '밖으로 펼치는 십 년',
       '재성': '거두고 쌓는 십 년', '관성': '자리를 만드는 십 년',
       '인성': '배우고 채우는 십 년'}
ROLE = {'01': '올해 어떤 해인가', '02': '무엇이 움직이는가',
        '03': '무엇이 들어오는가', '04': '무엇을 조심해야 하는가',
        '05': '언제 기회가 커지는가', '06': '무엇을 시작하고 내려놓는가',
        '07': '돈과 일은 어떻게 움직이는가', '08': '사람과 관계는 어떻게 달라지는가',
        '09': '그래서 무엇을 기억해야 하는가', '10': '마지막으로 건네는 말'}


def text(h):
    s = re.sub(r'</(h2|h3|p|blockquote|pre)>', '\n\n', str(h or ''))
    s = s.replace('<br>', '\n')
    s = re.sub(r'<strong>(.*?)</strong>', r'**\1**', s, flags=re.S)
    s = re.sub(r'<blockquote[^>]*>', '> ', s)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\n{3,}', '\n\n', s).strip()


def run(year, mode):
    doc = json.loads(io.open(os.path.join(HERE, 'NY%s.json' % year),
                             encoding='utf-8').read())
    nos = sorted(k for k in doc if k.isdigit())
    o = []
    w = o.append
    title = {'세운': '세운 — 올해의 갈래 다섯',
             '대운': '대운 — 십 년의 갈래 다섯',
             '조합': '세운 × 대운 — 스물다섯 자리'}[mode]
    w(u'# %s년 원천 문장 · %s' % (year, title))
    w(u'')
    w(u'☞ 장마다 흩어져 있던 것을 **갈래 기준으로 세로로** 모았습니다.')
    w(u'☞ 한 갈래가 아홉 장에서 어떻게 변주되는지 한눈에 보입니다.')
    w(u'☞ 다음 해에는 이 핵심만 가져가고 표현만 그 해에 맞게 갈아입히면 됩니다.')
    w(u'☞ {연도} {간지} {올해오행} {이름} {올해이름} {대운이름} 은 자동으로 채워집니다.')

    def dump(sel, head):
        got = False
        for no in nos:
            for b in doc[no]:
                if not sel(b):
                    continue
                t = re.sub(r'<[^>]+>', '', str(b.get('t') or ''))
                body = text(b['h'])
                if not body and not t:
                    continue
                if not got:
                    w(u''); w(u'─' * 58); w(u'# %s' % head); w(u'─' * 58); got = True
                w(u'')
                w(u'## %s장 · %s' % (no, ROLE.get(no, '')))
                if t:
                    w(u'')
                    w(u'### 제목 「%s」' % t)
                w(u'')
                w(body or '(제목만)')

    if mode == '세운':
        for g in ORDER:
            dump(lambda b, g=g: b['kind'] == 'group' and b['key'] == g, '[%s]' % g)
    elif mode == '대운':
        for g in ORDER:
            dump(lambda b, g=g: b['kind'] == 'dae' and b['key'] == g, '[%s]' % DAE[g])
    else:
        for g in ORDER:
            for l in ORDER:
                dump(lambda b, g=g, l=l: b['kind'] == 'branch'
                     and b['group'] == g and b['key'] == l,
                     '[%s] × [%s]' % (g, DAE[l]))
    return '\n'.join(o) + '\n'


if __name__ == '__main__':
    year = sys.argv[1] if len(sys.argv) > 1 else '2026'
    mode = sys.argv[2] if len(sys.argv) > 2 else '세운'
    s = run(year, mode)
    path = os.path.join(HERE, '..', 'drafts', '원천문장-%s-%s.md' % (year, mode))
    io.open(path, 'w', encoding='utf-8').write(s)
    print('썼습니다 %s · %d자' % (os.path.normpath(path), len(s)))
