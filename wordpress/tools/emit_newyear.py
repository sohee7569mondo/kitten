# -*- coding: utf-8 -*-
"""NY<해>.json -> WPCode 조각 (신년운세 책 갈아끼우기)

    python3 emit_newyear.py 2026
    python3 emit_newyear.py 2027
"""
import io, json, sys, os, re


def year_luck_names(doc):
    """올해이름 · 대운이름을 원고에서 그대로 뽑습니다.

    2026-09-14 · 소희 님 : 「올해 이름에 값이 들어가야 하는거 아닌가?」
    맞습니다. {올해이름} {대운이름} 은 아무도 안 채우고 있어서 손님 책에
    중괄호 그대로 찍히고 있었습니다.

    손으로 옮겨 적지 않습니다 — 원고의 소제목에서 읽습니다.
      01장  「비겁 · 내가 정하고 내가 서는 해」        → 올해이름
            (2027 은 「비겁 → 식상 · …」 꼴이라 화살표도 흡수합니다)
      02장  「비겁 · 나를 세우는 십 년」                → 대운이름
            문장이 「「…」의 십 년을 지나고 있습니다」라서
            「십 년」을 떼고 「흐름」을 붙입니다.
    """
    G = ('비겁', '식상', '재성', '관성', '인성')
    yn, ln = {}, {}
    for b in doc.get('01', []):
        t = re.sub(r'<[^>]+>', '', str(b.get('t', '')))
        m = re.match(r'^(비겁|식상|재성|관성|인성)\s*(?:→\s*\S+\s*)?·\s*(.+?)\s*$', t)
        if m:
            yn[m.group(1)] = m.group(2)
    for b in doc.get('02', []):
        t = re.sub(r'<[^>]+>', '', str(b.get('t', '')))
        m = re.match(r'^(비겁|식상|재성|관성|인성)\s*·\s*(.+?)\s*십\s*년\s*$', t)
        if m:
            ln[m.group(1)] = m.group(2) + ' 흐름'
    miss = [g for g in G if g not in yn or g not in ln]
    if miss:
        raise SystemExit('★ 이름표를 못 뽑았습니다: %s' % ', '.join(miss))
    return yn, ln

YEAR = sys.argv[1] if len(sys.argv) > 1 else '2026'
HERE = os.path.dirname(os.path.abspath(__file__))
NY = io.open(os.path.join(HERE, 'NY%s.json' % YEAR), encoding='utf-8').read()

# 그 해 세운 천간의 오행 — 2026 병(화) · 2027 정(화)
YEAR_EL = {'2026': '화', '2027': '화'}[YEAR]
YEAR_GAN = {'2026': '병오년', '2027': '정미년'}[YEAR]

HEAD = u'''<?php
/* ══════════════════════════════════════════════════════════
   %(Y)s년 운세 — 열 장짜리 별도 구조 책
                                        ★ 2026-09-14 · 소희 님께
                                        판 NY%(Y)s-1

   ── 무엇을 하나 ───────────────────────────────────────
   door-fortune 에서 「%(Y)s년 운세」를 고르면 우리 열 장이 나옵니다.
   지금은 그 주제가 DOOR_TOPICS 에 없어서 문 단위 일반판이 나옵니다.

   ★ 먼저 patch160_nydoor 를 넣으셔야 단추가 생깁니다.

   ── 앵커를 안 잡습니다 ────────────────────────────────
   쪽 글을 한 글자도 안 바꿉니다. 책이 다 그려진 뒤, 주제가
   「%(Y)s년 운세」면 책 그릇의 내용을 우리 열 장으로 갈아끼웁니다.
   그래서 「0군데」가 날 일이 없습니다.
   되돌리기도 없습니다 — 스니펫을 끄면 원래대로입니다.

   ── 스물다섯 갈래를 어떻게 고르나 ─────────────────────
   %(Y)s 은 %(YG)s 입니다. 천간이 %(YE)s 이므로 —

       무리(다섯)  = groupOf(일간 오행, %(YE)s)
                     일간 병·정 → 비겁 / 갑·을 → 식상 / 임·계 → 재성
                     경·신 → 관성 / 무·기 → 인성
       대운(다섯)  = groupOf(일간 오행, 그 해 대운 천간의 오행)
       갈래        = 무리 × 대운 = 스물다섯

   ★ 대운은 nowLuck 과 같은 셈입니다 — chart.luck.list 에서
     fromYear 가 %(Y)s 이하인 마지막 칸.
   ★ ②는 축이 넷 더 있습니다 (강도 · 이동 · 대운 · 관계).
     강도는 그 해 오행이 사주에 몇 개인가로 봅니다.

   ── 셈은 전부 책에 이미 있는 것을 씁니다 ──────────────
       window.StellaSaju.locate / compute      원국
       window.StellaRead.interpret             풀이
       chart.pillars.day.han                   일간
       chart.luck.list                         대운
       chart.five                              오행 분포

   ── 붙이는 법 ─────────────────────────────────────────
   ★ 새 조각입니다. WPCode -> 새 스니펫 -> PHP Snippet -> 저장 -> Active
   ★ 위치(Location)를 「어디서나 실행 / Run Everywhere」로.
   ★ 크롬 번역을 끄고 붙여넣으세요.

   넣으신 뒤 door-fortune 에서 「%(Y)s년 운세」를 골라 책을 뽑아보세요.

   ── 검사한 것 ─────────────────────────────────────────
   php -l           문법
   앰퍼샌드 세기      0 이어야 합니다
   node --check     스크립트 문법
   node 로 스물다섯 갈래를 다 그려봄
   ══════════════════════════════════════════════════════════ */

add_action( 'wp_head', function () {
	/* ★ 이 책은 전자책 쪽에서만 씁니다.
	   2026-09-14 · 소희 님 : 「스니펫이 많아서 그거 읽느라 사주가
	   문제있다고 햇었는데」 — 그 말씀이 맞았습니다.
	   울타리가 없으면 이 조각(수십만 자)이 홈 · 무료 쪽 · 문 쪽까지
	   모든 쪽에 실립니다. 2026 과 2027 두 권이면 반 메가가 넘습니다.
	   reading-book 에서만 내보내면 다른 쪽은 한 글자도 안 받습니다.
	   (쪽 슬러그는 워드프레스에서 직접 확인했습니다 — id 160) */
	if ( ! is_page( 'reading-book' ) ) { return; }
	?>
<style>
#ssb .keepline{ font-weight:600; }
#ssb .mini{ font-size:.86rem; color:#6a6a78; }
#ssb .nybox{ font-family:IBM Plex Mono,monospace; font-size:.74rem; line-height:1.9;
  background:#faf8f4; border:1px solid #ece6dc; border-radius:8px;
  padding:12px 14px; margin:10px 0; white-space:pre-wrap; color:#4a4a58; }
#ssb .nysay{ margin:14px 0; padding:14px 16px; border-left:3px solid #9E2B50;
  background:#fbf7f8; border-radius:0 8px 8px 0; line-height:1.85; }
#ssb .nymark{ font-family:IBM Plex Mono,monospace; font-size:.62rem;
  letter-spacing:.18em; color:#9E2B50; margin:0 0 6px; }

/* ── 쪽 폭 울타리 ──────────────────────────────────────────
   2026-09-14 · 소희 님 : 「중간에 폭이 달라짐」
                          「폭잡는것도 여러번 있던일이라서 찾아보면
                            답이 있을거야」 — 있었습니다.

   ★ 책 전체 폭은 patch160_width (WIDTH-7) 하나가 정합니다.
     그 조각 머리말에 「책의 모양 — 이 조각 하나가 정합니다」라고
     적혀 있습니다. 쪽 900px · 좌우 여백 78px · 글줄 744px.
     제가 여기에 max-width 를 또 걸어 두어 둘이 싸우고 있었습니다.
     그래서 우리 쪽에서는 폭을 아예 정하지 않습니다.

   ★ 이기는 규칙으로 씁니다 — 앞에 #ssb 를 붙입니다.
       WIDTH-7   #ssb .page                      (아이디+클래스)
       전에 우리    [data-ny%(Y)s="1"] > .page      → 힘이 모자라 집니다
       지금 우리  #ssb .book[data-ny%(Y)s="1"] > .page  → 이깁니다
     가족운 책(FAMILY-1)이 같은 탈을 겪고 이 꼴로 고쳤습니다.
     그 책과 똑같이 적어 두 책이 같은 자리에서 시작합니다.

   깃발이 .book 에 달릴 수도, #bkBook 에만 달릴 수도 있어 둘 다 겁니다. */
@media screen{
  /* ★ 왜 쪽마다 폭이 달랐나 — 2026-09-14 크로미움으로 재현해서 잡았습니다
     소희 님 : 「중간에 폭이 달라짐」 · 「폭잡는것도 여러번 있던일이라서
                찾아보면 답이 있을거야」 — 있었습니다.

     책(.book)은 display:flex · flex-direction:column 입니다.
     WIDTH-7 은 쪽을 `width:auto` + `margin-left/right:auto` 로 가운데
     놓습니다. 그런데 flex 안에서 좌우 margin 이 auto 면 stretch 가
     꺼집니다 — 쪽이 글 길이만큼 줄어들고 가운데로 몰립니다.
     재 보니 239px 부터 780px 까지 제각각이었고 글 시작 자리가
     세 가지(210 · 283 · 320)였습니다. 소희 님이 보신 그 모습입니다.

     그래서 auto margin 을 0 으로 눌러 stretch 가 살아나게 합니다.
     가족운 책(FAMILY-1)이 같은 탈을 겪고 똑같이 고쳤습니다 —
     그래서 두 책이 같은 자리에서 시작합니다.

     ★ 앞에 #ssb 를 꼭 붙입니다. WIDTH-7 이 `#ssb .page` 로 걸어서,
       전에 쓰던 `[data-ny%(Y)s="1"] > .page` 는 힘이 모자라 졌습니다.
       이것이 어떤 쪽은 제 규칙이, 어떤 쪽은 WIDTH-7 이 이기던 까닭입니다. */
  #ssb .book[data-ny%(Y)s="1"] > .page,
  #ssb [data-ny%(Y)s="1"] > .page{
    margin-left:0 !important; margin-right:0 !important;
    padding-left:0 !important; padding-right:0 !important;
    max-width:none !important; width:auto !important; }
  #ssb .book[data-ny%(Y)s="1"] > .page > *,
  #ssb [data-ny%(Y)s="1"] > .page > *{
    padding-left:0 !important; padding-right:0 !important;
    margin-left:0 !important; margin-right:0 !important;
    max-width:none !important; }
  /* 장 속표지는 가운데 정렬이라 위 못에서 빼 줍니다 */
  #ssb .book[data-ny%(Y)s="1"] > .page.divider > *,
  #ssb [data-ny%(Y)s="1"] > .page.divider > *{
    margin-left:auto !important; margin-right:auto !important; }
}
}
</style>
<script>
(function(){
  if(window.StellaNY%(Y)s){ return; }
  window.StellaNY%(Y)s = 1;

  var YEAR = %(Y)s;
  var YEAR_EL = '%(YE)s';
  /* 장 표지 얼굴 — 문(door-fortune)의 그 해 사진입니다 */
  var GUARDIAN = '미르';
  var DOORALT  = '%(Y)s년 운세';
  var DOORIMG  = 'https://i0.wp.com/stellasaju.com/wp-content/uploads/2026/09/STELLASAJU_FORTUNE-%(Y)s.jpg?resize=264%%2C264';
  var YEARNAME = %(YN)s;
  var LUCKNAME = %(LN)s;
  var TOPICS = ['%(Y)s년 운세', '%(Y)s년운세', '%(Y)s 운세'];

  function read(k){
    try{ var r=localStorage.getItem(k); if(!r){ return null; } return JSON.parse(r); }
    catch(e){ return null; }
  }
  function esc(s){
    return String(s===undefined?'':s).split('<').join('').split('>').join('');
  }
  function two(x){ return (x<10?'0':'')+x; }
  /* 이름이 비면 「님」까지 같이 걷어내고 「당신」으로 바꿉니다.
     — 그냥 비워두면 「님의 2026년 운세」가 되고,
       '손님' 을 넣으면 「손님님」이 됩니다. */
  /* 올해이름 · 대운이름 — build() 가 손님 무리를 셈한 뒤 채웁니다.
     2026-09-14 : 그전에는 아무도 안 채워서 손님 책에
     「{올해이름}」이 중괄호째로 찍혔습니다. */
  var YN = '', LN = '';
  function fill(s, nm){
    var t=String(s);
    if(!nm){ t = t.split('{이름}님').join('당신').split('{이름}').join('당신'); }
    else { t = t.split('{이름}').join(nm); }
    if(YN){ t = t.split('{올해이름}').join(YN); }
    if(LN){ t = t.split('{대운이름}').join(LN); }
    return t;
  }

  /* ── 손님을 무엇이라 부를까 ────────────────────────────
     2026-09-14 · 소희 님 : 「우린 이소희라고 안 부르고 소희님이라고
     부르기로 했어. 성까지 부르면 너무 딱딱해보여」
     그리고 : 「입력폼을 성 따로 이름 따로 넣기로 했었어」

     ★ 폼이 성·이름을 따로 주면 그것을 그대로 씁니다 — 추측이 없습니다.
       남궁민수도 Sohee Lee 도 폼이 갈라준 대로 부릅니다.
     ★ 아직 한 칸으로만 오는 폼(gName)도 있으니, 그때만 뒤로 물러나
       한글 세 글자 이상이면 성을 뗍니다.
     ── 폼이 쓸 수 있는 이름을 두루 봅니다 ───────────────── */
  function firstOf(pr){
    var K=['firstName','first_name','given','givenName','gFirst',
           'name1','nameFirst','이름'];
    var i, v;
    for(i=0;i<K.length;i++){
      v=pr[K[i]];
      if(v){ v=String(v).split(' ').join(''); if(v){ return v; } }
    }
    return '';
  }
  var SURNAME2=['남궁','선우','황보','제갈','사공','서문','독고','동방'];
  function cutSurname(v){
    var i;
    for(i=0;i<SURNAME2.length;i++){
      if(v.indexOf(SURNAME2[i])===0){
        if(v.length>=4){ return v.slice(2); }
        return v;
      }
    }
    if(v.length>=3){ return v.slice(1); }   /* 이소희 → 소희 */
    return v;                                /* 김솔 두 글자는 그대로 */
  }
  function isHangul(v){
    var i, c;
    for(i=0;i<v.length;i++){
      c=v.charCodeAt(i);
      if(c<44032){ return false; }
      if(c>55203){ return false; }
    }
    return v.length>0;
  }
  /* 한 칸 폼에 외국 이름이 오면 앞 토막만 씁니다 — Sohee Lee → Sohee */
  function headWord(v){
    var a=String(v).split(' '), i;
    for(i=0;i<a.length;i++){ if(a[i]){ return a[i]; } }
    return '';
  }
  function callName(pr){
    var f=firstOf(pr);
    if(f){ return f; }                       /* 폼이 갈라줬으면 그대로 */
    var raw=String(pr.name===undefined?'':pr.name);
    var v=raw.split(' ').join('');
    if(!v){ return ''; }                     /* 이름이 없으면 빈 채로 */
    if(!isHangul(v)){ return headWord(raw); }
    return cutSurname(v);
  }

  function isMine(tp){
    var i; for(i=0;i<TOPICS.length;i++){ if(tp===TOPICS[i]){ return true; } }
    return false;
  }

  /* ── 오행 · 십성 무리 (책의 groupOf 와 같은 셈) ──────── */
  var SAENG={'목':'화','화':'토','토':'금','금':'수','수':'목'};
  var GEUK ={'목':'토','토':'수','수':'화','화':'금','금':'목'};
  var GAN_EL_H={'甲':'목','乙':'목','丙':'화','丁':'화','戊':'토',
                '己':'토','庚':'금','辛':'금','壬':'수','癸':'수'};
  var GAN_EL_I=['목','목','화','화','토','토','금','금','수','수'];

  function groupOf(myEl, el){
    if(el===myEl){ return '비겁'; }
    if(SAENG[myEl]===el){ return '식상'; }
    if(GEUK[myEl]===el){ return '재성'; }
    if(GEUK[el]===myEl){ return '관성'; }
    if(SAENG[el]===myEl){ return '인성'; }
    return '';
  }

  /* 그 해에 걸린 대운 한 칸 — 책의 nowLuck 과 같습니다 */
  function nowLuck(chart){
    if(!chart.luck){ return null; }
    var list=chart.luck.list;
    if(!list){ return null; }
    var i, best=null;
    for(i=0;i<list.length;i++){ if(list[i].fromYear<=YEAR){ best=list[i]; } }
    if(best===null){ if(list.length){ best=list[0]; } }
    return best;
  }

  /* 그 해 오행이 사주에 얼마나 있나 — ② 1층 */
  function powerOf(chart){
    var m={'목':0,'화':0,'토':0,'금':0,'수':0}, i;
    if(chart.five){
      for(i=0;i<chart.five.length;i++){ m[chart.five[i].element]=chart.five[i].count; }
    }
    var n=m[YEAR_EL]||0;
    if(n>=3){ return 'much'; }
    if(n<=1){ return 'few'; }
    return 'even';
  }

  var FIVE=['비겁','식상','재성','관성','인성'];
  function nextOf(x){ return FIVE[(FIVE.indexOf(x)+1)%%5]; }
  function relOf(x, d){
    var k=(FIVE.indexOf(d)-FIVE.indexOf(x)+5)%%5;
    return ['겹침','빠져나감','부딪힘','어긋남','받쳐줌'][k];
  }

  var NY = '''

TAIL = u''';

  /* ── 책 그리기 ──────────────────────────────────────── */
  function build(){
    var S=window.StellaSaju, R=window.StellaRead;
    if(!S){ return null; }
    if(!R){ return null; }
    var o=read('stella_demo');
    if(!o){ return null; }
    var pr=o.profile||o;
    if(!pr.year){ return null; }

    var loc=S.locate(pr.city, pr.country);
    var chart=S.compute({ year:pr.year, month:pr.month, day:pr.day,
      hour:pr.hour, minute:pr.minute||0, sex:pr.sex,
      lon:loc.lon, lat:loc.lat, tz:loc.tz });

    /* 일간 오행 */
    var dayHan='';
    try{ dayHan=String(chart.pillars.day.han).charAt(0); }catch(e){}
    var myEl=GAN_EL_H[dayHan];
    if(!myEl){ return null; }

    /* 무리 = 일간이 그 해 천간을 만나 무엇이 되나 */
    var SP=groupOf(myEl, YEAR_EL);
    if(!SP){ return null; }

    /* 대운 = 일간이 지금 대운 천간을 만나 무엇이 되나 */
    var lk=nowLuck(chart);
    var DAE='';
    if(lk){
      var lel=GAN_EL_I[lk.gan];
      if(!lel){ lel=GAN_EL_H[String(lk.han||'').charAt(0)]; }
      if(lel){ DAE=groupOf(myEl, lel); }
    }
    if(!DAE){ DAE=SP; }

    var WANT={ move:SP, dae:DAE, power:powerOf(chart), rel:relOf(SP, DAE) };
    YN = YEARNAME[SP] || '';
    LN = LUCKNAME[DAE] || '';
    var nm=esc(callName(pr));

    var pages=[], n=0;
    function page(html, part){
      n++;
      var attr=part?' data-part="'+part+'"':'';
      pages.push('<div class="page"'+attr+'>'+html+
                 '<div class="folio">'+two(n)+'</div></div>');
    }

    /* ── 장 속표지 ────────────────────────────────────────
       2026-09-14 · 소희 님 : 「다른 카테고리처럼 문 사진에 건강운 사진
       넣고 제1장 0000 이렇게만 넣는 장이야. 템플릿 있을거야」
       있었습니다 — patch160_divider 가 만들고 patch160_dvbig 이 키운
       그 틀입니다. 클래스 이름을 그대로 쓰면 책에 이미 있는 CSS 가
       그대로 먹습니다. 새 CSS 를 만들지 않는 까닭입니다.
         .dvmark > img   얼굴 (132px 동그라미)
         .dvwho          가디언 이름
         .dvno dvch      제 N 장   ← 이 쪽이 있는 이유. 제일 큽니다
         h2              장 제목
         .dvrule         밑줄
       소희 님이 「제1장 0000 이렇게만」이라 하셔서 설명(.dvwhat)은
       넣지 않습니다. */
    function sheet(no, title, part){
      n++;
      var attr=part?' data-part="'+part+'"':'';
      return '<div class="page divider"'+attr+'>'+
             '<div class="dvmark dvface"><img loading="lazy" decoding="async" '+
             'alt="'+DOORALT+'" src="'+DOORIMG+'"></div>'+
             '<p class="dvwho">'+GUARDIAN+'</p>'+
             '<p class="dvno dvch">'+no+'</p>'+
             '<h2>'+title+'</h2>'+
             '<div class="dvrule"></div>'+
             '<div class="folio">'+two(n)+'</div></div>';
    }
    function bare(t){
      var v=String(t);
      while(v.length){
        var c=v.charCodeAt(0);
        if(c>=9312){ if(c<=9331){ v=v.slice(1); continue; } }
        if(c===32){ v=v.slice(1); continue; }
        break;
      }
      return v;
    }

    var NOS=['01','02','03','04','05','06','07','08','09','10'];
    var MARK=['제 1 장','제 2 장','제 3 장','제 4 장','제 5 장',
              '제 6 장','제 7 장','제 8 장','제 9 장','제 10 장'];
    var i, j, blocks, b, html, tt;

    for(i=0;i<NOS.length;i++){
      blocks=NY[NOS[i]];
      if(!blocks){ continue; }
      /* 장 표지 한 쪽을 먼저 놓습니다 */
      var ct='';
      for(j=0;j<blocks.length;j++){
        if(blocks[j].kind==='title'){ ct=bare(blocks[j].t); break; }
      }
      var hadSheet=false;
      if(ct){ pages.push(sheet(MARK[i], fill(ct, nm), (i<4?'one':'two'))); hadSheet=true; }
      html='';
      for(j=0;j<blocks.length;j++){
        b=blocks[j];
        if(b.kind==='title'){
          /* 원고에 붙은 ①②③ 은 제가 쓰기 좋으라고 단 번호입니다.
             책에는 「제 1 장」 딱지가 따로 있으니 뗍니다. */
          tt=String(b.t);
          while(tt.length){
            var c0=tt.charCodeAt(0);
            if(c0>=9312){ if(c0<=9331){ tt=tt.slice(1); continue; } }
            if(c0===32){ tt=tt.slice(1); continue; }
            break;
          }
          /* 장 속표지를 바로 앞에 놓았으면 같은 제목을 또 쓰지 않습니다.
             2026-09-14 · ?leadwhy=1 차례에 제목이 두 번씩 찍혀 드러났습니다
             (1. 올해나는어떤해를보내는가 / 2. 올해나는어떤해를보내는가).
             속표지에 큰 글씨로 이미 있으니 본문은 머리글부터 시작합니다. */
          if(hadSheet){ html+=fill(b.h, nm); continue; }
          html+='<h2>'+fill(tt, nm)+'</h2>'+fill(b.h, nm);
          continue;
        }
        if(b.kind==='always'){
          tt=b.t?('<h3>'+fill(b.t, nm)+'</h3>'):'';
          html+=tt+fill(b.h, nm);
          continue;
        }
        if(b.kind==='group'){
          if(b.key!==SP){ continue; }
          tt=b.t?('<h3>'+fill(b.t, nm)+'</h3>'):'';
          html+=tt+fill(b.h, nm);
          continue;
        }
        if(b.kind==='branch'){
          if(b.group!==SP){ continue; }
          if(b.key!==DAE){ continue; }
          tt=b.t?('<h3>'+fill(b.t, nm)+'</h3>'):'';
          html+=tt+fill(b.h, nm);
          continue;
        }
        if(b.kind==='pick'){
          if(WANT[b.axis]!==b.key){ continue; }
          tt=b.t?('<h3>'+fill(b.t, nm)+'</h3>'):'';
          html+=tt+fill(b.h, nm);
          continue;
        }
      }
      page(html, (i<4?'one':'two'));
    }

    if(n===0){ return null; }
    return { html:pages.join(''), n:n,
             title:(nm?nm+'님의 ':'당신의 ')+YEAR+'년 운세',
             sp:SP, dae:DAE };
  }

  window.StellaNY={ build:build, has:isMine, year:YEAR };

  var tries=0;
  function go(){
    tries++;
    try{
      var bk=document.getElementById('bkBook');
      if(bk){
        if(bk.getAttribute('data-ny'+YEAR)!=='1'){
          var o=read('stella_demo');
          if(o){
            if(isMine(String(o.topic===undefined?'':o.topic))){
              if(String(bk.innerHTML).length>200){
                var r=build();
                if(r){
                  bk.innerHTML=r.html;
                  bk.setAttribute('data-ny'+YEAR,'1');
                  var t=document.getElementById('bkTitle');
                  if(t){ t.textContent=r.title; }
                  var c=document.getElementById('bkN');
                  if(c){ c.textContent=r.n+'쪽'; }
                  return;
                }
              }
            } else { return; }
          }
        } else { return; }
      }
    }catch(e){}
    if(tries>40){ return; }
    setTimeout(go, 300);
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', go);
  } else {
    go();
  }

})();
</script>
	<?php
}, 3 );
'''

_YN, _LN = year_luck_names(json.loads(NY))
print('  올해이름 %d · 대운이름 %d 개를 원고에서 뽑았습니다' % (len(_YN), len(_LN)))


def _jstable(d):
    """홑따옴표 JS 표 — 쌍따옴표를 안 써서 역빗금이 안 생깁니다."""
    return '{' + ', '.join("'%s':'%s'" % (k, v) for k, v in sorted(d.items())) + '}'


head = HEAD % {'Y': YEAR, 'YE': YEAR_EL, 'YG': YEAR_GAN,
               'YN': _jstable(_YN), 'LN': _jstable(_LN)}
out = head + NY + TAIL
path = os.path.join(HERE, '..', 'php', 'patch160_ny%s.WPCODE.txt' % YEAR)
io.open(path, 'w', encoding='utf-8').write(out)
print('썼습니다 %s' % os.path.normpath(path))
print('  바이트 %d · 글자 %d' % (len(out.encode('utf-8')), len(out)))
print('  앰퍼샌드 %d (0 이어야 합니다)' % out.count('&'))
