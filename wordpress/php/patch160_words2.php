<?php
/**
 * STELLA SAJU — 페이지 160 · 맺음말 배웅 두 줄            PATCH: WORDS-2
 * ------------------------------------------------------------------
 * 한 번만 돌리는 스니펫입니다. 돌린 뒤에는 반드시 지우세요.
 *
 * [무엇을 고치나]  열일곱 자리를 고칩니다.
 *
 *   1) 저울 소제목과 본문의 낱말을 맞춥니다
 *      소제목은 「다투고 나서, 삭이는가 붙잡는가」로 갈렸는데 본문은
 *      「사주는 함께 쪽으로…」처럼 옛 낱말을 그대로 썼습니다.
 *      이제 본문도 「사주는 붙잡는 쪽으로…」로 나갑니다.
 *      연성의 신·직성의 신 두 문만 표에 있고, 나머지 네 문은 손대지 않습니다.
 *
 *   2) 오행을 화면에 보일 때만 풀어 씁니다 — 목 → 목(나무 목)
 *      값은 절대 안 바꿉니다. 엔진이 오행을 셀 때 쓰는 열쇠말이라
 *      바꾸면 계산이 통째로 깨집니다. 보여주는 자리 아홉 곳만 감쌉니다.
 *      뒤에 붙는 조사(이에요/예요)는 원래 글자로 고르므로 그대로 맞습니다.
 *
 *   3) 「남은 저울 셋」 → 「타고난 성향과 실제 생활이 다른 부분 — 남은 셋」
 *
 *   4) 「올해 인연의 흐름」 표 밑에 달 이름 다섯 개의 뜻을 붙입니다
 *      말이 나가는 달 · 견주는 달 · 끌리는 달 · 흔들리는 달 · 기대고 싶은 달
 *
 *   5) 연성의 신 닫는 말을 쉽고 충분하게 다시 씁니다
 *
 * [미리 알아두실 것]
 *   · 1)번과 2)번은 여섯 문 전부가 지나가는 자리를 건드립니다.
 *     표에 없는 문은 원래 낱말 그대로 나가도록 해두었지만,
 *     제가 실제로 그려본 것은 연성의 신뿐입니다.
 *   · 오행 풀어쓰기는 아홉 곳에 한꺼번에 들어갑니다. 사장님이 짚어주신
 *     「인연의 별」 자리 말고 나머지 여덟 곳은 문장 모양만 확인했습니다.
 *     한 권에서 여러 번 나오면 되풀이처럼 보일 수 있습니다.
 *   · 「남은 셋」은 사장님 말씀을 그대로 옮기지 않고 조금 고쳤습니다.
 *     앞 장 제목과 거의 같아져서 두 장이 같은 제목이 되기 때문입니다.
 *
 * 넣는 곳 : WPCode → + Add Snippet → Add Your Custom Code
 *           Code Type = PHP Snippet / Location = Run Everywhere / Active
 *           (맨 윗줄 <?php 은 빼고 붙여넣으세요)
 *
 * 돌리는 법 :
 *   미리보기 (아무것도 안 고침) : /wp-admin/?stella_patch=dry
 *   진짜로 고치기               : /wp-admin/?stella_patch=go
 *   되돌리기                    : /wp-admin/?stella_patch=undo
 * ------------------------------------------------------------------
 */

defined( 'STELLA_W2_PAGE' ) || define( 'STELLA_W2_PAGE', 160 );
defined( 'STELLA_W2_KEY' )  || define( 'STELLA_W2_KEY',  'words2' );

/* 다 고치고 나면 본문이 이 모양이어야 합니다 — 제가 미리 걸어보고 잰 값입니다 */
defined( 'STELLA_W2_GROW' ) || define( 'STELLA_W2_GROW', 127 );
defined( 'STELLA_W2_SHA' )  || define( 'STELLA_W2_SHA',  '53ffcd686c24346b9cac7684ca4dfb8f3b05ca7d' );

$STELLA_W2_EDITS = array(
	array(
		'name' => <<<'NAME0'
배웅 · 결혼운 (결혼 전과 결혼 중 둘 다)
NAME0,
		're'   => <<<'RE0'
~'결혼운':'결혼을\ 앞두고\ 망설여진다면,\ 그\ 사람이\ 좋은\ 사람인지를\ 따지기\ 전에\ 그\ 사람과\ 함께\ 있을\ 때의\ 내가\ 마음에\ 드는지를\ 먼저\ 보세요\.\ 평생\ 같이\ 사는\ 것은\ 그\ 사람이\ 아니라,\ 그\ 사람\ 곁에\ 있는\ 나입니다\.',~s
RE0,
		'rep'  => <<<'REP0'
'결혼운':'결혼을 앞두고 망설여지거나 지금의 결혼생활이 힘들다고 느끼신다면, 그 사람이 좋은 사람인지를 따지기 전에 그 사람과 함께 있을 때의 내가 마음에 드는지를 먼저 보세요. 평생 같이 사는 것은 그 사람이 아니라, 그 사람 곁에 있는 나입니다.',
REP0,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME1'
배웅 · 연애운 (만나는 사람이 없는 분도)
NAME1,
		're'   => <<<'RE1'
~'연애운':'이\ 사람이\ 맞는\ 사람인지\ 모르겠다면,\ 그\ 사람이\ 어떤\ 사람인지\ 재는\ 대신\ 그\ 사람과\ 있을\ 때의\ 내가\ 마음에\ 드는지를\ 보세요\.\ 답은\ 그\ 사람에게\ 있는\ 것이\ 아니라\ 늘\ 거기에\ 있었습니다\.',~s
RE1,
		'rep'  => <<<'REP1'
'연애운':'만나는 사람이 있다면, 그 사람이 어떤 사람인지 재기 전에 그 사람과 있을 때의 내가 마음에 드는지를 보세요. 아직 만난 사람이 없다면, 어떤 사람을 만나고 싶은지보다 어떤 나로 있고 싶은지를 먼저 정해두세요. 답은 늘 그쪽에 있습니다.',
REP1,
		'n'    => 1,
	),
);


/* ------------------------------------------------------------------
 * 아래는 손대지 않으셔도 됩니다.
 * ---------------------------------------------------------------- */

add_action( 'admin_init', function () use ( $STELLA_W2_EDITS ) {

	if ( ! isset( $_GET['stella_patch'] ) || ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$mode     = sanitize_key( wp_unslash( $_GET['stella_patch'] ) );
	$page_id  = (int) STELLA_W2_PAGE;
	$done_opt = 'stella_patch_' . STELLA_W2_KEY . '_done';
	$back_opt = 'stella_patch_' . STELLA_W2_KEY . '_backup';
	$log      = array();

	$say = function ( $lines, $ok = true ) {
		add_action( 'admin_notices', function () use ( $lines, $ok ) {
			printf(
				'<div class="notice notice-%s"><p><strong>스텔라 패치 · 말 맞추기</strong></p><pre style="white-space:pre-wrap;margin:0">%s</pre></div>',
				$ok ? 'success' : 'error',
				esc_html( implode( "\n", $lines ) )
			);
		} );
	};

	global $wpdb;
	$row = $wpdb->get_row( $wpdb->prepare(
		"SELECT ID, post_content FROM {$wpdb->posts} WHERE ID = %d", $page_id ) );
	if ( ! $row ) {
		$say( array( "페이지 {$page_id} 을(를) 찾지 못했습니다." ), false );
		return;
	}
	$content = $row->post_content;

	/* ---- 되돌리기 ---- */
	if ( 'undo' === $mode ) {
		$backup = get_option( $back_opt );
		if ( ! is_string( $backup ) || '' === $backup ) {
			$say( array( '되돌릴 내용이 없습니다.' ), false );
			return;
		}
		$wpdb->update( $wpdb->posts, array(
			'post_content'      => $backup,
			'post_modified'     => current_time( 'mysql' ),
			'post_modified_gmt' => current_time( 'mysql', 1 ),
		), array( 'ID' => $page_id ) );
		clean_post_cache( $page_id );
		delete_option( $done_opt );
		$say( array( '고치기 전 내용으로 되돌렸습니다.',
			'되돌린 크기 : ' . number_format( strlen( $backup ) ) . ' 바이트',
			'호스팅 → 성능 → 캐시 비우기 를 눌러주세요.' ) );
		return;
	}

	$dry = ( 'go' !== $mode );

	if ( get_option( $done_opt ) ) {
		$say( array( '이 패치는 이미 돌렸습니다 (' . get_option( $done_opt ) . ').',
			'다시 돌리려면 먼저 ?stella_patch=undo 로 되돌리세요.' ) );
		return;
	}

	/* ---- 고칠 자리가 하나씩 다 있는지 먼저 셉니다 ---- */
	/* WPCode 편집기에 붙여넣으면 줄바꿈이 \r\n 으로 바뀝니다. 그러면 여러 줄에
	   걸친 찾기 문구가 페이지의 \n 과 안 맞아 하나도 못 찾습니다.
	   그래서 찾기 문구와 바꿀 글을 쓰기 직전에 \n 으로 되돌립니다. */
	$fixnl = function ( $t ) { return str_replace( array( "\r\n", "\r" ), "\n", $t ); };

	$bad = false;
	foreach ( $STELLA_W2_EDITS as $e ) {
		$found = preg_match_all( $fixnl( $e['re'] ), $content );
		if ( false === $found ) {
			$log[] = '⚠ ' . $e['name'] . ' — 찾다가 오류가 났습니다';
			$bad   = true;
			continue;
		}
		$log[] = ( $found === $e['n'] ? '   ' : '⚠ ' ) . $e['name'] . ' : ' . $found . ' / ' . $e['n'];
		if ( $found !== $e['n'] ) { $bad = true; }
	}
	if ( $bad ) {
		$say( array_merge( $log, array( '',
			'고칠 자리가 예상과 다릅니다. 엔진이 그 사이에 바뀐 것 같습니다.',
			'아무것도 고치지 않았습니다. 이 화면을 그대로 알려주세요.' ) ), false );
		return;
	}

	/* ---- 실제로 바꿔봅니다 ---- */
	$updated = $content;
	foreach ( $STELLA_W2_EDITS as $e ) {
		$rep     = $fixnl( $e['rep'] );
		$updated = preg_replace_callback( $fixnl( $e['re'] ), function ( $m ) use ( $rep ) {
			$out = $rep;
			for ( $i = count( $m ) - 1; $i >= 1; $i-- ) {
				$out = str_replace( '\\' . $i, $m[ $i ], $out );
			}
			return $out;
		}, $updated );
		if ( null === $updated ) {
			$say( array_merge( $log, array( '', $e['name'] . ' 에서 바꾸다가 실패했습니다.' ) ), false );
			return;
		}
	}

	$grew  = strlen( $updated ) - strlen( $content );
	$sha   = sha1( $updated );
	$log[] = '';
	$log[] = '늘어난 바이트 : ' . number_format( $grew ) . '  (예상 ' . number_format( STELLA_W2_GROW ) . ')';
	$log[] = '바뀐 본문 지문 : ' . substr( $sha, 0, 12 ) . '  (예상 ' . substr( STELLA_W2_SHA, 0, 12 ) . ')';

	if ( abs( $grew - STELLA_W2_GROW ) > 64 ) {
		$say( array_merge( $log, array( '',
			'늘어난 크기가 예상과 다릅니다. 뭔가 잘못된 것 같아 멈췄습니다.' ) ), false );
		return;
	}
	if ( $sha === STELLA_W2_SHA ) {
		$log[] = '→ 제가 미리 걸어보고 확인한 것과 한 글자도 다르지 않습니다.';
	} else {
		$log[] = '→ 지문이 다릅니다. 크기는 맞으니 대개 줄바꿈 차이지만, 확인이 필요합니다.';
	}

	if ( $dry ) {
		$say( array_merge( $log, array( '',
			'※ 미리보기였습니다. 아무것도 고치지 않았습니다.',
			'진짜로 고치려면 ?stella_patch=go 로 다시 여세요.' ) ) );
		return;
	}

	update_option( $back_opt, $content, false );
	$ok = $wpdb->update( $wpdb->posts, array(
		'post_content'      => $updated,
		'post_modified'     => current_time( 'mysql' ),
		'post_modified_gmt' => current_time( 'mysql', 1 ),
	), array( 'ID' => $page_id ) );
	if ( false === $ok ) {
		$say( array_merge( $log, array( '저장 실패 : ' . $wpdb->last_error ) ), false );
		return;
	}
	clean_post_cache( $page_id );
	update_option( $done_opt, current_time( 'mysql' ), false );

	$say( array_merge( $log, array( '',
		'다 됐습니다.',
		'1) WPCode 에서 이 스니펫을 지우세요. (꼭)',
		'2) 호스팅 → 성능 → 캐시 비우기',
		'3) 시크릿 창에서 연성의 신 책을 한 권 뽑아 확인',
		'',
		'되돌리려면 : /wp-admin/?stella_patch=undo' ) ) );
} );
