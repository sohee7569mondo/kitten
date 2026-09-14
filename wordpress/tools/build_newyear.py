# -*- coding: utf-8 -*-
"""신년운세 원고(.md) -> 조각 재료(JSON)

2026 · 2027 두 해를 같은 틀로 먹습니다.
각 장을 **차례 있는 블록 목록**으로 바꾸고, 블록마다 「언제 나가나」
딱지를 붙입니다. 조각은 그 목록을 차례로 돌며 걸러 내보내면 됩니다.

  always                    누가 읽어도 나갑니다
  pick  · axis · key        그 축에서 하나만 고릅니다 (강도 · 이동 · 대운 · 관계)
  group · key               무리 머리 (일간으로 고름)
  branch· group · key       갈래 (무리 × 대운)
  cond  · key               조건이 맞을 때만 (삼재 따위)
"""
import re, json, os, io, sys

SRC = '/home/user/kitten/wordpress/drafts'
# 2026-09-14 · 결과는 어디서 돌리든 이 도구 옆에 씁니다.
#   그전에는 현재 폴더에 써서, 저장소 뿌리에서 돌리면 NY2026.json 이
#   엉뚱한 데 떨어지고 emit 은 옛 파일을 읽었습니다 (⑩ 제목이 안 바뀜).
HERE = os.path.dirname(os.path.abspath(__file__))
FIVE = ['비겁', '식상', '재성', '관성', '인성']
DAE = {'나를 세우는 십 년': '비겁', '밖으로 펼치는 십 년': '식상',
       '거두고 쌓는 십 년': '재성', '자리를 만드는 십 년': '관성',
       '배우고 채우는 십 년': '인성'}
# 무리 제목 -> 그 무리의 출발 십성 (일간으로 고릅니다)
GROUP_SP = {
 '내가 세운 것을 밖으로 내놓는 해': '비겁', '내놓은 것이 결과가 되는 해': '식상',
 '거둔 것이 자리가 되는 해': '재성', '맡은 자리가 배움이 되는 해': '관성',
 '채운 것이 나를 세우는 해': '인성',
 # 2026 무리 이름
 '내가 정하고 내가 서는 해': '비겁', '내놓고 펼치는 해': '식상',
 '거두고 결과를 만드는 해': '재성', '자리를 만들고 책임지는 해': '관성',
 '채우고 다음을 준비하는 해': '인성',
}

def md2html(block):
    out = []
    for para in re.split(r'\n\s*\n', block.strip()):
        para = para.strip()
        if not para or para == '---':
            continue
        if para.lstrip().startswith(u'★') or para.lstrip().startswith(u'☞'):
            continue                              # ★ ☞ 는 제 메모입니다
        if para.startswith('    ') or para.startswith('\t'):
            txt = '\n'.join(l.strip() for l in para.split('\n'))
            out.append("<pre class='nybox'>%s</pre>" % txt)
            continue
        if para.startswith('> '):
            txt = '<br>'.join(re.sub(r'^>\s?', '', l) for l in para.split('\n'))
            txt = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', txt, flags=re.S)
            out.append("<blockquote class='nysay'>%s</blockquote>" % txt)
            continue
        para = para.replace('\n', '<br>')
        para = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', para, flags=re.S)
        para = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', para)
        cls = ''
        if para.startswith('<em>') and para.endswith('</em>'):
            cls = " class='mini'"
        elif para.startswith('<strong>') and para.endswith('</strong>'):
            cls = " class='keepline'"
        out.append('<p%s>%s</p>' % (cls, para))
    return ''.join(out)

def strip_marks(t):
    return re.sub(r'\*\*(.+?)\*\*', r'\1', t).strip()

def body_of(fn):
    s = io.open(os.path.join(SRC, fn), encoding='utf-8').read()
    m = re.search(r'(?m)^#{4,5} [①②③④⑤⑥⑦⑧⑨⑩]', s)
    if not m:
        raise SystemExit('장 제목을 못 찾았습니다: ' + fn)
    return s[m.start():]

# ── 2층·3층 따위 「축」을 제목으로 알아봅니다 ───────────────────
def axis_of(title):
    t = strip_marks(title)
    if t.startswith('1층'): return 'power'      # 강도 셋
    if t.startswith('2층'): return 'move'       # 이동 다섯
    if t.startswith('3층'): return 'dae'        # 대운 다섯
    if '십 년과 만나는 자리' in t: return 'rel'  # 관계 다섯
    if t.startswith('{이름}님의 2027년은'): return 'move'
    if t.startswith('{이름}님의 2026년은'): return 'move'
    return None

POWER = {'넉넉한 자리': 'much', '비어 있던 자리': 'few', '알맞은 자리': 'even'}

def key_of(axis, title):
    t = strip_marks(title)
    if axis == 'power':
        for k, v in POWER.items():
            if t.startswith(k): return v
    if axis == 'move':
        m = re.match(r'^(\S+) → (\S+)', t)
        if m and m.group(1) in FIVE: return m.group(1)
    if axis == 'dae':
        m = re.match(r'^(\S+) · (.+ 십 년)$', t)
        if m: return m.group(1)
        for name, sp in DAE.items():
            if name in t: return sp
    if axis == 'rel':
        m = re.match(r'^(\S+) → (\S+)$', t)
        if m: return m.group(1)
    return None

def parse(fn):
    body = body_of(fn)
    blocks = []
    cur = {'lv': 0, 'title': None, 'buf': []}
    stack = []          # 지금 열려 있는 무리 / 축
    group = None        # 무리 안인가
    axis = None         # 축 안인가

    def flush(node, kind_hint=None):
        h = md2html('\n'.join(node['buf']))
        if not h and not node['title']:
            return
        blocks.append({'lv': node['lv'], 'title': node['title'], 'h': h})

    rows = []
    curt, curlv, buf = None, 0, []
    for line in body.split('\n'):
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            rows.append((curlv, curt, '\n'.join(buf)))
            curlv, curt, buf = len(m.group(1)), m.group(2).strip(), []
        else:
            buf.append(line)
    rows.append((curlv, curt, '\n'.join(buf)))

    out = []
    prev_branch = None
    for lv, title, text in rows:
        h = md2html(text)
        t = strip_marks(title) if title else None

        # ── 2026 꼴 · 제목 하나에 무리와 대운이 같이 있는 갈래 ──
        mb = re.match(r'^(.+?) × (.+ 십 년)$', t) if t else None
        if mb and GROUP_SP.get(mb.group(1)) and DAE.get(mb.group(2)):
            prev_branch = {'kind': 'branch', 'group': GROUP_SP[mb.group(1)],
                           'key': DAE[mb.group(2)], 't': t, 'h': h}
            out.append(prev_branch); group = None; axis = None; continue
        # 「× 대운이름」 꼴이면 깊이와 상관없이 갈래입니다 (2026 은 ## · 2027 은 ####)
        mm = re.match(r'^× (.+ 십 년)$', t or '')
        if mm and DAE.get(mm.group(1)) and group:
            prev_branch = {'kind': 'branch', 'group': group,
                           'key': DAE[mm.group(1)], 't': t, 'h': h}
            out.append(prev_branch); continue

        # 갈래 바로 뒤의 소제목/본문은 그 갈래에 이어 붙입니다
        if prev_branch is not None and lv >= 3 and not GROUP_SP.get(t or ''):
            # ★ 속성은 홑따옴표 — 쌍따옴표를 쓰면 JSON 이 \" 로 이스케이프해
            #   역빗금이 생기고, 편집기 저장에 벗겨지면 책이 안 그려집니다
            ttl = ("<p class='keepline'>%s</p>" % t) if t else ''
            prev_branch['h'] += ttl + h
            continue
        prev_branch = None

        if lv == 5 or lv == 4 and t and t[0] in '①②③④⑤⑥⑦⑧⑨⑩':
            out.append({'kind': 'title', 't': t, 'h': h}); group = None; axis = None; continue
        if lv in (1, 2):
            g = GROUP_SP.get(re.sub(r'^\d무리 · ', '', t)) if t else None
            if g:
                group = g; axis = None
                out.append({'kind': 'group', 'key': g, 't': t, 'h': h}); continue
            a = axis_of(title)
            group = None; axis = a
            out.append({'kind': 'always', 't': t, 'h': h}); continue
        if lv == 4 and axis:
            out.append({'kind': 'pick', 'axis': axis, 'key': key_of(axis, title), 't': t, 'h': h}); continue
        out.append({'kind': 'always', 't': t, 'h': h})
    return [b for b in out if b['h'] or b['kind'] in ('group', 'branch', 'title')]

if __name__ == '__main__':
    year = sys.argv[1] if len(sys.argv) > 1 else '2027'
    files = sorted(f for f in os.listdir(SRC)
                   if f.startswith(year + '년운세-')
                   and not f.startswith(year + '년운세-00')
                   and '보관' not in f)
    doc = {}
    for f in files:
        no = f.split('-')[1]
        bs = parse(f)
        doc[no] = bs
        kinds = {}
        for b in bs: kinds[b['kind']] = kinds.get(b['kind'], 0) + 1
        miss = [b['t'] for b in bs if b['kind'] in ('branch', 'pick') and not b.get('key')]
        print('%-4s %-34s %s%s' % (no, f[9:24], kinds, ('  ★ 열쇠 없음: ' + str(miss[:3])) if miss else ''))
    io.open(os.path.join(HERE, 'NY%s.json' % year), 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False))
    print('\nNY%s.json 썼습니다 (%d 장)' % (year, len(doc)))
