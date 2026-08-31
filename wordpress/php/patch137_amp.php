<?php
/**
 * STELLA SAJU — 페이지 137 (/reading-start/) 응급 수정
 *
 *  증상 : 「시작할게요」 버튼이 안 눌립니다. 어느 가디언이든 마찬가지입니다.
 *         (스크립트가 죽으면 화면은 붙박이로 적힌 「직성의 신」에서 멈춥니다.
 *          그래서 직성의 신만 고장난 것처럼 보입니다.)
 *
 *  원인 : script 안에 앰퍼샌드 두 개(&&)가 두 군데 들어가 있습니다.
 *         이 파일의 머리말이 직접 금지해 둔 것입니다 —
 *         「주의: script 안에서 앰퍼샌드 두 개 연산자를 쓰지 마세요.
 *           워드프레스가 엔티티로 바꿉니다.」
 *         엔티티로 바뀌면 브라우저가 스크립트 전체를 읽다 말고 멈춥니다.
 *         그러면 버튼에 손을 다는 일도 함께 사라집니다.
 *
 *  고치는 법 : 두 줄을 앰퍼샌드 없는 형태로 바꿉니다. 하는 일은 똑같습니다.
 *
 *  쓰는 법 (WPCode Lite)
 *    1) 새 스니펫 · PHP · 자동 실행 안 함(Do Not Run Automatically) 으로 저장
 *    2) 아래 주소를 열어 먼저 확인합니다 (아무것도 바꾸지 않습니다)
 *         https://stellasaju.com/?stella_patch=dry
 *    3) 초록불이면
 *         https://stellasaju.com/?stella_patch=go
 *    4) 되돌리려면
 *         https://stellasaju.com/?stella_patch=undo
 *    5) 다 되면 이 스니펫을 지웁니다.
 */

add_action( 'init', function () {

	if ( ! isset( $_GET['stella_patch'] ) && ! isset( $_GET['stella_137'] ) ) { return; }
	if ( ! current_user_can( 'manage_options' ) ) { return; }

	$mode = isset( $_GET['stella_patch'] ) ? sanitize_text_field( wp_unslash( $_GET['stella_patch'] ) )
	                                       : sanitize_text_field( wp_unslash( $_GET['stella_137'] ) );

	global $wpdb;
	$post_id  = 137;
	$bak_key  = 'stella_bak_137_amp';

	header( 'Content-Type: text/html; charset=utf-8' );
	echo '<meta charset="utf-8"><style>body{font:15px/1.7 -apple-system,"Apple SD Gothic Neo",sans-serif;max-width:900px;margin:40px auto;padding:0 20px}';
	echo 'code{background:#f4f4f4;padding:1px 5px;border-radius:3px;word-break:break-all}';
	echo '.ok{color:#0a7a2f}.no{color:#c0392b;font-weight:700}.box{border:1px solid #ddd;border-radius:8px;padding:14px 18px;margin:14px 0}</style>';
	echo '<h2>페이지 137 · 앰퍼샌드 응급 수정</h2>';

	/* ── 되돌리기 ───────────────────────────────────────── */
	if ( 'undo' === $mode ) {
		$bak = get_option( $bak_key );
		if ( ! $bak ) { echo '<p class="no">되돌릴 백업이 없습니다.</p>'; exit; }
		$wpdb->update( $wpdb->posts, array( 'post_content' => $bak ), array( 'ID' => $post_id ) );
		clean_post_cache( $post_id );
		echo '<p class="ok">되돌렸습니다. 길이 ' . strlen( $bak ) . ' 바이트.</p>';
		exit;
	}

	$content = $wpdb->get_var( $wpdb->prepare( "SELECT post_content FROM {$wpdb->posts} WHERE ID = %d", $post_id ) );
	if ( null === $content ) { echo '<p class="no">페이지 137 을 찾지 못했습니다.</p>'; exit; }

	$old_len  = strlen( $content );
	$old_hash = sha1( $content );
	echo '<div class="box">지금 길이 <b>' . $old_len . '</b> 바이트 · sha1 <code>' . substr( $old_hash, 0, 12 ) . '…</code></div>';

	/* ── 진단 : 앰퍼샌드가 브라우저까지 살아서 가는지 ────────
	   the_content 필터를 그대로 태워 보고, script 안에 엔티티가 생기는지 셉니다. */
	$rendered = apply_filters( 'the_content', $content );
	$amp_raw  = substr_count( $content,  '&&' );
	$amp_ent  = substr_count( $rendered, '&#038;&#038;' ) + substr_count( $rendered, '&amp;&amp;' );
	$amp_live = substr_count( $rendered, '&&' );

	echo '<div class="box"><b>진단</b><br>';
	echo '저장된 글 안의 <code>&amp;&amp;</code> : <b>' . $amp_raw . '</b> 개<br>';
	echo '화면에 그려낸 뒤 <code>&amp;&amp;</code> 그대로 : <b>' . $amp_live . '</b> 개<br>';
	echo '화면에 그려낸 뒤 엔티티로 바뀐 것 : <b class="' . ( $amp_ent > 0 ? 'no' : 'ok' ) . '">' . $amp_ent . '</b> 개';
	if ( $amp_ent > 0 ) {
		echo '<br><span class="no">→ 확인되었습니다. 워드프레스가 바꿔 놓고 있습니다. 이것이 버튼이 죽은 까닭입니다.</span>';
	} else {
		echo '<br>→ 이번 확인에서는 안 바뀌었습니다. 그래도 머리말이 금지한 것이니 걷어내는 편이 안전합니다.';
	}
	echo '</div>';

	/* ── 바꿀 두 줄 ─────────────────────────────────────── */
	$fixnl = function ( $t ) { return str_replace( array( "\r\n", "\r" ), "\n", $t ); };

	$edits = array(
		array(
			'name' => '직성의 신 · 주제 문항 고르는 줄',
			'find' => "var CAREER_TOPIC=(ORDER && ORDER.topic) ? ORDER.topic : '';",
			'rep'  => "var CAREER_TOPIC='';\n    if(ORDER){ if(ORDER.topic){ CAREER_TOPIC=ORDER.topic; } }",
		),
		array(
			'name' => '카드 섞는 씨앗에 주제를 더하는 줄',
			'find' => "var TSEED=0, tstr=(ORDER && ORDER.topic) ? String(ORDER.topic) : '';",
			'rep'  => "var TSEED=0, tstr='';\n    if(ORDER){ if(ORDER.topic){ tstr=String(ORDER.topic); } }",
		),
	);

	$updated = $content;
	$fail    = false;

	echo '<h3>자리 찾기</h3><ol>';
	foreach ( $edits as $e ) {
		$find = $fixnl( $e['find'] );
		$rep  = $fixnl( $e['rep'] );
		$n    = substr_count( $updated, $find );
		echo '<li>' . esc_html( $e['name'] ) . ' — 찾은 수 <b class="' . ( 1 === $n ? 'ok' : 'no' ) . '">' . $n . '</b> / 1';
		if ( 1 !== $n ) { $fail = true; echo ' <span class="no">← 어긋납니다</span>'; }
		echo '<br><code>' . esc_html( $find ) . '</code></li>';
		if ( 1 === $n ) { $updated = str_replace( $find, $rep, $updated ); }
	}
	echo '</ol>';

	$left = substr_count( $updated, '&&' );
	echo '<div class="box">고친 뒤 남는 <code>&amp;&amp;</code> : <b class="' . ( 0 === $left ? 'ok' : 'no' ) . '">' . $left . '</b> 개 ';
	echo '(0 이어야 합니다)</div>';
	if ( 0 !== $left ) { $fail = true; }

	$new_len  = strlen( $updated );
	$new_hash = sha1( $updated );
	echo '<div class="box">고친 뒤 길이 <b>' . $new_len . '</b> 바이트 (<b>' . sprintf( '%+d', $new_len - $old_len ) . '</b>) · sha1 <code>' . substr( $new_hash, 0, 12 ) . '…</code></div>';

	if ( $fail ) {
		echo '<p class="no">어긋난 곳이 있어 아무것도 바꾸지 않았습니다. 이 화면을 그대로 보여주세요.</p>';
		exit;
	}

	if ( 'go' !== $mode ) {
		echo '<p class="ok"><b>확인만 했습니다. 아무것도 바꾸지 않았습니다.</b></p>';
		echo '<p>이대로 넣으시려면 <code>?stella_patch=go</code> 로 여세요.</p>';
		exit;
	}

	/* ── 넣기 ───────────────────────────────────────────── */
	update_option( $bak_key, $content, false );
	$done = $wpdb->update( $wpdb->posts, array( 'post_content' => $updated ), array( 'ID' => $post_id ) );
	clean_post_cache( $post_id );

	$check = $wpdb->get_var( $wpdb->prepare( "SELECT post_content FROM {$wpdb->posts} WHERE ID = %d", $post_id ) );
	$ok    = ( sha1( $check ) === $new_hash );

	echo '<h3>' . ( $ok ? '<span class="ok">넣었습니다.</span>' : '<span class="no">확인 실패</span>' ) . '</h3>';
	echo '<p>쓰기 결과 <b>' . var_export( $done, true ) . '</b> · 지금 sha1 <code>' . substr( sha1( $check ), 0, 12 ) . '…</code></p>';
	echo '<p>백업은 <code>' . $bak_key . '</code> 에 두었습니다. 되돌리려면 <code>?stella_patch=undo</code>.</p>';
	echo '<p><a href="https://stellasaju.com/reading-start/">/reading-start/ 열어보기</a> — 「시작할게요」를 눌러보세요.</p>';
	echo '<p><b>이 스니펫은 이제 지우셔도 됩니다.</b></p>';
	exit;
}, 1 );
