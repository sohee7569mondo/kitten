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
    /* ★ 주소는 서버가 미디어에서 찾아 알려준 것을 먼저 씁니다.
       못 찾았으면 아래 박아둔 주소로 갑니다 (2026-09-15). */
    var DOORIMG=window.StellaPicSamjae ? window.StellaPicSamjae
      : 'https://stellasaju.com/wp-content/uploads/2026/09/STELLASAJU_samjae.jpg';
    COVPIC=DOORIMG; COVALT=DOORALT;   /* 표지에서 쓰려고 옮겨 담습니다 */
    var mark=0;

    function sheet(title){
      var no=MARK[mark] ? MARK[mark] : '';
      mark++;
      pages.push('<section class="page divider">'+
        /* ★ loading="lazy" 를 뺍니다 — 2026-09-16
           소희 님 「장표지의 그림은 안돼?」
           표지 아치에는 사진이 들어가는데 장 속표지 동그라미만
           비어 있었습니다. 진단 띠는 「받았습니다」라고 했는데
           그것은 **표지** 칸을 본 것이었습니다.
           우리는 책을 innerHTML 로 통째로 갈아끼웁니다. 그렇게
           끼운 lazy 그림은 브라우저가 화면에 들어온 줄 모르고
           끝까지 안 받는 일이 있습니다. 장 속표지는 열 장뿐이고
           같은 그림 하나라 한 번만 받으면 됩니다. 미루지 않습니다. */
        '<div class="dvmark dvface"><img decoding="async" '+
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

    /* ── 차례는 우리가 만들지 않습니다 ────────────────
       2026-09-15 · 소희 님 사진에 차례가 **두 번** 나왔습니다.

       까닭 : 원본 책이 이미 차례 쪽을 짓습니다. 우리 책의 장 제목을
       읽어 제 결(가운데 「차 례」 · 줄 사이 가로줄)로 그려 줍니다.
       그런데 우리가 또 하나 만들어 붙이고 있었습니다.

       처음에 「삼재에 목차페이지가 없어」 하셨던 것은 차례가 없어서가
       아니라, 겉표지를 안 살리던 때라 원본이 만든 차례까지 같이
       지워지고 있었기 때문입니다. 겉표지를 살리면서 차례도 돌아왔습니다.

       ★ 그러니 여기서는 아무것도 안 만듭니다. 장 이름을 모으던 표도
         뺍니다 — 쓰는 데가 없습니다. */

    /* ★ 카드 장 제목은 원고에 sjh2 로 이미 있습니다 (「카드 세 장 —
       삼재의 세 문」). 여기서 속표지를 또 놓으면 두 장이 됩니다. */
    var card=cardBlock(pr, nm, slot, blocks);
    if(card){ pages.push('<section class="page"><div class="folio"></div>'+card+'</section>'); }

    if(!pages.length){ return null; }
    return { html:pages.join(''), n:pages.length,
             title:(nm?nm+'님의 ':'당신의 ')+'삼재',
             slot:slot, sp:SP, first:first };
  }



  /* ── 장 속표지 사진이 안 뜨면 한 번 더 ───────────────
     2026-09-15 · 소희 님 「중간표지에도 그림 안들어감」

     동그라미 안에 사진 대신 흐린 로고만 보였습니다. 크기는 우리가
     박았으니 자리는 있는데 **그림이 안 받아졌다**는 뜻입니다.
     사이트 주소와 젯팩 주소(i0.wp.com) 가운데 어느 쪽이 살아 있는지
     제가 여기서 확인할 수 없으므로, 안 뜨면 다른 쪽으로 한 번 더
     시도하게 둡니다. 어느 쪽이 살아 있든 사진이 나옵니다. */
  function altURL(src){
    var s=String(src===null?'':src), k=s.indexOf('://');
    if(k<0){ return ''; }
    var rest=s.slice(k+3);
    if(rest.indexOf('i0.wp.com/')===0){ return ''; }
    return 'https://i0.wp.com/'+rest;
  }
  function retryImg(im){
    if(!im){ return; }
    /* ★ 미루지 말고 바로 받게 합니다 — 2026-09-16
       innerHTML 로 끼운 lazy 그림은 브라우저가 화면에 들어온 줄
       모르고 끝까지 안 받는 일이 있습니다. 옛 판으로 그려진
       그림에도 걸리도록 여기서 한 번 더 벗겨 줍니다. */
    try{
      if(im.getAttribute('loading')){
        im.removeAttribute('loading');
        var cur0=im.getAttribute('src');
        if(cur0){ im.setAttribute('src', cur0); }
      }
    }catch(e0){}
    if(im.getAttribute('data-retry')==='1'){ return; }
    var go=function(){
      if(im.getAttribute('data-retry')==='1'){ return; }
      im.setAttribute('data-retry','1');
      var u=altURL(im.getAttribute('src'));
      if(u){ im.setAttribute('src', u); }
    };
    im.addEventListener('error', go);
    if(im.complete){ if(!im.naturalWidth){ go(); } }
  }
  /* ── 겉표지 아치 ────────────────────────────
     2026-09-16 · 소희 님 사진에 아치가 **둘** 나왔습니다.

     원본 표지의 아치는 <img> 태그가 아니라 **배경 그림**으로
     그려집니다. 태그만 찾으면 「없다」고 보고 하나 더 만듭니다.
     그래서 책이 화면에 붙은 **뒤에** 배경까지 읽어 판단합니다.

     아치가 이미 있으면(태그로든 배경으로든) 아무것도 안 합니다.
     아예 없을 때만 만듭니다 — 신년운세 표지가 그렇습니다. */
  function fixCoverArch(root){
    try{
      var cov = root.querySelector('.page.cover');
      if(!cov){ cov = root.querySelector('.page[data-part="cover"]'); }
      if(!cov){ return; }
      if(cov.getAttribute('data-archdone') === '1'){ return; }
      cov.setAttribute('data-archdone', '1');

      /* ① 그림 태그가 있으면 이미 아치가 있는 것입니다 */
      if(cov.querySelector('img')){ return; }

      /* ② 배경 그림으로 그려진 것도 찾습니다 */
      var kids = cov.querySelectorAll('*'), i, st, bg;
      for(i = 0; i < kids.length; i++){
        try{
          st = window.getComputedStyle(kids[i]);
          if(!st){ continue; }
          bg = String(st.backgroundImage === undefined ? '' : st.backgroundImage);
          if(bg){ if(bg !== 'none'){ if(bg.indexOf('url') >= 0){ return; } } }
        }catch(e1){}
      }

      /* ③ 아무것도 없을 때만 만듭니다 */
      if(!COVPIC){ return; }
      var fa = document.createElement('div');
      fa.className = 'dvmark dvface';
      fa.setAttribute('data-ourarch', '1');
      var im = document.createElement('img');
      im.setAttribute('decoding', 'async');
      im.setAttribute('src', COVPIC);
      im.setAttribute('alt', COVALT ? COVALT : '');
      fa.appendChild(im);

      var mk = cov.querySelector('.mark'), h0 = cov.querySelector('h1');
      if(mk){
        if(mk.nextSibling){ cov.insertBefore(fa, mk.nextSibling); }
        else { cov.appendChild(fa); }
      }
      else if(h0){ cov.insertBefore(fa, h0); }
      else { cov.insertBefore(fa, cov.firstChild); }
      retryImg(im);
    }catch(e){}
  }

  function fixFaces(root){
    try{
      var ims=root.querySelectorAll('.dvmark.dvface img'), i;
      for(i=0;i<ims.length;i++){ retryImg(ims[i]); }
    }catch(e){}
  }
  /* ── 사진이 왜 안 뜨는지 찍어 줍니다 ──────────────────
     2026-09-15 · 소희 님 「장표지에 그림이 ...」
     표지 아치에는 사진이 들어가는데 장 속표지 동그라미만 비어
     있습니다. 더 짐작하지 않고 **실제 주소와 받아졌는지**를
     관리자 띠에 찍습니다. 한 번만 보시면 까닭이 바로 나옵니다.
     ★ 손님에게는 안 보입니다 (관리자 띠 안에서만 부릅니다). */
  function picReport(root){
    try{
      var ims=root.querySelectorAll('.dvmark.dvface img');
      if(!ims.length){ return '사진 — ★ 그림칸이 하나도 없습니다'; }
      var i, im, got=0, bad=0, wait=0, cov=0, dv=0, first='', badone='', size='';
      for(i=0;i<ims.length;i++){
        im=ims[i];
        var onCover=0;
        try{ if(im.closest){ if(im.closest('.page.cover')){ onCover=1; } } }catch(e2){}
        if(onCover){ cov++; } else { dv++; }
        if(!im.complete){ wait++; }
        else if(im.naturalWidth){
          got++;
          if(!first){ first=String(im.getAttribute('src'));
                      size=im.naturalWidth+'x'+im.naturalHeight; }
        }
        else { bad++; if(!badone){ badone=String(im.getAttribute('src')); } }
      }
      var nl=String.fromCharCode(10);
      var s='사진 — 표지 '+cov+'칸 · 장 속표지 '+dv+'칸';
      s+=nl+'  받음 '+got+' · ★ 못 받음 '+bad+' · 받는 중 '+wait;
      if(first){ s+=nl+'  받은 것 '+size+' · '+first; }
      if(badone){ s+=nl+'  ★ 못 받은 주소 '+badone; }
      return s;
    }catch(e){ return '사진 — ★ '+e; }
  }

  /* ★ 표지에 쓸 사진 — 책을 지을 때 담아 둡니다.
     사진 주소(DOORIMG)는 book()/build() **안**에 있어서 fixCover 에서는
     안 보입니다. 보이는 자리에 옮겨 담습니다 (2026-09-15).
     이 한 줄이 없어 가족운·삼재 표지에 아치가 안 만들어졌습니다. */
  var COVPIC, COVALT;   /* ★ 여기서 ='' 로 두면 안 됩니다 — 신년운세는
     사진 주소를 이 줄보다 **위**에서 담는데, 그 값을 빈 글자로
     덮어써서 표지에 사진이 안 들어갔습니다 (2026-09-15 에 그랬습니다). */

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
      /* ★ 표지 아치는 여기서 만들지 않습니다 — 2026-09-16
         소희 님 사진에 아치가 또 둘 나왔습니다.
         까닭 : 원본 표지의 아치는 <img> 태그가 아니라 **배경 그림**
         으로 그려집니다. querySelector('img') 로는 못 찾습니다.
         그리고 여기서는 쪽이 아직 화면에 붙기 전이라 배경을 읽을
         수도 없습니다. 그래서 책을 다 그린 뒤에 fixCoverArch() 가
         배경까지 보고 판단합니다. 여기서는 글자만 고칩니다. */
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
        /* ★ 겉표지는 **한 장만** 살립니다 — 2026-09-15
           소희 님 「건강운 표지가 2번들어감 목차 뒤에 또 표지가있음」
           원본 책이 겉표지 꼴의 쪽을 둘 짓습니다 (겉표지 + 속표지).
           둘 다 옮기면 목차 뒤에 또 표지가 나옵니다. 맨 앞 하나만. */
        if(cs.length){ cov.push(fixCover(cs[0], r.title)); }
      /* ★ 원본 책의 차례 쪽도 살립니다 — 2026-09-15
         소희 님 「목차가 없어졌어」
         차례(.tocpage)는 원본 책이 짓고, 우리 책의 장 제목을 읽어
         제 결로 채웁니다. innerHTML 로 덮으면 그 **그릇**까지
         사라져서 다시 채울 데가 없어집니다. 겉표지처럼 살립니다. */
      var toc=[];
      try{
        var ts=bk.querySelectorAll('.tocpage'), ti;
        for(ti=0; ti<ts.length; ti++){ toc.push(ts[ti].outerHTML); }
      }catch(e){}
      }catch(e){}

      bk.innerHTML=cov.join('')+toc.join('')+r.html;
      fixFaces(bk);   /* 사진이 안 뜨면 다른 주소로 한 번 더 */
      fixCoverArch(bk);   /* 표지 아치가 아예 없을 때만 만듭니다 */
      bk.setAttribute('data-samjae','1');
      bk.setAttribute('data-sjcover', String(cov.length));
      var t=document.getElementById('bkTitle');
      if(t){ t.textContent=r.title; }
      var ps=bk.querySelectorAll('.folio'), i;
      for(i=0;i<ps.length;i++){ ps[i].textContent=two(i+1); }
      say('그렸습니다 · '+SLOTNAME[r.slot]+' × '+r.sp+
          ' · 삼재 '+r.first+'~'+(r.first+2)+
          ' · 겉표지 '+cov.length+'쪽 · 모두 '+(r.n+cov.length)+'쪽');
      setTimeout(function(){ say(picReport(bk)); }, 1400);
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
