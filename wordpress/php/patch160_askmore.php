<?php
/* ═══════════════════════════════════════════════════════
   홈 아래 줄 — 가디언 소개를 주제 배너로       patch160_askmore
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」
   ★ patch160_nydoor 가 먼저 들어가 있어야 합니다 — 2026·2027 을
     가르는 것이 그 조각입니다.

   소희 님 : 「여기 가디언소개 말고 2026운세 2027운세 건강운 가족운
              인생총운 삼재 배너를 넣자고」

   무엇을 바꾸나
   지금 넷 : 건강·가족 / 흐름·시기 / 점성술 / 스텔라타로 (문 소개)
   바꾼 뒤 : 2026년 운세 · 2027년 운세 · 건강운 · 가족운 ·
             인생총운 · 삼재 (주제 배너 여섯)
   위 줄들과 같은 ask-card 꼴이라 홈 전체가 한 결로 읽힙니다.

   ★ 점성술 · 스텔라타로는 홈에서 사라집니다
     다만 사이트 머리글 차림표에 그대로 있습니다 (별을 읽는 신 ·
     아르카나). 그래도 홈에 두고 싶으시면 말씀만 주세요 — 뒤에 두 장
     더 붙이면 됩니다.

   왜 앵커를 안 잡나
   살아 있는 홈은 제 사본보다 새롭습니다. 글자를 잡으면 한 칸 차이로
   「0군데」가 납니다. 그래서 /door-astro/ 로 가는 카드를 찾아 그
   카드가 든 줄(rail)을 통째로 갈아 끼웁니다 — 사본이 낡아도 맞습니다.

   ★ 점(dots)을 다시 그립니다
     홈의 줄 스크립트는 처음에 카드 수를 세어 두고 그 수만큼 점을
     만듭니다. 넷에서 여섯으로 늘었으니 점도 여섯으로 다시 그리고,
     어느 점을 켤지도 우리가 다시 셉니다. 우리 것이 나중에 걸리므로
     옛 셈을 덮습니다.

   되돌리기
   이 스니펫을 끄면 원래대로 돌아옵니다. 쪽을 안 건드립니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_head', function () {
	/* ★ 홈에서만 씁니다 — 이 줄은 홈에만 있습니다. */
	if ( ! is_front_page() ) { return; }
	?>
<style id="stella-askmore-css">
/* 오픈기념 무료 딱지 — 2026-09-14 · 소희 님 「무료 표시를 좀 눈에 확 띄게」
   ① 붉은 바탕에 흰 글씨. 사진이 보랏빛이라 붉은색이 제일 튑니다.
   ② 주제 딱지(왼쪽 위)와 같은 줄에 두면 좁은 화면에서 부딪힙니다.
      그래서 주제 딱지 바로 아래에 쌓습니다 — 어느 폭에서도 안 겹칩니다.
   ③ 글씨를 키우고 그림자를 줘서 사진 위에 떠 보이게 합니다. */
#stellar-home .ask-card .freetag{
  position:absolute; top:46px; left:12px; z-index:6;
  font-size:.82rem; letter-spacing:.02em; font-weight:800;
  color:#FFFDF9; background:#C4453A;
  border-radius:6px; padding:6px 13px; line-height:1.5;
  box-shadow:0 8px 20px -6px rgba(196,69,58,.75),
             0 0 0 3px rgba(255,253,249,.22); }
@media(max-width:420px){
  #stellar-home .ask-card .freetag{
    top:42px; font-size:.74rem; padding:5px 11px; } }
</style>
<script>
(function(){
  if(window.StellaAskMore){ return; }
  window.StellaAskMore = 1;

  var UP = '/wp-content/uploads/2026/09/';
  var GO = ' ' + String.fromCharCode(8250);   /* › — 앰퍼샌드를 안 씁니다 */

  /* [ 문, 주제, 사진, 딱지, 질문, 가디언, 무료딱지 ]
     2026-09-14 · 소희 님 : 「2026년운세를 제일 앞에 오픈기념 무료라는
     버튼을 위에 넣어줘」 · 「무조건 유료로 시작을 해도 되는게
     2026 신년운세도 공짜고」
     무료를 상품 하나로 옮기면 가입 축하 구슬을 안 줘도 됩니다 —
     손님은 여기서 한 권을 통째로 맛보고, 결제창은 살아 있습니다. */
  var CARDS = [
    ['/door-fortune/', '2026년 운세', 'STELLASAJU_FORTUNE-2026.jpg',
     '2026년 운세', '올해 왜 이렇게 안 풀렸을까요?', '미르', '오픈기념 무료'],
    ['/door-fortune/', '2027년 운세', 'STELLASAJU_FORTUNE-2027.jpg',
     '2027년 운세', '내년엔 좀 나아질까요?', '미르'],
    ['/door-health/',  '건강운', 'STELLASAJU_HEALTH-CAR.jpg',
     '건강운', '왜 나만 이렇게 피곤할까요?', '아람'],
    ['/door-health/',  '가족운', 'STELLASAJU_family.jpg',
     '가족운', '가족인데 왜 이렇게 어려울까요?', '아람'],
    ['/door-fortune/', '평생운', 'STELLASAJU_turn.jpg',
     '인생총운', '제 인생은 지금 어디쯤일까요?', '미르'],
    ['/door-fortune/', '삼재', 'STELLASAJU_samjae.jpg',
     '삼재', '삼재, 언제쯤 끝날까요?', '미르']
  ];

  var HEAD = {
    kick: '올해와 내년 · 몸과 가족 · 인생의 큰 흐름',
    dek : '한 해가 어떻게 흐를지, 몸이 왜 무거운지, '
        + '지금이 인생의 어디쯤인지 봅니다.'
  };

  function cdn(file){
    return 'https://i0.wp.com/' + location.host + UP + file + '?resize=640%2C960';
  }

  function card(c){
    var a = document.createElement('a');
    a.className = 'ask-card';
    a.setAttribute('href', c[0] + '?topic=' + encodeURIComponent(c[1]));

    var wrap = document.createElement('div');
    wrap.className = 'imgwrap';
    var img = document.createElement('img');
    img.setAttribute('loading', 'lazy');
    img.setAttribute('decoding', 'async');
    img.setAttribute('width', '640');
    img.setAttribute('height', '960');
    img.setAttribute('alt', c[3]);
    img.setAttribute('src', cdn(c[2]));
    wrap.appendChild(img);

    var tag = document.createElement('span');
    tag.className = 'tag';
    tag.textContent = c[3];

    /* 무료 딱지 — 있는 배너에만 붙습니다 */
    var free = null;
    if(c[6]){
      free = document.createElement('span');
      free.className = 'freetag';
      free.textContent = c[6];
    }

    var info = document.createElement('div');
    info.className = 'info';
    var q = document.createElement('div');
    q.className = 'q';
    q.textContent = c[4];
    var go = document.createElement('div');
    go.className = 'go';
    go.textContent = c[5] + '에게 물어보기' + GO;
    info.appendChild(q);
    info.appendChild(go);

    a.appendChild(wrap);
    a.appendChild(tag);
    if(free){ a.appendChild(free); }
    a.appendChild(info);
    return a;
  }

  /* 점을 다시 그리고, 어느 점을 켤지도 우리가 셉니다 */
  function redots(rail){
    var bar = rail.nextElementSibling;
    if(!bar){ return; }
    if(String(bar.className).indexOf('railbar') < 0){ return; }
    var dots = bar.querySelector('[data-dots]');
    if(!dots){ return; }
    var kids = rail.children, n = kids.length, i;
    dots.innerHTML = '';
    for(i = 0; i < n; i++){ dots.appendChild(document.createElement('i')); }
    function paint(){
      var mid = rail.scrollLeft + rail.clientWidth / 2;
      var best = 0, bestD = 1e9, j, c, cc, d;
      for(j = 0; j < n; j++){
        c = kids[j];
        cc = c.offsetLeft + c.offsetWidth / 2;
        d = Math.abs(cc - mid);
        if(d < bestD){ bestD = d; best = j; }
      }
      for(j = 0; j < n; j++){
        dots.children[j].className = (j === best) ? 'on' : '';
      }
    }
    rail.addEventListener('scroll', paint);
    window.addEventListener('resize', paint);
    paint();
  }

  function head(rail){
    var rh = rail.previousElementSibling;
    if(!rh){ return; }
    if(String(rh.className).indexOf('rowhead') < 0){ return; }
    var k = rh.querySelector('.kick');
    if(k){ k.textContent = HEAD.kick; }
    var d = rh.querySelector('.rh-d');
    if(!d){ return; }
    /* 「미리보기」 단추는 그대로 두고 앞의 글만 바꿉니다 */
    var btn = d.querySelector('.sbtn');
    d.textContent = HEAD.dek;
    if(btn){ d.appendChild(btn); }
  }

  var tries = 0;
  function run(){
    var seed = document.querySelector('a.door-card[href$="/door-astro/"]');
    if(!seed){ return 0; }
    var rail = seed.parentNode;
    if(!rail){ return 0; }
    if(rail.getAttribute('data-askmore') === '1'){ return 1; }
    rail.setAttribute('data-askmore', '1');
    rail.innerHTML = '';
    var i;
    for(i = 0; i < CARDS.length; i++){ rail.appendChild(card(CARDS[i])); }
    head(rail);
    redots(rail);
    return 1;
  }

  if(!run()){
    document.addEventListener('DOMContentLoaded', function(){ run(); });
    var t = setInterval(function(){
      tries++;
      if(run()){ clearInterval(t); return; }
      if(tries > 40){ clearInterval(t); }
    }, 250);
  }
})();
</script>
	<?php
} );
