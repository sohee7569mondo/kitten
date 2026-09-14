<?php
/* ═══════════════════════════════════════════════════════
   띠별운세 화면 손질   patch92_look
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   소희 님 : 「예전엔 내가 호랑이띠라서 들어가면 호랑이띠가
              강조되게 보였거든?」
              「동물 사진이 갑자기 바뀌었어. 예전 그림이 더 좋은데」
              「바탕이 남색에서 아이보리로 바뀌면서 디자인이 바뀐듯해」
              「디자인이 별로야. 무료라서 신경 안 쓴 듯한?」

   소희 님 말씀이 맞습니다. 2026-09-08 에 이 쪽을 흰 바탕으로
   덮으면서 남색 바탕을 전제로 하던 것들이 한꺼번에 묻혔습니다.

   ① 내 띠 강조가 안 보입니다
      쪽 CSS 는 #ssp .acard.mine{ border-color:var(--gold);
      box-shadow:0 0 0 1px var(--gold) } — **금빛 테 1px** 하나뿐입니다.
      남색 바탕에서는 확 띄었지만 아이보리에서는 거의 안 보입니다.
      강조가 안 되는 게 아니라 **안 보이는** 것이었습니다.

   ② 동물 자리가 이모지입니다
      소희 님 : 「사주운세에 넣은 그림을 넣으면 어떨까?」
      미디어에 띠 그림 열두 장이 이미 올라가 있습니다 —
      ji-rat · ji-ox · ji-tiger … ji-pig (2026/09).
      이모지를 그 그림으로 갈아끼웁니다. 폰에 따라 모양이 달라지는
      이모지와 달리 어디서나 같게 보이고, 사주풀이 쪽과도 결이 맞습니다.

   ③ 관계 딱지가 다 같은 회색입니다
      열두 띠가 이번주 기운과 맺는 관계는 네 가지인데 색이 하나라
      한눈에 안 갈립니다. 무료 쪽이 손님의 첫인상인데 아깝습니다.

   ④ 「무관」이 어렵습니다
      소희 님 : 「삼합 육합이 뭔 뜻인지 모르겠어」
      손님도 모릅니다. 한자말은 화면에서 걷어냅니다.
      쪽의 딱지는 「삼합 · 손이 맞는 주」처럼 **앞이 한자말, 뒤가
      쉬운 우리말**입니다. 그래서 앞을 떼기만 하면 됩니다 —
         같은 기운 · 손이 맞는 주 · 붙잡아 주는 주 ·
         흔들리는 주 · 어긋나는 주 · 잔잔한 주
      본문에는 「삼합(三合)으로 묶입니다」처럼 한자가 그대로 있어
      그것도 우리말로 바꿉니다.

   무엇을 하나
      · 내 띠 칸에 남색 테 두 겹과 「내 띠」 딱지
      · 동물 자리의 이모지를 띠 그림 열두 장으로 갈아끼웁니다
      · 관계 딱지를 넷으로 색을 갈라 줍니다
      · 딱지의 한자말을 쉬운 말로 바꿉니다
      · 열두 칸 위에 「이번주는 어떤 사이인가」 안내를 놓습니다
        · 내 띠가 정해지면 「호랑이띠이신 당신은 이번주 잔잔한 주를
          지납니다」 한 줄과 그 줄에 「내 띠」 표시
        (2026-09-14 · 소희 님 : 「삼합(띠 셋이 한편이 되는 것) —
         이렇게 넣으면 어때?」 좋은 생각입니다. 다만 두 가지를
         바로잡았습니다 —
         ① 육합과 충은 해마다 바뀌는 것이 아니라 **고정된 짝**입니다.
            쥐-소 · 범-돼지 · 토끼-개 · 용-닭 · 뱀-원숭이 · 말-양 (육합)
            쥐-말 · 소-양 · 범-원숭이 · 용-개 · 뱀-돼지 · 토끼-닭 (충)
            「2026년엔 토끼-개, 말-양」이라 쓰면 올해만 그런 것처럼
            읽힙니다.
         ② 이 쪽은 **이번주** 운세입니다. 카드 딱지가 이번주 기운
            기준이라 「2026년엔」이라고 쓰면 카드와 어긋납니다.
            삼재는 해 단위, 카드는 주 단위예요.
         ★ 그리고 제가 다시 세지 않습니다. **카드가 이미 붙여둔
           딱지를 읽어** 목록을 만듭니다. 두 번 세면 언젠가 어긋납니다.)
      · 칸에 생년이 있는데 강조가 없으면 「내 띠 찾기」를 눌러줍니다
      · 그것도 비었으면 로그인하신 분의 생년월일로 채워 눌러줍니다
        (브라우저를 바꾸면 저장값이 없어 강조가 안 되던 것을 메웁니다)

   ★ 쪽 글은 한 자도 안 고칩니다. 끄면 그대로 돌아갑니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_footer', function () {

	if ( ! is_page( 'zodiac-year' ) ) { return; }
	?>
<style id="stella-look-css">
/* ═══ 카드 디자인 ═══════════════════════════════════════
   2026-09-14 · 소희 님 : 「디자인이 별로야. 무료라서 신경 안 쓴 듯한?」
                          「너무 그냥 박스에 글만 넣은 듯한 느낌이 들어」
   맞습니다. 흰 상자 하나에 글이 쭉 이어져 층이 없었습니다.
   층을 셋으로 나눕니다 — 색 띠 · 머리 · 본문. */

#ssp .acard{
  position:relative; overflow:hidden;
  padding:0 !important;
  border-radius:16px !important;
  border:1px solid #E7E0D2 !important;
  background:#FFFFFF !important;
  box-shadow:0 1px 2px rgba(34,28,51,.04),
             0 14px 30px -20px rgba(34,28,51,.26) !important; }
#ssp .acard:hover{
  transform:translateY(-4px) !important;
  border-color:#D5CCB8 !important;
  box-shadow:0 1px 2px rgba(34,28,51,.05),
             0 26px 46px -22px rgba(34,28,51,.32) !important; }

/* ① 카드 맨 위 색 띠 — 한눈에 갈립니다 */
#ssp .acard:before{
  content:''; display:block; height:4px; background:#E2DACB; }
#ssp .acard[data-rel="합"]:before{ background:#2F7D4A; }
#ssp .acard[data-rel="짝"]:before{ background:#5A3FA0; }
#ssp .acard[data-rel="충"]:before{ background:#C4453A; }
#ssp .acard[data-rel="해"]:before{ background:#C08A3E; }
#ssp .acard[data-rel="무"]:before{ background:#DCD5C6; }

/* ② 머리 — 옅은 바탕에 그림과 이름, 딱지는 오른쪽 */
#ssp .ahead{
  margin:0 !important; padding:18px 20px 16px !important;
  gap:14px !important; align-items:center !important;
  flex-wrap:wrap !important;
  background:linear-gradient(180deg,#FAF7F0 0%,#FFFFFF 100%);
  border-bottom:1px solid #F1EBDD; }
#ssp .asym{
  width:66px !important; height:66px !important; flex:0 0 66px !important;
  padding:0 !important; overflow:hidden;
  background:#241C4E !important;
  border:1px solid #3A2E77 !important;
  box-shadow:0 8px 18px -9px rgba(36,28,78,.5) !important; }
#ssp .asym img{
  width:100%; height:100%; display:block;
  object-fit:cover; border-radius:50%; }
#ssp .asym[data-pic="no"]{ font-size:1.8rem !important; }
#ssp .aname{
  font-size:1.2rem !important; color:#221C33 !important;
  letter-spacing:-.01em; }
#ssp .ayears{
  margin-top:5px !important; font-size:.7rem !important;
  color:#A79FB8 !important; line-height:1.75; }

/* ③ 관계 딱지 — 머리 오른쪽으로, 색을 갈라서 */
#ssp .ahead .arel{
  margin:0 0 0 auto !important;
  padding:6px 13px !important; border-radius:20px;
  font-family:inherit !important;
  font-size:.76rem !important; font-weight:700 !important;
  letter-spacing:0 !important; }
#ssp .arel{
  display:inline-block;
  padding:5px 12px !important; border-radius:20px;
  font-family:inherit !important;
  font-size:.76rem !important; font-weight:700 !important;
  letter-spacing:0 !important; }
#ssp .arel[data-rel="합"]{
  background:#EDF7F0 !important; color:#2F7D4A !important;
  border:1px solid #BFE0C9 !important; }
#ssp .arel[data-rel="짝"]{
  background:#F3EFFA !important; color:#5A3FA0 !important;
  border:1px solid #D9CFF2 !important; }
#ssp .arel[data-rel="충"]{
  background:#FBEFEE !important; color:#C4453A !important;
  border:1px solid #EBC7C3 !important; }
#ssp .arel[data-rel="해"]{
  background:#FDF4EC !important; color:#A9611F !important;
  border:1px solid #EDD7BE !important; }
#ssp .arel[data-rel="무"]{
  background:#F7F3EA !important; color:#8B849C !important;
  border:1px solid #EAE2D2 !important; }

/* ④ 본문 — 첫 문단을 조금 크게 (읽는 눈이 걸릴 자리) */
#ssp .atext{
  margin:0 20px !important; padding-top:14px;
  font-size:.94rem !important; line-height:1.9 !important;
  color:#4E4763 !important; }
#ssp .ahead + .atext{
  font-size:1rem !important; color:#332B47 !important; }
#ssp .atext + .atext{ padding-top:10px; }

/* ⑤ 아래 표 — 줄을 나누고 이름은 작게 */
#ssp .arows{
  margin:16px 20px 18px !important; padding-top:12px !important;
  border-top:1px solid #F1EBDD !important; }
#ssp .arow{
  padding:9px 0 !important; font-size:.87rem !important;
  border-bottom:1px dashed #F1EBDD; }
#ssp .arow:last-child{ border-bottom:0; }
#ssp .arow dt{
  flex:0 0 82px !important; font-family:inherit !important;
  font-size:.78rem !important; color:#9A92AC !important;
  padding-top:2px !important; }
#ssp .arow dd{ color:#221C33 !important; font-weight:500; }
#ssp .swatch{
  width:14px !important; height:14px !important; border-radius:50% !important;
  margin-right:7px !important;
  border:1px solid rgba(34,28,51,.14) !important;
  box-shadow:0 1px 3px rgba(34,28,51,.18) !important; }
#ssp .amine{
  margin:0 20px 18px !important; padding:11px 13px;
  border-radius:9px; background:#F3EFFA;
  font-size:.86rem !important; color:#4A3A86 !important; line-height:1.8; }

/* ⑥ 내 띠 — 아이보리 바탕에서도 한눈에 */
#ssp .acard.mine{
  border-color:#3A2E77 !important;
  box-shadow:0 0 0 2px #3A2E77,
             0 22px 46px -24px rgba(58,46,119,.5) !important; }
#ssp .acard.mine .ahead{
  background:linear-gradient(180deg,#F3EFFA 0%,#FFFFFF 100%) !important;
  border-bottom-color:#E4DBF6 !important; }
#ssp .acard.mine .aname:after{
  content:'내 띠'; margin-left:8px; padding:3px 10px; border-radius:20px;
  background:#3A2E77; color:#FFFDF9;
  font-size:.68rem; font-weight:800; vertical-align:middle; }

/* ⑤ 이번주는 어떤 사이인가 — 열두 칸 위 안내 */
#relBox{ margin:30px 0 6px; padding:18px 0; text-align:left;
  border-top:1px solid rgba(128,128,128,.28);
  border-bottom:1px solid rgba(128,128,128,.28); }
#relBox h3{ margin:0 0 12px; font-size:1.02rem; font-weight:700; }
#relBox .rb{ display:flex; gap:11px; align-items:baseline;
  padding:7px 0; flex-wrap:wrap; }
#relBox .rb .k{ flex:0 0 auto; }
#relBox .rb .who{ font-weight:700; }
#relBox .rb .why{ font-size:.9rem; opacity:.72; flex:1 1 16em;
  min-width:12em; line-height:1.75; }
#relBox .rb.me{ background:#FBF9F4; border-radius:9px;
  padding:11px 13px; margin:4px -13px;
  box-shadow:0 0 0 1px #3A2E77 inset; }
#relBox .rb.me .who{ color:#3A2E77; }
#relBox .rb .memark{ margin-left:7px; padding:3px 9px; border-radius:20px;
  background:#3A2E77; color:#FFFDF9; font-size:.68rem; font-weight:800; }
#relBox .mine1{ margin:0 0 13px; font-size:1rem; line-height:1.8; }
#relBox .mine1 b{ color:#3A2E77; }

/* ③ 관계 딱지 — 넷으로 색을 가릅니다 */
#ssp .arel{
  display:inline-block; padding:5px 12px !important; border-radius:20px;
  font-size:.76rem !important; font-weight:700 !important;
  letter-spacing:.02em; }
#ssp .arel[data-rel="합"]{
  background:#EDF7F0 !important; color:#2F7D4A !important;
  border:1px solid #BFE0C9 !important; }
#ssp .arel[data-rel="짝"]{
  background:#F3EFFA !important; color:#5A3FA0 !important;
  border:1px solid #D9CFF2 !important; }
#ssp .arel[data-rel="충"]{
  background:#FBEFEE !important; color:#C4453A !important;
  border:1px solid #EBC7C3 !important; }
#ssp .arel[data-rel="해"]{
  background:#FDF4EC !important; color:#A9611F !important;
  border:1px solid #EDD7BE !important; }
#ssp .arel[data-rel="무"]{
  background:#F7F3EA !important; color:#8B849C !important;
  border:1px solid #EAE2D2 !important; }
</style>
<script>
(function(){
  if(window.StellaLook){ return; }
  window.StellaLook = 1;

  function num(v){
    var n = parseInt(String(v === undefined ? '' : v), 10);
    if(isNaN(n)){ return 0; }
    return n;
  }

  /* ② 띠 그림 — 미디어에 올라가 있는 열두 장 */
  var UP = 'https://i0.wp.com/stellasaju.com/wp-content/uploads/2026/09/';
  var FILE = ['rat', 'ox', 'tiger', 'rabbit', 'dragon', 'snake',
              'horse', 'goat', 'monkey', 'rooster', 'dog', 'pig'];
  var ANIMAL = ['쥐', '소', '범', '토끼', '용', '뱀',
                '말', '양', '원숭이', '닭', '개', '돼지'];

  function pics(){
    var cards = document.querySelectorAll('#ssp .acard[data-z]');
    var i, z, sym;
    for(i = 0; i < cards.length; i++){
      if(cards[i].getAttribute('data-pic') === '1'){ continue; }
      z = parseInt(cards[i].getAttribute('data-z'), 10);
      if(isNaN(z)){ continue; }
      if(z < 0){ continue; }
      if(z > 11){ continue; }
      sym = cards[i].querySelector('.asym');
      if(!sym){ continue; }

      /* 그림이 안 뜨면 빈 동그라미만 남습니다. 원래 이모지를 적어두고
         못 불러올 때 되살립니다 (2026-09-14 · 크로미움으로 그려보다가
         그림이 없을 때 남색 원만 남는 것을 보고 넣었습니다). */
      var keep = String(sym.textContent);
      sym.setAttribute('data-emoji', keep);
      sym.innerHTML = '<img loading="lazy" decoding="async" alt="'
        + ANIMAL[z] + '띠" src="' + UP + 'ji-' + FILE[z]
        + '.webp.jpg?resize=128%2C128">';
      (function(box){
        var im = box.querySelector('img');
        if(!im){ return; }
        im.onerror = function(){
          box.textContent = box.getAttribute('data-emoji');
          box.setAttribute('data-pic', 'no');
        };
      })(sym);
      cards[i].setAttribute('data-pic', '1');
    }
  }

  /* ④ 한자말을 쉬운 말로 — 앞의 갈래 이름만 갈아끼웁니다 */
  var WORD = [
    ['무관', '잔잔'],
    ['삼합', '잘 맞음'],
    ['육합', '짝'],
    ['반합', '잘 맞음'],
    ['충', '부딪힘'],
    ['형', '껄끄러움'],
    ['해', '어긋남'],
    ['파', '흔들림'],
    ['원진', '거스름']
  ];

  /* 갈래 판단 — 쪽이 실제로 쓰는 말 그대로 봅니다
     비화 · 같은 기운   삼합 · 손이 맞는 주   육합 · 붙잡아 주는 주
     충 · 흔들리는 주   해 · 어긋나는 주      무관 · 잔잔한 주      */
  function relKind(t){
    if(t.indexOf('무관') > -1){ return '무'; }
    if(t.indexOf('잔잔') > -1){ return '무'; }
    if(t.indexOf('충') > -1){ return '충'; }
    if(t.indexOf('흔들') > -1){ return '충'; }
    if(t.indexOf('해 ') > -1){ return '해'; }
    if(t.indexOf('어긋') > -1){ return '해'; }
    if(t.indexOf('육합') > -1){ return '짝'; }
    if(t.indexOf('붙잡') > -1){ return '짝'; }
    if(t.indexOf('삼합') > -1){ return '합'; }
    if(t.indexOf('손이 맞') > -1){ return '합'; }
    if(t.indexOf('비화') > -1){ return '합'; }
    if(t.indexOf('같은 기운') > -1){ return '합'; }
    return '무';
  }

  /* 본문에 남은 한자 — 손님이 읽는 글입니다 */
  var BODY = [
    ['삼합(三合)으로 묶입니다', '한편이 됩니다'],
    ['육합(六合)으로 만납니다', '서로 붙잡아 주는 사이로 만납니다'],
    ['충(沖)은 나쁜 게 아니라', '부딪힌다는 것은 나쁜 게 아니라'],
    ['삼합(三合)', '한편'],
    ['육합(六合)', '붙잡아 주는 사이'],
    ['충(沖)', '부딪힘'],
    ['비화(比和)', '같은 기운'],
    ['해(害)', '어긋남']
  ];

  function plain(){
    var ps = document.querySelectorAll('#ssp .acard .atext');
    var i, j, el, t, was;
    for(i = 0; i < ps.length; i++){
      el = ps[i];
      if(el.getAttribute('data-plain') === '1'){ continue; }
      was = String(el.textContent);
      t = was;
      for(j = 0; j < BODY.length; j++){
        t = t.split(BODY[j][0]).join(BODY[j][1]);
      }
      if(t !== was){ el.textContent = t; }
      el.setAttribute('data-plain', '1');
    }
  }

  function tidy(){
    var rs = document.querySelectorAll('#ssp .arel');
    var i, el, t, k, j;
    for(i = 0; i < rs.length; i++){
      el = rs[i];
      if(el.getAttribute('data-rel')){ continue; }
      t = String(el.textContent);
      k = relKind(t);
      for(j = 0; j < WORD.length; j++){
        t = t.split(WORD[j][0]).join(WORD[j][1]);
      }
      /* 「삼합 · 한 무리인 주」처럼 앞에 갈래 이름이 붙어 있으면
         뒤쪽만 남깁니다. 뒤쪽이 이미 쉬운 우리말이라 그것으로 충분하고,
         「부딪힘 · 부딪히는 주」처럼 같은 말이 두 번 나오는 것도 막습니다. */
      var bits = t.split('·');
      if(bits.length === 2){
        var tail = bits[1].split(' ').join('');
        if(tail){ t = bits[1]; }
      }
      while(t.charAt(0) === ' '){ t = t.slice(1); }
      el.textContent = t.split('  ').join(' ');
      el.setAttribute('data-rel', k);

      /* 카드에도 갈래를 적어 맨 위 색 띠를 칠합니다 */
      var card = el.parentNode;
      while(card){
        if(card.className.indexOf('acard') > -1){ break; }
        card = card.parentNode;
        if(!card){ break; }
        if(card === document.body){ card = null; break; }
      }
      if(card){
        card.setAttribute('data-rel', k);
        /* 딱지를 머리 오른쪽으로 옮깁니다 */
        var hd = card.querySelector('.ahead');
        if(hd){ if(el.parentNode !== hd){ hd.appendChild(el); } }
      }
    }
    return rs.length;
  }

  /* 로그인하신 분의 생년월일 */
  function me(){
    var u = window.STELLA_USER;
    if(!u){ return null; }
    var p = u.profile ? u.profile : u;
    if(!p){ return null; }
    if(!p.year){ return null; }
    return { y: num(p.year), m: num(p.month), d: num(p.day) };
  }

  function findMine(){
    var btn = document.getElementById('zFind');
    var yIn = document.getElementById('zYear');
    var grid = document.getElementById('zGrid');
    if(!btn){ return; }
    if(!yIn){ return; }
    if(!grid){ return; }
    if(grid.querySelector('.acard.mine')){ return; }

    if(!num(yIn.value)){
      var m = me();
      if(!m){ return; }
      yIn.value = m.y;
      var mIn = document.getElementById('zMon');
      var dIn = document.getElementById('zDay');
      if(mIn){ if(m.m){ mIn.value = m.m; } }
      if(dIn){ if(m.d){ dIn.value = m.d; } }
    }
    btn.click();
  }

  /* ⑤ 이번주는 어떤 사이인가 — 카드가 붙여둔 딱지를 읽어 모읍니다.
     제가 다시 세지 않습니다. 두 번 세면 언젠가 어긋납니다. */
  /* 갈래별 풀이. 비화(같은 기운)는 삼합과 색은 같아도 뜻이 다르므로
     딱지 글로 먼저 찾고, 없으면 갈래로 물러납니다. */
  var WHY_TAG = {
    '같은 기운': '이번주 기운이 이 띠와 **같은 결**로 들어옵니다. 힘이 두 배로 '
        + '실리는 대신 고집도 같이 세집니다. 밀어붙일 일이 있다면 이번주예요.'
  };
  var WHY = {
    '합': '띠 셋이 **한편**이 되는 자리예요. 혼자 하던 일에 사람이 붙고, '
        + '부탁이 잘 통합니다.',
    '짝': '둘이 **짝**을 이루는 자리입니다. 크게 뻗기보다 안으로 단단해져요. '
        + '미뤄둔 정리와 재계약에 좋습니다.',
    '충': '정면으로 **부딪히는** 자리예요. 붙어 있던 것이 떨어지고 미뤄둔 것이 '
        + '터져 나옵니다. 이동과 정리에는 오히려 힘이 실립니다.',
    '해': '살짝 **어긋나는** 자리입니다. 크게 무너지진 않는데 말이 헛돌고 '
        + '일정이 밀립니다. 약속은 한 번 더 확인하세요.',
    '무': '이번주 기운과 특별히 얽히지 않습니다. 내가 정한 속도로 가기 좋아요.'
  };
  var ORDER = ['합', '짝', '충', '해', '무'];

  function whyOf(tag, k){
    if(WHY_TAG[tag]){ return WHY_TAG[tag]; }
    return WHY[k] ? WHY[k] : '';
  }

  /* 굵게 — 별표 두 개로 감싼 곳만 */
  function bold(t){
    var bits = String(t).split('**');
    var out = '', i;
    for(i = 0; i < bits.length; i++){
      out += (i % 2) ? ('<b>' + bits[i] + '</b>') : bits[i];
    }
    return out;
  }

  /* 이번주가 무슨 띠인가 — 쪽이 이미 찍어둔 간지에서 읽습니다.
     2026-09-14 · 소희 님 : 「호랑이띠의 기운과 열두 띠는 이런
     사이입니다」 — 제목에 띠를 넣자는 말씀이 맞습니다. 다만 이번주
     기운은 호랑이가 아니라 **토끼**(辛卯)입니다. 쪽 위에 「신묘 ·
     토끼의 자리」라고 나와 있어요. 호랑이는 소희 님 띠고요.
     그래서 제가 정하지 않고 쪽이 세운 간지에서 그때그때 읽습니다. */
  var JI_H = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];

  function weekAnimal(){
    var el = document.getElementById('zGz');
    if(!el){ return ''; }
    var t = String(el.textContent);
    var i;
    for(i = 0; i < JI_H.length; i++){
      if(t.indexOf(JI_H[i]) > -1){ return ANIMAL[i]; }
    }
    /* 한자를 못 찾으면 한글 풀이에서 — 「신묘 · 토끼의 자리」 */
    var k = document.getElementById('zGzk');
    if(k){
      var s2 = String(k.textContent);
      for(i = 0; i < ANIMAL.length; i++){
        if(s2.indexOf(ANIMAL[i] + '의 자리') > -1){ return ANIMAL[i]; }
      }
    }
    return '';
  }

  function relBox(){
    if(document.getElementById('relBox')){ return; }
    var grid = document.getElementById('zGrid');
    if(!grid){ return; }
    var cards = grid.querySelectorAll('.acard[data-z]');
    if(cards.length < 12){ return; }

    /* 딱지 **글**로 모읍니다. 갈래(색)로 모으면 「같은 기운」과
       「손이 맞는 주」가 한 줄로 묶여버립니다 — 색은 같아도 뜻이
       다릅니다 (2026-09-14 에 검사에서 잡았습니다). */
    var bag = {}, keys = [], i, z, el, k, tag, name;
    for(i = 0; i < cards.length; i++){
      el = cards[i].querySelector('.arel');
      if(!el){ continue; }
      k = el.getAttribute('data-rel');
      if(!k){ continue; }
      tag = String(el.textContent);
      z = parseInt(cards[i].getAttribute('data-z'), 10);
      if(isNaN(z)){ continue; }
      if(!bag[tag]){ bag[tag] = { rel: k, who: [] }; keys.push(tag); }
      bag[tag].who.push(ANIMAL[z] + '띠');
    }

    /* 합 → 짝 → 충 → 해 → 잔잔 차례로, 같은 갈래는 나온 차례로 */
    var sorted = [], oi, ki;
    for(oi = 0; oi < ORDER.length; oi++){
      for(ki = 0; ki < keys.length; ki++){
        if(bag[keys[ki]].rel === ORDER[oi]){ sorted.push(keys[ki]); }
      }
    }

    var wa = weekAnimal();
    var title = wa
      ? ('이번주는 ' + wa + '의 기운입니다 — 열두 띠와 이런 사이예요')
      : '이번주 기운과 열두 띠는 이런 사이입니다';
    var h = '<h3>' + title + '</h3>';
    var got = 0;
    for(i = 0; i < sorted.length; i++){
      tag = sorted[i];
      k = bag[tag].rel;
      if(k === '무'){
        name = (bag[tag].who.length > 6) ? '나머지 띠' : bag[tag].who.join(' · ');
      } else {
        name = bag[tag].who.join(' · ');
      }
      h += '<div class="rb">'
        + '<span class="k"><span class="arel" data-rel="' + k + '">'
        + tag + '</span></span>'
        + '<span class="who">' + name + '</span>'
        + '<span class="why">' + bold(whyOf(tag, k)) + '</span>'
        + '</div>';
      got++;
    }
    if(got === 0){ return; }

    var box = document.createElement('div');
    box.id = 'relBox';
    box.innerHTML = h;
    grid.parentNode.insertBefore(box, grid);
  }

  /* 내 띠가 정해지면 그 줄을 짚어 줍니다.
     2026-09-14 · 소희 님 : 「그냥 이번주 기운과 열두 띠라 하니까
     모르겠더라고. 누구 얘기인지」 — 제목에 이번주 띠를 넣는 것만으로는
     모자랍니다. 손님이 궁금한 것은 **내 띠가 어디 있느냐**입니다.
     쪽이 mine 을 늦게 붙일 수 있어 따로 지켜보다가 표시합니다. */
  function markMine(){
    var box = document.getElementById('relBox');
    if(!box){ return; }
    if(box.getAttribute('data-me') === '1'){ return; }
    var card = document.querySelector('#zGrid .acard.mine');
    if(!card){ return; }
    var z = parseInt(card.getAttribute('data-z'), 10);
    if(isNaN(z)){ return; }
    var tag = card.querySelector('.arel');
    if(!tag){ return; }
    var want = String(tag.textContent);

    var rows = box.querySelectorAll('.rb');
    var i, t;
    for(i = 0; i < rows.length; i++){
      t = rows[i].querySelector('.arel');
      if(!t){ continue; }
      if(String(t.textContent) !== want){ continue; }
      rows[i].className = 'rb me';
      var m = document.createElement('span');
      m.className = 'memark';
      m.textContent = '내 띠';
      rows[i].querySelector('.who').appendChild(m);
      break;
    }

    var one = document.createElement('p');
    one.className = 'mine1';
    one.innerHTML = '<b>' + ANIMAL[z] + '띠</b>이신 당신은 이번주 '
      + '<b>' + want + '</b>를 지납니다.';
    box.insertBefore(one, box.querySelector('.rb'));
    box.setAttribute('data-me', '1');
  }

  function run(){
    var grid = document.getElementById('zGrid');
    if(!grid){ return 0; }
    if(grid.querySelectorAll('.acard').length < 12){ return 0; }
    pics();
    tidy();
    plain();
    findMine();
    relBox();
    markMine();
    return 1;
  }

  function watch(){
    var ready = run();
    var n = 0;
    var t = setInterval(function(){
      n++;
      if(!ready){ ready = run(); }
      else { markMine(); }   /* 쪽이 늦게 내 띠를 붙여도 잡습니다 */
      if(n > 60){ clearInterval(t); }
    }, 300);
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', watch);
  } else {
    watch();
  }
})();
</script>
	<?php
} );
