<?php
/* ═══════════════════════════════════════════════════════
   머리글 로고를 글씨로   patch_logotext
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   소희 님 : 「로고 바꾸기로 한 얘기 있을 거야. 한번 찾아봐.
              지금 로고가 눈에 안 띄어」

   찾았습니다. 이미 결론이 나 있었습니다 —
       NEXT.md 2번 · 할일-0909.md
       「헤더 로고를 글씨로 — 그림 로고가 작아서 안 읽힙니다.
        외모 → 편집기 → 헤더 → 로고 블록 지우고 「사이트 제목」 블록」

   테마 편집기를 안 건드립니다
   편집기로 헤더를 고치면 되돌리기가 번거롭고, 나중에 테마가
   바뀌면 또 손봐야 합니다. 조각으로 하면 끄는 순간 옛 로고가
   그대로 돌아옵니다.

   무엇을 하나
     머리글의 로고 그림을 찾아 그 자리에 글씨를 넣습니다.
     고리(홈으로 가는 링크)는 그대로 씁니다 — 누르면 홈으로 갑니다.

         스텔라사주        ← 크고 굵게
         STELLA SAJU       ← 작게, 자간 넓게, 금빛

   ★ 그림을 지우지 않고 감춥니다. 되돌릴 때 자리가 그대로입니다.
   ★ 바닥글 로고는 건드리지 않습니다 — 거기는 작아도 괜찮고,
     머리글만 손봐도 「눈에 안 띈다」는 문제가 풀립니다.
     바닥글도 바꾸시려면 아래 FOOT 를 1 로 두세요.

   살펴보기 : 어느 쪽이든 열어 머리글을 보시면 됩니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_head', function () {
	?>
<style id="stella-logotext-css">
.stella-logotext{
  display:block; line-height:1.15; text-align:left;
  white-space:nowrap; text-decoration:none; }
.stella-logotext .lt-ko{
  display:block;
  font-family:'Noto Sans KR',-apple-system,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  font-size:1.34rem; font-weight:800; letter-spacing:-.02em;
  color:#F2ECE0; }
.stella-logotext .lt-en{
  display:block; margin-top:3px;
  font-family:'Cinzel',serif;
  font-size:.6rem; letter-spacing:.34em;
  color:#D4AF6A; }
.stella-logotext:hover .lt-ko{ color:#FFFFFF; }
.stella-logohide{ display:none !important; }
@media(max-width:600px){
  .stella-logotext .lt-ko{ font-size:1.16rem; }
  .stella-logotext .lt-en{ font-size:.54rem; letter-spacing:.28em; }
}
</style>
<script>
(function(){
  if(window.StellaLogoText){ return; }
  window.StellaLogoText = 1;

  var FOOT = 0;   /* 1 로 두면 바닥글 로고도 글씨로 바꿉니다 */

  function make(doc){
    var a = doc.createElement('span');
    a.className = 'stella-logotext';
    a.innerHTML = '<span class="lt-ko">스텔라사주</span>'
      + '<span class="lt-en">STELLA SAJU</span>';
    return a;
  }

  /* 로고 그림을 찾습니다 — 테마마다 이름이 달라 여러 가지로 봅니다 */
  function logos(){
    var sel = '.custom-logo, .wp-block-site-logo img, '
            + '.site-logo img, header img[class*="logo"], '
            + 'header a[rel="home"] img';
    return document.querySelectorAll(sel);
  }

  function inFooter(el){
    var n = el;
    while(n){
      if(!n.tagName){ break; }
      var t = n.tagName.toLowerCase();
      if(t === 'footer'){ return 1; }
      if(t === 'header'){ return 0; }
      if(t === 'body'){ break; }
      n = n.parentNode;
    }
    return 0;
  }

  function run(){
    var imgs = logos();
    if(imgs.length === 0){ return 0; }
    var i, im, box, done = 0;
    for(i = 0; i < imgs.length; i++){
      im = imgs[i];
      if(im.getAttribute('data-logotext') === '1'){ continue; }
      if(!FOOT){ if(inFooter(im)){ continue; } }

      /* 그림이 든 자리에 글씨를 끼우고 그림은 감춥니다 */
      box = im.parentNode;
      if(!box){ continue; }
      box.insertBefore(make(document), im);
      im.className = im.className + ' stella-logohide';
      im.setAttribute('data-logotext', '1');
      done++;
    }
    return done ? 1 : 0;
  }

  function watch(){
    if(run()){ return; }
    var n = 0;
    var t = setInterval(function(){
      n++;
      if(run()){ clearInterval(t); return; }
      if(n > 30){ clearInterval(t); }
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
