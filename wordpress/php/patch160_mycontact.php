<?php
/* ═══════════════════════════════════════════════════════
   내 자리에 이메일 · 휴대폰 보이기   patch160_mycontact
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   소희 님 : 「마이 페이지에 이메일이랑 전화번호도 있어야 할듯
              입력햇다면」

   왜 필요한가
   들어오시는 길이 이메일 링크 하나뿐입니다. 그런데 내 자리에서
   내 이메일이 무엇인지 볼 수가 없습니다. 오타가 났어도 모릅니다.
   휴대폰도 결제와 안내에 쓰는데 확인할 자리가 없습니다.

   어디에 담겨 있나
       이메일    워드프레스 계정의 user_email
       휴대폰    user meta 'stella_phone'
                 (patch_pay_phone 이 결제 때 쓰고, 문 쪽 gPhone 칸이 받습니다)

   ★ 「있어 보이는데 가짜」인 이메일
     이메일을 안 적으면 guest-XXXX@stellasaju.com 로 계정이 만들어집니다
     (stella-signup 1781줄). 그건 「아직 없음」으로 보여드립니다.

   고치는 길
       이메일    이미 있는 POST /stella/v1/email 이 합니다
       휴대폰    여기서 POST /stella/v1/myphone 을 냅니다

   같이 하는 일 — 큰 제목
   쪽 제목은 「마이 페이지」로 바꿨는데 본문 큰 글씨가 「내 자리」라
   다른 쪽에 온 느낌이 납니다. 쪽 글을 고치지 않고 화면에서만
   갈아 끼웁니다 (앵커를 안 잡으므로 사본이 낡아도 맞습니다).

   되돌리기
   이 스니펫을 끄면 칸이 사라지고 제목도 「내 자리」로 돌아갑니다.
   담긴 값은 그대로입니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'rest_api_init', function () {

	register_rest_route( 'stella/v1', '/contact', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			if ( ! is_user_logged_in() ) {
				return array( 'member' => false );
			}
			$uid   = get_current_user_id();
			$u     = get_userdata( $uid );
			$email = $u ? (string) $u->user_email : '';
			$host  = wp_parse_url( home_url(), PHP_URL_HOST );
			$host  = $host ? $host : 'stellasaju.com';

			$fake = false;
			if ( '' === $email ) { $fake = true; }
			if ( get_user_meta( $uid, 'stella_needs_email', true ) ) { $fake = true; }
			if ( 0 === strpos( $email, 'guest-' ) ) {
				if ( substr( $email, - ( strlen( $host ) + 1 ) ) === '@' . $host ) {
					$fake = true;
				}
			}

			return array(
				'member' => true,
				'email'  => $fake ? '' : $email,
				'phone'  => (string) get_user_meta( $uid, 'stella_phone', true ),
			);
		},
	) );

	register_rest_route( 'stella/v1', '/myphone', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => function ( $req ) {
			if ( ! is_user_logged_in() ) {
				return new WP_Error( 'stella_login', '먼저 들어와 주세요.', array( 'status' => 401 ) );
			}
			$uid = get_current_user_id();
			$raw = (string) $req->get_param( 'phone' );

			/* 숫자만 남깁니다 */
			$num = preg_replace( '/[^0-9]/', '', $raw );
			if ( strlen( $num ) < 9 ) {
				return new WP_Error( 'stella_phone', '휴대폰 번호를 정확히 적어주세요.',
					array( 'status' => 400 ) );
			}
			if ( strlen( $num ) > 11 ) {
				return new WP_Error( 'stella_phone', '휴대폰 번호를 정확히 적어주세요.',
					array( 'status' => 400 ) );
			}

			/* 결제 조각이 쓰는 다듬기가 있으면 그것을 씁니다 — 모양을 맞춥니다 */
			$tidy = $num;
			if ( function_exists( 'stella_pay_tidy_phone' ) ) {
				$t = stella_pay_tidy_phone( $num );
				if ( '' !== $t ) { $tidy = $t; }
			}
			update_user_meta( $uid, 'stella_phone', $tidy );

			return array( 'ok' => true, 'phone' => $tidy );
		},
	) );
} );

add_action( 'wp_footer', function () {
	if ( ! is_page( 'mypage' ) ) { return; }
	?>
<style id="stella-mycontact-css">
#ctBox .ct-row{ display:flex; justify-content:space-between; align-items:baseline;
  gap:14px; padding:13px 0; border-bottom:1px solid #EAE2D2; }
#ctBox .ct-row:last-of-type{ border-bottom:0; }
#ctBox .ct-k{ color:#8B849C; font-size:.92rem; flex:0 0 auto; }
#ctBox .ct-v{ font-family:IBM Plex Mono,monospace; color:#221C33;
  word-break:break-all; text-align:right; }
#ctBox .ct-v.none{ color:#C4453A; font-family:inherit; }
#ctBox .ct-edit{ margin-left:10px; border:0; background:none; padding:0;
  color:#6B4FB0; font:inherit; font-size:.9rem; cursor:pointer;
  text-decoration:underline; }
#ctBox .ct-form{ display:none; margin-top:10px; }
#ctBox .ct-form.on{ display:block; }
#ctBox input{ width:100%; padding:12px 14px; border:1px solid #D5CCB8;
  border-radius:8px; background:#FAF7F0; color:#221C33; font:inherit;
  margin-bottom:8px; }
#ctBox .ct-go{ padding:11px 18px; border:0; border-radius:8px;
  background:linear-gradient(120deg,#3A2E77,#241C4E); color:#FFFDF9;
  font:inherit; font-weight:700; cursor:pointer; }
#ctBox .ct-say{ margin-top:9px; font-size:.92rem; display:none; }
#ctBox .ct-say.on{ display:block; }
#ctBox .ct-say.no{ color:#C4453A; }
#ctBox .ct-say.ok{ color:#2F7D4A; }
#ctBox .ct-why{ margin-top:12px; font-size:.88rem; color:#8B849C; line-height:1.8; }
</style>
<script>
(function(){
  if(window.StellaMyContact){ return; }
  window.StellaMyContact = 1;

  /* 큰 제목을 「마이 페이지」로 — 쪽 글은 안 건드립니다 */
  function retitle(){
    var hs = document.querySelectorAll('#ssm h1, .wrap > h1, h1');
    var i, t;
    for(i = 0; i < hs.length; i++){
      t = String(hs[i].textContent || '').split(' ').join('');
      if(t === '내자리'){ hs[i].textContent = '마이 페이지'; return 1; }
    }
    return 0;
  }
  (function(){
    if(retitle()){ return; }
    var n = 0;
    var tt = setInterval(function(){
      n++;
      if(retitle()){ clearInterval(tt); return; }
      if(n > 30){ clearInterval(tt); }
    }, 200);
  })();

  var data = null;

  function put(){
    var e = document.getElementById('ctMail');
    var p = document.getElementById('ctPhone');
    if(!e){ return; }
    if(data.email){
      e.textContent = data.email;
      e.className = 'ct-v';
    } else {
      e.textContent = '아직 없습니다';
      e.className = 'ct-v none';
    }
    if(data.phone){
      p.textContent = data.phone;
      p.className = 'ct-v';
    } else {
      p.textContent = '아직 없습니다';
      p.className = 'ct-v none';
    }
  }

  function say(id, t, k){
    var s = document.getElementById(id);
    if(!s){ return; }
    s.textContent = t;
    s.className = 'ct-say on ' + (k ? k : '');
  }

  function send(url, body, okFn, sayId, btn){
    var was = btn.textContent;
    btn.disabled = true;
    btn.textContent = '저장 중…';
    fetch(url, {
      method:'POST', headers:{'Content-Type':'application/json'},
      credentials:'same-origin', body:JSON.stringify(body)
    })
    .then(function(r){ return r.json().then(function(j){ return {ok:r.ok, j:j}; }); })
    .then(function(res){
      btn.disabled = false;
      btn.textContent = was;
      if(!res.ok){
        var m = '';
        if(res.j){ if(res.j.message){ m = res.j.message; } }
        say(sayId, m ? m : '저장하지 못했어요.', 'no');
        return;
      }
      okFn(res.j);
      say(sayId, '저장했어요.', 'ok');
    })
    .catch(function(){
      btn.disabled = false;
      btn.textContent = was;
      say(sayId, '잠시 뒤에 다시 해주세요.', 'no');
    });
  }

  function build(){
    var num = document.getElementById('oNum');
    if(!num){ return 0; }
    if(document.getElementById('ctBox')){ return 1; }
    if(!data){ return 0; }

    var sec = num;
    while(sec){
      if(sec.tagName === 'SECTION'){ break; }
      sec = sec.parentNode;
      if(sec === document.body){ sec = null; break; }
    }
    if(!sec){ return 0; }

    var box = document.createElement('section');
    box.id = 'ctBox';
    box.innerHTML =
      '<h2>연락처</h2>'
      + '<p class="sub">들어오실 때와 결제에 쓰는 것들이에요.</p>'
      + '<div class="ct-row"><span class="ct-k">이메일</span>'
      + '<span><span class="ct-v" id="ctMail">—</span>'
      + '<button type="button" class="ct-edit" id="ctMailEdit">고치기</button></span></div>'
      + '<div class="ct-form" id="ctMailForm">'
      + '<input type="email" id="ctMailIn" placeholder="you@example.com" '
      + 'autocomplete="email" autocapitalize="off" spellcheck="false">'
      + '<button type="button" class="ct-go" id="ctMailGo">저장</button>'
      + '<div class="ct-say" id="ctMailSay"></div></div>'
      + '<div class="ct-row"><span class="ct-k">휴대폰</span>'
      + '<span><span class="ct-v" id="ctPhone">—</span>'
      + '<button type="button" class="ct-edit" id="ctPhoneEdit">고치기</button></span></div>'
      + '<div class="ct-form" id="ctPhoneForm">'
      + '<input type="tel" id="ctPhoneIn" placeholder="010-1234-5678" '
      + 'inputmode="numeric" autocomplete="tel" maxlength="20">'
      + '<button type="button" class="ct-go" id="ctPhoneGo">저장</button>'
      + '<div class="ct-say" id="ctPhoneSay"></div></div>'
      + '<div class="ct-why">이메일이 틀리면 폰을 바꾸거나 브라우저를 지웠을 때 '
      + '받으신 풀이를 다시 찾으실 수 없어요. 한 번 봐주세요.</div>';

    if(sec.nextSibling){ sec.parentNode.insertBefore(box, sec.nextSibling); }
    else { sec.parentNode.appendChild(box); }

    put();

    document.getElementById('ctMailEdit').addEventListener('click', function(){
      var f = document.getElementById('ctMailForm');
      f.className = 'ct-form on';
      var i = document.getElementById('ctMailIn');
      i.value = data.email ? data.email : '';
      i.focus();
    });
    document.getElementById('ctPhoneEdit').addEventListener('click', function(){
      var f = document.getElementById('ctPhoneForm');
      f.className = 'ct-form on';
      var i = document.getElementById('ctPhoneIn');
      i.value = data.phone ? data.phone : '';
      i.focus();
    });

    document.getElementById('ctMailGo').addEventListener('click', function(){
      var v = String(document.getElementById('ctMailIn').value || '').split(' ').join('');
      if(v.indexOf('@') < 1){ say('ctMailSay', '이메일을 정확히 적어주세요.', 'no'); return; }
      send('/wp-json/stella/v1/email', { email: v }, function(j){
        data.email = j.email ? j.email : v;
        put();
        document.getElementById('ctMailForm').className = 'ct-form';
      }, 'ctMailSay', this);
    });

    document.getElementById('ctPhoneGo').addEventListener('click', function(){
      var v = String(document.getElementById('ctPhoneIn').value || '');
      send('/wp-json/stella/v1/myphone', { phone: v }, function(j){
        data.phone = j.phone ? j.phone : v;
        put();
        document.getElementById('ctPhoneForm').className = 'ct-form';
      }, 'ctPhoneSay', this);
    });

    return 1;
  }

  fetch('/wp-json/stella/v1/contact', { credentials:'same-origin' })
    .then(function(r){ return r.json(); })
    .then(function(d){
      if(!d){ return; }
      if(!d.member){ return; }
      data = d;
      build();
      var tries = 0;
      var t = setInterval(function(){
        tries++;
        if(build()){ clearInterval(t); return; }
        if(tries > 60){ clearInterval(t); }
      }, 300);
    })
    .catch(function(){});
})();
</script>
	<?php
} );
