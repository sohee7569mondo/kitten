# -*- coding: utf-8 -*-
"""갈래로 갈라 쓴 것만 모아서 보여줍니다.

2026-09-14 · 소희 님 : 「개인 설명부분을 갈래쓰기로 모아주면 수정할수
있을듯해 갈라쓰기항목만 줘봐」

모두에게 나가는 글(always · title)은 빼고, 손님마다 달라지는 것만
모읍니다. 소희 님이 고치기 좋게 갈래별로 묶어 냅니다.

    python3 dump_split.py 2026 01      한 장만
    python3 dump_split.py 2026         열 장 다
"""
import io, json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ['비겁', '식상', '재성', '관성', '인성']
DAE = {'비겁': '나를 세우는 십 년', '식상': '밖으로 펼치는 십 년',
       '재성': '거두고 쌓는 십 년', '관성': '자리를 만드는 십 년',
       '인성': '배우고 채우는 십 년'}
POW = {'much': '넉넉한 자리', 'few': '비어 있던 자리', 'even': '알맞은 자리'}


def text(h):
    s = str(h or '')
    s = re.sub(r'</(h2|h3|p|blockquote|pre)>', '\n\n', s)
    s = s.replace('<br>', '\n')
    s = re.sub(r'<strong>(.*?)</strong>', r'**\1**', s, flags=re.S)
    s = re.sub(r'<em>(.*?)</em>', r'*\1*', s, flags=re.S)
    s = re.sub(r'<blockquote[^>]*>', '> ', s)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\n{3,}', '\n\n', s).strip()


def blank(b):
    n = len(text(b['h']))
    return u'(여기에 쓰세요 · 지금 %d자)\n\n\n' % n


def run(year, only=None, skel=False):
    doc = json.loads(io.open(os.path.join(HERE, 'NY%s.json' % year),
                             encoding='utf-8').read())
    out = []
    w = out.append
    if skel:
        w(u'# %s년 운세 — 갈라쓰기 칸' % year)
        w(u'')
        w(u'소희 님이 채우실 자리만 모았습니다. **모두에게 나가는 글은 뺐습니다.**')
        w(u'')
        w(u'☞ 대괄호 **[비겁] [거두고 쌓는 십 년] 은 그대로 두세요.**')
        w(u'   제가 갈래를 고르는 표시입니다 — 책에는 안 나갑니다.')
        w(u'☞ **{이름} {올해이름} {대운이름}** 도 그대로 두세요.')
        w(u'   손님 것으로 채워집니다 (소희 님이면 「채우고 다음을 준비하는 해」).')
        w(u'☞ 「지금 N자」는 제가 써 둔 글의 길이입니다. 맞추실 필요 없습니다 —')
        w(u'   가늠만 하시라고 적었습니다. 0자는 아직 빈 칸입니다.')
        w(u'☞ 줄을 나눠 적으셔도 책에서는 한 줄로 흐릅니다. 인용은 「> 」로 시작.')
        w(u'☞ **한 자리라도 비면 그 손님 책에 구멍이 납니다.**')
    else:
        w(u'# %s년 운세 — 갈래로 갈라 쓴 것만' % year)
        w(u'')
        w(u'☞ 모두에게 나가는 글은 뺐습니다. 손님마다 달라지는 것만 모았습니다.')
        w(u'☞ 고치실 때 **대괄호 꼬리표 [비겁] 은 그대로 두세요** — 제가 갈래를')
        w(u'   고르는 표시입니다. 책에는 안 나갑니다.')
        w(u'☞ {이름} {올해이름} {대운이름} 도 그대로 두세요 — 손님 것으로 채워집니다.')
    for no in sorted(k for k in doc if k.isdigit()):
        if only and no != only:
            continue
        bs = doc[no]
        ttl = ''
        for b in bs:
            if b['kind'] == 'title':
                ttl = re.sub(r'^[①②③④⑤⑥⑦⑧⑨⑩]\s*', '',
                             re.sub(r'<[^>]+>', '', str(b['t'] or '')))
                break
        picks = [b for b in bs if b['kind'] not in ('always', 'title')]
        if not picks:
            continue
        w(u'')
        w(u'─' * 58)
        w(u'# %s장 · %s' % (no, ttl))
        w(u'─' * 58)

        # 갈래(세운) — 비겁부터 차례로, 한 갈래에 여러 토막이면 차례대로
        for g in ORDER:
            ps = [b for b in picks if b['kind'] == 'group' and b['key'] == g]
            if not ps:
                continue
            w(u'')
            w(u'## [%s]' % g)
            for i, b in enumerate(ps):
                t = re.sub(r'<[^>]+>', '', str(b.get('t') or ''))
                w(u'')
                w(u'### %d번째 토막%s' % (i + 1, (' · 제목 「%s」' % t) if t else ''))
                w(u'')
                w(blank(b) if skel else (text(b['h']) or '(제목만 있고 본문 없음)'))

        # 대운
        for g in ORDER:
            ps = [b for b in picks if b['kind'] == 'dae' and b['key'] == g]
            if not ps:
                continue
            w(u'')
            w(u'## [%s]' % DAE[g])
            for b in ps:
                t = re.sub(r'<[^>]+>', '', str(b.get('t') or ''))
                w(u'')
                if t:
                    w(u'### 제목 「%s」' % t)
                    w(u'')
                w(blank(b) if skel else text(b['h']))

        # 강도 셋
        for k in ('much', 'few', 'even'):
            ps = [b for b in picks if b['kind'] == 'pick'
                  and b.get('axis') == 'power' and b['key'] == k]
            for b in ps:
                w(u'')
                w(u'## [%s]' % POW[k])
                w(u'')
                w(blank(b) if skel else text(b['h']))

        # 갈래 × 대운 스물다섯
        br = [b for b in picks if b['kind'] == 'branch']
        if br:
            w(u'')
            w(u'## 갈래 × 십 년 — 스물다섯 자리')
            for g in ORDER:
                for d in ORDER:
                    for b in br:
                        if b['group'] == g and b['key'] == d:
                            w(u'')
                            w(u'### [%s] × [%s]' % (g, DAE[d]))
                            w(u'')
                            w(blank(b) if skel else text(b['h']))
        # 그 밖의 pick
        for b in picks:
            if b['kind'] == 'pick' and b.get('axis') != 'power':
                w(u'')
                w(u'## [%s · %s]' % (b.get('axis'), b.get('key')))
                w(u'')
                w(text(b['h']))
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    year = sys.argv[1] if len(sys.argv) > 1 else '2026'
    args = sys.argv[2:]
    skel = '틀' in args
    args = [a for a in args if a != '틀']
    only = args[0] if args else None
    s = run(year, only, skel)
    name = '갈래쓰기%s-%s%s.md' % (('칸' if skel else ''), year,
                                   ('-' + only) if only else '')
    path = os.path.join(HERE, '..', 'drafts', name)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('썼습니다 %s · %d자' % (os.path.normpath(path), len(s)))
