<?php
/* ═══════════════════════════════════════════════════════
   벼리 문이 좁은 것 — 고침   patch141_lovewide
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   소희 님 : 「며칠 전부터 얘기한건데 벼리만 폭이 틀려 좁아……
              데스크탑에서만 한한 거지만」

   재서 찾았습니다 (tool_doorwide · ?stella_doorwide=1)

       어디             door-love          door-career
       #ssg .g-inner    1136px max 1180px  1136px max 1180px
       #ssg .g-cols     760px  max 760px   1084px max none    ← 여기
       div#ssg          1136px             1136px
       … 바깥 여덟 겹이 전부 같음 …

   바깥 상자는 한 겹도 안 다릅니다. 딱 한 군데, .g-cols 에
   **max-width:760px** 가 벼리에만 걸려 있었습니다.

   어디서 오나
       스니펫 「벼리 입력폼」(patch_door_love_form) 안에
       #ssg .g-cols{ grid-template-columns:1fr !important; max-width:760px; … }
       폼을 한 줄로 세우려던 규칙인데, 지금은 두 칸으로 나오면서
       max-width 만 남아 칸을 좁히고 있습니다.

   왜 FIT-2 를 안 쓰나
       patch160_fit(FIT-2)이 바로 이걸 풀려고 만든 조각입니다.
       다만 FIT-2 는 ① 울타리가 없어 모든 쪽에서 돌고
       ② 책(#ssb)의 여백까지 건드립니다. 책 폭은 지금
       patch160_width(WIDTH-7)가 정하고 있어 둘이 부딪힐 수 있습니다.
       그래서 ①만 떼어내고 문 여섯 쪽에만 울타리를 쳤습니다.

   두 겹으로 겁니다
       ① CSS — html body 를 앞에 붙여 특이도를 올립니다
       ② 자바스크립트 — 상대가 인라인 스타일이면 CSS 로는 못 이깁니다.
          setProperty(…, 'important') 로 직접 밀어넣습니다.
          (2026-09-11 FIT-1 이 CSS 로만 하다가 졌습니다)

   이미 넓은 문은 아무 일도 안 일어납니다 — max-width 가 none 이면
   none 으로 다시 두는 것뿐입니다.

   되돌리기 : 스니펫을 끄면 그대로 돌아갑니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_footer', function () {

	if ( ! is_page( array( 'door-love', 'door-career', 'door-health',
		'door-fortune', 'door-astro', 'door-tarot' ) ) ) { return; }
	?>
<style id="stella-lovewide-css">
html body #ssg .g-cols{ max-width:none !important; }
</style>
<script>
(function(){
  if(window.StellaLoveWide){ return; }
  window.StellaLoveWide = 1;

  function fix(){
    var g = document.querySelector('#ssg .g-cols');
    if(!g){ return 0; }
    g.style.setProperty('max-width', 'none', 'important');
    return 1;
  }

  fix();
  var n = 0;
  var t = setInterval(function(){
    n++;
    fix();
    if(n > 20){ clearInterval(t); }
  }, 300);

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', fix);
  }
})();
</script>
	<?php
} );
