<?php
/* ═══════════════════════════════════════════════════════
   무료 배너에 사진 얹기            patch160_freeimg
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」
   ★ patch160_freelabel 과 짝입니다 — 그것이 글씨를, 이것이 사진을
     맡습니다. 둘 다 주소(href)로 배너를 찾으므로 서로 안 부딪힙니다.

   무엇을 하나
   소희 님 : 「무료풀이운세 배너들이 너무 약해서 그것도 수정하자」
   지금 무료 배너는 색 타일뿐이라 유료 배너(사진 + 아래 검은
   그라데이션 + 흰 글씨) 옆에서 확실히 약합니다. 같은 결로 맞춥니다.

   ★ 아직 안 올라온 사진은 스스로 물러납니다
     사진이 없으면(404) img 의 onerror 가 사진 층을 통째로 걷어내고
     지금 모습 그대로 돌아갑니다. 그래서 여섯 장을 다 안 올리셔도
     화면이 안 깨집니다 — 올리는 대로 한 장씩 살아납니다.

   왜 앵커를 안 잡나
   살아 있는 홈은 제 사본보다 새롭습니다. 글자를 잡아 바꾸면 한 칸
   차이로 「0군데」가 납니다. 그래서 a.free-card 를 주소로 찾아
   사진 층만 앞에 끼웁니다 — 사본이 낡아도 맞습니다.

   되돌리기
   이 스니펫을 끄면 원래대로 돌아옵니다. 쪽을 안 건드립니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_head', function () {
	?>
<style id="stella-freeimg-css">
/* 우리가 사진을 얹은 배너에만 걸립니다 — 깃발이 붙은 것만.
   다른 배너는 건드리지 않습니다. */
#stellar-home a.free-card[data-freeimg="1"]{
  aspect-ratio:2/3; min-height:0; overflow:hidden;
  background:var(--paper-2); }
#stellar-home a.free-card[data-freeimg="1"] .fimg{
  position:absolute; inset:0; z-index:0; overflow:hidden; }
#stellar-home a.free-card[data-freeimg="1"] .fimg img{
  width:100%; height:100%; object-fit:cover; display:block; }
/* 유료 배너(.ask-card)와 똑같은 그라데이션입니다 */
#stellar-home a.free-card[data-freeimg="1"] .fimg::after{
  content:''; position:absolute; inset:0; z-index:2;
  background:linear-gradient(to top,
    rgba(16,11,34,.94) 4%, rgba(16,11,34,.48) 44%, rgba(16,11,34,.04) 76%); }
/* 로또 배너는 홈 줄에서 뺍니다 (소희 님: 「로또 없애자」).
   ★ 쪽(/lotto/)은 그대로 있습니다 — 배너만 안 보이게 합니다.
     지우지 않고 숨기는 까닭 : 가로로 미는 줄(rail)에 딸린 스크립트가
     배너 수를 세고 있을 수 있어, 통째로 들어내면 화살표 셈이 틀어집니다.
     display:none 이면 자리도 안 차지하면서 줄은 안 건드립니다. */
#stellar-home a.free-card[data-freehide="1"]{ display:none !important; }

/* 글씨는 사진 위로 올리고 흰색으로.
   ★ 「Free」 딱지는 원래 position:absolute 로 오른쪽 위에 붙어 있습니다.
     여기서 통째로 relative 로 덮으면 딱지가 흐름 안으로 들어와
     가로로 늘어나면서 글씨를 덮습니다 (크로미움으로 보고 잡았습니다).
     그래서 딱지만 absolute 를 다시 박아 둡니다. */
#stellar-home a.free-card[data-freeimg="1"] > *{ position:relative; z-index:3; }
#stellar-home a.free-card[data-freeimg="1"] > .free-tag{ position:absolute; z-index:4; }
#stellar-home a.free-card[data-freeimg="1"] .free-kicker{ color:rgba(255,253,249,.82); }
#stellar-home a.free-card[data-freeimg="1"] .free-sub,
#stellar-home a.free-card[data-freeimg="1"] .free-line{ color:#FFFDF9; }
#stellar-home a.free-card[data-freeimg="1"] .free-date{ color:#FFFDF9 !important; }
#stellar-home a.free-card[data-freeimg="1"] .free-tag{
  color:#FFFDF9; border-color:rgba(255,253,249,.72);
  background:rgba(16,11,34,.32); }
</style>
<script>
(function(){
  if(window.StellaFreeImg){ return; }
  window.StellaFreeImg = 1;

  /* 올린 파일 이름은 소희 님과 맞춘 것입니다.
     달 칸(2026/09)은 올리신 달을 따라갑니다 — 여러 달을 다 찾아봅니다. */
  var BASE = '/wp-content/uploads/';
  var MONTHS = ['2026/09/', '2026/10/', '2026/11/'];
  /* 홈 줄에서 뺄 배너 */
  var HIDE = ['/lotto/'];

  var MAP = [
    ['/zodiac-year/',    'STELLASAJU_free_zodiac-year.jpg', '이번주 띠별운세'],
    ['/zodiac/',         'STELLASAJU_free_zodiac.jpg',      '이번주 별자리 운세'],
    ['/saju/',           'STELLASAJU_free_saju.jpg',        '나의 사주풀이'],
    ['/weekly-summary/', 'STELLASAJU_free_weekly.jpg',      '이번주 사주총평'],
    ['/today/',          'STELLASAJU_free_today.jpg',       '오늘의 운세']
  ];

  /* 젯팩 이미지 서버를 거쳐 작게 받습니다 — 원본이 커도 손님은
     640x960 한 장만 받습니다. 유료 배너가 쓰는 것과 같은 꼴입니다. */
  function cdn(path){
    return 'https://i0.wp.com/' + location.host + path + '?resize=640%2C960';
  }

  function tail(h){
    var s = String(h === null ? '' : h);
    var q = s.indexOf('?');
    if(q >= 0){ s = s.slice(0, q); }
    var g = s.indexOf('#');
    if(g >= 0){ s = s.slice(0, g); }
    if(s.length){ if(s.charAt(s.length - 1) !== '/'){ s = s + '/'; } }
    return s;
  }
  function ends(s, t){
    if(s.length < t.length){ return false; }
    return s.slice(s.length - t.length) === t;
  }

  /* 사진 한 장 붙이기.
     달을 하나씩 넘어가며 찾고, 다 없으면 사진 층을 걷어내
     지금 모습(색 타일)으로 돌아갑니다. */
  function attach(card, file, alt){
    var wrap = document.createElement('div');
    wrap.className = 'fimg';
    var img = document.createElement('img');
    img.setAttribute('loading', 'lazy');
    img.setAttribute('decoding', 'async');
    img.setAttribute('alt', alt);
    var mi = 0;
    img.onerror = function(){
      mi++;
      if(mi < MONTHS.length){
        img.src = cdn(BASE + MONTHS[mi] + file);
        return;
      }
      /* 아직 안 올라온 사진 — 조용히 물러납니다 */
      if(wrap.parentNode){ wrap.parentNode.removeChild(wrap); }
      card.removeAttribute('data-freeimg');
    };
    img.src = cdn(BASE + MONTHS[0] + file);
    wrap.appendChild(img);
    card.insertBefore(wrap, card.firstChild);
    card.setAttribute('data-freeimg', '1');
  }

  var done = 0;
  function run(){
    var cards = document.querySelectorAll('a.free-card');
    if(!cards.length){ return; }
    var i, j, a, h;
    for(i = 0; i < cards.length; i++){
      a = cards[i];
      if(a.getAttribute('data-freeimg-seen') === '1'){ continue; }
      h = tail(a.getAttribute('href'));
      var hid = 0;
      for(j = 0; j < HIDE.length; j++){
        if(ends(h, HIDE[j])){
          a.setAttribute('data-freehide', '1');
          a.setAttribute('data-freeimg-seen', '1');
          hid = 1;
          break;
        }
      }
      if(hid){ continue; }
      for(j = 0; j < MAP.length; j++){
        if(!ends(h, MAP[j][0])){ continue; }
        a.setAttribute('data-freeimg-seen', '1');
        attach(a, MAP[j][1], MAP[j][2]);
        break;
      }
    }
  }

  run();
  document.addEventListener('DOMContentLoaded', function(){ run(); });
  var t = setInterval(function(){
    done++;
    run();
    if(done > 20){ clearInterval(t); }
  }, 300);
})();
</script>
	<?php
} );
