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
        # ★ 2026-09-14 · 소희 님 : 「문단은 짧게 가지 말고 한 줄씩
        #   갔으면 좋겠어」 — 보기로 주신 것 :
        #     돈이 남아도 좋고,↵경력이 남아도 좋고,↵…    ← 쪼개짐
        #     돈이 남아도 좋고, 경력이 남아도 좋고, …      ← 이것
        #   원고에 줄을 나눠 적으셔도 책에서는 한 줄로 흐르게 합니다.
        #   (인용구는 위에서 따로 다루므로 줄바꿈이 그대로 남습니다)
        para = para.replace('\n', ' ')
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
        # ★ 2026-09-14 · 소희 님 : 「신년운세에 나온 1층 2층 3층…
        #   단어를 바꿔야해」 · 「2개 다 삭제」
        #   「1층 · 」 「2층 · 」 「3층 · 」 은 제가 원고를 짜면서 붙인
        #   건축 낱말입니다. 손님에게는 뜻이 안 통합니다 — 딱지만 뗍니다.
        #   ★ axis_of() · key_of() 는 원래 제목(title)을 그대로 보므로
        #     2027 의 갈래 고르기는 그대로 돕니다. 보이는 글만 바뀝니다.
        if t:
            t = re.sub(r'^\d\s*층\s*·\s*', '', t)
        # ★ 2026-09-14 · 소희 님 : 「알맞은 자리 · 이미 균형이 잡혀 있는 경우
        #   — 이건 우리가 분리 하려고 만든거라 삭제」
        #   맞습니다. 셋 가운데 하나만 나가므로 손님은 「알맞은 자리」라는
        #   이름을 볼 까닭이 없습니다. 고르는 데는 그대로 쓰고
        #   (key_of 는 원래 제목을 봅니다) 보이는 제목만 지웁니다.
        if t and re.match(r'^(넉넉한 자리|비어 있던 자리|알맞은 자리)\s*·', t):
            t = ''

        # ── 2026 꼴 · 제목 하나에 무리와 대운이 같이 있는 갈래 ──
        mb = re.match(r'^(.+?) × (.+ 십 년)$', t) if t else None
        if mb and GROUP_SP.get(mb.group(1)) and DAE.get(mb.group(2)):
            prev_branch = {'kind': 'branch', 'group': GROUP_SP[mb.group(1)],
                           'key': DAE[mb.group(2)], 't': t, 'h': h}
            out.append(prev_branch); group = None; axis = None; continue
        # 「× 대운이름」 꼴이면 깊이와 상관없이 갈래입니다 (2026 은 ## · 2027 은 ####)
        # ★ 2026-09-14 · ⑤장(때)이 25갈래를 통째로 모두에게 내보내고
        #   있었습니다 (10,613자 중 8,250자). 까닭이 둘이었습니다 —
        #     ① 제목이 「× 나를 세우는 십 년 · 겹침」이라 뒤에 관계말이
        #        붙어 있는데 정규식이 줄 끝($)을 요구했습니다
        #     ② 무리 제목이 「내가 정하고 내가 서는 해의 시간」이라
        #        GROUP_SP 의 열쇠와 정확히 같지 않아 group 이 안 열렸습니다
        #   둘 다 풀어 줍니다. 꼬리말은 제목에 그대로 남깁니다.
        mm = re.match(r'^× (.+? 십 년)(?:\s*·\s*.+)?$', t or '')
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
            # ★ 「작은 제목 · 」 은 소희 님이 원고를 쓰실 때 다신 딱지입니다.
            #   2026-09-14 화면에 「작은 제목 · 25개의 조합을…」로 그대로
            #   찍혀 있었습니다 (열아홉 장 전부). 뒤의 글이 진짜 소제목이라
            #   딱지만 떼고 글은 그대로 둡니다.
            h = re.sub(r'(<strong>)\s*작은\s*제목\s*·\s*', r'\1', h)
            h = re.sub(r'(<p[^>]*>)\s*작은\s*제목\s*·\s*', r'\1', h)
            h = h.replace('작은 제목 · ', '')
            out.append({'kind': 'title', 't': t, 'h': h}); group = None; axis = None; continue
        # ── 대괄호 꼬리표 — 원고가 스스로 갈래를 알려 줍니다 ────────
        #   2026-09-14 · 소희 님이 ②장을 새로 쓰시면서 제목 끝에
        #   [비겁] [넉넉한 자리] 같은 표를 달아 두셨습니다.
        #   원고 머리말에 「[비겁] 같은 꼬리표는 제가 갈래를 고르려고
        #   다는 표시입니다. 책에는 안 나갑니다」라고 적혀 있습니다.
        #   ★ 이것이 제일 든든한 길입니다 — 제목 글을 바꾸셔도 안 깨집니다.
        #   ★ 꼬리표는 제목에서 뗍니다. 책에 나가면 안 됩니다.
        # ── 「[이음]」 — 제목 없이 한 문장만 내보내는 자리 ───────────
        #   2026-09-14 · 소희 님이 ④장을 이렇게 그려 주셨습니다 —
        #     지금 지나는 「거두고 쌓는 십 년」까지 겹치면
        #     사람마다 조심해야 할 자리가 달라집니다.
        #     ×  ← 「× 거두고 쌓는 십 년」 제목은 지우자
        #   갈래로 넘어가는 다리 한 줄입니다. 제목을 달면 같은 말이
        #   두 번 나오니, 제목 없이 문장만 냅니다.
        #   ★ 머리(#)가 있어야 앞 덩어리에 글이 붙지 않습니다. 그래서
        #     머리는 두되 보이는 제목만 비웁니다.
        if re.match(r'^\[이음\]$', t or ''):
            group = None; axis = None; prev_branch = None
            out.append({'kind': 'always', 't': '', 'h': h}); continue

        _TAGS = list(FIVE) + list(POWER.keys()) + list(DAE.keys())
        mt = re.match(r'^(.*?)\s*\[(' + '|'.join(re.escape(x) for x in _TAGS)
                      + r')\]\s*$', t or '')
        if mt:
            bare_t = mt.group(1).strip()
            tag = mt.group(2)
            if tag in DAE:
                # 대운 갈래 — 지금 지나는 십 년 것 하나만 나갑니다
                out.append({'kind': 'dae', 'key': DAE[tag],
                            't': bare_t, 'h': h}); continue
            if tag in POWER:
                # 1층 — 그 해 오행이 사주에 몇 개인가로 고릅니다.
                # emit 의 powerOf() 가 much / few / even 을 냅니다.
                out.append({'kind': 'pick', 'axis': 'power', 'key': POWER[tag],
                            't': bare_t, 'h': h}); continue
            # 무리 머리(#·##)가 꼬리표만 달고 있으면 갈래 열쇠도 같이 엽니다.
            # 2026-09-14 · ③장에서 「# 내가 정하고 내가 서는 해」 머리가
            # 손님 화면에 그대로 찍혔습니다 — 소희 님 판에는 없는 줄입니다.
            # 「# [비겁]」 으로 적으면 제목은 안 나가고 갈래만 열립니다.
            if lv in (1, 2):
                group = tag; axis = None
            out.append({'kind': 'group', 'key': tag, 't': bare_t, 'h': h}); continue

        # ── 갈래 이름으로 시작하는 제목도 그 갈래 것입니다 ──────────
        #   2026-09-14 · 소희 님 : 「시작부터 겹쳐서…」
        #   ①장과 ②장이 비겁·식상·재성·관성·인성 다섯을 모두에게
        #   내보내고 있었습니다(kind='always'). 손님은 자기와 상관없는
        #   남의 이야기를 세 번씩 읽었습니다 — 다섯 가운데 넷이 남의 것.
        #   「반복된다」는 리뷰의 진짜 자리가 여기입니다.
        #     비겁 · 내가 정하고 내가 서는 해   → 세운 갈래 (group)
        #     비겁 · 나를 세우는 십 년          → 대운 갈래 (dae)
        mg = re.match(r'^(비겁|식상|재성|관성|인성)\s*·\s*(.+)$', t or '')
        if mg:
            gname = mg.group(1)
            rest = mg.group(2)
            if re.search(r'십\s*년\s*$', rest):
                out.append({'kind': 'dae', 'key': gname, 't': t, 'h': h}); continue
            out.append({'kind': 'group', 'key': gname, 't': t, 'h': h}); continue

        if lv in (1, 2):
            bare = re.sub(r'^\d무리 · ', '', t) if t else ''
            g = GROUP_SP.get(bare)
            if not g and bare:
                # 「내가 정하고 내가 서는 해의 시간」처럼 뒷말이 붙은 꼴
                for _nm in GROUP_SP:
                    if bare.startswith(_nm):
                        g = GROUP_SP[_nm]; break
            if g:
                group = g; axis = None
                out.append({'kind': 'group', 'key': g, 't': t, 'h': h}); continue
            a = axis_of(title)
            group = None; axis = a
            out.append({'kind': 'always', 't': t, 'h': h}); continue
        if lv == 4 and axis:
            out.append({'kind': 'pick', 'axis': axis, 'key': key_of(axis, title), 't': t, 'h': h}); continue
        out.append({'kind': 'always', 't': t, 'h': h})
    out = [b for b in out if b['h'] or b['kind'] in ('group', 'branch', 'dae', 'title')]
    # ★ 2026-09-14 · 그 장이 이미 「{대운이름}」을 말해 줬다면 갈래마다
    #   「× 거두고 쌓는 십 년」 머리를 또 찍지 않습니다. 소희 님 판에는
    #   그 줄이 없습니다 — 같은 말을 두 번 읽게 되니까요.
    if any('{대운이름}' in str(b.get('h') or '') for b in out):
        for b in out:
            if b['kind'] == 'branch' and re.match(r'^\s*×\s', str(b.get('t') or '')):
                b['t'] = ''
    # ★ 2026-09-14 · 소희 님 : 「× 거두고 쌓는 십 년 에서 × 삭제하자」
    #   곱셈표는 제가 원고에서 갈래를 가르려고 쓰는 표시입니다.
    #   손님에게는 뜻이 안 통합니다 — 제목에서만 뗍니다.
    #   (원고의 「## × …」 는 그대로 둡니다. 그것으로 갈래를 찾습니다)
    for b in out:
        if b['kind'] == 'branch':
            b['t'] = re.sub(r'^\s*×\s*', '', str(b.get('t') or ''))
    return out

if __name__ == '__main__':
    year = sys.argv[1] if len(sys.argv) > 1 else '2027'
    files = sorted(f for f in os.listdir(SRC)
                   if f.startswith(year + '년운세-')
                   and not f.startswith(year + '년운세-00')
                   and '보관' not in f)
    doc = {}
    # ── 대운이름 표를 여기서 같이 적어 둡니다 ─────────────────────
    #   2026-09-14 · 소희 님이 ②장에서 3층(대운 다섯 설명)을 빼셨습니다
    #   — ①장에서 이미 한 이야기라 되풀이였습니다. 그런데 emit 이
    #   {대운이름} 을 ②장 소제목에서만 읽고 있어서 2026 이 통째로
    #   안 만들어졌습니다 (★ 이름표를 못 뽑았습니다).
    #   원고 구조가 바뀌어도 안 깨지도록, 표를 아는 쪽(여기)이 적습니다.
    #   「나를 세우는 십 년」 → 「나를 세우는 흐름」 (본문이 「의 십 년」 앞에
    #   놓고 쓰므로 「십 년」을 떼고 「흐름」을 붙입니다)
    # 올해이름 — 해마다 다섯. ①장 제목에서 못 뽑으면 이 표로 물러납니다.
    #   2026-09-14 · 소희 님이 ①장을 편지 꼴로 다시 쓰시면서 제목에
    #   「…해」가 안 들어가게 됐습니다. 원고가 어떻게 바뀌어도
    #   이름표가 비지 않도록 표를 여기에 둡니다.
    YEAR_NAMES = {
        '2026': {'비겁': '내가 정하고 내가 서는 해',
                 '식상': '내놓고 펼치는 해',
                 '재성': '거두고 결과를 만드는 해',
                 '관성': '자리를 만들고 책임지는 해',
                 '인성': '채우고 다음을 준비하는 해'},
        '2027': {'비겁': '내가 세운 것을 밖으로 내놓는 해',
                 '식상': '내놓은 것이 결과가 되는 해',
                 '재성': '거둔 것이 자리가 되는 해',
                 '관성': '맡은 자리가 배움이 되는 해',
                 '인성': '채운 것이 나를 세우는 해'},
    }
    #   {대운이름}  「거두고 쌓는 흐름」   — 「…의 십 년」 앞에 놓고 쓸 때
    #   {대운십년}  「거두고 쌓는 십 년」   — 그 자체로 쓸 때
    #   2026-09-14 · 소희 님이 다리 문장을 「지금 지나는 「거두고 쌓는
    #   십 년」까지 겹치면」으로 쓰셔서 둘을 갈랐습니다.
    doc['_names'] = {'year': dict(YEAR_NAMES.get(year) or {}),
                     'ten': dict((sp, name) for name, sp in DAE.items()),
                     'luck': dict(
        (sp, re.sub(r'\s*십\s*년\s*$', '', name).strip() + ' 흐름')
        for name, sp in DAE.items())}
    for f in files:
        no = f.split('-')[1]
        bs = parse(f)
        doc[no] = bs
        # ── 올해이름 표 — ①장의 갈래 제목에서 「 」 안을 떠옵니다 ──────
        #   2026-09-14 · 소희 님이 ①장을 다시 쓰시면서 제목이
        #   「{이름}님의 2026년은 「채우고 다음을 준비하는 해」입니다」로
        #   바뀌었습니다. emit 이 「비겁 · …」 꼴만 읽고 있어서 이름표를
        #   못 뽑게 됐습니다. 원고가 또 바뀌어도 안 깨지도록,
        #   갈래를 아는 쪽(여기)이 제목 속 「 」 를 떠서 적어 둡니다.
        if no == '01':
            yn = {}
            for b in bs:
                if b['kind'] != 'group':
                    continue
                m2 = re.search(u'\u300c(.+?)\u300d', str(b.get('t') or ''))
                if m2 and b['key'] not in yn:
                    yn[b['key']] = m2.group(1)
            if len(yn) == 5:
                doc['_names']['year'] = yn
        kinds = {}
        for b in bs: kinds[b['kind']] = kinds.get(b['kind'], 0) + 1
        miss = [b['t'] for b in bs if b['kind'] in ('branch', 'pick') and not b.get('key')]
        print('%-4s %-34s %s%s' % (no, f[9:24], kinds, ('  ★ 열쇠 없음: ' + str(miss[:3])) if miss else ''))
    io.open(os.path.join(HERE, 'NY%s.json' % year), 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False))
    print('\nNY%s.json 썼습니다 (%d 장)' % (year, len(files)))
