<?php
/* ═══════════════════════════════════════════════════════
   로또를 스텔라 랩으로            patch160_lablotto
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   소희 님 : 「로또 없애자」 → 「그건 스텔라 랩에 넣자」

   무엇을 하나
   홈의 무료 줄에서 뺀 로또를 스텔라 랩(/lab/) 목록 맨 끝에 넣습니다.
   랩은 「가벼운 마음으로 봐주세요」 하는 자리라 로또가 제자리를 찾습니다.

   왜 앵커를 안 잡나
   랩 카드는 stella_lab 스니펫이 그립니다 — 제 사본에 없습니다.
   그래서 글자를 잡지 않고, 카드가 다 그려진 뒤 맨 끝에 한 장을
   덧붙입니다. stella_lab 을 고칠 필요가 없습니다.

   ★ 먼저 그려진 카드가 있어야만 붙입니다
     랩 쪽에는 「검사를 준비하고 있습니다」 안내가 따로 있는데,
     그것은 목록이 비었을 때만 나옵니다. 우리가 먼저 끼어들면
     stella_lab 이 고장나도 그 안내가 안 나와 눈치를 못 챕니다.
     그래서 .card 가 하나라도 있을 때만 붙입니다.

   되돌리기
   이 스니펫을 끄면 원래대로 돌아옵니다. 쪽을 안 건드립니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_head', function () {
	/* ★ 스텔라 랩 쪽에서만 씁니다.
	   ☞ 2026-09-14 오늘 기준으로 사이트에 lab 쪽이 아직 없습니다.
	     쪽을 올리시면 이 조각이 저절로 일합니다. 슬러그가 lab 이
	     아니면 여기 이름만 바꾸면 됩니다. */
	if ( ! is_page( 'lab' ) ) { return; }
	?>
<style id="stella-lablotto-css">
/* 랩 카드 CSS 는 button 을 두고 쓴 것이라, a 를 넣으면 밑줄이 그어지고
   글씨가 링크색으로 바뀝니다 (크로미움으로 그려 보고 잡았습니다).
   우리 카드에만 그것을 끕니다. */
#slab .card[data-lablotto="1"],
#slab .card[data-lablotto="1"] *{ text-decoration:none; }
#slab .card[data-lablotto="1"]{ color:inherit; }
</style>
<script>
(function(){
  if(window.StellaLabLotto){ return; }
  window.StellaLabLotto = 1;

  function two(n){
    if(n < 10){ return '0' + n; }
    return '' + n;
  }

  function make(no){
    var a = document.createElement('a');
    a.className = 'card';
    a.setAttribute('href', '/lotto/');
    a.setAttribute('data-lablotto', '1');

    var s1 = document.createElement('span');
    s1.className = 'no';
    s1.textContent = two(no);

    var d1 = document.createElement('div');
    d1.className = 'nm';
    d1.textContent = '이번주 로또 추첨';

    var d2 = document.createElement('div');
    d2.className = 'sb';
    d2.textContent = '검사는 아닙니다. 명성의 신이 원판을 돌려 번호를 '
      + '뽑아 드려요. 누를 때마다 새로 나오니 마음에 드는 것이 나올 '
      + '때까지 돌리셔도 됩니다. 맞히려고 만든 것이 아니라 고르는 '
      + '재미로 둔 자리예요.';

    var d3 = document.createElement('div');
    d3.className = 'mt';
    d3.textContent = '삼십 초 · 답할 것 없음';

    a.appendChild(s1);
    a.appendChild(d1);
    a.appendChild(d2);
    a.appendChild(d3);
    return a;
  }

  var tries = 0;
  function run(){
    var box = document.getElementById('lab-cards');
    if(!box){ return 0; }
    if(box.querySelector('[data-lablotto]')){ return 1; }
    var cards = box.querySelectorAll('.card');
    if(!cards.length){ return 0; }   /* stella_lab 이 아직 안 그렸습니다 */
    /* 번호는 앞 카드의 번호 다음으로 매깁니다.
       카드 수로만 세면 stella_lab 이 03 부터 시작하거나 한 장을 빼도
       번호가 어긋납니다. 못 읽으면 그때만 카드 수로 물러납니다. */
    var last = cards[cards.length - 1].querySelector('.no');
    var n = 0;
    if(last){ n = parseInt(String(last.textContent).replace(/[^0-9]/g, ''), 10); }
    if(!n){ n = cards.length; }
    box.appendChild(make(n + 1));
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
