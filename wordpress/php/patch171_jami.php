<?php
/* ═══════════════════════════════════════════════════════
   별자리를 거두고 자미두수로   patch171_jami
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   소희 님 : 「별자리는 변별력이 없어서 거두기로 했어.
              그냥 이름을 자미두수라고 바꾸고 (예정중)으로 하자」
              「문 자체를 바꾸는 것 — 지금 파는 상품을 내립니다」

   그래서 이름만 바꾸면 안 됩니다
   이름을 자미두수로 바꿔놓고 문을 열어두면, 손님이 3,000원을 내고
   **별자리 책**을 받습니다. 그건 파는 것과 다른 것을 주는 것이라
   결제대행 심사에서 가장 크게 걸리는 대목입니다.
   그래서 **문을 같이 잠급니다.**

   무엇을 하나
     ① door-astro 쪽
        · 이름을 「아라 · 자미두수」로, 영문을 Zi Wei Dou Shu 로
        · 「준비 중」 안내를 맨 위에 크게
        · STEP 들과 물어보기 단추를 감춥니다 (결제로 가는 길을 끊습니다)
        · 다른 문 다섯으로 가는 길을 대신 냅니다
     ② 모든 쪽의 차림표 · 링크
        · door-astro 로 가는 고리의 글에서 별자리 · 점성술을
          자미두수로 바꾸고 「준비 중」을 붙입니다

   이미 아라 풀이를 받으신 분
     받으신 책은 그대로 열립니다. 이 조각은 문만 잠급니다.

   되돌리기
     스니펫을 끄면 문이 그대로 다시 열립니다. 쪽 글은 한 자도
     고치지 않았습니다.

   ☞ 아직 남은 것 (쪽 글이라 따로 고쳐야 합니다)
     · 이용약관 제5조의 「아라(별자리)」
     · /reading-astro/ 견본 쪽
     · 무료 /zodiac/ (이번주 별자리 운세) — 무료라 두어도 됩니다
   ═══════════════════════════════════════════════════════ */

/* ── ① 문 쪽 ───────────────────────────────────────────── */
add_action( 'wp_footer', function () {

	if ( ! is_page( 'door-astro' ) ) { return; }
	?>
<style id="stella-jami-css">
#jamiBox{ margin:30px 0 8px; padding:30px 28px; border-radius:14px;
  background:#FFFDF9; border:1px solid #E2DACB; text-align:left;
  box-shadow:0 2px 4px -2px rgba(34,28,51,.10),
             0 18px 40px -20px rgba(34,28,51,.3); }
#jamiBox .jm-kick{ font-size:.72rem; letter-spacing:.28em; color:#A9791F;
  margin-bottom:12px; }
#jamiBox h3{ margin:0 0 14px; font-size:1.42rem; font-weight:800;
  color:#221C33; line-height:1.5; }
#jamiBox p{ margin:0 0 11px; font-size:1rem; line-height:1.9; color:#4E4763; }
#jamiBox p:last-of-type{ margin-bottom:0; }
#jamiBox .jm-soon{ display:inline-block; margin-left:8px; padding:4px 12px;
  border-radius:20px; background:#C4453A; color:#FFFDF9;
  font-size:.72rem; font-weight:800; vertical-align:middle; }
#jamiBox .jm-doors{ display:flex; flex-wrap:wrap; gap:9px; margin-top:22px; }
#jamiBox .jm-doors a{ padding:12px 17px; border-radius:9px;
  background:#FAF7F0; border:1px solid #D5CCB8; color:#221C33;
  font-size:.94rem; font-weight:700; text-decoration:none; }
#jamiBox .jm-doors a:hover{ border-color:#A9791F; }
#ssg .jm-hide{ display:none !important; }
</style>
<script>
(function(){
  if(window.StellaJami){ return; }
  window.StellaJami = 1;

  var GO = String.fromCharCode(8594);

  var DOORS = [
    ['/door-career/',  '마루 · 일과 돈'],
    ['/door-love/',    '벼리 · 연애와 결혼'],
    ['/door-health/',  '아람 · 건강과 가족'],
    ['/door-fortune/', '미르 · 흐름과 시기'],
    ['/door-tarot/',   '아르카나 · 타로']
  ];

  /* ssg 의 직계 자식까지 거슬러 올라갑니다 */
  function topIn(el, root){
    var n = el;
    while(n){
      if(n.parentNode === root){ return n; }
      n = n.parentNode;
      if(!n){ return null; }
      if(n === document.body){ return null; }
    }
    return null;
  }

  function run(){
    var ssg = document.getElementById('ssg');
    if(!ssg){ return 0; }
    if(ssg.getAttribute('data-jami') === '1'){ return 1; }

    /* 이름을 바꿉니다 — 자리만 찾고 글자는 안 잡습니다 */
    var en = ssg.querySelector('.g-en');
    if(en){ en.textContent = 'Zi Wei Dou Shu'; }

    /* 잠글 덩어리를 모읍니다 — STEP 표가 든 곳과 물어보기 단추 */
    var hide = [];
    var marks = ssg.querySelectorAll('.step-no');
    var i, t;
    for(i = 0; i < marks.length; i++){
      t = topIn(marks[i], ssg);
      if(t){ if(hide.indexOf(t) < 0){ hide.push(t); } }
    }
    var btn = document.getElementById('goBtn');
    if(btn){
      t = topIn(btn, ssg);
      if(t){ if(hide.indexOf(t) < 0){ hide.push(t); } }
      btn.disabled = true;
    }
    /* 못 찾았으면 아무것도 안 합니다 — 문이 반만 잠기면 더 나쁩니다 */
    if(hide.length === 0){ return 0; }

    var box = document.createElement('div');
    box.id = 'jamiBox';
    box.innerHTML =
      '<div class="jm-kick">ZI WEI DOU SHU</div>'
      + '<h3>아라의 자미두수<span class="jm-soon">준비 중</span></h3>'
      + '<p>별자리 풀이는 <b>거두었습니다.</b> 태양 별자리 하나로는 '
      + '사람을 가를 수 없다는 것이 저희 판단이었어요. '
      + '열두 갈래로 나눈 이야기는 누구에게나 맞는 말이 되기 쉽습니다.</p>'
      + '<p>대신 <b>자미두수</b>로 다시 짓고 있습니다. 태어난 때로 열두 자리를 '
      + '세우고 별을 앉히는 셈이라, 같은 날 태어나도 시가 다르면 다른 그림이 '
      + '나옵니다. 저희가 사주에서 하려던 것과 결이 같아요.</p>'
      + '<p>준비되면 이 자리에 열어두겠습니다. '
      + '그동안은 다른 문으로 가주세요.</p>'
      + '<div class="jm-doors">'
      + DOORS.map(function(d){
          return '<a href="' + d[0] + '">' + d[1] + ' ' + GO + '</a>';
        }).join('')
      + '</div>';

    /* 잠그는 덩어리 가운데 맨 앞 자리에 안내를 놓습니다 */
    hide[0].parentNode.insertBefore(box, hide[0]);
    for(i = 0; i < hide.length; i++){
      hide[i].className = hide[i].className + ' jm-hide';
    }

    ssg.setAttribute('data-jami', '1');
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

/* ── ② 차림표와 링크 ───────────────────────────────────────
   머리글은 모든 쪽에 있어 울타리를 칠 수가 없습니다. 대신 아주
   짧게 씁니다 — door-astro 로 가는 고리만 찾아 글자를 갈아끼웁니다.
   찾는 것이 없으면 그대로 물러납니다. */
add_action( 'wp_footer', function () {
	?>
<script>
(function(){
  if(window.StellaJamiMenu){ return; }
  window.StellaJamiMenu = 1;

  function fix(){
    var a = document.querySelectorAll('a[href*="door-astro"]');
    if(a.length === 0){ return 0; }
    var i, t;
    for(i = 0; i < a.length; i++){
      if(a[i].getAttribute('data-jami') === '1'){ continue; }
      if(a[i].children.length > 0){ continue; }   /* 사진이 든 고리는 건드리지 않습니다 */
      t = String(a[i].textContent);
      if(t.indexOf('자미두수') > -1){ continue; }
      t = t.split('점성술').join('자미두수');
      t = t.split('별자리').join('자미두수');
      if(t.indexOf('준비 중') < 0){ t = t + ' (준비 중)'; }
      a[i].textContent = t;
      a[i].setAttribute('data-jami', '1');
    }
    return 1;
  }

  fix();
  var n = 0;
  var k = setInterval(function(){
    n++;
    fix();
    if(n > 10){ clearInterval(k); }
  }, 400);
})();
</script>
	<?php
} );
