# -*- coding: utf-8 -*-
"""NY<해>.json -> WPCode 조각 (신년운세 책 갈아끼우기)

    python3 emit_newyear.py 2026
    python3 emit_newyear.py 2027
"""
import io, json, sys, os

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

/* ── 쪽 폭 울타리 — 우리 책에만 걸립니다 ──────────────────
   ★ 깃발이 .book 에 달릴 수도, #bkBook 에만 달릴 수도 있어 둘 다 겁니다.
     2026-09-14 · 책이 왼쪽으로 쏠려 글이 잘렸습니다. 살아 있는 쪽에
     제 사본에 없는 여백 규칙이 얹혀 있어서입니다. */
@media screen{
  [data-ny%(Y)s="1"]{
    margin-left:auto !important; margin-right:auto !important;
    padding-left:20px !important; padding-right:20px !important;
    max-width:760px !important; width:auto !important;
    box-sizing:border-box !important; }
  [data-ny%(Y)s="1"] > .page{
    padding-left:0 !important; padding-right:0 !important;
    margin-left:0 !important; margin-right:0 !important;
    max-width:none !important; width:auto !important; }
  [data-ny%(Y)s="1"] > .page > *{
    padding-left:0 !important; padding-right:0 !important;
    margin-left:0 !important; margin-right:0 !important;
    max-width:none !important; }
}
@media(max-width:820px){
  [data-ny%(Y)s="1"]{ padding-left:16px !important; padding-right:16px !important; }
}
</style>
<script>
(function(){
  if(window.StellaNY%(Y)s){ return; }
  window.StellaNY%(Y)s = 1;

  var YEAR = %(Y)s;
  var YEAR_EL = '%(YE)s';
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
  function fill(s, nm){
    var t=String(s);
    if(!nm){ return t.split('{이름}님').join('당신').split('{이름}').join('당신'); }
    return t.split('{이름}').join(nm);
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
    var nm=esc(callName(pr));

    var pages=[], n=0;
    function page(html, part){
      n++;
      var attr=part?' data-part="'+part+'"':'';
      pages.push('<div class="page"'+attr+'>'+html+
                 '<div class="folio">'+two(n)+'</div></div>');
    }

    var NOS=['01','02','03','04','05','06','07','08','09','10'];
    var MARK=['제 1 장','제 2 장','제 3 장','제 4 장','제 5 장',
              '제 6 장','제 7 장','제 8 장','제 9 장','제 10 장'];
    var i, j, blocks, b, html, tt;

    for(i=0;i<NOS.length;i++){
      blocks=NY[NOS[i]];
      if(!blocks){ continue; }
      html='<p class="nymark">'+MARK[i]+'</p>';
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

head = HEAD % {'Y': YEAR, 'YE': YEAR_EL, 'YG': YEAR_GAN}
out = head + NY + TAIL
path = os.path.join(HERE, '..', 'php', 'patch160_ny%s.WPCODE.txt' % YEAR)
io.open(path, 'w', encoding='utf-8').write(out)
print('썼습니다 %s' % os.path.normpath(path))
print('  바이트 %d · 글자 %d' % (len(out.encode('utf-8')), len(out)))
print('  앰퍼샌드 %d (0 이어야 합니다)' % out.count('&'))
