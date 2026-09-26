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
	if ( ! is_page( array( 'pay', 'door-love', 'door-career', 'door-health',
	                       'door-fortune', 'door-astro', 'door-tarot' ) ) ) { return; }
	?>
<style id="stella-listprice-css">
#sso .bill .r.lp-list .v{ color:#8B849C; text-decoration:line-through; }
#sso .bill .r.lp-off .l,
#sso .bill .r.lp-off .v{ color:#A9791F; }
#sso .bill .lp-why{ margin-top:10px; font-size:.84rem; color:#8B849C; line-height:1.8; }

/* ── 문 쪽 값 상자 (2026-09-14) ───────────────────────────
   소희 님 : 「금액이 아래에 9000원인데 할인된다는 말이 있는데 거기
   읽는 사람 없어. 9000원에 중간에 작대기 긋고 3000원이 보이게 해줘」
   맞습니다. 눈이 가는 곳은 값 상자입니다. 거기에 바로 긋습니다. */
.lp-was{ color:#8B849C; text-decoration:line-through; margin-right:7px;
  font-weight:400; }
.lp-now{ color:#C4453A; font-weight:700; }
.lp-until{ font-weight:400; font-size:.82em; opacity:.75; margin-left:5px; }
.btotal-v .lp-won{ font-size:.86em; color:#C4453A; margin-left:6px;
  font-weight:700; }
</style>
<script>
(function(){
  if(window.StellaListPrice){ return; }
  window.StellaListPrice = 1;

  /* 구슬 수 → 정가(구슬). 가격 안내에 적힌 값만 씁니다.
     모르는 것은 아무것도 안 보탭니다 — 지어내지 않습니다. */
  var LIST = { 3: 9 };
  var WON_PER_ORB = 1000;
  /* 2026-09-14 · 소희 님 : 「이벤트 할인기간에 기간도 쓰자 10월말까지」
     여는 기념 값이 언제까지인지 못 박아 둡니다. 기간을 늘리시면
     이 한 줄만 고치시면 됩니다. */
  var UNTIL = '10월 31일까지';

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

  /* 맨 앞에 나오는 숫자 하나만 읽습니다.
     ★ 2026-09-14 : 처음에는 숫자를 다 이어붙였더니
       「3구슬 · 3,000원」이 33000 이 되어 「33000구슬」로 나왔습니다.
       쉼표는 건너뛰고, 숫자가 아닌 글자를 만나면 거기서 끊습니다. */
  function firstNum(s){
    var t = String(s), out = '', i, c, seen = 0;
    for(i = 0; i < t.length; i++){
      c = t.charAt(i);
      if(c >= '0'){ if(c <= '9'){ out += c; seen = 1; continue; } }
      if(c === ','){ if(seen){ continue; } }
      if(seen){ break; }
    }
    return parseInt(out, 10);
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
      if(v){ orbs = firstNum(v.textContent); }
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
            + row('lp-off', '여는 기념 할인 (' + UNTIL + ')', '-' + won(offWon));
    box.innerHTML = add + box.innerHTML;

    var why = document.createElement('div');
    why.className = 'lp-why';
    why.textContent = '여는 기념으로 ' + won(listWon) + ' 짜리를 '
      + won(nowWon) + '에 드리고 있어요. ' + UNTIL + '입니다.';
    box.parentNode.appendChild(why);

    box.setAttribute('data-lp', '1');
    return 1;
  }

  /* ── 문 쪽 값 상자 ────────────────────────────────────
     <div class="bline"><b>기본 풀이</b><span id="pBase">3구슬 · 3,000원</span></div>
     <div class="btotal">…<div class="btotal-v"><span id="total">3</span><small>구슬</small></div></div>
     ① 기본 풀이 줄에 정가를 그어 보입니다
     ② 합계가 구슬만 말하고 있어 원을 같이 붙입니다
     합계는 쪽 스크립트가 다시 쓸 수 있어 지켜보며 고칩니다. */
  function doorOnce(){
    var base = document.getElementById('pBase');
    if(!base){ return; }
    if(base.getAttribute('data-lp') === '1'){ return; }
    var now = firstNum(base.textContent);       /* 지금 값 3구슬 */
    if(!now){ return; }
    var list = LIST[now];                        /* 정가 9구슬 */
    base.textContent = (list ? list : now) + '구슬 · '
                     + won((list ? list : now) * WON_PER_ORB);
    base.setAttribute('data-lp', '1');

    if(!list){ return; }
    var off = list - now;
    if(off <= 0){ return; }

    /* 「여는 기념 할인」 줄을 기본 풀이 바로 밑에 끼웁니다 */
    var line = base.parentNode;                  /* .bline */
    if(!line){ return; }
    if(line.parentNode.querySelector('.lp-off-line')){ return; }
    var row = document.createElement('div');
    row.className = line.className + ' lp-off-line';
    row.innerHTML = '<b>여는 기념 할인<small class="lp-until"> ' + UNTIL+ '</small></b><span class="lp-now">-' + off
                  + '구슬 · -' + won(off * WON_PER_ORB) + '</span>';
    if(line.nextSibling){ line.parentNode.insertBefore(row, line.nextSibling); }
    else { line.parentNode.appendChild(row); }
  }

  function doorTotal(){
    var tv = document.querySelector('.btotal-v');
    if(!tv){ return; }
    var tn = document.getElementById('total');
    if(!tn){ return; }
    var n = firstNum(tn.textContent);
    if(!n){ return; }
    var want = won(n * WON_PER_ORB);
    var tag = tv.querySelector('.lp-won');
    if(!tag){
      tag = document.createElement('span');
      tag.className = 'lp-won';
      tv.appendChild(tag);
    }
    if(tag.textContent !== '· ' + want){ tag.textContent = '· ' + want; }
  }

  /* ── 문 쪽 발치의 안내 줄 ──────────────────────────────
     2026-09-14 · 소희 님 : 「구슬 1개가 1000원이라는 문구도 빼자」
     지금 이렇게 돼 있습니다 —
       「구슬 1개는 1,000원이에요. 이 풀이 한 편은 3구슬 · 3,000원입니다.
         여는 기념 값이고, 여는 기간이 끝나면 9구슬 · 9,000원이 됩니다.」
     값 상자에서 이미 9,000원에 줄을 긋고 3,000원을 보여드리므로
     이 줄에서 구슬 환산을 또 말할 까닭이 없습니다.
     앞 문장을 떼고, 남은 곳의 「N구슬 · 」도 지웁니다. */
  function payNote(){
    var el = document.querySelector('.pay-note');
    if(!el){ return; }
    if(el.getAttribute('data-lp') === '1'){ return; }
    var h = el.innerHTML;
    if(h.indexOf('구슬') < 0){ el.setAttribute('data-lp', '1'); return; }
    var at = h.indexOf('이 풀이 한 편은');
    if(at > 0){ h = h.slice(at); }
    var i;
    for(i = 1; i <= 99; i++){
      h = h.split(i + '구슬 · ').join('');
    }
    el.innerHTML = h;
    el.setAttribute('data-lp', '1');
  }

  var tries = 0;
  var t = setInterval(function(){
    tries++;
    run();
    doorOnce();
    doorTotal();
    payNote();
    if(tries > 80){ clearInterval(t); }
  }, 250);
  run();
  doorOnce();
  doorTotal();
  payNote();
})();
</script>
	<?php
} );
