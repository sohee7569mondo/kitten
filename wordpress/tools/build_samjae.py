# -*- coding: utf-8 -*-
"""삼재 원고(.md) -> 조각 재료(SAMJAE.json)

블록마다 「언제 나가나」 딱지를 붙입니다. 조각은 목록을 돌며 걸러 냅니다.

  always                      누가 읽어도 나갑니다
  slotlead · slot             삼재 자리 여는 글 (그 자리 손님에게만)
  cell     · slot · stem      ④장 스무 칸 (자리 × 세운)
  cardslot · slot             카드 장 「지금 서 계신 문」
  gauge    · axis · key       겹쳐 읽기 아홉 문장

★ ☞ 나 ★ 로 시작하는 문단은 제 메모라 책에 안 내보냅니다.
★ 삼재는 띠로 정해집니다. 십성은 「그 해에 무엇이 흔들리나」를
  읽으려고 겹치는 것입니다 (전통 삼재론에 십성은 없습니다).
"""
import re, json, os, io

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'drafts', '삼재-원고.md')

FIVE = ['비겁', '식상', '재성', '관성', '인성']
SLOTS = ['들어오는 해', '머무는 해', '나가는 해', '삼재가 아닐 때']
SLOTKEY = {'들어오는 해': 'in', '머무는 해': 'stay',
           '나가는 해': 'out', '삼재가 아닐 때': 'none'}
AXIS = {'큰 카드가 몇 장인가': 'major',
        '숫자가 오르나 내리나': 'trend',
        '뒤집힌 것이 몇 장인가': 'rev'}
GKEY = {'없음': 'none', '한 장': 'one', '두 장 이상': 'many',
        '오름': 'up', '내림': 'down', '평평': 'flat'}


def md2html(block):
    """원고 한 덩어리를 HTML 로. 태그 속성은 홑따옴표 — 역빗금이 안 생깁니다."""
    out = []
    for para in re.split(r'\n\s*\n', block.strip()):
        para = para.strip()
        if not para or para == '---':
            continue
        if para.lstrip().startswith('★') or para.lstrip().startswith('☞'):
            continue
        if para.startswith('> '):
            txt = '<br>'.join(re.sub(r'^>\s?', '', l) for l in para.split('\n'))
            txt = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', txt, flags=re.S)
            out.append("<blockquote class='sjsay'>%s</blockquote>" % txt)
            continue
        if para.startswith('    ') or para.startswith('\t'):
            txt = '\n'.join(l.strip() for l in para.split('\n'))
            out.append("<pre class='sjbox'>%s</pre>" % txt)
            continue
        para = para.replace('\n', ' ')
        para = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', para, flags=re.S)
        para = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', para)
        out.append('<p>%s</p>' % para)
    return ''.join(out)


def chunks(text):
    """빈 줄로 나눈 뒤 메모를 버리고 남은 것만."""
    keep = []
    for para in re.split(r'\n\s*\n', text.strip()):
        p = para.strip()
        if not p or p == '---':
            continue
        if p.startswith('★') or p.startswith('☞'):
            continue
        keep.append(p)
    return '\n\n'.join(keep)


def parse():
    src = io.open(SRC, encoding='utf-8').read()
    heads = [m for m in re.finditer(r'^## (.+)$', src, re.M)]
    out = []
    for k, m in enumerate(heads):
        end = heads[k + 1].start() if k + 1 < len(heads) else len(src)
        title = m.group(1).split('☞')[0].strip()
        body = src[m.end():end]
        is_card = title.startswith('카드 세 장')

        # 장 제목
        out.append({'kind': 'always', 'h': "<h2 class='sjh2'>%s</h2>" % title})

        # 갈래(# [..]) 가 없는 앞부분
        cut = body.find('\n# [')
        head_part = body if cut < 0 else body[:cut]
        h = md2html(sub_heads(head_part))
        if h:
            out.append({'kind': 'always', 'h': h})
        if cut < 0:
            continue

        for gm in re.finditer(r'^# \[(.+?)\]\s*$', body, re.M):
            name = gm.group(1)
            nx = re.search(r'^# \[', body[gm.end():], re.M)
            seg = body[gm.end():gm.end() + nx.start()] if nx else body[gm.end():]

            if name in AXIS:                       # 겹쳐 읽기 아홉 문장
                axis = AXIS[name]
                for para in re.split(r'\n\s*\n', chunks(seg)):
                    mm = re.match(r'^\*\*(.+?)\*\*\s*—\s*(.+)$', para.strip(), re.S)
                    if not mm:
                        continue
                    key = GKEY.get(mm.group(1).strip())
                    if not key:
                        raise SystemExit('모르는 잣대 열쇠 : %s' % mm.group(1))
                    out.append({'kind': 'gauge', 'axis': axis, 'key': key,
                                'h': md2html(mm.group(2))})
                continue

            if name not in SLOTKEY:
                raise SystemExit('모르는 갈래 : %s' % name)
            slot = SLOTKEY[name]

            # 갈래 여는 글 (### 앞)
            c2 = seg.find('\n### ')
            lead = seg if c2 < 0 else seg[:c2]
            h = md2html(lead)
            if h:
                out.append({'kind': 'cardslot' if is_card else 'slotlead',
                            'slot': slot, 'h': h})
            if c2 < 0:
                continue

            for cm in re.finditer(r'^### (.+?)\s*\[(%s)\]\s*$' % '|'.join(FIVE),
                                  seg, re.M):
                nx2 = re.search(r'^### ', seg[cm.end():], re.M)
                cell = seg[cm.end():cm.end() + nx2.start()] if nx2 else seg[cm.end():]
                out.append({'kind': 'cell', 'slot': slot, 'stem': cm.group(2),
                            't': cm.group(1).strip(), 'h': md2html(cell)})
    return out


def sub_heads(text):
    """### 소제목을 굵은 줄로 바꿉니다 (갈래가 아닌 것)."""
    return re.sub(r'^### (.+?)$', r'**\1**', text, flags=re.M)


if __name__ == '__main__':
    blocks = parse()
    doc = {'blocks': blocks}
    p = os.path.join(HERE, 'SAMJAE.json')
    io.open(p, 'w', encoding='utf-8').write(
        json.dumps(doc, ensure_ascii=False, indent=1))
    n = {}
    for b in blocks:
        n[b['kind']] = n.get(b['kind'], 0) + 1
    print('SAMJAE.json 썼습니다 — 블록 %d개' % len(blocks))
    for k in sorted(n):
        print('   %-9s %d' % (k, n[k]))
    cells = [b for b in blocks if b['kind'] == 'cell']
    if len(cells) != 20:
        print('★ 스무 칸이 아닙니다 : %d' % len(cells))
    g = [b for b in blocks if b['kind'] == 'gauge']
    if len(g) != 9:
        print('★ 겹쳐 읽기가 아홉이 아닙니다 : %d' % len(g))
