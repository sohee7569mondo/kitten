# -*- coding: utf-8 -*-
"""가족운 원고(.md) -> WPCode 조각(JS 표) 만들기"""
import re, json, os, io

SRC = '/home/user/kitten/wordpress/drafts'

def md2html(block):
    """문단 덩어리를 <p>..</p> 로. **굵게** -> <strong>, 「」 그대로."""
    out=[]
    for para in re.split(r'\n\s*\n', block.strip()):
        para = para.strip()
        if not para: continue
        if para == '---': continue
        # ★ 로 시작하는 문단은 제 메모입니다. 책에 내보내지 않습니다.
        if para.lstrip().startswith(u'\u2605'): continue
        # 한 문단 안의 줄바꿈은 살린다 (소희 님 글이 행갈이로 호흡을 만듦)
        para = para.replace('\n', '<br>')
        # **굵게**
        para = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', para, flags=re.S)
        # *기울임* (의학 문구 등)
        para = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', para)
        cls = ''
        if para.startswith('<em>') and para.endswith('</em>'):
            cls = " class='mini'"
        elif para.startswith('<strong>') and para.endswith('</strong>'):
            cls = " class='keepline'"
        out.append('<p%s>%s</p>' % (cls, para))
    return ''.join(out)

def load(fn):
    s = io.open(os.path.join(SRC, fn), encoding='utf-8').read()
    # 머리말(파일 첫 --- 까지)을 떼어낸다
    parts = s.split('\n---\n', 1)
    body = parts[1] if len(parts)>1 else s
    return body

def sections(body):
    """[(제목 or None, 본문html)] — 제목 없는 앞머리는 title=None"""
    rows=[]
    cur_t=None; buf=[]
    for line in body.split('\n'):
        m = re.match(r'^#{2,6}\s+(.*)$', line)
        if m:
            if buf: rows.append((cur_t, md2html('\n'.join(buf))))
            cur_t = m.group(1).strip(); buf=[]
        else:
            buf.append(line)
    if buf: rows.append((cur_t, md2html('\n'.join(buf))))
    return [(t,h) for (t,h) in rows if h.strip()]

# ── 장마다 어느 대목이 「갈림」이고 어느 대목이 「늘 붙음」인가 ──────
# pick : 사주로 하나를 고르는 무리 (열쇠 -> 제목)
# soft : 조건이 맞을 때만 (지금은 늘 붙임 — 조건 셈은 다음 판에)
# 나머지 제목은 전부 늘 붙습니다.
RULES = {
 '01': {'key':'group', 'pick':{
        '비겁':'대등하게 서는 자리 — 비겁이 많을 때',
        '식상':'내어주는 자리 — 식상이 많을 때',
        '재성':'떠안는 자리 — 재성이 많을 때',
        '관성':'지키는 자리 — 관성이 많을 때',
        '인성':'품는 자리 — 인성이 많을 때'}},
 '02': {'key':'in3', 'pick':{
        'much':'많이 받은 자리 — 인성이 넉넉할 때',
        'mid' :'자연스럽게 받은 자리 — 인성이 안정되어 있을 때',
        'thin':'일찍 혼자 선 자리 — 인성이 약하게 나타날 때'}},
 '03': {'key':'bi3', 'pick':{
        'much':'나란히 서는 사이 — 비겁이 넉넉할 때',
        'mid' :'챙기는 쪽에 선 사이 — 식상·재성이 강하게 나타날 때',
        'thin':'각자의 삶으로 가는 사이 — 비겁이 약하게 나타날 때'}},
 '04': {'key':'sik2', 'pick':{
        'much':'내어주며 키우는 결 — 식상이 넉넉할 때',
        'thin':'지켜보는 결 — 식상이 약하게 나타날 때'}},
 '05': {'key':'give3', 'pick':{
        'give':'주는 쪽이 큰 자리',
        'take':'받는 쪽이 큰 자리',
        'even':'주고받는 것이 엇비슷한 자리'}},
 '06': {'key':'stuck', 'pick':{
        'parent':'부모 자리에서 걸릴 때',
        'sib'   :'형제 자리에서 걸릴 때',
        'child' :'자녀 자리에서 걸릴 때',
        'none'  :'크게 걸리는 자리가 없을 때'}},
 '07': {'key':'move', 'pick':{
        'parent':'부모 자리가 움직이는 때',
        'child' :'자녀 자리가 움직이는 때',
        'sib'   :'형제 사이가 움직이는 때',
        'none'  :'크게 움직이지 않는 때'}},
 '08': {}, '09': {}, '10': {},
}

CH = [
 ('01','① 나는 가족 안에서 어떤 사람인가','가족운-01-가족안의나.md'),
 ('02','② 부모와 나는 어떤 인연으로 만나는가','가족운-02-부모.md'),
 ('03','③ 형제자매와 나는 어떤 관계를 맺는가','가족운-03-형제자매.md'),
 ('04','④ 자녀와 나는 어떤 인연으로 만나는가','가족운-04-자녀.md'),
 ('05','⑤ 나는 가족에게 무엇을 주고, 무엇을 기대하는가','가족운-05-주고받기.md'),
 ('06','⑥ 가족 안에서 내가 반복해서 걸리는 곳은 어디인가','가족운-06-반복해서걸리는곳.md'),
 ('07','⑦ 가족에게 큰 변화가 생기는 때는 언제인가','가족운-07-변화가생기는때.md'),
 ('08','⑧ 그래서 가족과 어떻게 지내야 서로 편안한가','가족운-08-거리와몫.md'),
 ('09','⑨ 가족운에서 딱 세 가지만 기억하기','가족운-09-세가지.md'),
 ('10','⑩ 마지막으로 당신에게 건네는 말','가족운-10-건네는말.md'),
]

book = {}
for no, title, fn in CH:
    body = load(fn)
    secs = sections(body)
    rule = RULES.get(no, {})
    picks = rule.get('pick', {})
    picktitles = set(picks.values())
    lead = ''
    always = []   # [ {h, b} ] 차례대로
    branch = {}   # key -> {h, b}
    for t, h in secs:
        if t is None:
            lead += h
        elif t in picktitles:
            for k, v in picks.items():
                if v == t: branch[k] = {'h':t, 'b':h}
        else:
            always.append({'h':t, 'b':h})
    bare = re.sub(u'^[\u2460-\u2469]\\s*', '', title)
    ent = {'t':title, 't2':bare, 'lead':lead, 'always':always}
    if branch:
        ent['key'] = rule['key']; ent['branch'] = branch
    book[no] = ent

# 여는 글
ob = load('가족운-00-여는글.md')
osecs = sections(ob)
voice=''; guide=''
for t,h in osecs:
    if t and '말상자' in t: voice=h
    elif t and '장 안내' in t: guide=h
open_ = {'voice':voice, 'guide':guide}

# 십성 열 개
ls = load('가족운-십성열개.md')
lens = {}
for t,h in sections(ls):
    if not t: continue
    m = re.match(r'^(비견|겁재|식신|상관|편재|정재|정관|편관|정인|편인)\s*·\s*(.+)$', t)
    if m: lens[m.group(1)] = {'h':t, 'b':h}

out = {'open':open_, 'book':book, 'lens':lens}
js = json.dumps(out, ensure_ascii=False, separators=(',',':'))
io.open('/tmp/claude-0/-home-user-kitten/c2a43b1d-0c4f-566e-ae2a-79f351d35055/scratchpad/fam/F.json','w',encoding='utf-8').write(js)

print('여는글 말상자', len(voice), '· 장안내', len(guide))
print('십성', len(lens), '개:', ' '.join(sorted(lens)))
for no,_,_ in CH:
    e=book[no]
    print(no, '| 앞머리', len(e['lead']), '| 갈림', len(e.get('branch',{})), '| 늘', len(e['always']),
          '|', ' / '.join(a['h'][:16] for a in e['always'])[:70])
print('표 전체', len(js), '글자')
amp = js.count('&')
print('앰퍼샌드', amp)
