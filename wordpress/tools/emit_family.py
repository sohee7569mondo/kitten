# -*- coding: utf-8 -*-
import io, json
F = io.open('F.json', encoding='utf-8').read()

HEAD = u'''/* ══════════════════════════════════════════════════════════
   가족운 — 열 장짜리 별도 구조 책
                                        ★ 2026-09-13 · 소희 님께
                                        판 FAMILY-1

   지금 가족운을 고르면 무엇이 나오나 —
     제목만 「가족운에 대해」이고, 말상자는 아람의 건강 말상자가
     나옵니다. 「몸은 거짓말을 하지 않습니다 … 아픈 곳은 반드시
     병원에서 확인하세요」. 장 안내도 「타로 세 장으로 여섯 달을」
     이라는 문 단위 일반판입니다.
     까닭 — 책에 가족운용 여는 글·말상자·열 장이 없어서 문(아람)
     기본값으로 떨어집니다.

   ── 앵커를 안 잡습니다 ────────────────────────────────
   쪽 글을 한 글자도 안 바꿉니다. 책이 다 그려진 뒤, 주제가
   가족운이면 책 그릇의 내용을 우리 열 장으로 갈아끼웁니다.
   그래서 「0군데」가 날 일이 없습니다.
   되돌리기도 없습니다 — 스니펫을 끄면 원래대로입니다.

   ── 무엇이 바뀌나 ─────────────────────────────────────
   여는 글 말상자   아람의 건강 말상자 → 가족운 말상자
   장 안내          타로·별자리 일반판 → 가족운 열 장 안내
   1부 렌즈         「비견 · 혼자 버티는 몸」 열 개
                    → 「비견 · 나란히 서는 사람」 열 개
   본문             가족운 ① ~ ⑩

   ── 장마다 무엇으로 갈리나 ────────────────────────────
   ①  십성 무리 으뜸        비겁 / 식상 / 재성 / 관성 / 인성
   ②  인성의 두께           넉넉 / 안정 / 약함
   ③  비겁의 두께           넉넉 / 식상·재성이 셀 때 / 약함
   ④  식상의 두께           넉넉 / 약함
   ⑤  주는 힘과 받는 힘      식상+재성  대  인성+비겁
   ⑥  가장 얇은 무리        인성 얇음 → 부모 자리 / 비겁 얇음 → 형제 /
                           식상 얇음 → 자녀 / 셋 다 있으면 「없을 때」
   ⑦  두 번째로 많은 무리    인성 → 부모 / 식상 → 자녀 / 비겁 → 형제 /
                           그 밖 → 「크게 움직이지 않는 때」
   ⑧ ⑨ ⑩                  갈리지 않습니다. 전부 늘 붙습니다.

   ★ ⑥ ⑦ 의 셈은 이 판에서 십성 무리만 씁니다. 다음 판에서 월지·시지의
     충·형과 대운을 넣어 더 정확하게 하겠습니다. 지금도 ① 과 겹치지
     않게 짜 두었습니다 — ① 은 가장 많은 것, ⑥ 은 가장 얇은 것,
     ⑦ 은 두 번째로 많은 것을 봅니다.

   ── 셈은 전부 책에 이미 있는 것을 씁니다 ──────────────
       window.StellaSaju.locate / compute      원국
       window.StellaRead.interpret             풀이
       it.groups                               십성 다섯 무리
       chart.five                              오행 분포

   ── 붙이는 법 ─────────────────────────────────────────
   ★ 새 조각입니다. WPCode -> 새 스니펫 -> PHP Snippet -> 저장 -> Active
   ★ 위치(Location)를 「어디서나 실행 / Run Everywhere」로.
   ★ 크롬 번역을 끄고 붙여넣으세요.

   넣으신 뒤 door-health 에서 가족운을 골라 책을 뽑아보세요.
   안 나오면 ?gwhy=1 로 까닭을 보실 수 있습니다.

   ── 검사한 것 ─────────────────────────────────────────
   php -l           문법
   앰퍼샌드 세기       0 이어야 합니다
   node --check     스크립트 문법
   node 로 열 장을 실제로 그려봄
   ══════════════════════════════════════════════════════════ */

add_action( 'wp_head', function () {
	?>
<style>
#ssb .keepline{ font-weight:600; }
#ssb .hmark{ font-family:IBM Plex Mono,monospace; font-size:.62rem; letter-spacing:.18em;
  color:#9E2B50; margin:0 0 6px; }
#ssb .hcount{ font-family:IBM Plex Mono,monospace; font-size:.72rem; letter-spacing:.06em;
  color:#7a7a8c; margin:-6px 0 10px; }
#ssb .mini{ font-size:.86rem; color:#6a6a78; }

/* ── 쪽 폭 울타리 ──────────────────────────────────────────
   소희 님 : 「가족운 책 폭이 이상해. 이것만 그런가봐, 다른건 괜찮아」
   책의 화면 CSS 는 쪽 좌우 여백을 0 으로 둡니다
   (@media screen 안에서 padding:46px 0 6px).
   그런데 살아 있는 쪽에서 어떤 규칙이 우리 쪽만 밀어 넣고 있었습니다.
   그래서 우리가 갈아끼운 책 안에서만 좌우를 0 으로 못 박습니다.
   data-family 가 붙은 책에만 걸리므로 다른 책은 안 건드립니다. */
@media screen{
  #ssb .book[data-family="1"] > .page{
    padding-left:0 !important; padding-right:0 !important;
    margin-left:0 !important; margin-right:0 !important;
    max-width:none !important; width:auto !important;
  }
  #ssb .book[data-family="1"] > .page > *{
    margin-left:0 !important; margin-right:0 !important;
    padding-left:0 !important; padding-right:0 !important;
  }
  #ssb .book[data-family="1"] > .page > h2,
  #ssb .book[data-family="1"] > .page > h3,
  #ssb .book[data-family="1"] > .page > p{ text-align:left; }
}
</style>
<script>
/* ═══ 가족운 열 장 (FAMILY-1) ═══
   글은 소희 님 원고 그대로입니다. 쪽은 안 건드립니다. */
(function(){

  if(window.StellaFamily){ return; }

  var AMP=String.fromCharCode(38);
  function esc(s){
    s=String(s===undefined?'':s);
    s=s.split(AMP).join(AMP+'amp;');
    s=s.split('<').join(AMP+'lt;');
    s=s.split('>').join(AMP+'gt;');
    return s;
  }
  function read(k){
    try{ var v=localStorage.getItem(k); return v?JSON.parse(v):null; }catch(e){ return null; }
  }
  function two(x){ return (x<10?'0':'')+x; }
  function fill(s, nm){ return String(s).split('{이름}').join(nm); }

  var TOPICS=['가족운','가족'];
  function isMine(tp){
    var i; for(i=0;i<TOPICS.length;i++){ if(tp===TOPICS[i]){ return true; } }
    return false;
  }

  var F = '''

TAIL = u''';

  var GK=['비겁','식상','재성','관성','인성'];

  /* ── 갈림 고르기 ────────────────────────────────────── */
  function pickKey(no, g){
    var bi=g['비겁']||0, sik=g['식상']||0, jae=g['재성']||0,
        gwan=g['관성']||0, inn=g['인성']||0;

    if(no==='01'){
      var top=GK[0], tn=-1, i;
      for(i=0;i<GK.length;i++){ if((g[GK[i]]||0)>tn){ tn=(g[GK[i]]||0); top=GK[i]; } }
      return top;
    }
    if(no==='02'){
      if(inn>=3){ return 'much'; }
      if(inn>=1){ return 'mid'; }
      return 'thin';
    }
    if(no==='03'){
      /* 나란히 / 챙기는 쪽 / 각자의 삶 — 셋이 고르게 갈리도록 */
      if(bi>=3){ return 'much'; }
      if(sik+jae>=bi+3){ return 'mid'; }
      if(bi<=1){ return 'thin'; }
      return 'much';
    }
    if(no==='04'){
      if(sik>=2){ return 'much'; }
      return 'thin';
    }
    if(no==='05'){
      var give=sik+jae, take=inn+bi;
      if(give>take+1){ return 'give'; }
      if(take>give+1){ return 'take'; }
      return 'even';
    }
    if(no==='06'){
      /* 가장 얇은 무리에서 걸립니다 */
      var lo=99, which='';
      if(inn<lo){ lo=inn; which='parent'; }
      if(bi<lo){ lo=bi; which='sib'; }
      if(sik<lo){ lo=sik; which='child'; }
      if(lo>=2){ return 'none'; }
      return which;
    }
    if(no==='07'){
      /* 두 번째로 많은 무리 — ① 과 겹치지 않게 */
      var rank=GK.slice().sort(function(a,b){ return (g[b]||0)-(g[a]||0); });
      var second=rank[1];
      if(second==='인성'){ return 'parent'; }
      if(second==='식상'){ return 'child'; }
      if(second==='비겁'){ return 'sib'; }
      return 'none';
    }
    return '';
  }

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
    var it=R.interpret(chart);
    var g=it.groups||{};

    var nm=esc(pr.name||'손님');

    var pages=[], n=0;
    function page(html, kind, part){
      n++;
      var cls='page'+(kind?' '+kind:'');
      var attr=part?' data-part="'+part+'"':'';
      var folio=(kind==='cover')?'':'<div class="folio">'+two(n)+'</div>';
      pages.push('<div class="'+cls+'"'+attr+'>'+html+folio+'</div>');
    }
    function head(no, title){
      return '<p class="hmark">'+no+'</p><h2>'+title+'</h2>';
    }

    /* ── 표지 ── */
    page('<div class="mark">STELLA SAJU</div>'+
         '<h1>'+nm+'님의<br>가족운</h1>'+
         '<p class="dek">아람이 여덟 글자를 가족의 자리로 읽습니다</p>', 'cover');

    /* ── 여는 글 ── */
    page('<p class="eyebrow">여는 글</p>'+
         '<h2>가족운에 대해 <span class="byline">— 아람</span></h2>'+
         '<div class="voice"><div class="who">아람</div>'+
         fill(F.open.voice, nm)+'</div>'+
         fill(F.open.guide, nm), null, 'one');

    /* ── 1부 렌즈 · 십성 ── */
    var lensHtml='<p>여덟 글자를 가족의 자리로 읽으면 이렇게 보입니다.</p>';
    var rank=GK.slice();
    var ORDER=['비견','겁재','식신','상관','편재','정재','정관','편관','정인','편인'];
    var cnt=it.count||{};
    var got=0, i2;
    var mine=ORDER.filter(function(k){ return (cnt[k]||0)>0; });
    mine.sort(function(a,b){ return (cnt[b]||0)-(cnt[a]||0); });
    for(i2=0;i2<mine.length;i2++){
      var one=F.lens[mine[i2]];
      if(!one){ continue; }
      got++;
      lensHtml+='<h3>'+one.h+' '+(cnt[mine[i2]]||0)+'</h3>'+fill(one.b, nm);
    }
    if(got===0){
      var k2;
      for(k2 in F.lens){
        if(F.lens.hasOwnProperty(k2)){
          lensHtml+='<h3>'+F.lens[k2].h+'</h3>'+fill(F.lens[k2].b, nm);
        }
      }
    }
    page(head('1 부','여덟 글자가 말하는 '+nm+'님의 자리')+lensHtml, null, 'one');

    /* ── 열 장 ── */
    var NOS=['01','02','03','04','05','06','07','08','09','10'];
    var MARK=['제 1 장','제 2 장','제 3 장','제 4 장','제 5 장',
              '제 6 장','제 7 장','제 8 장','제 9 장','제 10 장'];
    var i3;
    for(i3=0;i3<NOS.length;i3++){
      var no=NOS[i3], e=F.book[no];
      if(!e){ continue; }
      var h=fill(e.lead, nm);
      if(e.branch){
        var key=pickKey(no, g);
        var b=e.branch[key];
        if(!b){
          var kk;
          for(kk in e.branch){ if(e.branch.hasOwnProperty(kk)){ if(!b){ b=e.branch[kk]; } } }
        }
        if(b){ h+='<h3>'+b.h+'</h3>'+fill(b.b, nm); }
      }
      var j;
      for(j=0;j<e.always.length;j++){
        var a=e.always[j];
        var ah=String(a.h).split('★ ').join('');
        h+='<h3>'+ah+'</h3>'+fill(a.b, nm);
      }
      page(head(MARK[i3], e.t2)+h,
           null, (i3<4?'one':'two'));
    }

    return { html:pages.join(''), n:n,
             title:nm+'님의 가족운' };
  }

  window.StellaFamily={ build:build, has:isMine };

  var tries=0;
  function go(){
    tries++;
    try{
      var bk=document.getElementById('bkBook');
      if(bk){
        if(bk.getAttribute('data-family')!=='1'){
          var o=read('stella_demo');
          if(o){
            if(isMine(String(o.topic===undefined?'':o.topic))){
              if(String(bk.innerHTML).length>200){
                var r=build();
                if(r){
                  bk.innerHTML=r.html;
                  bk.setAttribute('data-family','1');
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

out = HEAD + F + TAIL
io.open('/home/user/kitten/wordpress/php/patch160_family.WPCODE.txt','w',encoding='utf-8').write(out)
print('바이트', len(out.encode('utf-8')))
print('앰퍼샌드', out.count('&'))
print('쌍따옴표 in 표', F.count('"') - F.count('\\"'))
