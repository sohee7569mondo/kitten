<?php
/* ═══════════════════════════════════════════════════════
   결제창에 정가를 함께 보이기        patch160_listprice
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   소희 님 : 「결제창에 9000원인데 3000원이라는 표시가 있어야 할듯해
              그냥 싼 사주풀이 같은 느낌이 안들게」

   맞는 말씀입니다. 지금은 이렇게만 보입니다 —

       이 풀이의 값   3구슬
       내실 값        3,000원

   3,000원만 덩그러니 있으면 「싸구려」로 읽힙니다.
   정가를 함께 보이면 「스무 쪽짜리 책을 지금은 깎아 드린다」가 됩니다.

       정가                9,000원   (가운데 줄)
       여는 기념 할인     -6,000원
       ─────────────────────────
       내실 값             3,000원

   ★ 정가는 지어낸 값이 아닙니다
     가격 안내와 소개 쪽에 이미 이렇게 적혀 있습니다 —
     「정가는 9구슬 · 9,000원이고, 여는 기간이 끝나면 그 값이 됩니다」
     실제로 그 값에 파실 예정이라야 표시광고법에 걸리지 않습니다.
     여는 기간을 접으실 때 이 조각도 같이 꺼주세요.

   왜 앵커를 안 잡나
   결제창의 줄은 그 쪽 스크립트가 그립니다. 글자를 잡지 않고,
   다 그려진 뒤 줄 하나를 읽어 앞에 두 줄을 끼웁니다.
   값은 서버가 정한 그대로 두고 **보여드리는 줄만** 더합니다.

   되돌리기
   이 스니펫을 끄면 원래대로 돌아옵니다. 쪽을 안 건드립니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_footer', function () {
	if ( ! is_page( 'pay' ) ) { return; }
	?>
<style id="stella-listprice-css">
#sso .bill .r.lp-list .v{ color:#8B849C; text-decoration:line-through; }
#sso .bill .r.lp-off .l,
#sso .bill .r.lp-off .v{ color:#A9791F; }
#sso .bill .lp-why{ margin-top:10px; font-size:.84rem; color:#8B849C; line-height:1.8; }
</style>
<script>
(function(){
  if(window.StellaListPrice){ return; }
  window.StellaListPrice = 1;

  /* 구슬 수 → 정가(구슬). 가격 안내에 적힌 값만 씁니다.
     모르는 것은 아무것도 안 보탭니다 — 지어내지 않습니다. */
  var LIST = { 3: 9 };
  var WON_PER_ORB = 1000;

  function won(n){
    var s = String(n), out = '', i, c = 0;
    for(i = s.length - 1; i >= 0; i--){
      out = s.charAt(i) + out;
      c++;
      if(c % 3 === 0){ if(i > 0){ out = ',' + out; } }
    }
    return out + '원';
  }

  function row(cls, l, v){
    return '<div class="r ' + cls + '"><span class="l">' + l
         + '</span><span class="v">' + v + '</span></div>';
  }

  function digits(s){
    var t = String(s), out = '', i, c;
    for(i = 0; i < t.length; i++){
      c = t.charAt(i);
      if(c >= '0'){ if(c <= '9'){ out += c; } }
    }
    return out;
  }

  function run(){
    var box = document.getElementById('oRows');
    if(!box){ return 0; }
    if(box.getAttribute('data-lp') === '1'){ return 1; }
    var rows = box.querySelectorAll('.r');
    if(!rows.length){ return 0; }

    /* 「이 풀이의 값 N구슬」 줄에서 N 을 읽습니다 */
    var i, orbs = 0;
    for(i = 0; i < rows.length; i++){
      var l = rows[i].querySelector('.l');
      if(!l){ continue; }
      if(String(l.textContent).indexOf('이 풀이의 값') < 0){ continue; }
      var v = rows[i].querySelector('.v');
      if(v){ orbs = parseInt(digits(v.textContent), 10); }
      break;
    }
    if(!orbs){ return 0; }

    var listOrbs = LIST[orbs];
    if(!listOrbs){ box.setAttribute('data-lp', '1'); return 1; }  /* 모르는 값은 그냥 둡니다 */

    var listWon = listOrbs * WON_PER_ORB;
    var nowWon  = orbs * WON_PER_ORB;
    var offWon  = listWon - nowWon;
    if(offWon <= 0){ box.setAttribute('data-lp', '1'); return 1; }

    /* 「이 풀이의 값 3구슬」 만으로는 셈이 안 따라옵니다.
       원을 나란히 붙여 3구슬 = 3,000원 이 눈에 보이게 합니다. */
    for(i = 0; i < rows.length; i++){
      var l2 = rows[i].querySelector('.l');
      if(!l2){ continue; }
      if(String(l2.textContent).indexOf('이 풀이의 값') < 0){ continue; }
      var v2 = rows[i].querySelector('.v');
      if(v2){ v2.textContent = orbs + '구슬 · ' + won(nowWon); }
      break;
    }

    var add = row('lp-list', '정가', won(listWon))
            + row('lp-off', '여는 기념 할인', '-' + won(offWon));
    box.innerHTML = add + box.innerHTML;

    var why = document.createElement('div');
    why.className = 'lp-why';
    why.textContent = '여는 기념으로 ' + won(listWon) + ' 짜리를 '
      + won(nowWon) + '에 드리고 있어요. 여는 기간이 끝나면 정가가 됩니다.';
    box.parentNode.appendChild(why);

    box.setAttribute('data-lp', '1');
    return 1;
  }

  var tries = 0;
  var t = setInterval(function(){
    tries++;
    if(run()){ clearInterval(t); return; }
    if(tries > 60){ clearInterval(t); }
  }, 250);
  run();
})();
</script>
	<?php
} );
