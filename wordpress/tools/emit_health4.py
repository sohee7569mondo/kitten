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
	/* ★★ 사진 주소를 짐작하지 않고 워드프레스에게 묻습니다
	   2026-09-15 · 소희 님 「장표지 글미 없음 — 저거 로고 같은데」

	   동그라미 안에 사진 대신 흐린 로고(책 CSS 의 바탕무늬)만
	   보였습니다. 자리도 크기도 맞으니 **그림을 못 받아온** 것입니다.

	   까닭 : 같은 그림을 다시 올리시면 워드프레스가 파일 이름 끝에
	   -1 을 붙입니다. 미디어를 열어보니 실제로
	       STELLASAJU_FORTUNE-2026.jpg  와  STELLASAJU_FORTUNE-2026-1.jpg
	   이 둘 다 있었습니다. 조각에 박아둔 주소가 살아 있는 쪽이
	   아닐 수 있다는 뜻입니다.

	   그래서 이름으로 미디어를 찾아 **워드프레스가 아는 주소**를
	   씁니다. 못 찾으면 빈 값이 되고, 그때는 아래 박아둔 주소로
	   물러납니다. */
	$pic = '';
	$hit = get_posts( array(
		'post_type'      => 'attachment',
		'post_status'    => 'inherit',
		'post_mime_type' => 'image',
		'posts_per_page' => 1,
		'orderby'        => 'ID',
		'order'          => 'DESC',
		's'              => 'STELLASAJU_HEALTH-CAR',
	) );
	if ( $hit ) {
		$one = wp_get_attachment_image_url( $hit[0]->ID, 'large' );
		if ( $one ) { $pic = $one; }
	}
	?>
<script>window.StellaPicHealth4 = '<?php echo esc_js( $pic ); ?>';</script>
	<?php
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
/* ══ 폭은 책 상자 한 곳에서만 정합니다 ═══════════════════════
   2026-09-14 · 소희 님 : 「폭이 안맞는건」 「여러번 언급했음 찾아봐」
   찾아보니 같은 날 두 번 고치면서 한 번은 되돌려 놓았습니다 —
     a711f94  살아 있는 쪽의 여백 규칙 때문에 책이 왼쪽으로 쏠림
              → 쪽을 max-width · margin auto 로 못 박음
     405b0a2  flex 안에서 auto margin 이 stretch 를 끔
              → 그 못을 빼고 margin 0 · max-width none 으로
   둘 다 맞는 말인데 같은 자리(.page)에 걸어서, 하나를 고치면 다른
   하나가 되살아났습니다. 자리를 갈라 놓습니다 —
     책 상자(.book)  폭을 정합니다   max-width · margin auto · padding
     쪽(.page)       늘어나게 둡니다 margin 0 · max-width none
   auto margin 이 stretch 를 끄는 것은 flex 아이템에서 생기는 일이라,
   상자 자신에 걸면 쪽은 그대로 늘어납니다. 그리고 상자에 못을 박으면
   살아 있는 쪽이 무슨 여백을 얹든 우리 책은 안 밀립니다.
   ★ 네 책(신년운세 둘 · 가족운 · 건강운)이 같은 값을 씁니다. */
@media screen{
  #ssb .book[data-health4="1"],
  #ssb [data-health4="1"]{
    max-width:900px !important;
    margin-left:auto !important; margin-right:auto !important;
    /* ★★ 좌우 여백 78px — 2026-09-15
       소희 님 「왼쪽에 여백이 너무 없고」
       까닭 : 쪽(.page)에 padding-left:0 을 못 박으면서, 원래 책이
       갖고 있던 좌우 78px(patch160_spacerun)까지 같이 날아갔습니다.
       크로미움으로 재 보니 1280px 화면에서 글줄이 744px 이 아니라
       860px 이었습니다 — 116px 더 넓게 퍼져 있었습니다.
       여백을 쪽이 아니라 **상자**에 줍니다. 그래야 flex 의 stretch 를
       끄지 않으면서 900 - 156 = 744px 로 원래 폭과 같아집니다.
       휴대폰은 spacerun 과 같은 22px. */
    padding-left:78px !important; padding-right:78px !important;
    box-sizing:border-box !important; }
}
@media screen and (max-width:820px){
  #ssb .book[data-health4="1"],
  #ssb [data-health4="1"]{
    padding-left:22px !important; padding-right:22px !important; }
}
@media screen{
  #ssb .book[data-health4="1"] > .page,
  #ssb [data-health4="1"] > .page{
    margin-left:0 !important; margin-right:0 !important;
    padding-left:0 !important; padding-right:0 !important;
    max-width:none !important; width:auto !important; }
    /* ★★ padding 은 누르지 않습니다 — 2026-09-15
       소희 님 「왼쪽에 바가 있을경우 여백이 좁고」
       인용 한 마디(왼쪽 바)와 말상자의 안쪽 여백이 이 못에 눌려
       글이 바에 딱 붙어 있었습니다. 예외를 하나씩 다는 대신
       padding 을 아예 안 건드립니다. 밀려나는 것을 막는 데는
       margin 과 max-width 만으로 충분합니다. */
  #ssb .book[data-health4="1"] > .page:not(.divider):not(.cover):not([data-part="cover"]) > *,
  #ssb [data-health4="1"] > .page:not(.divider):not(.cover):not([data-part="cover"]) > *{
    margin-left:0 !important; margin-right:0 !important;
    max-width:none !important; }
  #ssb .book[data-health4="1"] > .page.divider > *,
  #ssb [data-health4="1"] > .page.divider > *{
    margin-left:auto !important; margin-right:auto !important; }
}

/* ══ 겉표지의 아치문 — 크기와 모양도 우리가 박습니다 ══════
   2026-09-15 · 소희 님 「삼재는 아직 메인에 그림안들어감」
                        「2026 도 비슷하게 메인 사진 없고」
   원본 책은 우리 주제를 몰라 표지 아치를 못 만들거나 비워 둡니다.
   fixCover() 가 없으면 만들어 사진을 넣고, 모양은 여기서 정합니다.
   네 책이 같은 모양이라야 한 세트로 보입니다. */
#ssb .book[data-health4="1"] > .page.cover > .dvmark.dvface,
#ssb [data-health4="1"] > .page.cover > .dvmark.dvface{
  display:block !important;
  width:262px !important; height:360px !important;
  max-width:72% !important; min-width:0 !important;
  margin:14px auto 30px !important; padding:0 !important;
  border-radius:131px 131px 12px 12px !important;
  overflow:hidden !important; box-sizing:border-box !important; }
#ssb .book[data-health4="1"] > .page.cover > .dvmark.dvface img,
#ssb [data-health4="1"] > .page.cover > .dvmark.dvface img{
  width:100% !important; height:100% !important; display:block !important;
  max-width:none !important; object-fit:cover !important;
  object-position:center 34% !important; }
@media (max-width:640px){
  #ssb .book[data-health4="1"] > .page.cover > .dvmark.dvface,
  #ssb [data-health4="1"] > .page.cover > .dvmark.dvface{
    width:200px !important; height:275px !important;
    border-radius:100px 100px 10px 10px !important;
    margin-bottom:24px !important; }
}
@media print{
  #ssb .book[data-health4="1"] > .page.cover > .dvmark.dvface img,
  #ssb [data-health4="1"] > .page.cover > .dvmark.dvface img{
    -webkit-print-color-adjust:exact; print-color-adjust:exact; }
}

/* ══ 장 속표지의 얼굴 — 우리가 직접 박습니다 ═════════════
   2026-09-15 · 소희 님 「중간에 미르 사진 안들어가고」
                        「중간에 중간에 사진없음」

   까닭 : 동그라미(.dvmark.dvface)의 크기를 정하는 규칙이 우리
   조각에 없었습니다. 남의 조각(patch160_face)이 살아 있는 쪽에
   넣어둔 CSS 에 기대고 있었는데, 우리가 갈아끼운 책에는 그것이
   안 닿았습니다. 크로미움으로 재 보니 사진이 0 x 0 이었습니다 —
   자리는 있는데 크기가 없어 한 점도 안 그려집니다.

   그래서 남에게 기대지 않고 우리 울타리 안에 크기를 박습니다.
   화면과 인쇄 둘 다에 걸리도록 @media 밖에 둡니다. */
#ssb .book[data-health4="1"] > .page.divider > .dvmark.dvface,
#ssb [data-health4="1"] > .page.divider > .dvmark.dvface{
  display:block !important;
  width:132px !important; height:132px !important;
  max-width:132px !important; min-width:0 !important;
  margin:0 auto 16px !important; padding:0 !important;
  border-radius:50% !important; overflow:hidden !important;
  box-sizing:border-box !important; }
#ssb .book[data-health4="1"] > .page.divider > .dvmark.dvface img,
#ssb [data-health4="1"] > .page.divider > .dvmark.dvface img{
  width:100% !important; height:100% !important; display:block !important;
  max-width:none !important; object-fit:cover !important;
  object-position:center 16% !important; }
@media (max-width:640px){
  #ssb .book[data-health4="1"] > .page.divider > .dvmark.dvface,
  #ssb [data-health4="1"] > .page.divider > .dvmark.dvface{
    width:108px !important; height:108px !important; max-width:108px !important;
    margin-bottom:14px !important; }
}
@media print{
  #ssb .book[data-health4="1"] > .page.divider > .dvmark.dvface img,
  #ssb [data-health4="1"] > .page.divider > .dvmark.dvface img{
    -webkit-print-color-adjust:exact; print-color-adjust:exact; }
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
    /* ★★ i0.wp.com(젯팩 사진 가속기)을 거치지 않습니다 — 2026-09-15
       소희 님 「중간에 중간에 사진없음」. 파일은 미디어에 다 있는데
       i0.wp.com 주소로는 안 떴습니다. 사이트 주소를 곧장 씁니다. */
    /* ★ 주소는 서버가 미디어에서 찾아 알려준 것을 먼저 씁니다.
       못 찾았으면 아래 박아둔 주소로 갑니다 (2026-09-15). */
    var DOORIMG=window.StellaPicHealth4 ? window.StellaPicHealth4
               : 'https://stellasaju.com/wp-content/uploads/'
                +'2026/09/STELLASAJU_HEALTH-CAR.jpg';
    COVPIC=DOORIMG; COVALT=DOORALT;   /* 표지에서 쓰려고 옮겨 담습니다 */
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

    /* ── 표지는 우리가 만들지 않습니다 ─────────────────
       2026-09-15 · 소희 님 「건강운 표지가 2번들어감 목차 뒤에 또
       표지가있음」

       까닭 : 겉표지는 원본 책이 짓습니다 — 아치문 사진이 들어간 그
       표지입니다. 우리도 하나 더 만들고 있어서 둘이 되었습니다.
       원본 것이 더 낫습니다(사진이 있습니다). 우리 것을 뺍니다.
       제목과 부제는 fixCover() 가 원본 표지에 갈아 끼웁니다. */

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
  function fixFaces(root){
    try{
      var ims=root.querySelectorAll('.dvmark.dvface img'), i;
      for(i=0;i<ims.length;i++){ retryImg(ims[i]); }
    }catch(e){}
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
  var COVSUB='THE BODY';
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
      /* ★ 표지 아치 안이 비어 있으면 우리 사진을 넣습니다 — 2026-09-15
         소희 님 「삼재는 아직 메인에 그림안들어감」
         원본 책은 「삼재」 같은 주제를 몰라 표지 사진을 못 고릅니다.
         가족운 표지에는 사진이 들어 있고 삼재 표지는 비어 있던 까닭입니다. */
      var fa=e.querySelector('.dvmark.dvface');
      if(!fa){ fa=e.querySelector('.dvmark'); }
      if(!fa){
        /* ★ 아치가 아예 없으면 만들어 넣습니다 — 2026-09-15
           소희 님 「2026 도 비슷하게 메인 사진 없고」
           신년운세 표지에는 원본 책이 아치를 아예 안 만듭니다.
           가족운 표지에는 있고 신년운세에는 없던 까닭입니다.
           STELLA SAJU 딱지 바로 뒤, 제목 앞에 놓습니다. */
        fa=document.createElement('div');
        fa.className='dvmark dvface';
        var mk=e.querySelector('.mark'), h0=e.querySelector('h1');
        if(mk){ if(mk.nextSibling){ e.insertBefore(fa, mk.nextSibling); }
                else { e.appendChild(fa); } }
        else if(h0){ e.insertBefore(fa, h0); }
        else { e.insertBefore(fa, e.firstChild); }
      }
      if(fa){
        var cls2=String(fa.className===undefined?'':fa.className);
        if(cls2.indexOf('dvface')<0){ fa.className=cls2+' dvface'; }
        var fi=fa.querySelector('img');
        if(!fi){
          fi=document.createElement('img');
          fi.setAttribute('decoding','async');
          fa.appendChild(fi);
        }
        var cur=String(fi.getAttribute('src')===null?'':fi.getAttribute('src'));
        if(!cur){ if(COVPIC){
          fi.setAttribute('src', COVPIC);
          fi.setAttribute('alt', COVALT?COVALT:'');
        } }
      }
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
                  /* ★ 원본 책의 겉표지를 살려 맨 앞에 붙입니다 — 2026-09-15
                     소희 님 「삼재에 속표지 붙었는제 제일 겉표지 안붙었어」
                     겉표지(.page.cover)는 우리가 짓는 것이 아니라 원본 책이
                     짓습니다. innerHTML 로 통째로 갈아끼우면 같이 날아갑니다. */
                  var cov=[];
                  try{
                    var cs=bk.querySelectorAll('.page.cover, .page[data-part="cover"]'), ci;
                    /* ★ 겉표지는 **한 장만** 살립니다 — 2026-09-15
           소희 님 「건강운 표지가 2번들어감 목차 뒤에 또 표지가있음」
           원본 책이 겉표지 꼴의 쪽을 둘 짓습니다 (겉표지 + 속표지).
           둘 다 옮기면 목차 뒤에 또 표지가 나옵니다. 맨 앞 하나만. */
        if(cs.length){ cov.push(fixCover(cs[0], r.title)); }
                  }catch(e){}
                  bk.innerHTML=cov.join('')+r.html;
                  fixFaces(bk);   /* 사진이 안 뜨면 다른 주소로 한 번 더 */
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
