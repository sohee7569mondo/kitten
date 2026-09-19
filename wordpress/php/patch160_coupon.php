<?php
/* ═══════════════════════════════════════════════════════
   쿠폰 · friend1974               patch160_coupon
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」
   ★ stella-signup 조각이 켜져 있어야 합니다 — 구슬을 더하는 일은
     그 조각의 stella_orb_add() 가 합니다. 없으면 조용히 안내만 냅니다.

   소희 님 : 「쿠폰을 만들어서 내 친구들한테만 뿌리고」
             「쿠폰이름을 friend1974 로 해줘 구슬 30개 넣어주고」

   왜 쿠폰인가
   가입만 하면 모두에게 구슬을 주면 심사관 화면도 0원이 되어 결제창을
   못 봅니다 (KG이니시스 입점조건 2번 — 0원 불가). 코드를 아는 분만
   쓰게 하면, 심사관에게는 3,000원 결제창이 정상으로 뜨고 친구들은
   무료로 봅니다. 둘 다 됩니다.

   ★ 쿠폰은 「무상 지급」입니다 — 돈 받고 파는 것이 아닙니다.
     이니시스에 회신하신 내용과 그대로 맞습니다.

   쿠폰 표 (아래 COUPONS 를 고치면 됩니다)
       friend1974   구슬 30개   2026-12-31 까지   100 명까지
       구슬 30개 = 여는 기념 값으로 풀이 열 편입니다.

   막아둔 것
       · 들어오신 분만 (로그인 안 하면 안 됩니다)
       · 한 계정에 한 번만
       · 사람 수 한도
       · 기한
       · 대소문자 · 앞뒤 빈칸 가림 없이 받습니다 (FRIEND1974 도 됩니다)

   쓰는 곳
       마이페이지(내 자리)의 구슬 칸 바로 아래에 「쿠폰 코드」 칸이
       생깁니다. 친구에게는 이렇게 보내시면 됩니다 —
         stellasaju.com/mypage/  에서 쿠폰 코드  friend1974  넣으세요

   되돌리기
   이 스니펫을 끄면 칸이 사라지고 코드도 안 먹습니다.
   이미 드린 구슬은 그대로 남습니다.
   ═══════════════════════════════════════════════════════ */

/* ── 서버 · 쿠폰 받기 ──────────────────────────────────── */
add_action( 'rest_api_init', function () {

	register_rest_route( 'stella/v1', '/coupon', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => function ( $req ) {

			$COUPONS = array(
				'friend1974' => array(
					'orbs'  => 30,
					'until' => '2026-12-31',
					'max'   => 100,
					'name'  => '친구 쿠폰',
				),
			);

			$uid = get_current_user_id();
			if ( ! $uid ) {
				return new WP_Error( 'stella_login', '먼저 들어와 주세요.', array( 'status' => 401 ) );
			}

			$code = $req->get_param( 'code' );
			$code = strtolower( trim( sanitize_text_field( (string) $code ) ) );
			if ( '' === $code ) {
				return new WP_Error( 'stella_code', '쿠폰 코드를 넣어주세요.', array( 'status' => 400 ) );
			}
			if ( ! isset( $COUPONS[ $code ] ) ) {
				return new WP_Error( 'stella_none', '그런 쿠폰이 없어요. 코드를 다시 봐주세요.', array( 'status' => 404 ) );
			}

			$c = $COUPONS[ $code ];

			if ( ! empty( $c['until'] ) ) {
				if ( current_time( 'Y-m-d' ) > $c['until'] ) {
					return new WP_Error( 'stella_over', '이 쿠폰은 기간이 지났어요.', array( 'status' => 410 ) );
				}
			}

			$used = get_user_meta( $uid, 'stella_coupon_used', true );
			$used = is_array( $used ) ? $used : array();
			if ( in_array( $code, $used, true ) ) {
				return new WP_Error( 'stella_twice', '이미 쓰신 쿠폰이에요.', array( 'status' => 409 ) );
			}

			$key = 'stella_coupon_n_' . $code;
			$n   = (int) get_option( $key, 0 );
			if ( ! empty( $c['max'] ) ) {
				if ( $n >= (int) $c['max'] ) {
					return new WP_Error( 'stella_full', '이 쿠폰은 준비한 만큼 다 나갔어요.', array( 'status' => 410 ) );
				}
			}

			if ( ! function_exists( 'stella_orb_add' ) ) {
				return new WP_Error( 'stella_off', '지금은 쿠폰을 넣을 수 없어요. 조금 뒤에 다시 해주세요.',
					array( 'status' => 503 ) );
			}

			stella_orb_add( $uid, (int) $c['orbs'], '쿠폰 ' . $code );

			$used[] = $code;
			update_user_meta( $uid, 'stella_coupon_used', $used );
			update_option( $key, $n + 1, false );

			$bal = function_exists( 'stella_orb_balance' ) ? (int) stella_orb_balance( $uid ) : 0;

			return array(
				'ok'      => true,
				'orbs'    => (int) $c['orbs'],
				'balance' => $bal,
				'name'    => $c['name'],
			);
		},
	) );
} );

/* ── 화면 · 마이페이지에 쿠폰 칸 ───────────────────────── */
add_action( 'wp_footer', function () {
	/* 쿠폰을 넣는 자리(마이페이지)와, 코드를 적어두는 자리(로그인),
	   그리고 들어오신 직후 지나가는 쪽들에서 돕니다. */
	if ( ! is_page( array( 'mypage', 'login', 'pay', 'reading-start',
	                       'reading-ready', 'door-love', 'door-career',
	                       'door-health', 'door-fortune', 'door-astro',
	                       'door-tarot' ) ) ) { return; }
	?>
<style id="stella-coupon-css">
.cpn-row{ display:flex; gap:8px; flex-wrap:wrap; }
.cpn-row input{ flex:1 1 180px; min-width:0; padding:12px 14px;
  border:1px solid #D5CCB8; border-radius:8px; background:#FAF7F0;
  color:#221C33; font:inherit; font-size:1rem; letter-spacing:.04em; }
.cpn-row button{ flex:0 0 auto; padding:12px 20px; border:0; border-radius:8px;
  background:linear-gradient(120deg,#3A2E77,#241C4E); color:#FFFDF9;
  font:inherit; font-weight:700; cursor:pointer; }
.cpn-row button:disabled{ opacity:.45; cursor:default; }
.cpn-say{ margin-top:10px; font-size:.94rem; line-height:1.8; display:none; }
.cpn-say.on{ display:block; }
.cpn-say.ok{ color:#2F7D4A; }
.cpn-say.no{ color:#C4453A; }
</style>
<script>
(function(){
  if(window.StellaCoupon){ return; }
  window.StellaCoupon = 1;

  function build(){
    var num = document.getElementById('oNum');   /* 구슬 잔액 숫자 */
    if(!num){ return 0; }
    if(document.getElementById('cpnBox')){ return 1; }

    /* 구슬 칸(section)을 찾아 그 뒤에 붙입니다 */
    var sec = num;
    while(sec){
      if(sec.tagName === 'SECTION'){ break; }
      sec = sec.parentNode;
      if(sec === document.body){ sec = null; break; }
    }
    if(!sec){ return 0; }

    var box = document.createElement('section');
    box.id = 'cpnBox';
    box.innerHTML =
      '<h2>쿠폰 코드</h2>'
      + '<p class="sub">받으신 코드가 있으면 넣어주세요. 구슬로 들어옵니다.</p>'
      + '<div class="cpn-row">'
      + '<input type="text" id="cpnIn" placeholder="쿠폰 코드" autocomplete="off" '
      + 'autocapitalize="off" spellcheck="false" maxlength="40">'
      + '<button type="button" id="cpnGo">넣기</button>'
      + '</div>'
      + '<div class="cpn-say" id="cpnSay"></div>';

    if(sec.nextSibling){ sec.parentNode.insertBefore(box, sec.nextSibling); }
    else { sec.parentNode.appendChild(box); }

    var inp = document.getElementById('cpnIn');
    var btn = document.getElementById('cpnGo');
    var say = document.getElementById('cpnSay');

    function tell(t, k){
      say.textContent = t;
      say.className = 'cpn-say on ' + (k ? k : '');
    }

    function send(){
      var code = String(inp.value || '').split(' ').join('');
      if(!code){ tell('쿠폰 코드를 넣어주세요.', 'no'); return; }
      btn.disabled = true;
      var was = btn.textContent;
      btn.textContent = '넣는 중…';
      tell('확인하고 있어요…', '');

      fetch('/wp-json/stella/v1/coupon', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        credentials:'same-origin',
        body:JSON.stringify({ code: code })
      })
      .then(function(r){ return r.json().then(function(j){ return {ok:r.ok, j:j}; }); })
      .then(function(res){
        btn.disabled = false;
        btn.textContent = was;
        if(!res.ok){
          var m = '';
          if(res.j){ if(res.j.message){ m = res.j.message; } }
          tell(m ? m : '쿠폰을 넣지 못했어요.', 'no');
          return;
        }
        inp.value = '';
        tell('구슬 ' + res.j.orbs + '개가 들어왔어요. 이제 '
             + res.j.balance + '구슬입니다.', 'ok');
        if(num){ num.textContent = res.j.balance; }
      })
      .catch(function(){
        btn.disabled = false;
        btn.textContent = was;
        tell('잠시 뒤에 다시 해주세요.', 'no');
      });
    }

    btn.addEventListener('click', send);
    inp.addEventListener('keydown', function(e){
      if(e.key === 'Enter'){ send(); }
    });
    return 1;
  }

  /* ── 로그인 쪽 · 코드를 적어둡니다 ─────────────────────
     2026-09-14 · 소희 님 : 「로그인이나 회원가입에 쿠폰입력란도
     있어야 하네」
     ★ 쿠폰은 들어오신 뒤에야 넣을 수 있습니다 — 넣을 계정이 있어야
       하니까요. 그래서 로그인 쪽에서는 코드를 적어만 두고,
       들어오시는 순간 저절로 넣어 드립니다. */
  var KEEP = 'stella_coupon_pending';

  function keep(code){
    try{ localStorage.setItem(KEEP, code); }catch(e){}
  }
  function kept(){
    try{ return localStorage.getItem(KEEP) || ''; }catch(e){ return ''; }
  }
  function drop(){
    try{ localStorage.removeItem(KEEP); }catch(e){}
  }

  function loginBox(){
    if(document.getElementById('cpnKeep')){ return 1; }
    /* 「처음이신가요」 줄이나 로그인 단추를 찾아 그 아래에 둡니다 */
    var all = document.querySelectorAll('p, div, button'), i, host = null;
    for(i = 0; i < all.length; i++){
      if(String(all[i].textContent).indexOf('처음이신가요') < 0){ continue; }
      if(all[i].children.length > 2){ continue; }
      host = all[i];
    }
    if(!host){ return 0; }
    /* 안내 상자(joinNote)가 이미 붙었으면 그 아래에 둡니다 */
    var note = document.getElementById('joinNote');
    if(note){ host = note; }

    var box = document.createElement('div');
    box.id = 'cpnKeep';
    box.setAttribute('style', 'margin-top:14px');
    box.innerHTML =
      '<div style="font-size:.94rem;color:#4E4763;margin-bottom:8px">'
      + '<b style="color:#221C33">쿠폰 코드가 있으신가요?</b> '
      + '여기 적어두시면 들어오시는 순간 넣어드려요.</div>'
      + '<div class="cpn-row">'
      + '<input type="text" id="cpnKeepIn" placeholder="쿠폰 코드" '
      + 'autocomplete="off" autocapitalize="off" spellcheck="false" maxlength="40">'
      + '<button type="button" id="cpnKeepGo">적어두기</button>'
      + '</div><div class="cpn-say" id="cpnKeepSay"></div>';
    if(host.nextSibling){ host.parentNode.insertBefore(box, host.nextSibling); }
    else { host.parentNode.appendChild(box); }

    var inp = document.getElementById('cpnKeepIn');
    var btn = document.getElementById('cpnKeepGo');
    var say = document.getElementById('cpnKeepSay');
    var had = kept();
    if(had){
      inp.value = had;
      say.textContent = '적어뒀어요. 들어오시면 바로 넣어드릴게요.';
      say.className = 'cpn-say on ok';
    }
    btn.addEventListener('click', function(){
      var c = String(inp.value || '').split(' ').join('');
      if(!c){
        say.textContent = '쿠폰 코드를 넣어주세요.';
        say.className = 'cpn-say on no';
        return;
      }
      keep(c);
      say.textContent = '적어뒀어요. 들어오시면 바로 넣어드릴게요.';
      say.className = 'cpn-say on ok';
    });
    return 1;
  }

  /* ── 들어오신 뒤 · 적어둔 코드를 저절로 넣습니다 ─────── */
  function auto(){
    var c = kept();
    if(!c){ return; }
    if(window.StellaCouponTried){ return; }
    window.StellaCouponTried = 1;
    fetch('/wp-json/stella/v1/coupon', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      credentials:'same-origin',
      body:JSON.stringify({ code: c })
    })
    .then(function(r){ return r.json().then(function(j){ return {ok:r.ok, j:j}; }); })
    .then(function(res){
      if(!res.ok){
        /* 아직 안 들어오셨으면 다음에 다시 — 그 밖의 까닭이면 지웁니다 */
        var st = 0;
        if(res.j){ if(res.j.data){ if(res.j.data.status){ st = res.j.data.status; } } }
        if(st === 401){ window.StellaCouponTried = 0; return; }
        drop();
        return;
      }
      drop();
      var num = document.getElementById('oNum');
      if(num){ num.textContent = res.j.balance; }
      var say = document.getElementById('cpnSay');
      if(say){
        say.textContent = '구슬 ' + res.j.orbs + '개가 들어왔어요. 이제 '
                        + res.j.balance + '구슬입니다.';
        say.className = 'cpn-say on ok';
      }
    })
    .catch(function(){ window.StellaCouponTried = 0; });
  }

  var tries = 0;
  var t = setInterval(function(){
    tries++;
    build();
    loginBox();
    if(tries > 60){ clearInterval(t); }
  }, 300);
  build();
  loginBox();
  auto();
})();
</script>
	<?php
} );
