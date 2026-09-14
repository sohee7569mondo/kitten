# -*- coding: utf-8 -*-
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
H = io.open(os.path.join(HERE, 'H.json'), encoding='utf-8').read()

HEAD = u'''/* ══════════════════════════════════════════════════════════
   건강운 — 「나는 내 몸을 어떻게 다룰 것인가」 열 장
                                        ★ 2026-09-13 · 소희 님께
                                        판 HEALTH-4

   ★ 앞판(patch160_health, HEALTH-3)을 갈아치웁니다.
     앞판은 옛 목차(체질 · 현실의 몸 · 신호 …)였고, 가장 많은 오행
     하나를 ① ③ ⑥ 세 장에서 다 써서 「계속 토 얘기」가 나왔습니다.
     새 판은 장마다 다른 재료를 씁니다.

   ★ 앞판을 못 끄셨어도 이 판이 이깁니다 — 이 조각이 책을 갈아끼운 뒤
     앞판의 깃발(data-health)까지 같이 꽂아서 앞판이 다시 덮어쓰지
     못하게 합니다. 그래도 헷갈리니 WPCode 에서 앞판(patch160_health)은
     꺼두시는 편이 좋습니다.
   ★ 이름 붙은 PHP 함수를 쓰지 않습니다. 그래서 두 번 붙이셔도
     「Cannot redeclare function」 탈이 나지 않습니다. 스크립트도
     window.StellaHealth4 로 한 번만 돌게 막아 두었습니다.

   ── 앵커를 안 잡습니다 ────────────────────────────────
   쪽 글을 한 글자도 안 바꿉니다. 책이 다 그려진 뒤 주제가 건강운이면
   책 그릇을 우리 열세 쪽으로 갈아끼웁니다. 끄면 원래대로입니다.

   ── 장마다 무엇으로 갈리나 ────────────────────────────
   ①  오행 다섯은 다 나갑니다. 가장 많은 오행으로 {오행}·{강점}·{반응}
       세 빈칸을 채웁니다. 십성은 일곱 가운데 가진 것만, 많은 순으로.
   ②  잠의 결(화·수) · 밤형낮형(화 대 금수) · 사전질문 where ·
       스트레스(십성 무리 으뜸) · 사전질문 rest · 기운 세 갈래
   ③  십성 무리 으뜸 · 무너지는 시간대 · 살이 붙는 방식 · 기운 세 갈래
   ④  식사 결(토 / 목화 / 금) · 아침 · 시간대 · 사전질문 season
   ⑤  기운 세 갈래(두 무리) · 사전질문 rhythm
   ⑥ ⑦ ⑩  갈리지 않습니다
   ⑧  올해 기운이 내 오행 어디에 닿나 (다섯)
   ⑨  후보 여섯에서 셋 뽑기 — 위에서부터 해당하는 것으로 채웁니다

   ── 1부 렌즈는 안 나갑니다 ────────────────────────────
   소희 님 : 「①의 일곱 십성을 기준으로 통일하고, 1부의 열 개 렌즈는
   건강운에서 완전히 빼는 것이 가장 좋습니다.」
   책 그릇을 통째로 갈아끼우므로 애초에 안 나옵니다.

   ── 사전질문 답의 글자 ────────────────────────────────
   rest   푹 자고 아무것도 안 한다 / 몸을 움직여야 풀린다
   where  위 · 장 같은 속부터 온다 / 목 · 어깨 · 허리처럼 뻐근해진다
   season 추위를 많이 탄다 / 더위를 많이 탄다
   rhythm 규칙적으로 사는 편이다 / 몰아서 하고 몰아서 쉰다
   family 기대는 쪽이다 / 짊어지는 쪽이다
   ★ 질문 문장을 바꾸시면 이 글자도 같이 바꿔야 합니다.

   ── 붙이는 법 ─────────────────────────────────────────
   ★ 새 조각입니다. WPCode -> 새 스니펫 -> PHP Snippet -> 저장 -> Active
   ★ 위치(Location)를 「어디서나 실행 / Run Everywhere」로.
   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ 앞판 patch160_health 는 꺼두세요.

   ── 검사한 것 ─────────────────────────────────────────
   php -l           문법
   앰퍼샌드 · 역빗금  둘 다 0 이어야 합니다
   node --check     스크립트 문법
   node 로 실제로 그려봄 — 여러 사주꼴로
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
   2026-09-14 · 소희 님 : 「중간에 폭이 달라짐」
   책(.book)은 display:flex · flex-direction:column 입니다.
   WIDTH-7 은 쪽을 width:auto + margin-left/right:auto 로 가운데
   놓는데, flex 안에서 좌우 margin 이 auto 면 stretch 가 꺼집니다.
   그래서 글이 짧은 쪽은 글 길이만큼 줄어들고 가운데로 몰립니다
   (신년운세 책에서 239px ~ 780px 까지 제각각인 것을 재서 잡았습니다).
   auto margin 을 0 으로 눌러 stretch 를 살립니다.
   ★ 앞에 #ssb 를 꼭 붙입니다 — WIDTH-7 이 #ssb .page 로 걸어서
     그게 없으면 힘이 모자라 집니다. 가족운 책과 같은 꼴입니다. */
@media screen{
  #ssb .book[data-health4="1"] > .page,
  #ssb [data-health4="1"] > .page{
    margin-left:0 !important; margin-right:0 !important;
    padding-left:0 !important; padding-right:0 !important;
    max-width:none !important; width:auto !important; }
  #ssb .book[data-health4="1"] > .page > *,
  #ssb [data-health4="1"] > .page > *{
    padding-left:0 !important; padding-right:0 !important;
    margin-left:0 !important; margin-right:0 !important;
    max-width:none !important; }
  #ssb .book[data-health4="1"] > .page.divider > *,
  #ssb [data-health4="1"] > .page.divider > *{
    margin-left:auto !important; margin-right:auto !important; }
}
</style>
<script>
/* ═══ 건강운 열 장 (HEALTH-4) ═══
   글은 소희 님 원고 그대로입니다. 쪽은 안 건드립니다. */
(function(){

  if(window.StellaHealth4){ return; }

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

  var TOPICS=['건강운','체질','체질건강운','체질·건강운','체질 및 건강운',
              '체질 및 건강','내 몸'];
  function isMine(tp){
    var i; for(i=0;i<TOPICS.length;i++){ if(tp===TOPICS[i]){ return true; } }
    return false;
  }

  var H = '''

TAIL = u''';

  var FIVE=['목','화','토','금','수'];
  var GK=['비겁','식상','재성','관성','인성'];
  var SAENG={ '목':'화','화':'토','토':'금','금':'수','수':'목' };
  var KE   ={ '목':'토','화':'금','토':'수','금':'목','수':'화' };
  var GANEL=['목','목','화','화','토','토','금','금','수','수'];

  /* ① 의 빈칸 — 소희 님이 확정하신 표 */
  var ELSAY={
    '목':{ s:'움직이면서 몸을 푸는 힘',        r:'목과 어깨가 먼저 굳는 것' },
    '화':{ s:'빠르게 반응하고 밀고 나가는 힘',  r:'밤이 되어도 쉽게 가라앉지 않는 것' },
    '토':{ s:'흔들려도 받아내고 버티는 힘',    r:'몸이 무거워지고 속이 먼저 불편해지는 것' },
    '금':{ s:'정해둔 것을 지키는 힘',          r:'한 번 흐트러지면 통째로 놓아버리는 것' },
    '수':{ s:'쉬면 다시 채워지는 힘',          r:'회복이 늦고 아침이 무거운 것' }
  };

  var A_REST=['푹 자고 아무것도 안 한다','몸을 움직여야 풀린다'];
  var A_WHERE=['위 · 장 같은 속부터 온다','목 · 어깨 · 허리처럼 뻐근해진다'];
  var A_SEASON=['추위를 많이 탄다','더위를 많이 탄다'];
  var A_RHYTHM=['규칙적으로 사는 편이다','몰아서 하고 몰아서 쉰다'];
  var A_FAMILY=['기대는 쪽이다','짊어지는 쪽이다'];

  function gang3(gk){
    if(gk==='much'){ return 'strong'; }
    if(gk==='gang'){ return 'strong'; }
    if(gk==='yak'){ return 'weak'; }
    if(gk==='thin'){ return 'weak'; }
    return 'mid';
  }

  function chooser(ctx){
    var c=ctx.el, g=ctx.grp, ans=ctx.ans, G3=ctx.g3, top=ctx.top;
    function E(k){ return c[k]||0; }
    function P(k){ return g[k]||0; }
    function topGrp(){
      var b=GK[0], n=-1, i;
      for(i=0;i<GK.length;i++){ if(P(GK[i])>n){ n=P(GK[i]); b=GK[i]; } }
      return b;
    }
    return function(key){
      if(key==='gang3'){ return G3; }
      if(key==='grp'){ return topGrp(); }
      if(key==='sleep'){
        /* 「화의 힘이 강하게」라고 말하려면 화가 실제로 넉넉해야 합니다 */
        if(E('화')>=3){ return 'hwa'; }
        if(E('수')<=1){ return 'suthin'; }
        if(E('수')>=3){ return 'su'; }
        if(E('화')>E('수')){ return 'hwa'; }
        return 'su';
      }
      if(key==='clock'){
        if(E('화')>=3){ return 'night'; }
        if(E('금')+E('수')>=3){ return 'morning'; }
        if(E('화')>E('금')+E('수')){ return 'night'; }
        return 'morning';
      }
      if(key==='where'){
        if(ans.where===A_WHERE[0]){ return 'sok'; }
        if(ans.where===A_WHERE[1]){ return 'stiff'; }
        return 'none';
      }
      if(key==='rest'){
        if(ans.rest===A_REST[0]){ return 'still'; }
        if(ans.rest===A_REST[1]){ return 'move'; }
        return 'none';
      }
      if(key==='season'){
        if(ans.season===A_SEASON[0]){ return 'cold'; }
        if(ans.season===A_SEASON[1]){ return 'hot'; }
        return 'none';
      }
      if(key==='rhythm'){
        if(ans.rhythm===A_RHYTHM[0]){ return 'reg'; }
        if(ans.rhythm===A_RHYTHM[1]){ return 'burst'; }
        return 'none';
      }
      if(key==='when'){
        if(E('화')>=3){ return 'night'; }
        if(E('토')>=3){ return 'pm'; }
        if(P('재성')>=3){ return 'skip'; }
        return 'eve';
      }
      if(key==='when2'){
        if(E('화')>=E('토')){ if(E('화')>=2){ return 'night'; } }
        if(E('토')>=2){ return 'pm'; }
        return 'skip';
      }
      if(key==='gain'){
        var keep=E('토')+E('수'), burn=E('목')+E('화'), rule=E('금');
        if(rule>keep){ if(rule>burn){ return 'rule'; } }
        if(keep>=burn){ return 'keep'; }
        return 'burn';
      }
      if(key==='meal'){
        var t=E('토'), mh=E('목')+E('화'), gm=E('금');
        if(gm>t){ if(gm>=mh){ return 'rule'; } }
        if(t>=mh){ return 'often'; }
        return 'long';
      }
      if(key==='morn'){
        if(G3==='strong'){ return 'heavy'; }
        return 'need';
      }
      if(key==='year'){
        var y=ctx.yearEl;
        if(!y){ return 'far'; }
        if(y===top){ return 'same'; }
        if(E(y)===0){ return 'new'; }
        if(KE[y]===top){ return 'press'; }
        if(SAENG[y]===top){ return 'help'; }
        return 'far';
      }
      return '';
    };
  }

  /* ⑨ 세 가지 뽑기 — 위에서부터 해당하는 것으로 셋을 채웁니다 */
  function three(ctx){
    var c=ctx.el, g=ctx.grp, ans=ctx.ans, G3=ctx.g3;
    var on={
      weak  : (G3==='weak'),
      sleep : ((c['화']||0)>=3 || ans.rest===A_REST[0]),
      bear  : ((g['관성']||0)>=3 || ans.family===A_FAMILY[1]),
      strong: (G3==='strong'),
      burst : (ans.rhythm===A_RHYTHM[1]),
      sign  : true
    };
    var order=['weak','sleep','bear','strong','burst','sign'];
    var out=[], i;
    for(i=0;i<order.length;i++){
      if(out.length<3){ if(on[order[i]]){ out.push(order[i]); } }
    }
    i=0;
    while(out.length<3){
      if(order[i]){ if(out.indexOf(order[i])<0){ out.push(order[i]); } }
      i++;
      if(i>20){ break; }
    }
    return out;
  }

  function build(){
    var S=window.StellaSaju, R=window.StellaRead;
    if(!S){ return null; }
    if(!R){ return null; }
    var o=read('stella_demo');
    if(!o){ return null; }
    var pr=o.profile||o;
    if(!pr.year){ return null; }
    var ans=read('stella_answers')||{};

    var loc=S.locate(pr.city, pr.country);
    var chart=S.compute({ year:pr.year, month:pr.month, day:pr.day,
      hour:pr.hour, minute:pr.minute||0, sex:pr.sex,
      lon:loc.lon, lat:loc.lat, tz:loc.tz });
    var it=R.interpret(chart);
    var grp=it.groups||{};
    var cnt=it.count||{};
    var gang=null;
    if(window.StellaGang){ try{ gang=window.StellaGang.judge(chart, it); }catch(e){} }
    var G3=gang3(gang?gang.key:'mid');

    var el={}, i;
    for(i=0;i<FIVE.length;i++){ el[FIVE[i]]=0; }
    var fv=chart.five||[];
    for(i=0;i<fv.length;i++){ el[fv[i].element]=fv[i].count; }
    var rank=FIVE.slice().sort(function(a,b){ return (el[b]||0)-(el[a]||0); });
    var top=rank[0];

    var nowY=(new Date()).getFullYear();
    var yidx=((nowY-4)%10+10)%10;
    var yearEl=GANEL[yidx];

    var ctx={ el:el, grp:grp, ans:ans, g3:G3, top:top, yearEl:yearEl };
    var pick=chooser(ctx);

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
    /* ── 장 속표지 ────────────────────────────────────────
       2026-09-14 · 소희 님 : 「모든 책엔 안에 장 표지가 있어야 해」
       patch160_divider · patch160_dvbig 이 만든 틀을 그대로 씁니다.
       클래스 이름이 같으면 책에 이미 얹혀 있는 CSS 가 그대로 먹어서
       새 CSS 를 한 줄도 안 만들어도 다른 책과 모양이 같아집니다. */
    var GUARDIAN='아람';
    var DOORALT='건강운';
    var DOORIMG='https://i0.wp.com/stellasaju.com/wp-content/uploads/'
               +'2026/09/STELLASAJU_HEALTH-CAR.jpg?resize=264%2C264';
    function sheet(no, title, part){
      n++;
      var attr=part?' data-part="'+part+'"':'';
      pages.push('<div class="page divider"'+attr+'>'+
        '<div class="dvmark dvface"><img loading="lazy" decoding="async" '+
        'alt="'+DOORALT+'" src="'+DOORIMG+'"></div>'+
        '<p class="dvwho">'+GUARDIAN+'</p>'+
        '<p class="dvno dvch">'+no+'</p>'+
        '<h2>'+title+'</h2>'+
        '<div class="dvrule"></div>'+
        '<div class="folio">'+two(n)+'</div></div>');
    }

    page('<div class="mark">STELLA SAJU</div>'+
         '<h1>'+nm+'님의<br>몸과 건강</h1>'+
         '<p class="dek">아람이 여덟 글자를 몸으로 읽습니다</p>', 'cover');

    /* 십성 일곱 가운데 가진 것 */
    var TEN7=['비견','겁재','식신','상관','재성','관성','인성'];
    function ten7n(k){
      if(k==='재성'){ return grp['재성']||0; }
      if(k==='관성'){ return grp['관성']||0; }
      if(k==='인성'){ return grp['인성']||0; }
      return cnt[k]||0;
    }

    var NOS=['01','02','03','04','05','06','07','08','09','10'];
    var MARK=['제 1 장','제 2 장','제 3 장','제 4 장','제 5 장',
              '제 6 장','제 7 장','제 8 장','제 9 장','제 10 장'];
    var NUM=['하나','둘','셋'];

    var ci;
    for(ci=0;ci<NOS.length;ci++){
      var no=NOS[ci], e=H.book[no];
      if(!e){ continue; }

      /* 이 장의 갈림 무리를 제목 -> 살릴까 로 펼쳐 둡니다 */
      var dropA={}, dropB={}, three3=null;
      var gi;
      for(gi=0;gi<e.g.length;gi++){
        var G=e.g[gi];
        if(G.pick3){
          three3=three(ctx);
          var pj;
          for(pj=0;pj<G.pick3.length;pj++){
            if(three3.indexOf(G.pick3[pj][0])<0){ dropB[G.pick3[pj][1]]=1; }
          }
          continue;
        }
        if(G.multi){ continue; }
        var want=pick(G.key), kk, keepT=null;
        for(kk in G.map){ if(G.map.hasOwnProperty(kk)){ if(kk===want){ keepT=G.map[kk]; } } }
        if(keepT===null){ for(kk in G.map){ if(G.map.hasOwnProperty(kk)){ if(keepT===null){ keepT=G.map[kk]; } } } }
        for(kk in G.map){
          if(G.map.hasOwnProperty(kk)){
            if(G.map[kk]!==keepT){
              if(G.lv==='A'){ dropA[G.map[kk]]=1; } else { dropB[G.map[kk]]=1; }
            }
          }
        }
      }

      /* ① 의 십성 일곱 — 가진 것만, 많은 순으로 */
      var ten7map=null, ten7ord=null;
      for(gi=0;gi<e.g.length;gi++){
        if(e.g[gi].multi){ ten7map=e.g[gi].map; }
      }
      if(ten7map){
        ten7ord=TEN7.slice().filter(function(k){ return ten7n(k)>0; });
        ten7ord.sort(function(a,b){ return ten7n(b)-ten7n(a); });
        if(!ten7ord.length){ ten7ord=TEN7.slice(); }
        var keepTitles={}, tj;
        for(tj=0;tj<ten7ord.length;tj++){ keepTitles[ten7map[ten7ord[tj]]]=1; }
        var tk;
        for(tk in ten7map){
          if(ten7map.hasOwnProperty(tk)){
            if(!keepTitles[ten7map[tk]]){ dropA[ten7map[tk]]=1; }
          }
        }
      }

      var h='', ai, threeN=0;
      for(ai=0;ai<e.A.length;ai++){
        var a=e.A[ai];
        if(a.h){ if(dropA[a.h]){ continue; } }
        var body=a.b;
        if(a.h){
          var ah=fill(String(a.h).split('★ ').join(''), nm);
          /* 십성 일곱이면 개수를 붙입니다 */
          if(ten7map){
            var tn=null, tq;
            for(tq in ten7map){ if(ten7map.hasOwnProperty(tq)){ if(ten7map[tq]===a.h){ tn=tq; } } }
            if(tn!==null){ ah=ah+' '+ten7n(tn); }
          }
          h+='<h3>'+ah+'</h3>';
        }
        h+=fill(body, nm);
        var ki;
        for(ki=0;ki<a.kids.length;ki++){
          var kd=a.kids[ki];
          if(dropB[kd.h]){ continue; }
          var kh=fill(String(kd.h).split('★ ').join(''), nm);
          if(three3){ threeN++; kh=NUM[threeN-1]+' · '+kh; }
          h+='<h4>'+kh+'</h4>'+fill(kd.b, nm);
        }
      }

      /* ① 의 빈칸 셋 */
      if(no==='01'){
        var say=ELSAY[top]||ELSAY['토'];
        h=h.split('{오행}').join(top);
        h=h.split('{강점}').join(say.s);
        h=h.split('{생활에서 먼저 나타나는 반응}').join(say.r);
      }

      /* 장 표지를 먼저 한 쪽 (소희 님: 「모든 책엔 안에 장 표지가 있어야 해」) */
      sheet(MARK[ci], e.t2, (ci<4?'one':'two'));
      page(h, null, (ci<4?'one':'two'));
    }

    return { html:pages.join(''), n:n, title:nm+'님의 몸과 건강' };
  }

  window.StellaHealth4={ build:build, has:isMine };

  var tries=0;
  function go(){
    tries++;
    try{
      var bk=document.getElementById('bkBook');
      if(bk){
        if(bk.getAttribute('data-health4')!=='1'){
          var o=read('stella_demo');
          if(o){
            if(isMine(String(o.topic===undefined?'':o.topic))){
              if(String(bk.innerHTML).length>200){
                var r=build();
                if(r){
                  bk.innerHTML=r.html;
                  bk.setAttribute('data-health4','1');
                  /* 앞판(HEALTH-3)이 다시 덮어쓰지 않게 그쪽 깃발도 꽂습니다.
                     앞판을 못 끄셨더라도 이 판이 이깁니다. */
                  bk.setAttribute('data-health','1');
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
}, 4 );
'''

out = HEAD + H + TAIL
io.open('/home/user/kitten/wordpress/php/patch160_health4.WPCODE.txt','w',encoding='utf-8').write(out)
print('바이트', len(out.encode('utf-8')), '· 앰퍼샌드', out.count('&'), '· 역빗금', out.count('\\'))
