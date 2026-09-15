;

  /* ── 빈칸 채우기 ────────────────────────────────────── */
  var FILLV = {};
  function fill(s, nm){
    var t=String(s), k;
    if(!nm){ t = t.split('{이름}님').join('당신').split('{이름}').join('당신'); }
    else { t = t.split('{이름}').join(nm); }
    for(k in FILLV){ t = t.split('{'+k+'}').join(FILLV[k]); }
    t = t.split('{연도}').join(String(YEAR));
    t = t.split('{간지}').join(GANJI);
    return t;
  }

  /* ── 카드 세 장 ────────────────────────────────────────
     카드 풀이 글은 책이 이미 갖고 있습니다 — window.StellaTarot
     78장 × now·over·then, 그리고 StellaRev 의 뒤집힘 22장.
     자리 뜻이 삼재와 그대로 맞아 이름만 바꿔 읽습니다.
       now  지금 서 있는 자리 → 첫째 문 · 들어오는 문
       over 넘어야 할 것      → 둘째 문 · 머무는 문
       then 그 너머           → 셋째 문 · 나가는 문
     뒤집힘 판정은 door-tarot 과 같은 셈입니다 — 난수가 아니라
     생년월일시 + 오늘 날짜라 카드 쪽과 같은 모양이 나옵니다. */
  function cardBlock(pr, nm, slot, blocks){
    var T=window.StellaTarot;
    if(!T){ return ''; }
    var pick=read('stella_cards');
    if(!(pick instanceof Array)){ return ''; }
    if(pick.length<3){ return ''; }

    var REV = window.StellaRev ? window.StellaRev : {};
    function numOf(x){ if(typeof x==='number'){ return x; } return 0; }
    var d=new Date();
    var v=numOf(pr.year)*10007 + numOf(pr.month)*331 + numOf(pr.day)*97
        + numOf(pr.hour)*13 + numOf(pr.minute)*7
        + d.getFullYear()*1103 + (d.getMonth()+1)*37 + d.getDate()*3 + 29;
    var SEED=v % 2147483647;
    if(SEED<=0){ SEED+=2147483646; }
    function flip(ci, nth){
      if(Number(ci)>21){ return false; }
      var q=(SEED + (Number(ci)+1)*911 + (nth+1)*577) % 100;
      if(q<32){ return true; }
      return false;
    }
    var RVS=[], z;
    for(z=0;z<3;z++){ RVS.push(flip(pick[z], z)); }
    function sayOf(c, rv, key){
      if(rv){
        var r=REV[c.n];
        if(r){ if(r[key]){ return r[key]; } }
      }
      return c[key];
    }

    var SEAT=[['첫째 문','들어오는 문','now'],
              ['둘째 문','머무는 문','over'],
              ['셋째 문','나가는 문','then']];
    var BIG={'in':0, 'stay':1, 'out':2};
    var big = BIG[slot];
    if(big===undefined){ big=-1; }
    var UP='https://stellasaju.com/wp-content/uploads/2026/08/';

    var h='', i, c, no;
    /* 세 장을 나란히 */
    h+='<div style="display:flex;gap:12px;justify-content:center;'+
       'margin:24px 0 10px;flex-wrap:wrap">';
    for(i=0;i<3;i++){
      c=T[pick[i]];
      if(!c){ continue; }
      no=('00'+(Number(pick[i])+1));
      no=no.slice(no.length-3);
      h+='<figure style="flex:1 1 28%;max-width:190px;min-width:120px;'+
         'margin:0;text-align:center'+(i===big?';outline:2px solid #9E2B50;'+
         'outline-offset:6px;border-radius:10px':'')+'">'+
         '<img decoding="async" loading="lazy" alt="'+esc(c.ko)+'" '+
         'src="'+UP+'st'+no+'.jpg" '+
         'style="width:100%;display:block;border-radius:8px;'+
         'border:1px solid rgba(212,175,106,.35)'+
         (RVS[i] ? ';transform:rotate(180deg)' : '')+'">'+
         '<figcaption style="margin-top:9px;font-size:.78rem;line-height:1.6;'+
         'opacity:'+(i===big?'1':'.72')+'">'+SEAT[i][0]+' · '+SEAT[i][1]+
         '<br><b style="font-size:.92rem">'+esc(c.ko)+'</b>'+
         (RVS[i] ? '<br><span style="opacity:.8">뒤집혀 나왔습니다</span>' : '')+
         '</figcaption></figure>';
    }
    h+='</div>';

    /* 지금 서 계신 문 — 원고에서 그 자리 글을 가져옵니다 */
    var want=cellSlot(slot), j, b;
    for(j=0;j<blocks.length;j++){
      b=blocks[j];
      if(b.kind!=='cardslot'){ continue; }
      if(b.slot!==want){ continue; }
      h+=fill(b.h, nm);
    }

    /* 문마다 풀이 */
    for(i=0;i<3;i++){
      c=T[pick[i]];
      if(!c){ continue; }
      h+='<h3>'+SEAT[i][0]+' · '+SEAT[i][1]+' — 「'+esc(c.ko)+'」'+
         (RVS[i] ? ' <em>뒤집힘</em>' : '')+'</h3>';
      h+='<p>'+esc(sayOf(c, RVS[i], SEAT[i][2]))+'</p>';
    }

    /* 세 장을 겹쳐 놓으면 — 세 잣대 */
    function valOf(ci){
      var k=Number(ci);
      if(k<=21){ return k; }
      var cc=T[k];
      if(cc){ if(cc.spd){ return Number(cc.spd); } }
      return 11;
    }
    var maj=0, vs=[], q;
    for(q=0;q<3;q++){
      if(Number(pick[q])<=21){ maj++; }
      vs.push(valOf(pick[q]));
    }
    var rvn=0;
    for(q=0;q<3;q++){ if(RVS[q]){ rvn++; } }
    var gap=vs[2]-vs[0];
    var WANT={};
    WANT.major = (maj===0) ? 'none' : (maj===1 ? 'one' : 'many');
    WANT.trend = (gap>=5) ? 'up' : (gap<=-5 ? 'down' : 'flat');
    WANT.rev   = (rvn===0) ? 'none' : (rvn===1 ? 'one' : 'many');

    h+='<h3>세 장을 겹쳐 놓으면</h3>';
    for(j=0;j<blocks.length;j++){
      b=blocks[j];
      if(b.kind!=='gauge'){ continue; }
      if(WANT[b.axis]!==b.key){ continue; }
      h+=fill(b.h, nm);
    }
    return h;
  }

  /* ── 책 그리기 ──────────────────────────────────────── */
  function build(){
    var S=window.StellaSaju;
    if(!S){ return null; }
    var o=read('stella_demo');
    if(!o){ return null; }
    var pr=o.profile||o;
    if(!pr.year){ return null; }

    var loc=S.locate(pr.city, pr.country);
    var chart=S.compute({ year:pr.year, month:pr.month, day:pr.day,
      hour:pr.hour, minute:pr.minute||0, sex:pr.sex,
      lon:loc.lon, lat:loc.lat, tz:loc.tz });

    var dayHan='';
    try{ dayHan=String(chart.pillars.day.han).charAt(0); }catch(e){}
    var myEl=GAN_EL_H[dayHan];
    if(!myEl){ return null; }
    var SP=groupOf(myEl, YEAR_EL);
    if(!SP){ return null; }

    var first=samjaeFirst(pr.year, YEAR);
    var slot=slotOf(first, YEAR);
    var cs=cellSlot(slot);

    FILLV={};
    FILLV['삼재전']=String(first-1);
    FILLV['들삼재']=String(first);
    FILLV['눌삼재']=String(first+1);
    FILLV['날삼재']=String(first+2);
    FILLV['삼재후']=String(first+3);

    var nm=callName(pr);
    var doc=SJ, blocks=doc.blocks;
    var pages=[], html='', i, b;

    function page(h){
      if(!h){ return; }
      pages.push('<section class="page"><div class="folio"></div>'+h+'</section>');
    }

    /* ── 장 속표지 ────────────────────────────────────────
       2026-09-15 · 소희 님 「삼재 들어가니 표지가 없어 숫자가 없어지고
       제4장이라고 들어가야 하는거 같은데」

       삼재 책에는 장 속표지가 아예 없었습니다. 제목에 붙은 ①②③ 이
       본문 머리에 그대로 찍히고 있었습니다.
       신년운세·가족운과 **같은 클래스 이름**을 씁니다. 그러면 책에
       이미 있는 CSS 가 그대로 먹습니다 — 새 CSS 를 안 만드는 까닭입니다.
         .dvmark > img   얼굴 (132px 동그라미)
         .dvwho          가디언 이름
         .dvno dvch      제 N 장   ← 제일 큽니다
         h2              장 제목
         .dvrule         밑줄 */
    var MARK=['제 1 장','제 2 장','제 3 장','제 4 장','제 5 장',
              '제 6 장','제 7 장','제 8 장','제 9 장','제 10 장'];
    var GUARDIAN='미르';
    var DOORALT='삼재';
    /* ★★ i0.wp.com(젯팩 사진 가속기)을 거치지 않습니다 — 2026-09-15
       소희 님 「중간에 중간에 사진없음」. 파일은 미디어에 다 있는데
       i0.wp.com 주소로는 안 떴습니다. 사이트 주소를 곧장 씁니다.
       크기는 CSS(.dvmark img)가 잡으므로 resize 도 필요 없습니다. */
    /* ★ 삼재는 제 그림이 따로 있습니다 — STELLASAJU_samjae.jpg
       (신년운세 그림을 빌려 쓰고 있었습니다) */
    var DOORIMG='https://stellasaju.com/wp-content/uploads/2026/09/STELLASAJU_samjae.jpg';
    var mark=0;
    var TOC=[];          /* 목차에 쓸 장 이름을 여기 모읍니다 */

    function sheet(title){
      var no=MARK[mark] ? MARK[mark] : '';
      mark++;
      TOC.push([no, title]);
      pages.push('<section class="page divider">'+
        '<div class="dvmark dvface"><img loading="lazy" decoding="async" '+
        'alt="'+DOORALT+'" src="'+DOORIMG+'"></div>'+
        '<p class="dvwho">'+GUARDIAN+'</p>'+
        '<p class="dvno dvch">'+no+'</p>'+
        '<h2>'+title+'</h2>'+
        '<div class="dvrule"></div>'+
        '<div class="folio"></div></section>');
    }

    /* 제목 앞에 붙은 ①②③ 은 제가 쓰기 좋으라고 단 번호입니다.
       책에는 「제 N 장」 딱지가 따로 있으니 뗍니다. */
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
    /* <h2 class='sjh2'>④ 제목</h2> 에서 제목만 꺼냅니다 */
    function h2text(h){
      var v=String(h);
      var a=v.indexOf('>');
      if(a<0){ return ''; }
      var z=v.indexOf('<', a+1);
      if(z<0){ z=v.length; }
      return bare(v.slice(a+1, z));
    }

    for(i=0;i<blocks.length;i++){
      b=blocks[i];
      if(b.kind==='always'){
        if(String(b.h).indexOf('sjh2')>=0){
          page(html); html='';
          /* 제목은 속표지에 큰 글씨로 들어가므로 본문에는 안 넣습니다 */
          sheet(fill(h2text(b.h), nm));
          continue;
        }
        html+=fill(b.h, nm);
        continue;
      }
      if(b.kind==='slotlead'){
        if(b.slot!==cs){ continue; }
        html+=fill(b.h, nm);
        continue;
      }
      if(b.kind==='cell'){
        if(b.slot!==cs){ continue; }
        if(b.stem!==SP){ continue; }
        html+='<h3>'+fill(b.t, nm)+'</h3>'+fill(b.h, nm);
        continue;
      }
      /* cardslot · gauge 는 카드 대목에서 씁니다 */
    }
    page(html);

    /* ── 목차 ──────────────────────────────────────────
       2026-09-15 · 소희 님 「이거 보니 삼재에 목차페이지가 없어」
       장이 일곱이라 한눈에 보는 쪽이 있어야 합니다.
       ★ 장 이름은 속표지를 만들 때 모아 둔 것을 그대로 씁니다 —
         따로 적어두면 원고를 고칠 때 어긋납니다. */
    function tocPage(){
      if(!TOC.length){ return ''; }
      var h=['<section class="page sjtoc">',
             '<p class="sjtoc-lab">차례</p>',
             '<ol class="sjtoc-list">'], i;
      for(i=0;i<TOC.length;i++){
        h.push('<li><span class="sjtoc-no">'+TOC[i][0]+'</span>'+
               '<span class="sjtoc-t">'+TOC[i][1]+'</span></li>');
      }
      h.push('</ol><div class="folio"></div></section>');
      return h.join('');
    }

    /* ★ 카드 장 제목은 원고에 sjh2 로 이미 있습니다 (「카드 세 장 —
       삼재의 세 문」). 여기서 속표지를 또 놓으면 두 장이 됩니다. */
    var card=cardBlock(pr, nm, slot, blocks);
    if(card){ pages.push('<section class="page"><div class="folio"></div>'+card+'</section>'); }

    /* 목차를 맨 앞에 놓습니다 (겉표지는 그보다 더 앞에 붙습니다) */
    var toc=tocPage();
    if(toc){ pages.unshift(toc); }

    if(!pages.length){ return null; }
    return { html:pages.join(''), n:pages.length,
             title:(nm?nm+'님의 ':'당신의 ')+'삼재',
             slot:slot, sp:SP, first:first };
  }


  /* ── 겉표지 손보기 ──────────────────────────
     2026-09-15 · 소희 님 「아치문이 없어」

     ① 아치문(표지의 금빛 테두리)은 patch160_cover 가 쪽에 심어둔
        CSS 가 그립니다. 그 CSS 는 `.page[data-part="cover"]` 에
        걸려 있습니다. 살려온 표지에 그 **속성**이 없으면 테두리가
        한 줄도 안 그려집니다 — 클래스(.cover)만으로는 안 걸립니다.
        그래서 옮길 때 속성을 반드시 붙여 줍니다.

     ② 부제(.sub)와 제목(h1)은 원본 책이 정합니다. 원본은 우리
        주제를 모르므로 엉뚱한 기본값을 찍습니다 (소희 님이 보신
        「THE ARCHITECT」 — 그것은 직업운 부제입니다).
        글자만 갈아 끼웁니다. 테두리와 자리는 그대로입니다. */
  var COVSUB='THE THREE YEARS';
  function fixCover(el, ttl){
    try{
      var e=el.cloneNode(true);
      e.setAttribute('data-part','cover');
      var cls=String(e.className===undefined?'':e.className);
      if(cls.indexOf('page')<0){ cls=cls+' page'; }
      if(cls.indexOf('cover')<0){ cls=cls+' cover'; }
      e.className=cls;
      var s=e.querySelector('.sub');
      if(s){ if(COVSUB){ s.textContent=COVSUB; } }
      var h=e.querySelector('h1');
      if(h){ if(ttl){
        var t=String(ttl), i=t.indexOf('님의 ');
        h.textContent='';
        if(i<0){ h.appendChild(document.createTextNode(t)); }
        else{
          h.appendChild(document.createTextNode(t.slice(0, i+2)));
          h.appendChild(document.createElement('br'));
          h.appendChild(document.createTextNode(t.slice(i+3)));
        }
      } }
      return e.outerHTML;
    }catch(err){ return el.outerHTML; }
  }

  window.StellaSamjae={ build:build, has:isMine, year:YEAR };

  /* ── 관리자 진단 띠 ──────────────────────────────────── */
  var LOG=[];
  function paint(){
    if(!ADMIN){ return; }
    try{
      var d=document.getElementById('sj-admin');
      if(!d){
        d=document.createElement('div');
        d.id='sj-admin';
        d.setAttribute('style','margin:12px;padding:10px 14px;'+
          'border:2px solid #2F7D4A;background:#F3F8F4;border-radius:8px;'+
          'font:13px/1.8 system-ui;color:#1d3a27;white-space:pre-wrap;');
        var ssb=document.getElementById('ssb');
        if(ssb){ if(ssb.parentNode){ ssb.parentNode.insertBefore(d, ssb); } }
        else { if(document.body){ document.body.appendChild(d); } }
      }
      d.textContent='관리자에게만 보입니다 · 삼재 판 '+STAMP+
        String.fromCharCode(10)+LOG.join(String.fromCharCode(10));
    }catch(e){}
  }
  function say(x){ LOG.push(x); paint(); }

  var SLOTNAME={'before':'들어오기 전','in':'들어오는 해','stay':'머무는 해',
                'out':'나가는 해','after':'나간 뒤','far':'삼재가 멀리 있는 때'};
  var tries=0;
  function go(){
    tries++;
    try{
      var bk=document.getElementById('bkBook');
      if(!bk){
        if(tries===1){ say('책 그릇(#bkBook)을 아직 못 찾음 — 기다립니다'); }
        if(tries>40){ say('★ 끝까지 책 그릇을 못 찾았습니다'); return; }
        setTimeout(go, 300); return;
      }
      if(bk.getAttribute('data-samjae')==='1'){ return; }

      /* ★★ 원본 책이 다 그려질 때까지 기다립니다 — 2026-09-15
         소희 님 「삼재에 속표지 붙었는제 제일 겉표지 안붙었어」

         까닭이 여기 있었습니다. 지금까지는 원본을 안 기다리고 바로
         갈아끼워서, 책이 아직 비어 있을 때 덮어버리면 **겉표지가
         통째로 사라졌습니다.** 겉표지는 우리가 짓는 것이 아니라
         원본 책이 짓는 것입니다 (.page.cover). */
      if(String(bk.innerHTML).length<=200){
        if(tries===1){ say('원본 책을 기다립니다'); }
        if(tries>40){ say('원본 책이 끝까지 안 그려졌습니다 — 겉표지 없이 갑니다'); }
        if(tries<=40){ setTimeout(go, 300); return; }
      }

      var o=read('stella_demo');
      if(!o){
        if(tries===1){ say('주문(stella_demo)이 아직 없음 — 기다립니다'); }
        if(tries>40){ say('★ 끝까지 주문을 못 찾았습니다'); return; }
        setTimeout(go, 300); return;
      }
      var tp=String(o.topic===undefined?'':o.topic);
      if(!isMine(tp)){
        say('주제가 「'+tp+'」 — 삼재가 아니라 물러납니다');
        return;
      }
      var r=build();
      if(!r){
        say('★ 책을 못 지었습니다 — 사주 계산기나 주문을 확인하세요');
        return;
      }
      /* 원본 책의 겉표지를 살려 맨 앞에 붙입니다 */
      var cov=[];
      try{
        var cs=bk.querySelectorAll('.page.cover, .page[data-part="cover"]'), ci;
        for(ci=0; ci<cs.length; ci++){ cov.push(fixCover(cs[ci], r.title)); }
      }catch(e){}

      bk.innerHTML=cov.join('')+r.html;
      bk.setAttribute('data-samjae','1');
      bk.setAttribute('data-sjcover', String(cov.length));
      var t=document.getElementById('bkTitle');
      if(t){ t.textContent=r.title; }
      var ps=bk.querySelectorAll('.folio'), i;
      for(i=0;i<ps.length;i++){ ps[i].textContent=two(i+1); }
      say('그렸습니다 · '+SLOTNAME[r.slot]+' × '+r.sp+
          ' · 삼재 '+r.first+'~'+(r.first+2)+
          ' · 겉표지 '+cov.length+'쪽 · 모두 '+(r.n+cov.length)+'쪽');
    }catch(e){
      say('★ 멈췄습니다 — '+(e.message||e));
    }
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', go);
  } else { go(); }
})();
</script>
	<?php
} );
