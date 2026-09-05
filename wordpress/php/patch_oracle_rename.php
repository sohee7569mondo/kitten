<?php
/**
 * STELLA SAJU — 「운명의 책」을 「나에게 필요한 한마디」로
 *
 *  이름이 너무 거창하다 하셔서 가벼운 말로 바꿉니다.
 *  주소(/oracle/)는 그대로 두므로 걸어둔 링크는 하나도 안 끊깁니다.
 *
 *  손대는 곳
 *    페이지 85 (/oracle/)  제목 · 설명 · 단추 · 한마디 목록(10개 → 30개)
 *                          그리고 워드프레스 페이지 제목까지
 *    페이지 186 (/stars/)  허브 목록의 그 칸
 *
 *  홈(페이지 62)에서는 아예 빼기로 하셔서, 홈 스니펫 쪽에서 처리됩니다.
 *
 *  쓰는 법 (WPCode Lite) — PHP · 자동 실행 안 함
 *    확인 : https://stellasaju.com/?stella_patch=dry
 *    적용 : https://stellasaju.com/?stella_patch=go
 *    되돌리기 : https://stellasaju.com/?stella_patch=undo
 *    다 되면 스니펫을 지우세요.
 */

add_action( 'init', function () {

	if ( ! isset( $_GET['stella_patch'] ) ) { return; }
	if ( ! current_user_can( 'manage_options' ) ) { return; }
	$mode = sanitize_text_field( wp_unslash( $_GET['stella_patch'] ) );

	global $wpdb;
	$bak_key = 'stella_bak_oracle_rename';
	$new_title = '나에게 필요한 한마디';
	$old_title = '운명의 책';

	$jobs = array(
		array(
			'id' => 85,
			'name' => '/oracle/ · 한마디 페이지',
			'edits' => array(
				array( 'n' => '머리말 이름', 'a' => '  STELLA SAJU — 운명의 책 (페이지 ID 85)   BUILD: O2', 'b' => '  STELLA SAJU — 나에게 필요한 한마디 (페이지 ID 85 · /oracle/)   BUILD: O3

  2026-08-31 · 예전 이름이 너무 거창하다 하셔서
  「나에게 필요한 한마디」로 바꿨습니다. 주소(/oracle/)는 그대로라
  걸어둔 링크는 하나도 안 끊깁니다.' ),
				array( 'n' => '큰 제목', 'a' => '    <h1>운명의 책</h1>', 'b' => '    <h1>나에게 필요한 한마디</h1>' ),
				array( 'n' => '제목 아래 설명', 'a' => '    <p class="ssp-lead">질문 하나를 떠올리고 책장을 넘기면, 명성의 신이 짧은 한 줄을 전해드려요.<br>몇 번이든 열어보세요.</p>', 'b' => '    <p class="ssp-lead">지금 마음에 걸리는 것 하나만 떠올리고 넘겨보세요.<br>명성의 신이 짧은 한마디를 건네드립니다. 몇 번이든 괜찮아요.</p>' ),
				array( 'n' => '단추', 'a' => '      <button type="button" class="btn" id="oracleBtn">책장 넘기기 &rarr;</button>', 'b' => '      <button type="button" class="btn" id="oracleBtn">한마디 받기 &rarr;</button>' ),
				array( 'n' => '다시 누를 때', 'a' => '      btn.textContent = \'다시 넘기기 →\';', 'b' => '      btn.textContent = \'다시 받기 →\';' ),
				array( 'n' => '아래 안내', 'a' => '      <p>한 줄 말고, 제대로 된 풀이가 궁금하다면?</p>', 'b' => '      <p>한마디 말고, 제대로 된 풀이가 궁금하다면?</p>' ),
				array( 'n' => '한마디 서른 개', 'a' => '  var LINES = [
    \'오늘은 무리한 지출을 삼가세요.\',
    \'지금은 기다림이 답일 수 있어요.\',
    \'작은 결정이 큰 흐름을 바꿉니다.\',
    \'가까운 사람의 말에 귀 기울여보세요.\',
    \'서두르지 않아도 늦지 않아요.\',
    \'오늘 하루는 스스로를 먼저 돌보세요.\',
    \'지금의 선택, 나쁘지 않은 방향이에요.\',
    \'잠시 멈추는 것도 나아가는 방법이에요.\',
    \'마음이 가는 쪽이 답일 때가 많아요.\',
    \'오늘은 평소보다 조금 더 신중하게.\'
  ];', 'b' => '  /* 【문구】 한마디 — 여기에 한 줄씩 넣고 빼시면 그대로 나옵니다.
     열 개뿐이라 두세 번만 눌러도 같은 말이 돌아 나왔습니다. 서른 개로 늘렸습니다. */
  var LINES = [
    \'오늘은 큰돈 쓰는 결정을 하루만 미뤄보세요.\',
    \'지금은 기다리는 것이 게으른 게 아니에요.\',
    \'작게 정한 것 하나가 이번 달을 바꿉니다.\',
    \'가까운 사람이 지나가듯 한 말을 다시 떠올려 보세요.\',
    \'서두르지 않아도 늦지 않았습니다.\',
    \'오늘은 남보다 나를 먼저 챙기셔도 됩니다.\',
    \'지금 가고 계신 쪽, 나쁘지 않아요.\',
    \'잠깐 멈추는 것도 앞으로 가는 방법입니다.\',
    \'재보다가 안 되면, 마음이 가는 쪽이 답일 때가 많아요.\',
    \'오늘은 평소보다 한 번만 더 확인하세요.\',
    \'연락할까 말까 망설이셨다면, 오늘은 해보셔도 좋아요.\',
    \'하기 싫은 일 하나만 먼저 끝내면 오늘이 편해집니다.\',
    \'설명하지 않아도 되는 일까지 설명하고 계실 수 있어요.\',
    \'지금 붙잡고 있는 것, 정말 내 것이 맞는지 한 번만 보세요.\',
    \'오늘은 잘하려 하지 마시고 그냥 끝내세요.\',
    \'이미 지나간 일을 오늘 밤에는 꺼내지 마세요.\',
    \'누가 안 알아줘도 오늘 하신 건 남습니다.\',
    \'거절해도 괜찮습니다. 생각보다 아무 일도 안 일어나요.\',
    \'오늘 안 되는 건 방법이 아니라 때일 수 있어요.\',
    \'한 사람에게만 물어보세요. 여럿에게 물으면 더 흐려집니다.\',
    \'몸이 보내는 신호를 오늘은 무시하지 마세요.\',
    \'완벽하지 않아도 내놓는 편이 낫습니다.\',
    \'오늘 화가 났다면 그건 상대가 아니라 지친 탓일 수 있어요.\',
    \'이번 주에 한 번은 아무것도 안 하는 시간을 두세요.\',
    \'먼저 손을 내미셔도 지는 것이 아닙니다.\',
    \'지금 아까운 마음이 드는 건, 그만큼 애쓰셨다는 뜻이에요.\',
    \'오늘은 새로 벌이기보다 하나를 닫는 날입니다.\',
    \'고민이 길어졌다면 답은 이미 정하셨을 거예요.\',
    \'작은 약속 하나를 오늘 지키면 다음이 쉬워집니다.\',
    \'괜찮지 않아도 됩니다. 오늘 하루 지나온 것으로 충분해요.\'
  ];' ),
			),
		),
		array(
			'id' => 186,
			'name' => '/stars/ · 이번주 허브',
			'edits' => array(
				array( 'n' => '머리말 이름', 'a' => '    /oracle/        운명의 책', 'b' => '    /oracle/        나에게 필요한 한마디' ),
				array( 'n' => '허브 카드', 'a' => '          <div class="no">WEEKLY IV</div>
          <div class="tt">운명의 책</div>
          <div class="ds">묻고 싶은 것이 하나 있을 때. 책을 펼치듯 한 문장을 뽑습니다.</div>
          <span class="go">펼쳐 보기 →</span>', 'b' => '          <div class="no">ANYTIME</div>
          <div class="tt">나에게 필요한 한마디</div>
          <div class="ds">묻고 싶은 것이 하나 있을 때. 짧은 한마디를 건네드립니다. 매주가 아니라 아무 때나 몇 번이든요.</div>
          <span class="go">한마디 받기 →</span>' ),
			),
		),
	);

	header( 'Content-Type: text/html; charset=utf-8' );
	echo '<meta charset="utf-8"><style>body{font:15px/1.7 -apple-system,"Apple SD Gothic Neo",sans-serif;max-width:940px;margin:40px auto;padding:0 20px}';
	echo 'code{background:#f4f4f4;padding:1px 5px;border-radius:3px}';
	echo '.ok{color:#0a7a2f}.no{color:#c0392b;font-weight:700}.box{border:1px solid #ddd;border-radius:8px;padding:14px 18px;margin:14px 0}</style>';
	echo '<h2>「운명의 책」 &rarr; 「나에게 필요한 한마디」</h2>';

	if ( 'undo' === $mode ) {
		$bak = get_option( $bak_key );
		if ( ! $bak ) { echo '<p class="no">되돌릴 백업이 없습니다.</p>'; exit; }
		foreach ( $bak as $id => $row ) {
			$wpdb->update( $wpdb->posts,
				array( 'post_content' => $row['c'], 'post_title' => $row['t'] ),
				array( 'ID' => (int) $id ) );
			clean_post_cache( (int) $id );
		}
		echo '<p class="ok">되돌렸습니다.</p>'; exit;
	}

	$fixnl = function ( $t ) { return str_replace( array( "\r\n", "\r" ), "\n", $t ); };
	$mkre  = function ( $find ) use ( $fixnl ) {
		$lines = explode( "\n", $fixnl( $find ) );
		foreach ( $lines as $i => $l ) { $lines[ $i ] = preg_quote( $l, '/' ); }
		return '/' . implode( '\r?\n', $lines ) . '/u';
	};

	$fail = false; $plan = array(); $backup = array();

	foreach ( $jobs as $job ) {
		$id  = $job['id'];
		$row = $wpdb->get_row( $wpdb->prepare( "SELECT post_content, post_title FROM {$wpdb->posts} WHERE ID = %d", $id ), ARRAY_A );
		if ( ! $row ) { echo '<p class="no">페이지 ' . $id . ' 을 찾지 못했습니다.</p>'; $fail = true; continue; }

		$c = $row['post_content'];
		$backup[ $id ] = array( 'c' => $c, 't' => $row['post_title'] );

		echo '<h3>페이지 ' . $id . ' &middot; ' . esc_html( $job['name'] ) . '</h3>';
		echo '<div class="box">지금 ' . strlen( $c ) . ' 바이트 · sha1 <code>' . substr( sha1( $c ), 0, 12 ) . '…</code></div><ol>';

		foreach ( $job['edits'] as $e ) {
			$re = $mkre( $e['a'] );
			$n  = preg_match_all( $re, $c );
			echo '<li>' . esc_html( $e['n'] ) . ' — 찾은 수 <b class="' . ( 1 === $n ? 'ok' : 'no' ) . '">' . $n . '</b> / 1';
			if ( 1 !== $n ) { $fail = true; echo ' <span class="no">← 어긋납니다</span>'; }
			echo '</li>';
			if ( 1 === $n ) {
				$rp = $fixnl( $e['b'] );
				$c  = preg_replace_callback( $re, function ( $m ) use ( $rp ) { return $rp; }, $c, 1 );
			}
		}
		echo '</ol>';

		$left = substr_count( $c, $old_title );
		echo '<div class="box">고친 뒤 ' . strlen( $c ) . ' 바이트 · sha1 <code>' . substr( sha1( $c ), 0, 12 ) . '…</code><br>';
		echo '「' . esc_html( $old_title ) . '」 라는 말이 아직 남았나 : <b class="' . ( 0 === $left ? 'ok' : 'no' ) . '">' . $left . '</b> 곳 (0 이어야 합니다)<br>';
		echo '「' . esc_html( $new_title ) . '」 가 들어간 곳 : <b>' . substr_count( $c, $new_title ) . '</b><br>';
		echo '앰퍼샌드 두 개 (0이어야) : <b>' . substr_count( $c, '&&' ) . '</b></div>';
		if ( 0 !== $left ) { $fail = true; }

		$plan[ $id ] = $c;
	}

	if ( $fail ) { echo '<p class="no">어긋난 곳이 있어 아무것도 바꾸지 않았습니다. 이 화면을 그대로 보여주세요.</p>'; exit; }

	if ( 'go' !== $mode ) {
		echo '<p class="ok"><b>확인만 했습니다. 아무것도 바꾸지 않았습니다.</b></p>';
		echo '<p>이대로 넣으시려면 <code>?stella_patch=go</code> 로 여세요.</p>'; exit;
	}

	/* 2026-08-31 · 백업은 처음 한 번만 남깁니다.
	   이 스니펫을 두 번 돌리시면 두 번째에는 「이미 고친 것」이 백업으로 덮여서
	   되돌리기가 원래 자리까지 못 갑니다. 그래서 백업이 이미 있으면 손대지 않습니다. */
	if ( false === get_option( $bak_key ) ) { update_option( $bak_key, $backup, false ); }
	foreach ( $plan as $id => $c ) {
		$data = array( 'post_content' => $c );
		if ( 85 === (int) $id ) { $data['post_title'] = $new_title; }
		$wpdb->update( $wpdb->posts, $data, array( 'ID' => (int) $id ) );
		clean_post_cache( (int) $id );
		$chk = $wpdb->get_var( $wpdb->prepare( "SELECT post_content FROM {$wpdb->posts} WHERE ID = %d", (int) $id ) );
		echo '<p>페이지 <b>' . $id . '</b> — ' . ( sha1( $chk ) === sha1( $c ) ? '<span class="ok">넣었습니다.</span>' : '<span class="no">확인 실패</span>' ) . '</p>';
	}
	echo '<p><a href="https://stellasaju.com/oracle/">/oracle/ 열어보기 &rarr;</a> &middot; <a href="https://stellasaju.com/stars/">/stars/ 열어보기 &rarr;</a></p>';
	echo '<p>되돌리려면 <code>?stella_patch=undo</code>. <b>이 스니펫은 이제 지우셔도 됩니다.</b></p>';
	exit;
}, 1 );
