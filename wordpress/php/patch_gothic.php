<?php
/* ═══════════════════════════════════════════════════════
   명조를 고딕으로   patch_gothic
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   소희 님 : 「글씨는 고딕으로 해줘. 명조가 가독성이 떨어져……
              다른 데도 전부 고딕으로 하면 좋겠는데」

   지금 쪽들은 이렇게 돼 있습니다 —
       --serif : 'Gowun Batang','Noto Serif KR', serif
   그리고 제목과 이름표에 font-family:var(--serif) 를 씁니다.
   더러는 변수를 안 쓰고 'Noto Serif KR' 을 바로 적어둔 곳도 있습니다
       #ssp .aname{ font-family:'Noto Serif KR',serif; }

   그래서 두 겹으로 갑니다
     ① CSS 로 --serif 와 --latin 을 고딕으로 덮습니다
        (쪽이 #ssp{...} 처럼 id 로 정해두어 id 선택자로 맞받습니다)
     ② 그래도 남는 곳은 자바스크립트로 **실제로 그려진 글꼴**을 보고
        명조면 그 자리에서 바꿉니다. 선택자를 짐작하지 않고
        getComputedStyle 로 확인하므로 놓치는 곳이 없습니다.

   ★ 바꾸지 않는 것 두 가지
     · IBM Plex Mono — 연도와 쪽번호처럼 숫자가 줄 맞아야 하는 곳입니다
     · Cinzel — 「STELLA SAJU」 같은 라틴 장식 글자. 한글이 아니라
       가독성과 무관하고, 이것까지 고딕으로 바꾸면 브랜드 느낌이
       사라집니다. 이것도 바꾸시려면 말씀만 주세요 (아래 KEEP_LATIN).

   ★ 웹폰트를 새로 받지 않습니다
     쪽들이 이미 본문에 'Noto Sans KR' 을 쓰고 있어 그대로 씁니다.
     새 글꼴을 부르면 쪽이 그만큼 늦게 뜹니다.

   되돌리기 : 스니펫을 끄면 그대로 돌아갑니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_head', function () {
	?>
<style id="stella-gothic-css">
/* ① 변수를 고딕으로 — 쪽이 id 로 정해두어 id 로 맞받습니다 */
html body #ssp, html body #sst, html body #ssr, html body #ssg,
html body #ssb, html body #ssm, html body #ssd, html body #ssq,
html body #ssn, html body #ssl, html body #stellar-home,
html body .wp-site-blocks, html body{
  --serif:'Noto Sans KR',-apple-system,'Apple SD Gothic Neo','Malgun Gothic',sans-serif !important;
}
/* 제목은 고딕으로 오면 자칫 가벼워 보입니다. 굵기로 무게를 줍니다. */
html body #ssp h1, html body #sst h1, html body #ssr h1,
html body #ssg h1, html body #ssb h1, html body #ssm h1,
html body #ssp h2, html body #sst h2, html body #ssr h2,
html body #ssg h2, html body #ssb h2, html body #ssm h2{
  font-weight:800 !important; letter-spacing:-.015em !important; }
</style>
<script>
(function(){
  if(window.StellaGothic){ return; }
  window.StellaGothic = 1;

  var KEEP_LATIN = 1;   /* Cinzel(라틴 장식)을 남깁니다. 0 이면 같이 바꿉니다 */

  var GOTHIC = "'Noto Sans KR',-apple-system,'Apple SD Gothic Neo','Malgun Gothic',sans-serif";

  /* 명조로 그려지고 있는가 — 짐작하지 않고 실제 값을 봅니다 */
  function isSerif(f){
    var t = String(f);
    if(t.indexOf('Batang') > -1){ return 1; }
    if(t.indexOf('Serif') > -1){ return 1; }
    if(t.indexOf('Myeongjo') > -1){ return 1; }
    if(t.indexOf('Nanum Myeongjo') > -1){ return 1; }
    if(KEEP_LATIN){ if(t.indexOf('Cinzel') > -1){ return 0; } }
    else { if(t.indexOf('Cinzel') > -1){ return 1; } }
    /* 글꼴을 하나도 못 받은 자리 — 마지막이 serif 면 명조로 그려집니다 */
    var last = t.split(',').pop();
    last = last.split(' ').join('');
    if(last === 'serif'){ return 1; }
    return 0;
  }

  var SEL = 'h1,h2,h3,h4,h5,h6,p,li,dt,dd,span,div,a,b,strong,em,'
          + 'td,th,button,label,blockquote,figcaption,small,summary';

  function fix(root){
    var list = root.querySelectorAll(SEL);
    var i, el, f, n = 0;
    for(i = 0; i < list.length; i++){
      el = list[i];
      if(el.getAttribute('data-gothic') === '1'){ continue; }
      f = window.getComputedStyle(el).fontFamily;
      if(!isSerif(f)){ el.setAttribute('data-gothic', '1'); continue; }
      el.style.setProperty('font-family', GOTHIC, 'important');
      el.setAttribute('data-gothic', '1');
      n++;
    }
    return n;
  }

  function run(){ try{ return fix(document); }catch(e){ return 0; } }

  run();
  /* 책처럼 나중에 그려지는 쪽이 있어 한동안 지켜봅니다 */
  var k = 0;
  var t = setInterval(function(){
    k++;
    run();
    if(k > 20){ clearInterval(t); }
  }, 500);

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', run);
  }
})();
</script>
	<?php
} );
