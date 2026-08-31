<?php
/**
 * STELLA SAJU — WPCode 가 살아 있는지 보는 아주 작은 스니펫
 *
 *  스니펫을 붙여넣고 돌렸는데 아무 화면도 안 뜰 때, 어디서 막혔는지 찾습니다.
 *  아무것도 고치지 않습니다. 읽기만 합니다.
 *
 *  쓰는 법
 *    1) WPCode 새 스니펫 · PHP · 활성화(Active) 로 저장
 *       ※ 다른 스텔라 스니펫은 잠시 전부 꺼두세요
 *    2) 아래 두 주소를 차례로 열어보세요
 *         https://stellasaju.com/?stella_ping=1        ← 사이트 앞쪽
 *         https://stellasaju.com/wp-admin/?stella_ping=1  ← 관리자 쪽
 *    3) 화면을 그대로 보여주세요
 *
 *  둘 다 아무것도 안 뜨면 → WPCode 가 이 코드를 아예 안 돌리고 있는 겁니다
 *    (스니펫이 비활성 상태이거나, 삽입 위치가 「자동 삽입 안 함」이거나,
 *     WPCode 가 오류를 잡아 스니펫을 꺼버렸거나)
 *  앞쪽만 안 뜨고 관리자 쪽만 뜨면 → 삽입 위치가 「관리자 전용」입니다
 *  뜨긴 뜨는데 「관리자 아님」이라고 나오면 → 그 브라우저에서 로그인이 안 된 겁니다
 */

add_action( 'init', function () {

	if ( ! isset( $_GET['stella_ping'] ) ) { return; }

	/* 일부러 권한 검사를 먼저 하지 않습니다 — 권한 때문에 막힌 것인지도 봐야 하니까요.
	   비밀은 아무것도 내보내지 않습니다. */
	header( 'Content-Type: text/html; charset=utf-8' );
	header( 'Cache-Control: no-store, no-cache, must-revalidate, max-age=0' );
	header( 'X-Robots-Tag: noindex' );

	$admin = current_user_can( 'manage_options' );
	$uid   = get_current_user_id();

	echo '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">';
	echo '<style>body{font:16px/1.8 -apple-system,"Apple SD Gothic Neo",sans-serif;max-width:640px;margin:40px auto;padding:0 20px}';
	echo 'h1{font-size:1.5rem} .ok{color:#0a7a2f;font-weight:700} .no{color:#c0392b;font-weight:700}';
	echo 'table{border-collapse:collapse;width:100%;margin:18px 0} td{border-bottom:1px solid #eee;padding:9px 4px}';
	echo 'td:first-child{color:#666;width:46%} code{background:#f4f4f4;padding:1px 5px;border-radius:3px}</style>';

	echo '<h1 class="ok">WPCode 는 살아 있습니다.</h1>';
	echo '<p>이 화면이 보인다는 것은 스니펫의 PHP 가 실제로 돌고 있다는 뜻입니다.</p>';

	echo '<table>';
	echo '<tr><td>지금 보고 계신 쪽</td><td>' . ( is_admin() ? '관리자(wp-admin)' : '사이트 앞쪽' ) . '</td></tr>';
	echo '<tr><td>로그인한 사용자 번호</td><td>' . ( $uid ? $uid : '<span class="no">로그인 안 됨 (0)</span>' ) . '</td></tr>';
	echo '<tr><td>관리자 권한(manage_options)</td><td>' . ( $admin ? '<span class="ok">있음</span>' : '<span class="no">없음</span>' ) . '</td></tr>';
	echo '<tr><td>PHP</td><td>' . PHP_VERSION . '</td></tr>';
	echo '<tr><td>워드프레스</td><td>' . get_bloginfo( 'version' ) . '</td></tr>';
	echo '<tr><td>메모리 한도</td><td>' . ini_get( 'memory_limit' ) . '</td></tr>';
	echo '<tr><td>보낼 수 있는 글 크기</td><td>' . ini_get( 'post_max_size' ) . '</td></tr>';
	echo '<tr><td>페이지 62 (홈)</td><td>' . strlen( (string) get_post_field( 'post_content', 62 ) ) . ' 바이트</td></tr>';
	$today = get_page_by_path( 'today', OBJECT, 'page' );
	echo '<tr><td>/today/ 페이지</td><td>' . ( $today ? ( '있음 · 번호 ' . $today->ID ) : '<span class="no">아직 없음</span>' ) . '</td></tr>';
	echo '</table>';

	if ( ! $admin ) {
		echo '<p class="no">관리자 권한이 없습니다. 다른 스텔라 스니펫들은 이 검사에서 조용히 멈춥니다 — ';
		echo '그래서 아무 화면도 안 떴던 것입니다. 이 브라우저에서 워드프레스에 로그인하신 뒤 다시 열어보세요.</p>';
	} else {
		echo '<p class="ok">권한도 정상입니다. 그러면 다른 스니펫이 안 돌았던 까닭은 ';
		echo '그 스니펫이 꺼져 있었거나, 붙여넣다 잘렸거나, WPCode 가 오류를 잡아 꺼버린 것입니다. ';
		echo 'WPCode 목록에서 그 스니펫이 <b>활성(Active)</b> 인지 확인해 주세요.</p>';
	}

	echo '<p style="margin-top:26px;color:#888;font-size:.9rem">확인이 끝나면 이 스니펫도 지워주세요.</p>';
	exit;
}, 1 );
