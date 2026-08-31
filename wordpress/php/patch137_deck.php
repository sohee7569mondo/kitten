<?php
/**
 * STELLA SAJU — 페이지 137 · 주제마다 다른 카드가 나오게      PATCH: DECK-1
 * ------------------------------------------------------------------
 * 한 번만 돌리는 스니펫입니다. 돌린 뒤에는 반드시 지우세요.
 *
 * [무엇을 고치나]  한 자리만 고칩니다.
 *   카드를 섞는 씨앗이 생년월일시와 오늘 날짜만 봤습니다. 주제는 안 봤어요.
 *   그래서 같은 분이 같은 날 결혼운으로 한 번, 연애운으로 한 번 뽑으면
 *   — 같은 자리를 누르는 한 — 똑같은 카드 세 장이 나왔습니다.
 *   전자책의 타로 장이 두 주제에서 같아 보이던 가장 큰 이유입니다.
 *
 *   씨앗에 주제를 더해서, 주제가 다르면 패가 달라지게 합니다.
 *
 * [바뀌지 않는 것]
 *   · 주제가 비어 있으면 예전과 한 치도 다르지 않습니다 (더하는 값이 0).
 *   · 날이 바뀌면 카드가 달라지는 것도 그대로입니다.
 *   · 가디언마다 스무 장씩 나눠둔 패(POOL)도 그대로입니다.
 *   · 이미 카드를 뽑아두신 손님은 저장된 카드를 그대로 씁니다.
 *     새로 뽑는 분부터 적용됩니다.
 *
 * 넣는 곳 : WPCode → + Add Snippet → Add Your Custom Code
 *           Code Type = PHP Snippet / Location = Run Everywhere / Active
 *           (맨 윗줄 <?php 은 빼고 붙여넣으세요)
 *
 * 돌리는 법 :
 *   미리보기 (아무것도 안 고침) : /wp-admin/?stella_deck=dry
 *   진짜로 고치기               : /wp-admin/?stella_deck=go
 *   되돌리기                    : /wp-admin/?stella_deck=undo
 * ------------------------------------------------------------------
 */

defined( 'STELLA_D_PAGE' ) || define( 'STELLA_D_PAGE', 137 );
defined( 'STELLA_D_KEY' )  || define( 'STELLA_D_KEY',  'deck1' );

$STELLA_D_RE  = <<<'RE'
~\ \ \ \ var\ seed\ =\ \(P\.year\|\|0\)\*10007\ \+\ \(P\.month\|\|0\)\*331\ \+\ \(P\.day\|\|0\)\*97\
\ \ \ \ \ \ \ \ \ \ \ \ \ \+\ \(P\.hour\|\|0\)\*13\ \+\ \(P\.minute\|\|0\)\*7\
\ \ \ \ \ \ \ \ \ \ \ \ \ \+\ now\.getFullYear\(\)\*1103\ \+\ \(now\.getMonth\(\)\+1\)\*37\ \+\ now\.getDate\(\)\*3\ \+\ 11;~s
RE;
$STELLA_D_NEW = <<<'NEWJS'
    /* 2026-08-31 · 주제를 섞는 씨앗에 더합니다.
       지금까지는 생년월일시와 오늘 날짜만 봐서, 같은 분이 같은 날
       결혼운으로 한 번 연애운으로 한 번 뽑으면 — 같은 자리를 누르는 한 —
       똑같은 카드 세 장이 나왔습니다. 주제가 다르면 다른 패가 되도록 합니다.
       주제가 비어 있으면 TSEED 가 0 이라 예전과 한 치도 다르지 않습니다. */
    var TSEED=0, tstr=(ORDER && ORDER.topic) ? String(ORDER.topic) : '';
    for(var ti=0; ti < tstr.length; ti++){ TSEED=(TSEED*31 + tstr.charCodeAt(ti)) % 99991; }
    var seed = (P.year||0)*10007 + (P.month||0)*331 + (P.day||0)*97
             + (P.hour||0)*13 + (P.minute||0)*7
             + now.getFullYear()*1103 + (now.getMonth()+1)*37 + now.getDate()*3 + 11
             + TSEED*7919;
NEWJS;

/* ------------------------------------------------------------------ */

add_action( 'admin_init', function () use ( $STELLA_D_RE, $STELLA_D_NEW ) {

	if ( ! isset( $_GET['stella_deck'] ) || ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$mode     = sanitize_key( wp_unslash( $_GET['stella_deck'] ) );
	$page_id  = (int) STELLA_D_PAGE;
	$done_opt = 'stella_patch_' . STELLA_D_KEY . '_done';
	$back_opt = 'stella_patch_' . STELLA_D_KEY . '_backup';

	$say = function ( $lines, $ok = true ) {
		add_action( 'admin_notices', function () use ( $lines, $ok ) {
			printf(
				'<div class="notice notice-%s"><p><strong>스텔라 패치 · 주제마다 다른 카드</strong></p><pre style="white-space:pre-wrap;margin:0">%s</pre></div>',
				$ok ? 'success' : 'error',
				esc_html( implode( "\n", $lines ) )
			);
		} );
	};

	/* WPCode 편집기가 붙여넣은 코드의 줄바꿈을 \r\n 으로 바꿉니다.
	   여러 줄짜리 찾기 문구가 페이지의 \n 과 안 맞게 되므로 되돌립니다. */
	$fixnl = function ( $t ) { return str_replace( array( "\r\n", "\r" ), "\n", $t ); };
	$re    = $fixnl( $STELLA_D_RE );
	$new   = $fixnl( $STELLA_D_NEW );

	global $wpdb;
	$row = $wpdb->get_row( $wpdb->prepare(
		"SELECT ID, post_content FROM {$wpdb->posts} WHERE ID = %d", $page_id ) );
	if ( ! $row ) {
		$say( array( "페이지 {$page_id} 을(를) 찾지 못했습니다." ), false );
		return;
	}
	$content = $row->post_content;

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
			'호스팅 → 성능 → 캐시 비우기 를 눌러주세요.' ) );
		return;
	}

	$dry = ( 'go' !== $mode );
	$log = array();

	if ( false !== strpos( $content, 'TSEED' ) ) {
		$say( array( '이미 들어가 있습니다 (TSEED 를 찾았습니다). 아무것도 하지 않았습니다.',
			'WPCode 에서 이 스니펫을 지우셔도 됩니다.' ) );
		return;
	}

	$found = preg_match_all( $re, $content );
	$log[] = '카드 섞는 씨앗을 찾은 횟수 : ' . (int) $found . ' (1 이어야 함)';
	if ( 1 !== $found ) {
		$say( array_merge( $log, array( '',
			'찾는 자리가 하나가 아닙니다. 페이지가 그 사이에 바뀐 것 같습니다.',
			'아무것도 고치지 않았습니다. 이 화면을 그대로 알려주세요.' ) ), false );
		return;
	}

	$old_len = 0;
	$updated = preg_replace_callback( $re, function ( $m ) use ( $new, &$old_len ) {
		$old_len = strlen( $m[0] );
		return $new;
	}, $content, 1 );
	if ( null === $updated ) {
		$say( array_merge( $log, array( '바꾸다가 실패했습니다.' ) ), false );
		return;
	}

	$grew   = strlen( $updated ) - strlen( $content );
	$expect = strlen( $new ) - $old_len;
	$log[]  = '늘어난 바이트 : ' . number_format( $grew ) . '  (예상 ' . number_format( $expect ) . ')';

	if ( $grew !== $expect ) {
		$say( array_merge( $log, array( '', '늘어난 크기가 예상과 다릅니다. 멈췄습니다.' ) ), false );
		return;
	}
	if ( false === strpos( $updated, 'TSEED*7919' ) ) {
		$say( array_merge( $log, array( '', '바뀐 내용에 새 씨앗이 없습니다. 멈췄습니다.' ) ), false );
		return;
	}

	if ( $dry ) {
		$say( array_merge( $log, array( '',
			'※ 미리보기였습니다. 아무것도 고치지 않았습니다.',
			'진짜로 고치려면 ?stella_deck=go 로 다시 여세요.' ) ) );
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
		'3) 시크릿 창에서 연성의 신 → 결혼운으로 한 번, 연애운으로 한 번',
		'   같은 자리의 카드를 눌러 서로 다른 카드가 나오는지 확인',
		'',
		'되돌리려면 : /wp-admin/?stella_deck=undo' ) ) );
} );
