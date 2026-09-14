# -*- coding: utf-8 -*-
"""손님 한 명의 열 장을 골라봅니다 (조각이 할 일을 파이썬으로 흉내)"""
import io, json, sys
FIVE = ['비겁', '식상', '재성', '관성', '인성']
def nxt(x): return FIVE[(FIVE.index(x) + 1) % 5]
def rel(x, d):
    return ['겹침', '빠져나감', '부딪힘', '어긋남', '받쳐줌'][(FIVE.index(d) - FIVE.index(x)) % 5]

def pick(doc, sp, dae, power='even'):
    """sp = 일간이 정하는 무리(세운 십성) · dae = 대운 십성"""
    want = {'move': sp, 'dae': dae, 'power': power, 'rel': rel(sp, dae)}
    book = {}
    for no in sorted(doc):
        got = []
        for b in doc[no]:
            k = b['kind']
            if k in ('title', 'always'):
                got.append(b)
            elif k == 'group':
                if b['key'] == sp: got.append(b)
            elif k == 'branch':
                if b['group'] == sp and b['key'] == dae: got.append(b)
            elif k == 'pick':
                if want.get(b['axis']) == b['key']: got.append(b)
        book[no] = got
    return book

if __name__ == '__main__':
    year = sys.argv[1] if len(sys.argv) > 1 else '2027'
    doc = json.load(io.open('NY%s.json' % year, encoding='utf-8'))
    print('%-6s %-6s %s' % ('무리', '대운', '장마다 블록 수 · 글자 수'))
    bad = []
    sizes = []
    for sp in FIVE:
        for dae in FIVE:
            bk = pick(doc, sp, dae)
            n = {no: len(v) for no, v in bk.items()}
            ch = sum(len(b['h']) for v in bk.values() for b in v)
            sizes.append(ch)
            # 검사 — 갈래가 있는 장은 무리 1 + 갈래 1 이어야 합니다
            for no in doc:
                has_br = any(b['kind'] == 'branch' for b in doc[no])
                has_gp = any(b['kind'] == 'group'  for b in doc[no])
                br = [b for b in bk[no] if b['kind'] == 'branch']
                g  = [b for b in bk[no] if b['kind'] == 'group']
                if has_br and len(br) != 1: bad.append((sp, dae, no, 'branch', len(br)))
                if has_gp and len(g)  != 1: bad.append((sp, dae, no, 'group',  len(g)))
                ax = {}
                for b in doc[no]:
                    if b['kind'] == 'pick': ax[b['axis']] = 1
                got = {}
                for b in bk[no]:
                    if b['kind'] == 'pick': got[b['axis']] = got.get(b['axis'], 0) + 1
                for a in ax:
                    if got.get(a) != 1: bad.append((sp, dae, no, 'axis:' + a, got.get(a)))
            if sp == FIVE[0] and dae in (FIVE[0], FIVE[1]):
                print('%-6s %-6s %s  %d자' % (sp, dae, n, ch))
    print()
    print('스물다섯 조합 검사 — 어긋난 자리 %d' % len(bad))
    for b in bad[:8]: print('   ', b)
    print('손님 한 명이 받는 html %d ~ %d자 (평균 %d)' % (min(sizes), max(sizes), sum(sizes)//len(sizes)))
