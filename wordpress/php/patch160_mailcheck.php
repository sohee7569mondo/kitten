<?php
/* ═══════════════════════════════════════════════════════
   결제 전에 이메일 한 번 더 보기     patch160_mailcheck
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」
   ★ stella-signup 조각이 켜져 있어야 이메일을 고칠 수 있습니다.

   소희 님 : 「대충 둘러볼라고 이메일을 아무거나 눌렀어 그런데 결제를
              햇어 그런데 핸드폰이나 피씨가 리셋되면 어떻게 해?」
             「결제 누르면 확인 이메일이 맞는지만 틀리면 재입력하는
              방식이면 될거 같아」

   왜 필요한가
   들어오시는 길이 이메일 링크 하나뿐입니다. 이메일이 틀리면
   브라우저가 지워지는 순간 계정을 영영 못 찾습니다 — 돈은 냈는데
   책이 없어집니다. 약관 제4조에도 「계정이 그 브라우저에만 묶입니다」
   라고 적혀 있습니다.

   무엇을 하나
   결제 단추를 누르면 결제창이 열리기 전에 한 번 여쭙니다.
       받으실 곳   abc@gmail.com
       [ 맞아요, 결제할게요 ]   [ 고칠게요 ]
   이메일이 아예 없으면 넣으셔야 넘어갑니다 — 그때가 제일 위험합니다.

   ★ 이메일을 화면에 알려주는 길이 없어서 하나 냅니다
     /me 도 window.STELLA_USER 도 이메일을 안 담고 있습니다.
     그래서 GET /wp-json/stella/v1/myemail 를 엽니다 —
     들어오신 본인 것만 돌려줍니다. 남의 것은 못 봅니다.
     고치는 일은 이미 있는 POST /wp-json/stella/v1/email 이 합니다.

   되돌리기
   이 스니펫을 끄면 확인 단계가 사라집니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'rest_api_init', function () {
	register_rest_route( 'stella/v1', '/myemail', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			if ( ! is_user_logged_in() ) {
				return array( 'member' => false, 'email' => '' );
			}
			/* ★ 이메일을 안 적으신 분은 임시 주소로 계정이 만들어집니다 —
			   guest-XXXXXXXXXXXX@stellasaju.com 꼴입니다 (stella-signup 1781줄).
			   「있어 보이지만 가짜」라서, 이걸 진짜로 세면 안 됩니다.
			   stella_needs_email 표시도 같이 봅니다. */
			$uid   = get_current_user_id();
			$u     = get_userdata( $uid );
			$email = $u ? (string) $u->user_email : '';
			$host  = wp_parse_url( home_url(), PHP_URL_HOST );
			$host  = $host ? $host : 'stellasaju.com';

			$fake = false;
			if ( '' === $email ) { $fake = true; }
			if ( get_user_meta( $uid, 'stella_needs_email', true ) ) { $fake = true; }
			/* 임시 주소는 guest- 로 시작하면서 우리 도메인인 것만입니다.
			   소희 님이나 식구가 쓰시는 진짜 @stellasaju.com 주소까지
			   가짜로 보면 안 됩니다. 둘 다 맞을 때만 가짜로 셉니다. */
			if ( 0 === strpos( $email, 'guest-' ) ) {
				if ( substr( $email, - ( strlen( $host ) + 1 ) ) === '@' . $host ) {
					$fake = true;
				}
			}

			return array(
				'member' => true,
				'email'  => $fake ? '' : $email,
				'real'   => ! $fake,
			);
		},
	) );
} );

add_action( 'wp_footer', function () {
	/* 결제 앞(마지막 그물)과 문 여섯(입구)에서 돕니다. */
	if ( ! is_page( array( 'pay', 'door-love', 'door-career', 'door-health',
	                       'door-fortune', 'door-astro', 'door-tarot' ) ) ) { return; }
	?>
<style id="stella-mailcheck-css">
#mkBox{ margin-top:18px; padding:18px 20px; border-radius:10px;
  background:#F3EFFA; border:1px solid #D9CFF2; display:none; }
#mkBox.on{ display:block; }
#mkBox .mk-k{ font-size:.9rem; color:#8B849C; }
#mkBox .mk-v{ font-family:IBM Plex Mono,monospace; font-size:1.02rem;
  color:#221C33; word-break:break-all; margin:4px 0 10px; }
#mkBox .mk-why{ font-size:.9rem; color:#4E4763; line-height:1.85; margin-bottom:14px; }
#mkBox .mk-row{ display:flex; gap:8px; flex-wrap:wrap; }
#mkBox .mk-row button{ flex:0 0 auto; padding:12px 18px; border:0;
  border-radius:8px; font:inherit; font-weight:700; cursor:pointer; }
#mkBox .mk-ok{ background:linear-gradient(120deg,#3A2E77,#241C4E); color:#FFFDF9; }
#mkBox .mk-no{ background:none; color:#221C33; border:1px solid #D5CCB8 !important; }
#mkBox input{ width:100%; padding:12px 14px; border:1px solid #D5CCB8;
  border-radius:8px; background:#FFFFFF; color:#221C33; font:inherit;
  margin-bottom:10px; }
#mkBox .mk-say{ margin-top:10px; font-size:.92rem; display:none; }
#mkBox .mk-say.on{ display:block; }
#mkBox .mk-say.no{ color:#C4453A; }
</style>
<script>
(function(){
  if(window.StellaMailCheck){ return; }
  window.StellaMailCheck = 1;

  var okToGo = 0, mail = '', asked = 0;

  function box(){
    var b = document.getElementById('mkBox');
    if(b){ return b; }
    var go = document.getElementById('oGo');
    if(!go){ return null; }
    b = document.createElement('div');
    b.id = 'mkBox';
    b.innerHTML =
      '<div class="mk-k">받으실 곳</div>'
      + '<div class="mk-v" id="mkMail">—</div>'
      + '<div class="mk-why" id="mkWhy">폰을 바꾸거나 브라우저를 지우면 '
      + '<b>이 이메일로만</b> 다시 찾으실 수 있어요. 맞는지 한 번만 봐주세요.</div>'
      + '<div id="mkEdit" style="display:none">'
      + '<input type="email" id="mkIn" placeholder="이메일" autocomplete="email" '
      + 'autocapitalize="off" spellcheck="false"></div>'
      + '<div class="mk-row">'
      + '<button type="button" class="mk-ok" id="mkYes">맞아요, 결제할게요</button>'
      + '<button type="button" class="mk-no" id="mkNo">고칠게요</button>'
      + '</div><div class="mk-say" id="mkSay"></div>';
    go.parentNode.insertBefore(b, go.nextSibling);
    wire();
    return b;
  }

  function say(t, k){
    var s = document.getElementById('mkSay');
    if(!s){ return; }
    s.textContent = t;
    s.className = 'mk-say on ' + (k ? k : '');
  }

  function editOn(){
    var e = document.getElementById('mkEdit');
    var i = document.getElementById('mkIn');
    var y = document.getElementById('mkYes');
    if(e){ e.style.display = 'block'; }
    if(i){ i.value = mail; i.focus(); }
    if(y){ y.textContent = '이 이메일로 바꾸고 결제'; }
  }

  function wire(){
    var yes = document.getElementById('mkYes');
    var no  = document.getElementById('mkNo');
    if(no){
      no.addEventListener('click', function(){ editOn(); });
    }
    if(yes){
      yes.addEventListener('click', function(){
        var e = document.getElementById('mkEdit');
        var open = 0;
        if(e){ if(e.style.display === 'block'){ open = 1; } }
        if(!open){ pass(); return; }

        var v = String(document.getElementById('mkIn').value || '').split(' ').join('');
        if(v.indexOf('@') < 1){ say('이메일을 정확히 적어주세요.', 'no'); return; }
        say('바꾸고 있어요…', '');
        fetch('/wp-json/stella/v1/email', {
          method:'POST', headers:{'Content-Type':'application/json'},
          credentials:'same-origin', body:JSON.stringify({ email: v })
        })
        .then(function(r){ return r.json().then(function(j){ return {ok:r.ok, j:j}; }); })
        .then(function(res){
          if(!res.ok){
            var m = '';
            if(res.j){ if(res.j.message){ m = res.j.message; } }
            say(m ? m : '바꾸지 못했어요.', 'no');
            return;
          }
          mail = v;
          document.getElementById('mkMail').textContent = v;
          pass();
        })
        .catch(function(){ say('잠시 뒤에 다시 해주세요.', 'no'); });
      });
    }
  }

  /* 확인이 끝나면 원래 결제 단추를 그대로 한 번 더 누릅니다 */
  function pass(){
    okToGo = 1;
    var b = document.getElementById('mkBox');
    if(b){ b.className = ''; }
    var go = document.getElementById('oGo');
    if(go){ go.click(); }
  }

  function show(){
    var b = box();
    if(!b){ return; }
    document.getElementById('mkMail').textContent = mail ? mail : '아직 없습니다';
    if(!mail){
      document.getElementById('mkWhy').innerHTML =
        '<b>이메일이 아직 없습니다.</b> 지금 넣지 않으시면 폰을 바꾸거나 '
        + '브라우저를 지웠을 때 이 풀이를 다시 찾으실 수 없어요.';
      editOn();
    }
    b.className = 'on';
    b.scrollIntoView({ behavior:'smooth', block:'center' });
  }

  /* ── 문 쪽 · 이메일을 비우고 못 넘어가게 ──────────────────
     2026-09-14 · 소희 님 : 「이메일 란을 필수로 해야해」
     쪽에는 이미 「이메일 · 필수 (결제창을 열려면 꼭 필요해요)」라고
     적혀 있는데, 비워두면 서버가 임시 주소(guest-...@stellasaju.com)로
     계정을 만들어 그냥 넘어갑니다. 말과 동작이 어긋나 있었습니다.
     여기서 실제로 막습니다. */
  function mailOk(v){
    var s = String(v || '').split(' ').join('');
    var at = s.indexOf('@');
    if(at < 1){ return ''; }
    var dot = s.indexOf('.', at + 2);
    if(dot < 0){ return ''; }
    if(dot >= s.length - 1){ return ''; }
    return s;
  }

  function doorSay(t){
    var f = document.getElementById('gEmail');
    if(!f){ return; }
    var s = document.getElementById('mkDoorSay');
    if(!s){
      s = document.createElement('div');
      s.id = 'mkDoorSay';
      s.setAttribute('style',
        'margin-top:7px;font-size:.9rem;line-height:1.7;color:#C4453A;');
      if(f.nextSibling){ f.parentNode.insertBefore(s, f.nextSibling); }
      else { f.parentNode.appendChild(s); }
    }
    s.textContent = t;
  }

  document.addEventListener('click', function(e){
    var t = e.target;
    if(!t){ return; }
    if(t.id !== 'goBtn'){ return; }
    var f = document.getElementById('gEmail');
    if(!f){ return; }
    var v = mailOk(f.value);
    if(v){
      doorSay('');
      if(f.value !== v){ f.value = v; }
      return;
    }
    e.preventDefault();
    e.stopPropagation();
    doorSay('이메일을 넣어주세요. 폰을 바꾸거나 브라우저를 지우면 '
          + '이 이메일로만 받으신 풀이를 다시 찾으실 수 있어요.');
    try{ f.focus(); }catch(err){}
    try{ f.scrollIntoView({ behavior:'smooth', block:'center' }); }catch(err){}
  }, true);

  /* 결제 단추를 가로챕니다 — 확인 전에는 결제창이 안 열립니다 */
  document.addEventListener('click', function(e){
    var t = e.target;
    if(!t){ return; }
    if(t.id !== 'oGo'){ return; }
    if(okToGo){ return; }
    e.preventDefault();
    e.stopPropagation();
    if(asked){ show(); return; }
    asked = 1;
    fetch('/wp-json/stella/v1/myemail', { credentials:'same-origin' })
      .then(function(r){ return r.json(); })
      .then(function(d){
        mail = '';
        if(d){ if(d.email){ mail = String(d.email); } }
        show();
      })
      .catch(function(){ show(); });
  }, true);
})();
</script>
	<?php
} );
