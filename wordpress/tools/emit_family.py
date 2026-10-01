# -*- coding: utf-8 -*-
import io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
F = io.open(os.path.join(HERE, 'F.json'), encoding='utf-8').read()

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
		's'              => 'STELLASAJU_family',
	) );
	if ( $hit ) {
		/* ★★ image_url( ..., 'large' ) 를 쓰면 안 됩니다 — 2026-09-15
		   그것은 젯팩 주소에 물음표 뒤 값이 붙은 것을 돌려줍니다
		       i0.wp.com/....jpg?fit=683%2C1024   <- 앰퍼샌드가 섞입니다
		   집 규칙대로 조각 안에는 앰퍼샌드를 두지 않습니다. 워드프레스가
		   그 글자를 바꿔버리면 주소가 깨져 그림이 안 뜹니다.
		   파라미터 없는 원본 주소를 씁니다. */
		$one = wp_get_attachment_url( $hit[0]->ID );
		if ( $one ) {
			if ( false === strpos( $one, '?' ) ) { $pic = $one; }
		}
	}
	?>
<script>window.StellaPicFamily = '<?php echo esc_js( $pic ); ?>';</script>
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
  #ssb .book[data-family="1"],
  #ssb [data-family="1"]{
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
  #ssb .book[data-family="1"],
  #ssb [data-family="1"]{
    padding-left:22px !important; padding-right:22px !important; }
}
@media screen{
  #ssb .book[data-family="1"] > .page{
    padding-left:0 !important; padding-right:0 !important;
    margin-left:0 !important; margin-right:0 !important;
    max-width:none !important; width:auto !important;
  }
    /* ★★ padding 은 누르지 않습니다 — 2026-09-15
       소희 님 「왼쪽에 바가 있을경우 여백이 좁고」
       인용 한 마디(왼쪽 바)와 말상자의 안쪽 여백이 이 못에 눌려
       글이 바에 딱 붙어 있었습니다. 예외를 하나씩 다는 대신
       padding 을 아예 안 건드립니다. 밀려나는 것을 막는 데는
       margin 과 max-width 만으로 충분합니다. */
  #ssb .book[data-family="1"] > .page:not(.divider):not(.cover):not([data-part="cover"]) > *{
    margin-left:0 !important; margin-right:0 !important;
  }
  /* 장 속표지는 가운데 정렬이라 위 못에서 빼 줍니다 (2026-09-14) */
  #ssb .book[data-family="1"] > .page.divider > *{
    margin-left:auto !important; margin-right:auto !important; }
  #ssb .book[data-family="1"] > .page.divider > h2,
  #ssb .book[data-family="1"] > .page.divider > p{ text-align:center !important; }
  #ssb .book[data-family="1"] > .page > h2,
  #ssb .book[data-family="1"] > .page > h3,
  #ssb .book[data-family="1"] > .page > p{ text-align:left; }
}

/* ══ 겉표지의 아치문 — 크기와 모양도 우리가 박습니다 ══════
   2026-09-15 · 소희 님 「삼재는 아직 메인에 그림안들어감」
                        「2026 도 비슷하게 메인 사진 없고」
   원본 책은 우리 주제를 몰라 표지 아치를 못 만들거나 비워 둡니다.
   fixCover() 가 없으면 만들어 사진을 넣고, 모양은 여기서 정합니다.
   네 책이 같은 모양이라야 한 세트로 보입니다. */
#ssb .book[data-family="1"] > .page.cover > .dvmark.dvface,
#ssb [data-family="1"] > .page.cover > .dvmark.dvface{
  display:block !important;
  width:262px !important; height:360px !important;
  max-width:72% !important; min-width:0 !important;
  margin:14px auto 30px !important; padding:0 !important;
  border-radius:131px 131px 12px 12px !important;
  overflow:hidden !important; box-sizing:border-box !important; }
#ssb .book[data-family="1"] > .page.cover > .dvmark.dvface img,
#ssb [data-family="1"] > .page.cover > .dvmark.dvface img{
  width:100% !important; height:100% !important; display:block !important;
  max-width:none !important; object-fit:cover !important;
  object-position:center 34% !important; }
@media (max-width:640px){
  #ssb .book[data-family="1"] > .page.cover > .dvmark.dvface,
  #ssb [data-family="1"] > .page.cover > .dvmark.dvface{
    width:200px !important; height:275px !important;
    border-radius:100px 100px 10px 10px !important;
    margin-bottom:24px !important; }
}
@media print{
  #ssb .book[data-family="1"] > .page.cover > .dvmark.dvface img,
  #ssb [data-family="1"] > .page.cover > .dvmark.dvface img{
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
#ssb .book[data-family="1"] > .page.divider > .dvmark.dvface,
#ssb [data-family="1"] > .page.divider > .dvmark.dvface{
  display:block !important;
  width:132px !important; height:132px !important;
  max-width:132px !important; min-width:0 !important;
  margin:0 auto 16px !important; padding:0 !important;
  border-radius:50% !important; overflow:hidden !important;
  box-sizing:border-box !important; }
#ssb .book[data-family="1"] > .page.divider > .dvmark.dvface img,
#ssb [data-family="1"] > .page.divider > .dvmark.dvface img{
  width:100% !important; height:100% !important; display:block !important;
  max-width:none !important; object-fit:cover !important;
  object-position:center 16% !important; }
@media (max-width:640px){
  #ssb .book[data-family="1"] > .page.divider > .dvmark.dvface,
  #ssb [data-family="1"] > .page.divider > .dvmark.dvface{
    width:108px !important; height:108px !important; max-width:108px !important;
    margin-bottom:14px !important; }
}
@media print{
  #ssb .book[data-family="1"] > .page.divider > .dvmark.dvface img,
  #ssb [data-family="1"] > .page.divider > .dvmark.dvface img{
    -webkit-print-color-adjust:exact; print-color-adjust:exact; }
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
    /* ── 장 속표지 ────────────────────────────────────────
       2026-09-14 · 소희 님 : 「모든 책엔 안에 장 표지가 있어야 해」
       patch160_divider · patch160_dvbig 이 만든 틀을 그대로 씁니다.
       클래스 이름이 같으면 책에 이미 얹혀 있는 CSS 가 그대로 먹어서
       새 CSS 를 한 줄도 안 만들어도 다른 책과 모양이 같아집니다. */
    var GUARDIAN='아람';
    var DOORALT='가족운';
    /* ★★ i0.wp.com(젯팩 사진 가속기)을 거치지 않습니다 — 2026-09-15
       소희 님 「중간에 중간에 사진없음」. 파일은 미디어에 다 있는데
       i0.wp.com 주소로는 안 떴습니다. 사이트 주소를 곧장 씁니다.
       크기는 CSS(.dvmark img)가 잡으므로 resize 도 필요 없습니다. */
    /* ★ 주소는 서버가 미디어에서 찾아 알려준 것을 먼저 씁니다.
       못 찾았으면 아래 박아둔 주소로 갑니다 (2026-09-15). */
    var DOORIMG=window.StellaPicFamily ? window.StellaPicFamily
               : 'https://stellasaju.com/wp-content/uploads/'
                +'2026/09/STELLASAJU_family.jpg';
    COVPIC=DOORIMG; COVALT=DOORALT;   /* 표지에서 쓰려고 옮겨 담습니다 */
    function sheet(no, title, part){
      n++;
      var attr=part?' data-part="'+part+'"':'';
      pages.push('<div class="page divider"'+attr+'>'+
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
        '<div class="folio">'+two(n)+'</div></div>');
    }

    /* ── 표지는 우리가 만들지 않습니다 ─────────────────
       2026-09-15 · 소희 님 「건강운 표지가 2번들어감 목차 뒤에 또
       표지가있음」

       까닭 : 겉표지는 원본 책이 짓습니다 — 아치문 사진이 들어간 그
       표지입니다. 우리도 하나 더 만들고 있어서 둘이 되었습니다.
       원본 것이 더 낫습니다(사진이 있습니다). 우리 것을 뺍니다.
       제목과 부제는 fixCover() 가 원본 표지에 갈아 끼웁니다. */

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
      /* 장 표지를 먼저 한 쪽 놓고, 본문은 제목 없이 이어갑니다 —
         표지가 「제 N 장 · 제목」을 이미 말했으므로 두 번 쓰지 않습니다 */
      sheet(MARK[i3], e.t2, (i3<4?'one':'two'));
      page(h, null, (i3<4?'one':'two'));
    }

    return { html:pages.join(''), n:n,
             title:nm+'님의 가족운' };
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
  /* ★ 표지에서 **실제로 뜬** 사진 주소를 배워 둡니다 — 2026-09-16
     소희 님 「장표지는 왜 자꾸 스텔라 로고가 나오지?」
     표지 사진은 나오는데 장 속표지만 안 나옵니다. 표지 것은 원본 책이
     넣은 주소이고, 장 속표지는 우리가 아는 주소입니다. 우리 주소가
     이 사이트에서는 안 열린다는 뜻입니다(파일이 다른 이름이거나
     직접 주소가 막혔거나). 마지막 수단으로 **뜬 주소**를 씁니다.
     같은 문 사진이라 어색하지 않고, 빈 동그라미보다 낫습니다. */
  var COVSRC = '';
  function learnCover(root){
    try{
      var cov = root.querySelector('.page.cover');
      if(!cov){ return; }
      var ims = cov.querySelectorAll('img'), i, im, s;
      for(i = 0; i < ims.length; i++){
        im = ims[i];
        if(!im.complete){ continue; }
        if(!im.naturalWidth){ continue; }
        s = String(im.getAttribute('src'));
        if(s.indexOf('http') === 0){ COVSRC = s; return; }
      }
    }catch(e){}
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
    var go=function(){
      var step = Number(im.getAttribute('data-retry'));
      if(!step){ step = 0; }
      if(step >= 2){ return; }
      step++;
      im.setAttribute('data-retry', String(step));
      if(step === 1){
        /* 첫째 — 젯팩 주소로 한 번 더 */
        var u = altURL(im.getAttribute('src'));
        if(u){ im.setAttribute('src', u); return; }
        im.setAttribute('data-retry', '2');
        step = 2;
      }
      /* 둘째 — 표지에서 뜬 주소로 */
      if(COVSRC){
        if(String(im.getAttribute('src')) !== COVSRC){ im.setAttribute('src', COVSRC); }
      }
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

  /* ── 관리자 띠 ──────────────────────────────
     2026-09-16 · 소희 님 「가족운도 아직이야」
     새 판을 붙이셨는지 눈으로 확인할 길이 없었습니다.
     판 시각과 사진 상태를 찍습니다. 손님에게는 안 보입니다. */
  var ADMIN = <?php echo current_user_can( 'manage_options' ) ? 1 : 0; ?>;
  var STAMP = '2026-09-16 01:55';
  function band(msg){
    if(!ADMIN){ return; }
    try{
      var d = document.getElementById('stella-band-family');
      if(!d){
        d = document.createElement('div');
        d.id = 'stella-band-family';
        d.setAttribute('style', 'margin:12px;padding:10px 14px;'+
          'border:2px solid #2F7D4A;background:#F3F8F4;border-radius:8px;'+
          'font:13px/1.8 system-ui;color:#1d3a27;white-space:pre-wrap;');
        var ssb = document.getElementById('ssb');
        if(ssb){ if(ssb.parentNode){ ssb.parentNode.insertBefore(d, ssb); } }
        else if(document.body){ document.body.appendChild(d); }
      }
      d.textContent = '관리자에게만 보입니다 · 가족운 판 ' + STAMP +
        String.fromCharCode(10) + msg;
    }catch(e){}
  }

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
      var ims=root.querySelectorAll('.dvmark.dvface img'), i, im;
      for(i=0;i<ims.length;i++){
        im=ims[i];
        retryImg(im);
        /* ★ 두 번 시도했는데 아직 안 떴고, 그 사이에 표지에서 뜬
           주소를 배웠으면 그것을 물려 줍니다 (2026-09-16).
           재시도는 못 받자마자 끝나는데 표지 주소는 조금 뒤에야
           알 수 있어서, 여기서 한 번 더 기회를 줍니다. */
        if(COVSRC){
          if(im.complete){ if(!im.naturalWidth){
            if(String(im.getAttribute('src')) !== COVSRC){
              im.setAttribute('src', COVSRC);
            }
          } }
        }
      }
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
  var COVSUB='THE FAMILY';
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
            /* 표지 사진이 뜬 뒤에 그 주소를 배우고, 안 뜬 동그라미에 물려 줍니다 */
            setTimeout(function(){ learnCover(bk); fixFaces(bk); }, 900);
            setTimeout(function(){ learnCover(bk); fixFaces(bk); }, 2600);
                  bk.setAttribute('data-family','1');
                  /* 관리자에게 판 시각과 사진 상태를 알려 줍니다 */
                  band('그렸습니다 · ' + r.n + '쪽');
                  setTimeout(function(){
                    band('그렸습니다 · ' + r.n + '쪽' + String.fromCharCode(10) + picReport(bk));
                  }, 1400);
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
