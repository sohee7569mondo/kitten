<?php
/**
 * STELLA SAJU — 스타 사주(페이지 406) · 이름으로 바로 펴기
 *
 *  홈의 「이번주 ○○○ 스타 운세」 단추가 /star-saju/?star=이름 으로 옵니다.
 *  이 스니펫은 그 이름을 읽어 그 사람의 사주를 바로 펼쳐 보여줍니다.
 *  주소에 이름이 없으면 예전과 한 치도 다르지 않습니다.
 *
 *  쓰는 법 (WPCode Lite) — PHP · 자동 실행 안 함
 *    확인 : https://stellasaju.com/?stella_patch=dry
 *    적용 : https://stellasaju.com/?stella_patch=go
 *    되돌리기 : https://stellasaju.com/?stella_patch=undo
 *    다 되면 스니펫을 지우세요.
 */

add_action( 'init', function () {

	if ( ! isset( $_GET['stella_patch'] ) && ! isset( $_GET['stella_star'] ) ) { return; }
	if ( ! current_user_can( 'manage_options' ) ) { return; }

	$mode = isset( $_GET['stella_patch'] ) ? sanitize_text_field( wp_unslash( $_GET['stella_patch'] ) )
	                                       : sanitize_text_field( wp_unslash( $_GET['stella_star'] ) );

	global $wpdb;
	$post_id = 406;
	$bak_key = 'stella_bak_406_star';
	$expect_from  = '9d4733593f25963877c7739d84b99292c3fa8bd2';
	$expect_hash  = '2d4080b531d39c7732ff76c02f1066cd809f4eea';
	$expect_delta = 780;

	header( 'Content-Type: text/html; charset=utf-8' );
	echo '<meta charset="utf-8"><style>body{font:15px/1.7 -apple-system,"Apple SD Gothic Neo",sans-serif;max-width:940px;margin:40px auto;padding:0 20px}';
	echo 'code{background:#f4f4f4;padding:1px 5px;border-radius:3px}';
	echo '.ok{color:#0a7a2f}.no{color:#c0392b;font-weight:700}.box{border:1px solid #ddd;border-radius:8px;padding:14px 18px;margin:14px 0}</style>';
	echo '<h2>스타 사주(페이지 406) &middot; 이름으로 바로 펴기</h2>';

	if ( 'undo' === $mode ) {
		$bak = get_option( $bak_key );
		if ( ! $bak ) { echo '<p class="no">되돌릴 백업이 없습니다.</p>'; exit; }
		$wpdb->update( $wpdb->posts, array( 'post_content' => $bak ), array( 'ID' => $post_id ) );
		clean_post_cache( $post_id );
		echo '<p class="ok">되돌렸습니다.</p>'; exit;
	}

	$content = $wpdb->get_var( $wpdb->prepare( "SELECT post_content FROM {$wpdb->posts} WHERE ID = %d", $post_id ) );
	if ( null === $content ) { echo '<p class="no">페이지 406 을 찾지 못했습니다.</p>'; exit; }

	$old_hash = sha1( $content );
	$from_ok  = ( $old_hash === $expect_from );
	echo '<div class="box">지금 길이 <b>' . strlen( $content ) . '</b> 바이트 · sha1 <code>' . substr( $old_hash, 0, 12 ) . '…</code> ';
	$already = ( $old_hash === $expect_hash );
	if ( $from_ok ) { echo '<span class="ok">(바탕이 맞습니다)</span>'; }
	elseif ( $already ) { echo '<span class="ok">(이미 다 들어간 모습입니다)</span>'; }
	else { echo '<span class="no">(제가 보고 만든 바탕과 다릅니다)</span>'; }
	echo '</div>';
	/* 2026-08-31 · 이미 들어간 상태를 「어긋남」이라고 잘못 말하던 것을 고칩니다.
	   두 번째로 여시면 지금 해시가 「고친 뒤」 해시와 같습니다. 그건 사고가 아니라
	   이미 성공했다는 뜻이므로, 빨간 글씨 대신 그렇게 알려드립니다. */
	if ( ! $from_ok && $already ) {
		echo '<p class="ok"><b>이미 들어가 있습니다.</b> 지금 페이지가 바로 「고친 뒤」의 모습입니다 ';
		echo '&mdash; sha1 <code>' . substr( $expect_hash, 0, 12 ) . '…</code> 가 그 증거입니다.</p>';
		echo '<p>더 하실 일이 없습니다. <b>이 스니펫은 지우셔도 됩니다.</b><br>';
		echo '되돌리시려면 <code>?stella_patch=undo</code> 로 여세요.</p>';
		exit;
	}
	if ( ! $from_ok ) { echo '<p class="no">바탕이 달라 아무것도 바꾸지 않았습니다.</p>'; exit; }

	$fixnl = function ( $t ) { return str_replace( array( "\r\n", "\r" ), "\n", $t ); };
	$mkre  = function ( $find ) use ( $fixnl ) {
		$lines = explode( "\n", $fixnl( $find ) );
		foreach ( $lines as $i => $l ) { $lines[ $i ] = preg_quote( $l, '/' ); }
		return '/' . implode( '\r?\n', $lines ) . '/u';
	};

	$find = '
  draw();
})();';
	$rep  = '
  draw();

  /* 2026-08-31 · 홈의 「이번주 ○○○ 스타 운세」에서 넘어오시면
     그 사람의 사주를 바로 펴 드립니다.  /star-saju/?star=이름
     앰퍼샌드는 글자 코드로 만들어 씁니다 — 이 파일에 직접 쓰면
     워드프레스가 엔티티로 바꿔 스크립트가 죽습니다. */
  try{ (function(){
    var q = String(location.search || \'\');
    var at = q.indexOf(\'star=\');
    if(at < 0){ return; }
    var v = q.slice(at + 5);
    var amp = String.fromCharCode(38);
    var cut = v.indexOf(amp);
    if(cut >= 0){ v = v.slice(0, cut); }
    var nm = \'\';
    try{ nm = decodeURIComponent(v.replace(/\\+/g, \' \')); }catch(e2){ nm = v; }
    if(!nm){ return; }
    if(!find(nm)){ return; }
    open(nm);
  }()); }catch(err){}
})();';

	$re = $mkre( $find );
	$n  = preg_match_all( $re, $content );
	echo '<div class="box">자리 찾기 — 찾은 수 <b class="' . ( 1 === $n ? 'ok' : 'no' ) . '">' . $n . '</b> / 1</div>';
	if ( 1 !== $n ) { echo '<p class="no">어긋납니다. 아무것도 바꾸지 않았습니다.</p>'; exit; }

	$rp      = $fixnl( $rep );
	$updated = preg_replace_callback( $re, function ( $m ) use ( $rp ) { return $rp; }, $content, 1 );

	$len_ok  = ( ( strlen( $updated ) - strlen( $content ) ) === $expect_delta );
	$hash_ok = ( sha1( $updated ) === $expect_hash );
	echo '<div class="box">고친 뒤 <b>' . strlen( $updated ) . '</b> 바이트 (<b class="' . ( $len_ok ? 'ok' : 'no' ) . '">' . sprintf( '%+d', strlen( $updated ) - strlen( $content ) ) . '</b> · 기대 ' . sprintf( '%+d', $expect_delta ) . ')<br>';
	echo 'sha1 <code>' . substr( sha1( $updated ), 0, 12 ) . '…</code> · 기대 <code>' . substr( $expect_hash, 0, 12 ) . '…</code> ';
	echo $hash_ok ? '<span class="ok">일치</span>' : '<span class="no">불일치</span>';
	echo '<br>앰퍼샌드 두 개 (0이어야) : <b>' . substr_count( $updated, '&&' ) . '</b></div>';
	if ( ! $len_ok || ! $hash_ok ) { echo '<p class="no">어긋납니다. 아무것도 바꾸지 않았습니다.</p>'; exit; }

	if ( 'go' !== $mode ) {
		echo '<p class="ok"><b>확인만 했습니다. 아무것도 바꾸지 않았습니다.</b></p>';
		echo '<p>이대로 넣으시려면 <code>?stella_patch=go</code> 로 여세요.</p>'; exit;
	}

	/* 2026-08-31 · 백업은 처음 한 번만 남깁니다.
	   이 스니펫을 두 번 돌리시면 두 번째에는 「이미 고친 것」이 백업으로 덮여서
	   되돌리기가 원래 자리까지 못 갑니다. 그래서 백업이 이미 있으면 손대지 않습니다. */
	if ( false === get_option( $bak_key ) ) { update_option( $bak_key, $content, false ); }
	$done = $wpdb->update( $wpdb->posts, array( 'post_content' => $updated ), array( 'ID' => $post_id ) );
	clean_post_cache( $post_id );
	$check = $wpdb->get_var( $wpdb->prepare( "SELECT post_content FROM {$wpdb->posts} WHERE ID = %d", $post_id ) );

	echo '<h3>' . ( sha1( $check ) === $expect_hash ? '<span class="ok">넣었습니다.</span>' : '<span class="no">확인 실패</span>' ) . '</h3>';
	echo '<p>시험해보기 : <a href="https://stellasaju.com/star-saju/?star=%EC%9C%A0%EC%9E%AC%EC%84%9D">/star-saju/?star=유재석</a></p>';
	echo '<p>되돌리려면 <code>?stella_patch=undo</code>. <b>이 스니펫은 이제 지우셔도 됩니다.</b></p>';
	exit;
}, 1 );
