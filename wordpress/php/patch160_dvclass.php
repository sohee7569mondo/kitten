<?php
/* ═══════════════════════════════════════════════════════
   장 속표지 그림에 옷을 입힙니다   patch160_dvclass
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   소희 님 : 「2026 열었는데 이상해. 뭔가 위에 떠 있고
              문도 아치형으로 떠야 하는데」

   제 실수입니다
   가디언 그림의 모양과 크기는 patch160_face 가 정합니다.
   그런데 그 CSS 는 이렇게 걸려 있습니다 —

       #ssb .divider .dvmark.dvface img{ … }

   **.dvface 가 있어야** 걸립니다. 그런데 제가 신년운세 · 가족운 ·
   건강운 책의 장 속표지를 만들면서 이렇게만 썼습니다 —

       <div class="dvmark"><img …></div>

   dvface 를 안 붙였습니다. 그래서 그림이 CSS 를 하나도 못 받고
   원본 크기 그대로 나왔습니다. 작고 세로로 긴 네모가 그것입니다.

   고치는 길 둘 가운데
     ① 만드는 도구(emit_*.py)를 고쳐 조각을 다시 뽑는다
        → 소희 님이 ny2026 · ny2027 · family · health4 를 다시
          붙여넣으셔야 합니다. 네 개가 60만 자입니다.
     ② 화면에서 클래스만 붙인다  ← 이 조각
        → 붙여넣기 한 번이면 네 책이 한꺼번에 고쳐집니다.

   ★ 만드는 도구도 같이 고쳐두었습니다. 다음에 원고를 고쳐 다시
     뽑으실 때는 처음부터 dvface 가 붙어 나옵니다. 그때 이 조각을
     꺼도 되고, 켜둬도 이미 붙어 있으면 그냥 지나갑니다.

   되돌리기 : 스니펫을 끄면 그대로 돌아갑니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_head', function () {

	if ( ! is_page( 'reading-book' ) ) { return; }
	?>
<script>
(function(){
  if(window.StellaDvClass){ return; }
  window.StellaDvClass = 1;

  function fix(){
    var marks = document.querySelectorAll('#ssb .divider .dvmark');
    if(marks.length === 0){ return 0; }
    var i, m, n = 0;
    for(i = 0; i < marks.length; i++){
      m = marks[i];
      if(m.className.indexOf('dvface') > -1){ continue; }
      /* 글자(가디언 이름)만 든 표지는 그대로 둡니다 — 그림일 때만 */
      if(!m.querySelector('img')){ continue; }
      m.className = m.className + ' dvface';
      n++;
    }
    return n;
  }

  fix();
  var k = 0;
  var t = setInterval(function(){
    k++;
    fix();
    if(k > 40){ clearInterval(t); }
  }, 300);

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', fix);
  }
})();
</script>
	<?php
} );
