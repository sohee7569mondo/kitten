<?php
/* ═══════════════════════════════════════════════════════
   문 두 쪽의 폭을 나란히 재기   tool_doorwide
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」
   ★ 관리자로 로그인한 창에서 여세요.

       https://stellasaju.com/?stella_doorwide=1

   소희 님 : 「며칠 전부터 얘기한건데 벼리만 폭이 틀려 좁아……
              데스크탑에서만 한한 거지만」

   왜 이 도구인가
   door-love 와 door-career 의 CSS 는 제 사본에서 글자 하나 안 틀리고
   같습니다. 블록 형식도 둘 다 classic 으로 같고요. 그러면 차이는
   쪽 글 밖에 있습니다 — 얹힌 스니펫이거나 바깥 상자입니다.

   짐작으로 CSS 를 덧대면 한 쪽은 이기고 한 쪽은 집니다
   (2026-09-14 에 책 폭에서 그렇게 한 번 헤맸습니다).
   그래서 **두 쪽을 같은 폭의 틀에 넣고 실제로 재서** 나란히 놓습니다.
   다른 값만 붉게 나옵니다. 그 줄이 범인입니다.

   어떻게 재나
     보이지 않는 틀(iframe) 둘에 두 문을 1280px 폭으로 띄우고,
     #ssg 와 그 위 조상들을 body 까지 훑어 실제 그려진 넓이와
     max-width · 안팎 여백 · overflow 를 읽습니다.
     읽기만 합니다. 아무것도 바꾸지 않습니다.

   ★ 틀 안은 진짜 쪽이라 다른 스니펫도 다 실립니다. 그래서
     「살아 있는 화면 그대로」의 값이 나옵니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'template_redirect', function () {

	if ( ! isset( $_GET['stella_doorwide'] ) ) { return; }
	if ( ! is_user_logged_in() ) {
		wp_die( '관리자로 로그인한 창에서 열어주세요.', '스텔라', array( 'response' => 200 ) );
	}
	if ( ! current_user_can( 'manage_options' ) ) {
		wp_die( '관리자만 볼 수 있습니다.', '스텔라', array( 'response' => 200 ) );
	}

	$a = isset( $_GET['a'] ) ? sanitize_title( wp_unslash( $_GET['a'] ) ) : 'door-love';
	$b = isset( $_GET['b'] ) ? sanitize_title( wp_unslash( $_GET['b'] ) ) : 'door-career';
	$w = isset( $_GET['w'] ) ? max( 480, min( 2200, (int) $_GET['w'] ) ) : 1280;

	nocache_headers();
	header( 'Content-Type: text/html; charset=utf-8' );

	echo '<!doctype html><meta charset="utf-8">';
	echo '<meta name="viewport" content="width=device-width,initial-scale=1">';
	echo '<title>문 폭 견주기</title>';
	echo '<style>
body{margin:0;padding:24px 18px 90px;background:#F1EDE3;color:#221C33;
  font:15px/1.75 -apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;}
.w{max-width:1000px;margin:0 auto;}
h1{font-size:1.3rem;margin:0 0 6px;}
.dek{color:#8B849C;font-size:.9rem;margin:0 0 22px;}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #E2DACB;
  border-radius:9px;overflow:hidden;margin-top:14px;}
td,th{padding:9px 11px;border-bottom:1px solid #EFE9DC;text-align:left;
  font-size:.86rem;vertical-align:top;font-family:"IBM Plex Mono",monospace;}
th{background:#FAF7F0;color:#8B849C;font-weight:600;font-family:inherit;}
tr:last-child td{border-bottom:0;}
tr.diff td{background:#FBEFEE;color:#C4453A;font-weight:700;}
.lay{font-family:inherit;color:#4E4763;}
#frames{position:absolute;left:-9999px;top:0;}
#say{margin-top:16px;padding:14px 16px;border-radius:9px;background:#FFFDF9;
  border:1px solid #E2DACB;font-size:.92rem;}
.big{margin-top:16px;padding:15px 18px;border-radius:10px;
  background:#FBEFEE;border:1px solid #EBC7C3;color:#C4453A;font-weight:700;}
.big.fine{background:#EDF7F0;border-color:#BFE0C9;color:#2F7D4A;}
</style>';

	echo '<div class="w"><h1>문 두 쪽의 폭을 나란히</h1>';
	echo '<p class="dek">' . esc_html( $a ) . '  vs  ' . esc_html( $b )
		. '  ·  틀 너비 ' . (int) $w . 'px  ·  읽기만 합니다</p>';
	echo '<div id="say">재는 중…</div>';
	echo '<div id="out"></div>';
	echo '<div id="frames">'
		. '<iframe id="fa" src="/' . esc_attr( $a ) . '/" width="' . (int) $w . '" height="1500"></iframe>'
		. '<iframe id="fb" src="/' . esc_attr( $b ) . '/" width="' . (int) $w . '" height="1500"></iframe>'
		. '</div>';
	?>
<script>
(function(){
  var A = '<?php echo esc_js( $a ); ?>';
  var B = '<?php echo esc_js( $b ); ?>';
  var say = document.getElementById('say');
  var out = document.getElementById('out');

  function px(v){ return Math.round(v * 10) / 10; }

  function measure(doc, win){
    var rows = [];
    var el = doc.getElementById('ssg');
    if(!el){
      var main = doc.querySelector('[id^="ss"]');
      el = main;
    }
    if(!el){ return null; }

    /* 안쪽 몇 가지를 먼저 */
    var inner = [
      ['#ssg .g-inner', el.querySelector ? el.querySelector('.g-inner') : null],
      ['#ssg .g-cols',  el.querySelector ? el.querySelector('.g-cols')  : null]
    ];
    var i, n, cs, r;
    for(i = 0; i < inner.length; i++){
      n = inner[i][1];
      if(!n){ rows.push([inner[i][0], '(없음)']); continue; }
      cs = win.getComputedStyle(n);
      r = n.getBoundingClientRect();
      rows.push([inner[i][0], px(r.width) + 'px   max ' + cs.maxWidth
        + '   pad ' + cs.paddingLeft + '/' + cs.paddingRight]);
    }

    /* #ssg 부터 body 까지 거슬러 올라가며 */
    n = el;
    var depth = 0;
    while(n){
      cs = win.getComputedStyle(n);
      r = n.getBoundingClientRect();
      var who = n.tagName.toLowerCase();
      if(n.id){ who += '#' + n.id; }
      else if(n.className){
        var c = String(n.className).split(' ').join('.');
        if(c.length > 40){ c = c.slice(0, 40) + '…'; }
        if(c){ who += '.' + c; }
      }
      rows.push([
        (depth === 0 ? '' : '↑ ') + who,
        px(r.width) + 'px   max ' + cs.maxWidth
        + '   mar ' + cs.marginLeft + '/' + cs.marginRight
        + '   pad ' + cs.paddingLeft + '/' + cs.paddingRight
        + '   ovf ' + cs.overflowX
      ]);
      if(n.tagName.toLowerCase() === 'body'){ break; }
      n = n.parentElement;
      depth++;
      if(depth > 14){ break; }
    }
    rows.push(['(틀 너비)', win.innerWidth + 'px']);
    return rows;
  }

  function draw(ra, rb){
    var map = {}, order = [], i, k;
    for(i = 0; i < ra.length; i++){
      k = ra[i][0];
      if(!map[k]){ map[k] = ['', '']; order.push(k); }
      map[k][0] = ra[i][1];
    }
    for(i = 0; i < rb.length; i++){
      k = rb[i][0];
      if(!map[k]){ map[k] = ['', '']; order.push(k); }
      map[k][1] = rb[i][1];
    }

    var h = '<table><tr><th class="lay">어디</th><th class="lay">' + A
      + '</th><th class="lay">' + B + '</th></tr>';
    var bad = 0;
    for(i = 0; i < order.length; i++){
      k = order[i];
      var d = (map[k][0] !== map[k][1]);
      if(d){ bad++; }
      h += '<tr' + (d ? ' class="diff"' : '') + '><td class="lay">' + k + '</td>'
        + '<td>' + (map[k][0] || '—') + '</td>'
        + '<td>' + (map[k][1] || '—') + '</td></tr>';
    }
    h += '</table>';
    h += bad
      ? '<div class="big">다른 자리 ' + bad + '군데 — 붉은 줄이 범인입니다.</div>'
      : '<div class="big fine">두 쪽이 똑같습니다. 폭 차이가 없습니다.</div>';
    out.innerHTML = h;
    say.textContent = '다 쟀습니다.';
  }

  var got = {};
  function tryDraw(){
    if(!got.a){ return; }
    if(!got.b){ return; }
    draw(got.a, got.b);
  }

  function hook(id, key, name){
    var f = document.getElementById(id);
    f.addEventListener('load', function(){
      setTimeout(function(){
        try{
          var d = f.contentDocument;
          var win = f.contentWindow;
          var r = measure(d, win);
          if(!r){
            say.textContent = '★ ' + name + ' 쪽에서 #ssg 를 못 찾았습니다.';
            return;
          }
          got[key] = r;
          tryDraw();
        }catch(e){
          say.textContent = '★ ' + name + ' 을 읽다가 멈췄습니다 — ' + e.message;
        }
      }, 900);
    });
  }
  hook('fa', 'a', A);
  hook('fb', 'b', B);
})();
</script>
	<?php
	exit;
}, 1 );
