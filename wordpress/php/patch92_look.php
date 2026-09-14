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
      · 칸에 생년이 있는데 강조가 없으면 「내 띠 찾기」를 눌러줍니다
      · 그것도 비었으면 로그인하신 분의 생년월일로 채워 눌러줍니다
        (브라우저를 바꾸면 저장값이 없어 강조가 안 되던 것을 메웁니다)

   ★ 쪽 글은 한 자도 안 고칩니다. 끄면 그대로 돌아갑니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_footer', function () {

	if ( ! is_page( 'zodiac-year' ) ) { return; }
	?>
<style id="stella-look-css">
/* ① 내 띠 — 아이보리 바탕에서도 한눈에 */
#ssp .acard.mine{
  border-color:#3A2E77 !important;
  box-shadow:0 0 0 2px #3A2E77,
             0 20px 44px -24px rgba(58,46,119,.55) !important;
  background:#FBF9F4 !important; }
#ssp .acard.mine .aname:after{
  content:'내 띠'; margin-left:8px; padding:3px 10px; border-radius:20px;
  background:#3A2E77; color:#FFFDF9;
  font-size:.68rem; font-weight:800; vertical-align:middle; }

/* ② 동물 자리 — 그림으로 */
#ssp .asym{
  width:64px !important; height:64px !important; flex:0 0 64px !important;
  padding:0 !important; overflow:hidden;
  background:#241C4E !important;
  border:1px solid #3A2E77 !important;
  box-shadow:0 8px 18px -9px rgba(36,28,78,.55) !important; }
#ssp .asym img{
  width:100%; height:100%; display:block;
  object-fit:cover; border-radius:50%; }

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
      sym.innerHTML = '<img loading="lazy" decoding="async" alt="'
        + ANIMAL[z] + '띠" src="' + UP + 'ji-' + FILE[z]
        + '.webp.jpg?resize=128%2C128">';
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

  function run(){
    var grid = document.getElementById('zGrid');
    if(!grid){ return 0; }
    if(grid.querySelectorAll('.acard').length < 12){ return 0; }
    pics();
    tidy();
    plain();
    findMine();
    return 1;
  }

  function watch(){
    if(run()){ return; }
    var n = 0;
    var t = setInterval(function(){
      n++;
      if(run()){ clearInterval(t); return; }
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
