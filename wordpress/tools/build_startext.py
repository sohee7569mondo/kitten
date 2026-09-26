# -*- coding: utf-8 -*-
"""스타사주-글.md 를 읽어 갈래별 문단 꾸러미로 만듭니다.

원고를 손으로 옮겨 적지 않습니다 (CLAUDE.md).
emit_startext.py 가 이것을 불러 조각을 뽑습니다.
"""
import io, os, re, sys

HERE  = os.path.dirname(os.path.abspath(__file__))
DRAFT = os.path.join(HERE, '..', 'drafts', '스타사주-글.md')

GAN  = list('甲乙丙丁戊己庚辛壬癸')
OH   = ['목', '화', '토', '금', '수']
SIP  = ['비견', '겁재', '식신', '상관', '편재', '정재',
        '편관', '정관', '편인', '정인']


def paragraphs(lines):
    """빈 줄로 문단을 가릅니다. 문단 안 줄바꿈은 빈칸으로 잇습니다."""
    out, buf = [], []
    for ln in lines:
        s = ln.rstrip()
        if not s.strip():
            if buf:
                out.append(' '.join(buf))
                buf = []
            continue
        t = s.strip()
        if t.startswith('★') or t.startswith('☞'):   # 제 메모는 안 내보냅니다
            continue
        # ★ 2026-09-16 · what / good / care 딱지와 --- 이 글에 붙어 나갔습니다.
        #   원고에 딱지 바로 다음 줄부터 글이 와서 (빈 줄이 없어서) 한 문단으로
        #   이어붙었습니다. 딱지는 문단을 끊고 버립니다. --- 은 거기서 멈춥니다.
        if t in ('what', 'good', 'care'):
            if buf:
                out.append(' '.join(buf))
                buf = []
            continue
        if t.startswith('---'):
            break
        buf.append(t)
    if buf:
        out.append(' '.join(buf))
    return out


def read():
    src = io.open(DRAFT, encoding='utf-8').read()
    lines = src.split('\n')

    part, head, body = '', '', []
    day, much, none, sip = {}, {}, {}, {}
    problems = []

    def flush():
        if not head:
            return
        ps = paragraphs(body)
        if part == '1':
            # what / good / care 라벨을 떼고 차례대로 잇습니다
            keep = [p for p in ps if p not in ('what', 'good', 'care')]
            g = head.split()[0]
            if g in GAN:
                day[g] = keep
        elif part == '2':
            for o in OH:
                if head.startswith(o):
                    much[o] = ps
        elif part == '3':
            for o in OH:
                if head.startswith(o):
                    none[o] = ps
        elif part == '4':
            for s in SIP:
                if head.startswith(s):
                    sip[s] = ps

    for ln in lines:
        m1 = re.match(r'^# (\d)\. ', ln)
        if m1:
            flush(); head, body = '', []
            part = m1.group(1)
            continue
        if ln.startswith('# '):          # 그 밖의 큰 제목 — 갈래를 닫습니다
            flush(); head, body = '', []
            part = ''
            continue
        if ln.startswith('## '):
            flush()
            head = ln[3:].strip()
            body = []
            continue
        if head:
            body.append(ln)
    flush()

    # ── 규칙 검사 ────────────────────────────────────────
    for g in GAN:
        if g not in day:
            problems.append('일간 %s 가 원고에 없습니다' % g)
    for o in OH:
        if o not in much:
            problems.append('「%s 가장 강합니다」 가 없습니다' % o)
        if o not in none:
            problems.append('「%s 없습니다」 가 없습니다' % o)
    for s in SIP:
        if s not in sip:
            problems.append('십성 %s 가 없습니다' % s)

    allp = []
    for d in (day, much, none, sip):
        for v in d.values():
            allp.extend(v)
    for p in allp:
        if "'" in p:
            problems.append('홑따옴표가 있습니다 : %s' % p[:40])
        if '&' in p:
            problems.append('앰퍼샌드가 있습니다 : %s' % p[:40])
        if '\\' in p:
            problems.append('역빗금이 있습니다 : %s' % p[:40])
        if '"' in p:
            problems.append('큰따옴표가 있습니다 : %s' % p[:40])
        if p.count('**') % 2:
            problems.append('굵게 표시가 짝이 안 맞습니다 : %s' % p[:40])

    return day, much, none, sip, problems


if __name__ == '__main__':
    day, much, none, sip, probs = read()
    print('일간 %d · 강한오행 %d · 없는오행 %d · 십성 %d'
          % (len(day), len(much), len(none), len(sip)))
    n = sum(len(v) for d in (day, much, none, sip) for v in d.values())
    c = sum(len(p) for d in (day, much, none, sip) for v in d.values() for p in v)
    print('문단 %d개 · %d자' % (n, c))
    if probs:
        print('\n★ 걸린 것 %d :' % len(probs))
        for p in probs:
            print('   ' + p)
        sys.exit(1)
    print('검사 통과')
