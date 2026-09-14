# -*- coding: utf-8 -*-
"""건강운 원고(.md) -> WPCode 조각용 JS 표. 두 층(### / ######)을 살립니다."""
import re, json, os, io
SRC='/home/user/kitten/wordpress/drafts'
HERE = os.path.dirname(os.path.abspath(__file__))

def inline(p):
    p = p.replace('\n','<br>')
    p = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p, flags=re.S)
    p = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', p)
    return p

def md2html(block):
    out=[]
    for para in re.split(r'\n\s*\n', block.strip()):
        para=para.strip()
        if not para or para=='---': continue
        if para.lstrip().startswith(u'★'): continue      # ★ 내 메모
        if para.lstrip().startswith(u'☞'): continue      # ☞ 내 메모
        h=inline(para)
        cls=''
        if h.startswith('<em>') and h.endswith('</em>'): cls=" class='mini'"
        elif h.startswith('<strong>') and h.endswith('</strong>'): cls=" class='keepline'"
        out.append('<p%s>%s</p>'%(cls,h))
    return ''.join(out)

def tree(fn, chap_title_re):
    """[{h, b, kids:[{h,b}]}] — 장 제목(### ①…) 앞은 전부 버립니다."""
    s=io.open(os.path.join(SRC,fn),encoding='utf-8').read()
    lines=s.split('\n')
    start=None
    for i,l in enumerate(lines):
        if re.match(chap_title_re, l): start=i+1; break
    if start is None: raise SystemExit('장 제목 못 찾음: '+fn)
    A=[]; cur=None; kid=None; buf=[]
    def flush():
        if kid is not None: kid['b']+=md2html('\n'.join(buf))
        elif cur is not None: cur['b']+=md2html('\n'.join(buf))
        else: A.append({'h':None,'b':md2html('\n'.join(buf)),'kids':[]})
    for l in lines[start:]:
        m6=re.match(r'^######\s+(.*)$', l)
        m3=re.match(r'^###\s+(.*)$', l)
        if m6:
            flush(); buf=[]
            if cur is None: cur={'h':None,'b':'','kids':[]}; A.append(cur)
            kid={'h':m6.group(1).strip(),'b':''}; cur['kids'].append(kid)
        elif m3:
            flush(); buf=[]; kid=None
            cur={'h':m3.group(1).strip(),'b':'','kids':[]}; A.append(cur)
        else:
            buf.append(l)
    flush()
    # 빈 것 버리기
    out=[]
    for a in A:
        a['kids']=[k for k in a['kids'] if k['b'].strip()]
        if a['b'].strip() or a['kids'] or a['h']: out.append(a)
    return out

CH=[
 ('01','① 나는 어떤 몸을 타고났는가','건강운-01-타고난몸.md',  r'^### ① '),
 ('02','② 나는 어떻게 쉬어야 회복되는가','건강운-02-쉬기.md',  r'^### ② '),
 ('03','③ 나는 왜 살이 찌고, 빠지는가','건강운-03-살.md',      r'^### ③ '),
 ('04','④ 나는 어떻게 먹어야 몸이 편한가','건강운-04-먹기.md', r'^### ④ '),
 ('05','⑤ 나는 어떤 다이어트가 맞는가','건강운-05-다이어트.md', r'^### ⑤ '),
 ('06','⑥ 나는 어떤 운동을 해야 하는가','건강운-06-운동.md',   r'^### ⑥ '),
 ('07','⑦ 내 몸을 힘들게 하는 습관은 무엇인가','건강운-07-습관.md', r'^### ⑦ '),
 ('08','⑧ 올해 내 몸은 무엇을 바꾸라고 하는가','건강운-08-올해.md', r'^### ⑧ '),
 ('09','⑨ 건강운에서 딱 세 가지만 기억하세요','건강운-09-세가지.md', r'^### ⑨ '),
 ('10','⑩ 마지막으로 당신에게 건네는 말','건강운-10-건네는말.md', r'^### ⑩ '),
]

# ── 갈림 규칙 ────────────────────────────────────────────────
# {'key':열쇠, 'lv':'A'|'B', 'in':부모 제목(lv=B 일 때), 'map':{갈래:제목}}
R = {
 '01':[
   {'key':'ten7','lv':'A','multi':True,'map':{
     '비견':'비견 · 혼자 버티는 몸','겁재':'겁재 · 나눠 쓰는 몸',
     '식신':'식신 · 먹고 풀어내는 몸','상관':'상관 · 밖으로 풀어내는 몸',
     '재성':'재성 · 생활을 돌보느라 소모되는 몸','관성':'관성 · 참고 견디는 몸',
     '인성':'인성 · 생각이 먼저 지치는 몸'}},
 ],
 '02':[
   {'key':'sleep','lv':'B','in':'내 잠은 어떤 결인가','map':{
     'hwa':'밤이 되면 오히려 깨어나는 쪽 — 화의 힘이 강하게 나타날 때',
     'su':'자면 채워지지만 오래 걸리는 쪽 — 수의 힘이 강하게 나타날 때',
     'suthin':'자도 개운하지 않은 쪽 — 수의 힘이 얇게 나타날 때'}},
   {'key':'clock','lv':'B','in':'늦게 자는 쪽인가, 일찍 자는 쪽인가','map':{
     'night':'밤에 힘이 나는 쪽이라면',
     'morning':'아침이 편한 쪽이라면 — 금·수의 힘이 강하게 나타날 때'}},
   {'key':'where','lv':'B','in':'잠이 부족할 때 나는 어디부터 나타나는가','map':{
     'sok':'속부터 불편해진다고 하셨습니다',
     'stiff':'목·어깨·허리가 뻐근해진다고 하셨습니다',
     'none':'아직 답해주신 것이 없다면'}},
   {'key':'grp','lv':'B','in':'스트레스는 어떻게 쉬어야 풀리는가','map':{
     '식상':'말로 꺼내야 풀리는 쪽 — 식상이 넉넉하게 나타날 때',
     '재성':'몸을 움직이거나 일로 잊는 쪽 — 재성이 넉넉하게 나타날 때',
     '관성':'참는 것으로 넘기는 쪽 — 관성이 넉넉하게 나타날 때',
     '인성':'혼자 있어야 풀리는 쪽 — 인성이 넉넉하게 나타날 때',
     '비겁':'사람 곁에서 풀리는 쪽 — 비겁이 넉넉하게 나타날 때'}},
   {'key':'rest','lv':'B','in':'혼자 쉬는 쪽인가, 움직이며 푸는 쪽인가','map':{
     'still':'푹 자고 아무것도 안 한다고 하셨습니다',
     'move':'몸을 움직여야 풀린다고 하셨습니다',
     'none':'아직 답해주신 것이 없다면'}},
   {'key':'gang3','lv':'B','in':'회복에 필요한 생활 리듬','map':{
     'strong':'한 번에 몰아서 쓰는 쪽이라면',
     'mid':'천천히 유지하는 쪽이라면',
     'weak':'몸의 힘이 먼저 떨어지는 쪽이라면'}},
 ],
 '03':[
   {'key':'grp','lv':'B','in':'내가 먹는 이유부터 다릅니다','map':{
     '식상':'입이 심심해서 먹는 쪽 — 식상이 넉넉하게 나타날 때',
     '재성':'바빠서 몰아서 먹는 쪽 — 재성이 넉넉하게 나타날 때',
     '관성':'참다가 밤에 먹는 쪽 — 관성이 넉넉하게 나타날 때',
     '인성':'생각이 많을 때 먹는 쪽 — 인성이 넉넉하게 나타날 때',
     '비겁':'남을 챙기고 나중에 먹는 쪽 — 비겁이 넉넉하게 나타날 때'}},
   {'key':'when','lv':'B','in':'과식은 하루 중 어디에서 오는가','map':{
     'pm':'오후에 무너지는 쪽','eve':'저녁에 무너지는 쪽',
     'night':'밤늦게 무너지는 쪽','skip':'끼니를 건너뛴 뒤 무너지는 쪽'}},
   {'key':'gain','lv':'B','in':'살이 붙는 방식도 다릅니다','map':{
     'keep':'조금씩 모아두는 쪽 — 토·수의 힘이 강하게 나타날 때',
     'burn':'쓰면서 빠지는 쪽 — 목·화의 힘이 강하게 나타날 때',
     'rule':'한 번 정하면 끝까지 하는 쪽 — 금의 힘이 강하게 나타날 때'}},
   {'key':'gang3','lv':'B','in':'빠지고 난 뒤, 어디에서 다시 돌아오는가','map':{
     'strong':'목표에 도착하면 끝내는 쪽','mid':'천천히 빠지고 오래 두는 쪽',
     'weak':'굶으면 기운이 먼저 떨어지는 쪽'}},
 ],
 '04':[
   {'key':'meal','lv':'B','in':'먼저 볼 것은 식사 횟수가 아닙니다','map':{
     'often':'자주 먹어서 문제가 되는 쪽 — 토의 힘이 강하게 나타날 때',
     'long':'너무 오래 비워서 문제가 되는 쪽 — 목·화의 힘이 강하게 나타날 때',
     'rule':'규칙을 만들면 편해지는 쪽 — 금의 힘이 강하게 나타날 때'}},
   {'key':'morn','lv':'B','in':'아침을 먹어야 하는 사람, 억지로 먹지 않아도 되는 사람','map':{
     'need':'아침을 건너뛰면 저녁이 커지는 쪽',
     'heavy':'아침을 먹으면 오히려 무거운 쪽'}},
   {'key':'when2','lv':'B','in':'과식은 음식보다 먼저 시간이 보입니다','map':{
     'night':'늦은 밤에 커지는 쪽','pm':'오후에 무너지는 쪽',
     'skip':'끼니를 건너뛴 뒤 무너지는 쪽'}},
   {'key':'season','lv':'B','in':'추위를 많이 타는지, 더위를 많이 타는지','map':{
     'cold':'추위를 많이 탄다고 하셨다면','hot':'더위를 많이 탄다고 하셨다면',
     'none':'아직 답해주신 것이 없다면'}},
 ],
 '05':[
   {'key':'gang3','lv':'A','map':{
     'strong':'한 번에 몰아서 쓰는 쪽이라면','mid':'천천히 유지하는 쪽이라면',
     'weak':'몸의 힘이 먼저 떨어지는 쪽이라면'}},
   {'key':'gang3','lv':'A','map':{
     'strong':'짧게 집중하는 분께 권하는 방법','mid':'꾸준히 관리하는 분께 권하는 방법',
     'weak':'몸의 힘이 쉽게 떨어지는 분께 권하는 방법'}},
   {'key':'rhythm','lv':'A','map':{
     'reg':'사전질문에서 「규칙적으로 사는 편」이라고 답하셨다면',
     'burst':'사전질문에서 「몰아서 하고 몰아서 쉬는 편」이라고 답하셨다면',
     'none':'아직 사전질문에 답하지 않으셨다면'}},
 ],
 '06':[], '07':[],
 '08':[
   {'key':'year','lv':'B','in':'올해의 기운은 내 몸의 어디에 닿는가','map':{
     'same':'이미 넉넉한 힘이 또 들어오는 해라면',
     'new':'없던 힘이 들어오는 해라면',
     'press':'버티던 힘이 눌리는 해라면',
     'help':'나를 받쳐주는 힘이 들어오는 해라면',
     'far':'크게 닿지 않는 해라면'}},
 ],
 '09':[
   {'key':'three','lv':'B','in':None,'pick3':[
     ('weak','굶는 방식은 고르지 마세요'),
     ('sleep','잠을 먼저 되찾으세요'),
     ('bear','하루에 하나만 덜 참으세요'),
     ('strong','한 번에 바꾸려 하지 마세요'),
     ('burst','남의 방법보다 내 리듬으로'),
     ('sign','몸이 보내는 신호를 흘리지 마세요')]},
 ],
 '10':[],
}

book={}
for no,title,fn,tre in CH:
    A=tree(fn,tre)
    groups=[]
    for g in R.get(no,[]):
        gg={'key':g['key'],'lv':g['lv']}
        if 'in' in g: gg['in']=g['in']
        if g.get('multi'): gg['multi']=True
        if 'pick3' in g:
            gg['pick3']=[list(x) for x in g['pick3']]
        else:
            gg['map']=g['map']
        groups.append(gg)
    # 제목 확인 — 규칙에 적은 제목이 원고에 실제로 있나
    have=set()
    for a in A:
        if a['h']: have.add(a['h'])
        for k in a['kids']: have.add(k['h'])
    for g in R.get(no,[]):
        want = list(g['map'].values()) if 'map' in g else [t for _,t in g['pick3']]
        for t in want:
            if t not in have:
                print('★', no, '규칙에 적은 제목이 원고에 없습니다 :', t)
        if g.get('in') and g['in'] not in have:
            print('★', no, '부모 제목이 원고에 없습니다 :', g['in'])
    bare=re.sub(u'^[①-⑩]\\s*','',title)
    book[no]={'t':title,'t2':bare,'A':A,'g':groups}

js=json.dumps({'book':book},ensure_ascii=False,separators=(',',':'))
io.open(os.path.join(HERE, 'H.json'),'w',encoding='utf-8').write(js)
print()
for no,_,_,_ in CH:
    e=book[no]
    nk=sum(len(a['kids']) for a in e['A'])
    print(no,'| 큰 대목',len([a for a in e['A'] if a['h']]),'| 작은 대목',nk,'| 갈림 무리',len(e['g']))
print('표',len(js),'글자 · 앰퍼샌드',js.count('&'),'· 역빗금',js.count('\\'))
