# -*- coding: utf-8 -*-
"""스타 사주 쪽(406) **원본**을 고칩니다 — 조각으로 덮지 않습니다.

소희 님 2026-09-16 :
  「위 너비가 안바뀌는것도 그렇고 예전에 안보이게 햇던 연애인 리스트도
   떴다가 가려지는 형식이야 그럼 전체 코딩이 무거워지지 않아?」

맞는 말씀이었습니다. 브라우저는 CSS 를 **그리기 전에**, 자바스크립트를
**그린 뒤에** 읽습니다. 조각으로 덮으면 반드시 한 번은 옛 모습이 보입니다.

이제 워드프레스로 쪽 내용을 직접 읽을 수 있게 되어(pages.get), 밖에서
덮을 까닭이 없어졌습니다. 쪽 안의 표와 그리는 자리를 곧바로 고칩니다.

이 도구가 끝나면 조각 넷이 필요 없어집니다 —
    patch_startext (34KB) · patch_starfind (27KB)
    patch_starfix (13KB)  · patch_celebgo 의 스타 쪽 부분 (36KB)
"""
import io, os, re, sys, datetime
from build_startext import read as read_star, GAN, OH, SIP

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, '..', 'pages', 'star-saju.live.html')
NEW  = os.path.join(HERE, '..', 'pages', 'star-saju.new.html')
OUT  = os.path.join(HERE, '..', 'php', 'patch_starsrc.WPCODE.txt')

EDITS = []          # (이름, 찾을 것, 바꿀 것)


def E(name, a, b, where='t'):
    """where='t' 스타 사주 덩어리 / 'h' 그 앞(화면 뼈대와 모양)"""
    EDITS.append((name, a, b, where))


def para(ps):
    """문단 여럿을 한 덩어리로. ** 는 굵게, {이름}은 그대로 둡니다."""
    out = []
    for p in ps:
        t = ''
        bold = 0
        for i, seg in enumerate(p.split('**')):
            if i % 2:
                t += '<b>' + seg + '</b>'
                bold += 1
            else:
                t += seg
        cls = ''
        if bold == 1:
            if p.startswith('**'):
                if p.rstrip().endswith('**'):
                    cls = ' class="sr-key"'
        out.append('<p' + cls + '>' + t + '</p>')
    # 바깥에서 <p> 로 한 번 더 싸므로 첫 여는 태그와 끝 닫는 태그를 뗍니다
    joined = ''.join(out)
    joined = re.sub(r'^<p[^>]*>', '', joined)
    joined = re.sub(r'</p>$', '', joined)
    return joined


def js_map(d, keys, kor=None):
    rows = []
    for k in keys:
        rows.append("    '%s':'%s'" % (k, para(d[k])))
    return '{\n' + ',\n'.join(rows) + '\n  }'


def build():
    day, much, none, sip, probs = read_star()
    if probs:
        for p in probs:
            print('★ ' + p)
        sys.exit(1)

    whole = io.open(SRC, encoding='utf-8').read()

    # ★★ 표가 **두 번** 선언돼 있습니다 (CLAUDE.md 의 되풀이 탈).
    #   앞엣것은 전자책과 함께 쓰는 **풀이 엔진**이고,
    #   뒤엣것이 **스타 사주 화면**입니다. 뒤엣것만 고칩니다.
    # ★ 조각과 **똑같은 표지말**을 써야 자르는 자리가 같아집니다.
    #   줄바꿈이 든 표지말은 줄끝 표시가 바뀌면 못 찾습니다.
    MARK = 'var STARS='
    if whole.count(MARK) != 1:
        print('★ 스타 사주 덩어리를 못 찾았습니다 : %d군데' % whole.count(MARK))
        sys.exit(1)
    cut = whole.index(MARK)
    head, s = whole[:cut], whole[cut:]

    # ── ① 오행 막대 다섯 줄 → 한 줄, 사주표 바로 아래 ─────────
    E('오행 한 줄 만들기',
      """    }).join('');

    var sipTxt=p.sip.map(function(s){""",
      """    }).join('');

    /* 오행은 막대 다섯 줄 대신 한 줄로 (2026-09-16) */
    var barsOne=ELS.map(function(e){
      return e+' '+(p.el[e]?p.el[e]:0);
    }).join('   ·   ');

    /* 글 안의 {이름} 을 그 사람 이름으로 */
    function fill(t){ return String(t===undefined?'':t).split('{이름}').join(esc(p.n)); }

    var sipTxt=p.sip.map(function(s){""")

    E('십성 글에 이름 넣기',
      """      return '<h3>'+t.t+'</h3><p>'+t.d+'</p>';""",
      """      return '<h3>'+t.t+'</h3><p>'+fill(t.d)+'</p>';""")

    E('오행 글에 이름 넣기',
      """    if(p.hi){ elTxt+='<h3>'+ga(p.hi)+' 가장 강합니다</h3><p>'+EL_MUCH[p.hi]+'</p>'; }
    if(p.no.length){
      elTxt+='<h3>'+eun(p.no.join('·'))+' 한 글자도 없습니다</h3>'+
        p.no.map(function(e){ return '<p>'+EL_NONE[e]+'</p>'; }).join('');
    }""",
      """    if(p.hi){ elTxt+='<h3>'+ga(p.hi)+' 가장 강합니다</h3><p>'+fill(EL_MUCH[p.hi])+'</p>'; }
    if(p.no.length){
      elTxt+='<h3>'+eun(p.no.join('·'))+' 한 글자도 없습니다</h3>'+
        p.no.map(function(e){ return '<p>'+fill(EL_NONE[e])+'</p>'; }).join('');
    }""")

    E('막대를 한 줄로 바꿔 표 아래에',
      """      '</div>'+
      knownTxt+
      '<h3>일간 '+p.g+' — '+d.image+'</h3>'+
      '<p>'+d.what+'</p><p>'+d.good+'</p><p>'+d.care+'</p>'+
      '<div class="scale">'+bars+'</div>'+""",
      """      '</div>'+
      '<div class="el1">'+barsOne+'</div>'+
      knownTxt+
      '<h3>일간 '+p.g+' — '+d.image+'</h3>'+
      '<p>'+fill(d.what)+'</p>'+""")

    # ── ② 이름만 쉰 개 늘어놓던 명단 접기 ──────────────────────
    E('같은 일간 명단 접기',
      """    var sameTxt='';
    if(same.length){
      sameTxt='<h3>일간이 같은 사람 '+same.length+'명</h3>'+""",
      """    var sameTxt='';
    if(0){      /* 2026-09-16 · 소희 님 「관심없는 내용일듯」 */
      sameTxt='<h3>일간이 같은 사람 '+same.length+'명</h3>'+""")

    # ── ③ 통계 갈래 접기 ──────────────────────────────────────
    E('얼마나 드문가 접기',
      """    var r = $('svRare');
    if(r){ r.innerHTML = srRare(p); }""",
      """    var r = $('svRare');
    if(r){ r.innerHTML = ''; }   /* 2026-09-16 · 통계는 팬이 볼 것이 아닙니다 */""")

    # ── ④ 어려운 말 한 줄 빼기 ────────────────────────────────
    E('편재·기토 줄 빼기',
      """          '<h3>나와 이 사람</h3>' +
          '<p>당신은 <b>' + me.ko + '</b>입니다. ' +
          esc(p.n) + ' 님은 당신에게 <b>' + rel + '</b>입니다.</p>' +""",
      """          '<h3>나와 이 사람</h3>' +""")

    # ── ⑤ 「내 사주로」 → 「○○ 님과 나의 궁합 보기」 ──────────
    E('궁합 단추로 바꾸기',
      """      '<a class="go" href="/door-career/">내 사주로 같은 것을 보기 →</a>'+""",
      """      '<a class="go sr-um" href="/uandme/">'+esc(p.n)+
        ' 님과 나의 궁합 보기<span>내 생일만 넣으면 됩니다 · 무료</span></a>'+""")

    # ── ⑥ 덮개가 머리글에 안 가리게 + 이름 담기 ───────────────
    E('머리글에 안 가리게 · 이름 담기',
      """    $('svSheet').className='sheet open';
    document.body.style.overflow='hidden';""",
      """    $('svSheet').className='sheet open';
    document.body.style.overflow='hidden';

    /* 유앤미로 넘길 이름을 담아 둡니다 (2026-09-16) */
    try{ localStorage.setItem('stella_celeb_go', p.n); }catch(e){}

    /* 사이트 머리글이 붙박이라 덮개 위를 덮습니다. 머리글을 재서
       그만큼 내려 줍니다 — 짐작으로 고정값을 쓰면 화면 폭에 따라
       모자라거나 남습니다. */
    try{
      var hb=0, hx=document.elementsFromPoint
        ? document.elementsFromPoint(Math.round(window.innerWidth/2),6) : [];
      for(var hi2=0; hi2<hx.length; hi2++){
        var hs=window.getComputedStyle(hx[hi2]);
        if(!hs){ continue; }
        if(hs.position!=='fixed'){ if(hs.position!=='sticky'){ continue; } }
        var hr=hx[hi2].getBoundingClientRect();
        if(hr.top>4){ continue; }
        if(hr.height<20){ continue; }
        if(hr.height>220){ continue; }
        if(hr.bottom>hb){ hb=hr.bottom; }
      }
      var cd=$('svCard');
      if(cd){
        var cr=cd.getBoundingClientRect();
        if(cr.top < hb+12){ cd.style.paddingTop=Math.round(hb+20-cr.top)+'px'; }
      }
    }catch(e){}""")

    # ── ⑦ 판2 원고를 표에 박습니다 ────────────────────────────
    #     DAY 는 what 한 칸에 다 담고, 그리는 자리에서 한 번만 씁니다
    for g in GAN:
        m = re.search(r"'" + g + r"':\{ kor:'([^']*)', image:'([^']*)',\s*\n"
                      r"\s*what:'([^']*)',\s*\n"
                      r"\s*good:'([^']*)',\s*\n"
                      r"\s*care:'([^']*)' \}", s)
        if not m:
            print('★ 일간 %s 의 칸을 못 찾았습니다' % g)
            sys.exit(1)
        E('일간 ' + g + ' 글',
          m.group(0),
          "'%s':{ kor:'%s', image:'%s',\n      what:'%s',\n      good:'', care:'' }"
          % (g, m.group(1), m.group(2), para(day[g])))

    old_much = re.search(r'var EL_MUCH=\{[\s\S]*?\n  \};', s)
    if not old_much:
        print('★ EL_MUCH 를 못 찾았습니다'); sys.exit(1)
    E('가장 강한 오행 글', old_much.group(0), 'var EL_MUCH=' + js_map(much, OH) + ';')

    old_none = re.search(r'var EL_NONE=\{[\s\S]*?\n  \};', s)
    if not old_none:
        print('★ EL_NONE 을 못 찾았습니다'); sys.exit(1)
    E('없는 오행 글', old_none.group(0), 'var EL_NONE=' + js_map(none, OH) + ';')

    for k in SIP:
        m = re.search(r"'" + k + r"':\{ t:'([^']*)',\s*\n\s*d:'([^']*)' \}", s)
        if not m:
            print('★ 십성 %s 의 칸을 못 찾았습니다' % k); sys.exit(1)
        E('십성 ' + k + ' 글', m.group(0),
          "'%s':{ t:'%s',\n      d:'%s' }" % (k, m.group(1), para(sip[k])))

    # ── ⑧ 서강준을 명단에 넣습니다 ────────────────────────────
    #   네이버 검색어 추이 2026-09 에서 1위인데 명단에 없었습니다.
    #   생년월일은 서로 다른 세 곳에서 1993-10-12 로 확인했습니다.
    #   사주는 **쪽 안의 계산기**(StellaSaju.compute)로 세웠습니다 —
    #   제가 따로 셈하면 나머지 537명과 어긋납니다. 「산」으로 맞춰
    #   己卯·辛未·癸亥 가 명단과 같은 것을 확인했습니다.
    #   십성 두 개를 고르는 규칙도 537명 전부에 맞춰 되찾았습니다
    #   (일간을 뺀 다섯 글자에서 많은 둘, 같으면 먼저 나온 것).
    SEO = ('{"n":"서강준","c":"ㅅ","b":"1993-10-12","k":"","j":"배우","a":"닭",'
           '"y":"癸酉","m":"壬戌","dd":"丙寅","g":"丙","gk":"병화",'
           '"el":{"목":1,"화":1,"토":1,"금":1,"수":2},"hi":"수","no":[],'
           '"sip":["정관","정재"],"s":"천칭자리"}')
    # 이준혁 — 널리 알려진 「2월 11일」은 **음력**입니다.
    #   두 사주 사이트가 낸 명식(甲子·丁卯·丙午)을 우리 계산기로 되짚으니
    #   1984-03-13 하루만 그 명식을 냅니다. 세 번째 곳도 「병오일주」라
    #   적고 있습니다. 그래서 b 는 양력 3월 13일, k 에 알려진 날짜를 둡니다
    #   (쪽이 「그 날짜가 음력이거나 호적상 날짜여서…」라고 알려줍니다).
    JUN = ('{"n":"이준혁","c":"ㅇ","b":"1984-03-13","k":"1984-02-11","j":"배우","a":"쥐",'
           '"y":"甲子","m":"丁卯","dd":"丙午","g":"丙","gk":"병화",'
           '"el":{"목":2,"화":3,"토":0,"금":0,"수":1},"hi":"화","no":["토","금"],'
           '"sip":["편인","편관"],"s":"물고기자리"}')
    E('서강준 · 이준혁 넣기', 'var STARS=[{"n":"유재석"',
      'var STARS=[' + SEO + ',' + JUN + ',{"n":"유재석"')

    # ── 보기 이름을 서강준으로 (소희 님 「유재석 생일도 서강준으로」) ──
    #   생일 칸까지 같이 바꿉니다 — 이름만 바꾸면 1972.8.14 가 남아
    #   딴 사람 생일이 됩니다.
    E('보기 이름 서강준으로',
      """    <div class="fld wide"><label>이름</label><input id="qName" type="text" maxlength="20" placeholder="예) 유재석"></div>
    <div class="fld"><label>태어난 해</label><input id="qY" type="number" inputmode="numeric" placeholder="1972" min="1900" max="2026"></div>
    <div class="fld"><label>달</label><input id="qM" type="number" inputmode="numeric" placeholder="8" min="1" max="12" style="width:80px"></div>
    <div class="fld"><label>날</label><input id="qD" type="number" inputmode="numeric" placeholder="14" min="1" max="31" style="width:80px"></div>""",
      """    <div class="fld wide"><label>이름</label><input id="qName" type="text" maxlength="20" placeholder="예) 서강준"></div>
    <div class="fld"><label>태어난 해</label><input id="qY" type="number" inputmode="numeric" placeholder="1993" min="1900" max="2026"></div>
    <div class="fld"><label>달</label><input id="qM" type="number" inputmode="numeric" placeholder="10" min="1" max="12" style="width:80px"></div>
    <div class="fld"><label>날</label><input id="qD" type="number" inputmode="numeric" placeholder="12" min="1" max="31" style="width:80px"></div>""",
      'h')

    # ── ⑨ 검색칸 + 「요즘 많이 보는 사람」 여덟 ────────────────
    E('검색칸과 여덟 장',
      """  <div class="bar" id="svCho"><div class="lb">ㄱㄴㄷ 으로 찾기</div></div>""",
      """  <div class="find">
   <div class="lb">누구를 볼까요?</div>
   <input id="svFind" type="text" autocomplete="off" placeholder="이름을 쳐보세요 — 서강준">
   <div class="found" id="svFound" style="display:none"></div>
   <div class="lb2">요즘 많이 보는 사람</div>
   <div class="hot" id="svHot"></div>
   <button type="button" class="moreall" id="svMoreAll">537명 전체에서 찾기</button>
  </div>

  <div id="svAll" style="display:none">
  <div class="bar" id="svCho"><div class="lb">ㄱㄴㄷ 으로 찾기</div></div>""", 'h')

    E('전체 목록 닫기',
      """  <div class="empty" id="svEmpty" style="display:none">고른 조건에 맞는 사람이 없습니다.</div>""",
      """  <div class="empty" id="svEmpty" style="display:none">고른 조건에 맞는 사람이 없습니다.</div>
  </div>""", 'h')

    E('검색 돌리기',
      """  function open(name){
    var p=find(name);
    if(!p){ return; }
    show(p, true);
  }""",
      """  function open(name){
    var p=find(name);
    if(!p){ return; }
    show(p, true);
  }

  /* ── 2026-09-16 · 검색칸과 「요즘 많이 보는 사람」 ────────────
     소희 님 「아래 리스트는 필요없어 고르는게 더 힘들어」
     537명 벽 대신 검색칸 하나와 여덟 장을 둡니다. 전체는 접어
     두고 눌러야 열립니다.

     여덟은 **네이버 검색어 추이**(2026년 6~9월)로 골랐습니다.
     바꾸시려면 아래 HOT 한 줄만 고치면 됩니다. */
  var HOT = ['서강준','송강','아이유','변우석','이준혁','한소희','카리나','장원영'];

  function bindGo(box){
    var gs = box.querySelectorAll('[data-go]'), i;
    for(i = 0; i < gs.length; i++){
      gs[i].addEventListener('click', function(){
        open(this.getAttribute('data-go'));
      });
    }
  }

  function findRun(q){
    var r = $('svFound');
    if(!r){ return; }
    var s = '', i, ch;
    var raw = String(q === null ? '' : q);
    for(i = 0; i < raw.length; i++){
      ch = raw.charAt(i);
      if(ch !== ' '){ s += ch; }
    }
    if(!s){ r.innerHTML = ''; r.style.display = 'none'; return; }
    var h = '', n = 0;
    for(i = 0; i < STARS.length; i++){
      if(STARS[i].n.indexOf(s) < 0){ continue; }
      h += '<button type="button" data-go="' + esc(STARS[i].n) + '">' +
           esc(STARS[i].n) + '<span>' + esc(STARS[i].j) + '</span></button>';
      n++;
      if(n >= 16){ break; }
    }
    if(!h){
      h = '<p class="no">그 이름은 아직 없습니다. 아래 「찾는 사람이 목록에 없나요」' +
          '에서 생일로 바로 세울 수 있어요.</p>';
    }
    r.innerHTML = h;
    r.style.display = '';
    bindGo(r);
  }

  function findUI(){
    var box = $('svHot');
    if(!box){ return; }
    var i, h = '';
    for(i = 0; i < HOT.length; i++){
      if(!find(HOT[i])){ continue; }
      h += '<button type="button" data-go="' + esc(HOT[i]) + '">' + esc(HOT[i]) + '</button>';
    }
    box.innerHTML = h;
    bindGo(box);

    var inp = $('svFind');
    if(inp){
      inp.addEventListener('input', function(){ findRun(this.value); });
    }
    var mo = $('svMoreAll');
    if(mo){
      mo.addEventListener('click', function(){
        var a = $('svAll');
        if(!a){ return; }
        if(a.style.display === 'none'){
          a.style.display = '';
          mo.textContent = '전체 목록 접기';
        } else {
          a.style.display = 'none';
          mo.textContent = '537명 전체에서 찾기';
        }
      });
    }
  }
  setTimeout(findUI, 0);""")

    # ── ⑧ 새로 쓰는 모양 (한 줄 오행 · 맺음말 · 궁합 단추) ─────
    E('새 모양 CSS',
      """<style>
/* 2026-09-09 · 글꼴을 고딕으로, 작은 글씨를 키웁니다""",
      """<style>
/* ── 2026-09-16 · 한 줄 오행 · 맺음말 · 궁합 단추 ── */
  #ssv .el1{ margin:10px 0 18px; padding:9px 14px; border-radius:10px;
    background:rgba(94,69,166,.06); color:#5E45A6; text-align:center;
    font-size:.92rem; font-weight:700; letter-spacing:.02em; }
  #ssv .sr-key{ color:#5E45A6; font-weight:700; }
  #ssv a.go.sr-um{ display:block; box-sizing:border-box; width:100%;
    margin:22px 0 4px; padding:16px 20px; border-radius:14px; text-align:center;
    background:linear-gradient(135deg,#6B5BA8,#8E7BD0); color:#fff;
    font-weight:700; text-decoration:none; }
  #ssv a.go.sr-um span{ display:block; margin-top:5px;
    font-size:.82rem; font-weight:400; opacity:.88; }
  /* 검색칸과 여덟 장 */
  #ssv .find{ margin:18px 0 6px; }
  #ssv .find .lb{ font-size:13px; font-weight:700; margin-bottom:7px; }
  #ssv .find .lb2{ font-size:12px; opacity:.72; margin:16px 0 8px; }
  #ssv .find input{ width:100%; box-sizing:border-box; padding:13px 15px;
    border-radius:12px; font-size:16px; }
  #ssv .find .hot{ display:flex; flex-wrap:wrap; gap:8px; }
  #ssv .find .hot button{ padding:10px 15px; border-radius:11px; font-size:14px;
    font-weight:700; cursor:pointer; }
  #ssv .find .found{ margin-top:10px; display:flex; flex-wrap:wrap; gap:8px; }
  #ssv .find .found button{ padding:9px 13px; border-radius:10px; font-size:14px;
    font-weight:700; cursor:pointer; }
  #ssv .find .found button span{ display:block; font-size:11px; font-weight:400; opacity:.6; }
  #ssv .find .found .no{ font-size:13px; opacity:.7; margin:6px 2px; }
  #ssv .find .moreall{ display:block; width:100%; margin-top:16px; padding:12px;
    border-radius:11px; font-size:13.5px; cursor:pointer; }
</style>
<style>
/* 2026-09-09 · 글꼴을 고딕으로, 작은 글씨를 키웁니다""")

    # ── 적용 ──────────────────────────────────────────────────
    bad = []
    for name, a, b, where in EDITS:
        if where == 'h':
            n = head.count(a)
            if n != 1: bad.append('%s : %d군데 (앞쪽)' % (name, n))
            else: head = head.replace(a, b, 1)
        else:
            n = s.count(a)
            if n != 1: bad.append('%s : %d군데' % (name, n))
            else: s = s.replace(a, b, 1)
    if bad:
        print('★ 한 군데가 아닌 자리 %d :' % len(bad))
        for x in bad:
            print('   ' + x)
        sys.exit(1)

    io.open(NEW, 'w', encoding='utf-8').write(head + s)
    print('고친 쪽 : %s · %d자 (%d자 늘어남)'
          % (os.path.basename(NEW), len(head + s), len(head + s) - len(whole)))
    print('고친 자리 %d군데' % len(EDITS))
    return s


if __name__ == '__main__':
    build()


# ══════════════════════════════════════════════════════════════
#  살아 있는 쪽에 넣는 한 번짜리 조각
# ══════════════════════════════════════════════════════════════

HEAD = '''/* ════════════════════════════════════════════════════════════
   스타 사주 · 쪽 원본 고치기 %(P)d/3 — %(T)s
   판 %(S)s
   (도구가 뽑았습니다 — build_starpage.py. 손으로 고치지 마세요)

   소희 님 : 「연애인 리스트도 떴다가 가려지는 형식이야
              그럼 전체 코딩이 무거워지지 않아?」

   맞는 말씀이었습니다. 브라우저는 CSS 를 **그리기 전에**,
   자바스크립트를 **그린 뒤에** 읽습니다. 조각으로 덮으면
   반드시 한 번은 옛 모습이 보입니다.

   이제 워드프레스로 쪽 내용을 직접 읽을 수 있게 되어, 밖에서
   덮을 까닭이 없어졌습니다. 쪽 안의 표와 그리는 자리를 곧바로
   고칩니다. 깜빡임이 원천적으로 없어집니다.

   ── 이 조각이 끝나면 꺼도 되는 것 ───────────────────
       patch_startext   (34KB)  글을 덮던 것
       patch_starfind   (27KB)  리스트를 감추던 것
       patch_starfix    (13KB)  화면을 손보던 것
       patch_celebgo    (36KB)  스타 쪽 부분. ★ 유앤미 쪽에서
                                이름을 골라주는 일은 남으므로
                                **끄지 마시고** 그대로 두세요.

   ── 이 조각이 바꾸는 자리 %(N)d군데 ──────────────────
       · 일간 열 · 오행 열 · 십성 열의 글을 판2 원고로
       · 오행 막대 다섯 줄 → 사주표 아래 한 줄
       · 「일간이 같은 사람 N명」 이름 명단 접기
       · 「이 사람은 얼마나 드문가」 통계 접기
       · 「당신은 기토입니다 … 편재입니다」 어려운 줄 빼기
       · 「내 사주로 같은 것을 보기」 → 「○○ 님과 나의 궁합 보기」
       · 결과가 사이트 머리글에 안 가리게 (머리글을 재서 내림)

   ── 쓰는 법 ─────────────────────────────────────────
   ★★ 셋으로 쪼갰습니다 — 한 덩어리 52KB 는 붙여넣다 끊깁니다.
     셋 다 붙이셔야 다 바뀝니다. 순서는 안 가립니다.
     두 번 눌러도 안전합니다 (이미 들어간 자리는 그냥 지나갑니다).

   ① 미리보기  https://stellasaju.com/?%(K)s=1
              한 군데라도 못 찾으면 **아무것도 안 바꿉니다.**
   ② 넣기     미리보기 화면의 「이대로 넣기」
   ③ 되돌리기  https://stellasaju.com/?%(K)s=1&undo=1

   붙여넣기 : WPCode → 새 스니펫 → PHP Snippet → 저장 → Active
   ★ 위치(Location)를 「어디서나 실행 / Run Everywhere」로.
   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ 파일이 큽니다. 메모장에 먼저 붙였다가 Ctrl+A 로 통째로
     옮기시면 중간에 끊길 일이 없습니다.
   ════════════════════════════════════════════════════════════ */

add_action( 'init', function () {

	if ( ! isset( $_GET['%(K)s'] ) ) { return; }

	header( 'Content-Type: text/html; charset=utf-8' );
	echo '<meta charset="utf-8"><body style="font:15px/1.8 system-ui;'
		. 'background:#141018;color:#eee;padding:24px;max-width:900px">';

	if ( ! current_user_can( 'manage_options' ) ) {
		echo '<h1 style="color:#ff7b7b">관리자만 볼 수 있습니다.</h1>';
		exit;
	}

	$pid = 406;
	$bak = 'stella_bak_406_p%(P)d';
	$page = get_post( $pid );
	if ( ! $page ) {
		echo '<h1 style="color:#ff7b7b">쪽 406 을 못 찾았습니다.</h1>';
		exit;
	}
	/* ★★ 2026-09-16 · 줄끝 표시를 가지런히 합니다
	   살아 있는 쪽은 줄끝이 \r\n (윈도 방식)입니다. 제 쪽 도구는
	   \n 으로 읽어서, 눈에 안 보이는 한 글자 차이로 찾을 것을
	   못 찾았습니다. 먼저 \n 으로 맞춘 뒤에 고칩니다.
	   보이는 글은 하나도 안 바뀝니다. */
	$body = str_replace( array( "\r\n", "\r" ), "\n", $page->post_content );

	/* ★★ 표가 **두 번** 선언돼 있습니다 — 앞엣것은 전자책과 함께 쓰는
	   풀이 엔진이고, 뒤엣것이 스타 사주 화면입니다. 뒤엣것만 고칩니다. */
	/* ★★ 2026-09-16 · 못 찾던 까닭
	   전에는 줄바꿈이 든 글자("<script>\n(function(){\n  var STARS=")로
	   찾았습니다. 조각이 WPCode 에 담기는 동안 줄끝 표시가 \r\n 으로
	   바뀌면 그 한 글자 때문에 못 찾습니다.
	   이제 **줄바꿈이 하나도 없는** 표지말로 찾습니다. */
	$MARK = 'var STARS=';
	$cut  = strpos( $body, $MARK );
	if ( false === $cut ) {
		echo '<h1 style="color:#ff7b7b">스타 사주 덩어리를 못 찾았습니다.</h1>';
		/* ★ 짐작하지 않게 **쪽이 어떻게 생겼는지** 그대로 찍습니다.
		   이 표를 보여주시면 까닭이 한 번에 드러납니다. */
		$rawlen = strlen( $page->post_content );
		echo '<table cellpadding="6" style="border-collapse:collapse;font-size:13px">';
		printf( '<tr><td>쪽 406 글자 수</td><td><b>%%s</b> (제가 읽은 것은 246,854)</td></tr>',
			number_format( $rawlen ) );
		printf( '<tr><td>고친 때</td><td>%%s</td></tr>', esc_html( $page->post_modified ) );
		$look = array( 'var STARS=', 'STARS', '유재석', 'svCard', 'svGrid', 'EL_MUCH', '<script' );
		foreach ( $look as $w ) {
			printf( '<tr><td><code>%%s</code></td><td>%%d군데</td></tr>',
				esc_html( $w ), substr_count( $body, $w ) );
		}
		printf( '<tr><td>줄끝</td><td>\\r\\n %%d군데 · 홑 \\n %%d군데</td></tr>',
			substr_count( $page->post_content, "\r\n" ),
			substr_count( $page->post_content, "\n" ) - substr_count( $page->post_content, "\r\n" ) );
		printf( '<tr><td>역빗금</td><td>%%d개</td></tr>', substr_count( $body, chr( 92 ) ) );
		echo '</table>';
		echo '<h3 style="color:#ffd76a">쪽 맨 앞 200자</h3>';
		echo '<pre style="white-space:pre-wrap;word-break:break-all;background:#0b0810;'
			. 'padding:12px;border-radius:8px;font-size:12px;color:#c9c3d6">'
			. esc_html( substr( $body, 0, 200 ) ) . '</pre>';
		echo '<p>이 표를 그대로 보여주세요 — 까닭이 바로 보입니다.</p>';
		exit;
	}

	/* ★★ 찾을 글과 넣을 글의 줄끝도 가지런히 맞춥니다.
	   같은 까닭입니다 — 조각 쪽 줄끝이 \r\n 이면 쪽(\n)과 안 맞습니다. */
	foreach ( $EDITS as $ei => $ee ) {
		$EDITS[ $ei ][2] = str_replace( array( "\r\n", "\r" ), "\n", $ee[2] );
		$EDITS[ $ei ][3] = str_replace( array( "\r\n", "\r" ), "\n", $ee[3] );
	}
	$head = substr( $body, 0, $cut );
	$tail = substr( $body, $cut );

	/* ── 되돌리기 ─────────────────────────────────────── */
	if ( isset( $_GET['undo'] ) ) {
		$old = get_post_meta( $pid, $bak, true );
		if ( ! $old ) {
			echo '<h1 style="color:#ff7b7b">되돌릴 것이 없습니다.</h1>';
			exit;
		}
		echo '<h1 style="color:#ffd76a">되돌리기</h1>';
		printf( '<p>지금 %%s자 → 되돌리면 %%s자</p>',
			number_format( strlen( $body ) ), number_format( strlen( $old ) ) );
		if ( ! isset( $_GET['go'] ) ) {
			echo '<p style="font-size:18px"><a style="color:#ffd76a" '
				. 'href="?%(K)s=1&amp;undo=1&amp;go=1">→ 이대로 되돌리기</a></p>';
			exit;
		}
		wp_update_post( array( 'ID' => $pid, 'post_content' => $old ) );
		clean_post_cache( $pid );
		echo '<h2 style="color:#7bff9b">되돌렸습니다.</h2>';
		exit;
	}

'''

FOOT = '''
	/* ── 찾아보기 ─────────────────────────────────────── */
	$go   = isset( $_GET['go'] );
	$miss = array();
	$hit  = 0;
	foreach ( $EDITS as $e ) {
		$n = substr_count( 'h' === $e[1] ? $head : $tail, $e[2] );
		if ( 1 === $n ) { $hit++; }
		else { $miss[] = array( $e[0], $n ); }
	}

	printf( '<h1 style="color:#ffd76a">스타 사주 쪽 고치기 %(P)d/3 — %%s</h1>',
		$go ? '넣기' : '<span style="color:#9fd">미리보기 · 아무것도 안 바뀝니다</span>' );
	printf( '<p>쪽 406 · 지금 <b>%%s자</b> · 고칠 자리 <b>%%d</b>군데 가운데 '
		. '<b style="color:%%s">%%d군데</b>를 찾았습니다.</p>',
		number_format( strlen( $body ) ), count( $EDITS ),
		count( $miss ) ? '#ff7b7b' : '#7bff9b', $hit );

	/* 다 안 보이면 이미 들어간 것입니다 */
	if ( 0 === $hit ) {
		$zero = 0;
		foreach ( $miss as $m ) { if ( 0 === $m[1] ) { $zero++; } }
		if ( $zero === count( $EDITS ) ) {
			echo '<h2 style="color:#7bff9b">이 조각은 이미 들어가 있습니다.</h2>';
			echo '<p>바꿀 것이 없습니다. 다음 조각으로 가셔도 됩니다.</p>';
			exit;
		}
	}

	if ( count( $miss ) ) {
		echo '<h2 style="color:#ff7b7b">★ 못 찾은 자리가 있어 아무것도 안 바꿉니다</h2>';
		echo '<ul style="font-size:13px">';
		foreach ( $miss as $m ) {
			printf( '<li>%%s — %%d군데</li>', esc_html( $m[0] ), $m[1] );
		}
		echo '</ul>';
		echo '<p style="color:#888">쪽이 그 사이에 바뀐 것입니다. 저에게 알려주세요 — '
			. '지금 쪽을 다시 읽어 조각을 새로 뽑겠습니다.</p>';
		/* 빈칸만 다른 것인지 한 번 더 봅니다 — 그러면 까닭이 바로 보입니다 */
		echo '<h3 style="color:#ffd76a">빈칸을 다 떼고 보면</h3><ul style="font-size:13px">';
		foreach ( $miss as $m ) {
			$k = 0;
			foreach ( $EDITS as $e ) {
				if ( $e[0] !== $m[0] ) { continue; }
				$a = preg_replace( '/\s+/u', '', $e[2] );
				$t = preg_replace( '/\s+/u', '', 'h' === $e[1] ? $head : $tail );
				$k = substr_count( $t, $a );
			}
			printf( '<li>%%s — 빈칸 떼고 보면 %%d군데</li>', esc_html( $m[0] ), $k );
		}
		echo '</ul><p style="color:#888">「빈칸 떼고 보면 1군데」로 나오면 '
			. '줄끝이나 들여쓰기만 다른 것입니다.</p>';
		exit;
	}

	/* ── 미리보기 ─────────────────────────────────────── */
	$nh = $head;
	$nt = $tail;
	foreach ( $EDITS as $e ) {
		if ( 'h' === $e[1] ) { $nh = str_replace( $e[2], $e[3], $nh ); }
		else { $nt = str_replace( $e[2], $e[3], $nt ); }
	}
	$new = $nh . $nt;

	printf( '<p>고친 뒤 <b>%%s자</b> (%%+d자)</p>',
		number_format( strlen( $new ) ), strlen( $new ) - strlen( $body ) );

	echo '<table cellpadding="6" style="border-collapse:collapse;font-size:13px">';
	foreach ( $EDITS as $e ) {
		printf( '<tr><td style="color:#9fd">%%s</td><td style="color:#888">%%d자 → %%d자</td></tr>',
			esc_html( $e[0] ), strlen( $e[2] ), strlen( $e[3] ) );
	}
	echo '</table>';

	if ( ! $go ) {
		echo '<h2 style="color:#ffd76a;margin-top:22px">여기까지가 미리보기입니다.</h2>';
		echo '<p style="font-size:18px"><a style="color:#ffd76a" '
			. 'href="?%(K)s=1&amp;go=1">→ 이대로 넣기</a></p>';
		echo '<p style="color:#888">넣기 직전 쪽을 통째로 백업합니다. '
			. '?%(K)s=1&amp;undo=1 로 언제든 되돌립니다.</p>';
		exit;
	}

	/* ── 넣기 ─────────────────────────────────────────── */
	update_post_meta( $pid, $bak, $body );   /* 지금 쪽을 백업 */
	wp_update_post( array( 'ID' => $pid, 'post_content' => $new ) );
	clean_post_cache( $pid );
	if ( function_exists( 'wp_cache_flush' ) ) { wp_cache_flush(); }

	echo '<h2 style="color:#7bff9b">넣었습니다.</h2>';
	printf( '<p>백업 %%s자 · 지금 %%s자</p>',
		number_format( strlen( $body ) ), number_format( strlen( $new ) ) );
	printf( '<p style="font-size:18px"><a style="color:#ffd76a" href="%%s">→ 스타 사주 열어보기</a></p>',
		esc_url( get_permalink( $pid ) ) );
	echo '<h3 style="color:#ffd76a;margin-top:24px">이제 조각 셋을 꺼주세요</h3>';
	echo '<p><b>patch_startext</b> · <b>patch_starfind</b> · <b>patch_starfix</b><br>'
		. '세 조각이 하던 일이 쪽 안으로 들어갔습니다. 켜 두면 같은 일을 두 번 합니다.</p>';
	echo '<p style="color:#888">★ <b>patch_celebgo</b> 는 그대로 두세요 — '
		. '유앤미 쪽에서 이름을 골라주는 일이 남아 있습니다.</p>';
	echo '<p style="color:#888">이 조각도 이제 꺼두셔도 됩니다.</p>';
	exit;
}, 1 );
'''


def emit():
    """★ 2026-09-16 · 한 덩어리 52KB 는 붙여넣다 끊깁니다.
       소희 님이 주소를 열어도 「아무것도 안 나오고 그냥 스타 사주 쪽」
       이라고 하셨습니다 — 조각이 아예 안 켜진 것입니다. 삼재 때와
       같은 일입니다. 그래서 **셋으로 쪼갭니다.**

       셋은 순서를 안 가리고, 두 번 눌러도 안전합니다 —
       이미 들어간 자리는 찾을 글이 없으니 그냥 「이미 들어가 있습니다」."""
    build()
    stamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')

    sized = [(n, a, b, w, len(a.encode('utf-8')) + len(b.encode('utf-8')))
             for n, a, b, w in EDITS]
    total = sum(x[4] for x in sized)
    parts, cur, acc = [], [], 0
    for x in sized:
        cur.append(x)
        acc += x[4]
        if acc >= total / 3.0 and len(parts) < 2:
            parts.append(cur)
            cur, acc = [], 0
    parts.append(cur)

    names = ['글 · 일간 열', '글 · 오행과 십성', '화면 · 검색칸과 두 사람']
    for k, grp in enumerate(parts):
        rows = []
        for n, a, b, w, _ in grp:
            rows.append("\t\tarray( '%s', '%s',\n\t\t\t<<<'STELLA_A'\n%s\nSTELLA_A\n\t\t\t,\n\t\t\t<<<'STELLA_B'\n%s\nSTELLA_B\n\t\t),"
                        % (n.replace("'", ''), w, a, b))
        php = "\t$EDITS = array(\n" + '\n'.join(rows) + "\n\t);\n"
        key = 'stella_star%d' % (k + 1)
        out = (HEAD % {'S': stamp, 'N': len(grp), 'K': key,
                       'P': k + 1, 'T': names[k]}) + php + (FOOT % {'K': key, 'P': k + 1})
        dst = os.path.join(HERE, '..', 'php', 'patch_star%d.WPCODE.txt' % (k + 1))
        io.open(dst, 'w', encoding='utf-8').write(out)
        print('%d. %-20s %2d군데 · %6d바이트 · ?%s=1'
              % (k + 1, names[k], len(grp), len(out.encode('utf-8')), key))
