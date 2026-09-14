<?php
/* ═══════════════════════════════════════════════════════
   무료 배너 글씨 바로잡기          patch160_freelabel
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   무엇을 고치나
   ① /zodiac-year/ 배너가 「올해 띠별 운세」로 돼 있는데
      그 쪽의 제목은 「이번주 띠별운세」입니다. 셈도 그 주
      월요일 일간으로 합니다 — 글씨만 틀렸습니다.
      → 「이번주 띠별운세」로 고칩니다.
   ② 작은 글씨의 「간단한」·「심심풀이」를 뺍니다.
      공짜라서 가벼운 것이 아니라 「공짜인데 진짜」로 읽히도록,
      무엇을 넣으면 무엇이 나오는지를 적습니다.

   왜 앵커를 안 잡나
   살아 있는 홈은 제 사본보다 새롭습니다. 글자를 잡아 바꾸면
   한 칸 차이로 「0군데」가 납니다. 그래서 배너를 주소(href)로
   찾아 글씨만 갈아 끼웁니다 — 사본이 낡아도 맞습니다.

   되돌리기
   이 스니펫을 끄면 원래대로 돌아옵니다. 쪽을 안 건드립니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_head', function () {
	?>
<script>
(function(){
  if(window.StellaFreeLabel){ return; }
  window.StellaFreeLabel = 1;

  /* 주소 → [ 작은 글씨, 이름 ] */
  var MAP = [
    ['/zodiac-year/',    '태어난 해로',   '이번주<br>띠별운세'],
    ['/zodiac/',         '태어난 달로',   '이번주<br>별자리운세'],
    ['/saju/',           '네 기둥과 오행', '나의<br>사주풀이'],
    ['/weekly-summary/', '내 사주로',     '이번주<br>총평'],
    ['/lotto/',          '매주 새 번호',   '이번주<br>로또번호']
  ];

  /* href 가 그 주소로 끝나는지 봅니다.
     — 사이트가 https://stellasaju.com/zodiac-year/ 로 늘여 주므로
       앞은 보지 않고 뒤만 견줍니다. 물음표가 붙어도 잘라 냅니다. */
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

  var done = 0;
  function run(){
    var cards = document.querySelectorAll('a.free-card');
    if(!cards.length){ return 0; }
    var n = 0, i, j, a, h, k, b;
    for(i = 0; i < cards.length; i++){
      a = cards[i];
      if(a.getAttribute('data-freelabel') === '1'){ continue; }
      h = tail(a.getAttribute('href'));
      for(j = 0; j < MAP.length; j++){
        if(!ends(h, MAP[j][0])){ continue; }
        k = a.querySelector('.free-kicker');
        b = a.querySelector('.free-sub');
        if(k){ k.textContent = MAP[j][1]; }
        if(b){ b.innerHTML = MAP[j][2]; }
        a.setAttribute('data-freelabel', '1');
        n++;
        break;
      }
    }
    return n;
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
