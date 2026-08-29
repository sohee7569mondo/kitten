<?php
/**
 * STELLA SAJU — 페이지 160(나의 전자책) 블록 갈아끼우기
 * ------------------------------------------------------------------
 * 한 번만 돌리는 스니펫입니다. 돌린 뒤에는 반드시 지우세요.
 *
 * 넣는 곳 : WPCode → + Add Snippet → Add Your Custom Code
 *           Code Type = PHP Snippet / Location = Run Everywhere / Active
 *           (맨 윗줄 <?php 은 빼고 붙여넣으세요)
 *
 * 돌리는 법 :
 *   1) 저장하고 Active 로 켠 다음
 *   2) 관리자로 로그인한 채 아래 주소를 엽니다
 *        미리보기 (아무것도 안 고침) : https://stellasaju.com/wp-admin/?stella_patch=dry
 *        진짜로 고치기               : https://stellasaju.com/wp-admin/?stella_patch=go
 *   3) 화면 위쪽에 결과가 뜹니다
 *   4) 결과를 확인했으면 WPCode 에서 이 스니펫을 지웁니다
 *   5) 호스팅 → 성능 → 캐시 비우기
 *
 * 왜 이렇게 하나 :
 *   - wp_update_post() 를 쓰면 워드프레스가 kses 로 <script> 를 통째로 지워버립니다.
 *     페이지 160 은 거의 전부가 <script> 라서 그러면 페이지가 죽습니다.
 *     그래서 $wpdb 로 post_content 를 직접 씁니다.
 *   - 고치기 전 내용을 옵션에 통째로 넣어둡니다. 잘못되면 되돌릴 수 있습니다.
 *     되돌리기 : ?stella_patch=undo
 * ------------------------------------------------------------------
 */

/* ===== 설정 =================================================== */

defined( 'STELLA_PATCH_PAGE' )  || define( 'STELLA_PATCH_PAGE',  160 );        // 고칠 페이지
defined( 'STELLA_PATCH_KEY' )   || define( 'STELLA_PATCH_KEY',   'lv30' );     // 이 패치의 이름 (한 번만 돌게 하는 표시)

/* 갈아끼울 블록을 찾는 표시.
   페이지 160 안의 <!-- wp:html --> 블록 중에서 이 글자가 들어 있는 것 하나를 바꿉니다.
   지금 페이지에 올라가 있는 연성 블록의 머리글은 "BUILD: LV3" 입니다. */
defined( 'STELLA_PATCH_FIND' )  || define( 'STELLA_PATCH_FIND',  'BUILD: LV3' );

/* 이미 새 것이 올라가 있으면 아무것도 하지 않게 하는 표시.
   새 블록 머리글에 적어둔 이름을 그대로 씁니다. */
defined( 'STELLA_PATCH_STAMP' ) || define( 'STELLA_PATCH_STAMP', 'BUILD: LV30' );

/* 찾는 블록이 없을 때 어떻게 할지
     'append' — 페이지 맨 뒤에 새 블록을 붙입니다
     'stop'   — 아무것도 안 하고 멈춥니다 (안전) */
defined( 'STELLA_PATCH_MISSING' ) || define( 'STELLA_PATCH_MISSING', 'stop' );


/* ===== ▼▼▼ 여기에 LV30 블록 본문을 붙여넣으세요 ▼▼▼ ==============
 *
 *   - <!-- wp:html --> 로 시작해서 <!-- /wp:html --> 로 끝나야 합니다.
 *     이 두 줄이 없으면 워드프레스가 클래식 블록으로 저장해서
 *     wpautop 이 <script> 안에 <p> 를 끼워넣고 전부 깨집니다.
 *   - 머리글 주석의 BUILD 이름은 위 STELLA_PATCH_STAMP 와 같아야 합니다.
 *   - 여기는 nowdoc(<<<'HTML')이라 $ 나 \ 를 그대로 써도 안전합니다.
 *     끝나는 HTML; 줄은 반드시 줄 맨 앞에서 시작해야 합니다.
 */
$STELLA_PATCH_BLOCK = <<<'HTML'
<!-- wp:html -->
<script>
/* ═══════════════════════════════════════════════════════════════
   STELLA SAJU — 연성의 신 · 주제별 풀이                BUILD: LV30
   붙이는 곳 : 페이지 160
   ─────────────────────────────────────────────────────────────── */

/* ↑↑↑ 이 자리에 LV30 코드를 넣으세요 ↑↑↑ */

</script>
<!-- /wp:html -->
HTML;
/* ===== ▲▲▲ 여기까지 ▲▲▲ ===================================== */


/* ------------------------------------------------------------------
 * 아래는 손대지 않으셔도 됩니다.
 * ---------------------------------------------------------------- */

add_action( 'admin_init', function () use ( $STELLA_PATCH_BLOCK ) {

	if ( ! isset( $_GET['stella_patch'] ) ) {
		return;
	}
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$mode      = sanitize_key( wp_unslash( $_GET['stella_patch'] ) );
	$page_id   = (int) STELLA_PATCH_PAGE;
	$done_opt  = 'stella_patch_' . STELLA_PATCH_KEY . '_done';
	$back_opt  = 'stella_patch_' . STELLA_PATCH_KEY . '_backup';
	$log       = array();

	$say = function ( $lines, $ok = true ) {
		add_action( 'admin_notices', function () use ( $lines, $ok ) {
			printf(
				'<div class="notice notice-%s"><p><strong>스텔라 패치 %s</strong></p><pre style="white-space:pre-wrap;margin:0">%s</pre></div>',
				$ok ? 'success' : 'error',
				esc_html( strtoupper( STELLA_PATCH_KEY ) ),
				esc_html( implode( "\n", $lines ) )
			);
		} );
	};

	global $wpdb;

	$row = $wpdb->get_row(
		$wpdb->prepare( "SELECT ID, post_content FROM {$wpdb->posts} WHERE ID = %d", $page_id )
	);

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
		$wpdb->update(
			$wpdb->posts,
			array(
				'post_content'      => $backup,
				'post_modified'     => current_time( 'mysql' ),
				'post_modified_gmt' => current_time( 'mysql', 1 ),
			),
			array( 'ID' => $page_id )
		);
		clean_post_cache( $page_id );
		delete_option( $done_opt );
		$say( array(
			'고치기 전 내용으로 되돌렸습니다.',
			'되돌린 크기 : ' . number_format( strlen( $backup ) ) . ' 바이트',
			'호스팅 → 성능 → 캐시 비우기 를 한 번 눌러주세요.',
		) );
		return;
	}

	$dry = ( 'go' !== $mode );

	/* ---- 이미 했나 ---- */
	if ( get_option( $done_opt ) ) {
		$log[] = '이 패치는 이미 돌렸습니다. (' . get_option( $done_opt ) . ')';
	}
	if ( false !== strpos( $content, STELLA_PATCH_STAMP ) ) {
		$say( array_merge( $log, array(
			'페이지에 이미 ' . STELLA_PATCH_STAMP . ' 이(가) 들어 있습니다. 아무것도 하지 않았습니다.',
			'WPCode 에서 이 스니펫을 지우셔도 됩니다.',
		) ) );
		return;
	}

	/* ---- 갈아끼울 블록 찾기 ---- */
	$blocks = parse_blocks( $content );
	$hit    = -1;

	foreach ( $blocks as $i => $block ) {
		if ( 'core/html' !== $block['blockName'] ) {
			continue;
		}
		if ( false !== strpos( $block['innerHTML'], STELLA_PATCH_FIND ) ) {
			if ( $hit >= 0 ) {
				$say( array_merge( $log, array(
					'"' . STELLA_PATCH_FIND . '" 이 들어 있는 블록이 두 개 이상입니다.',
					'어느 것을 바꿔야 할지 알 수 없어 멈췄습니다. 표시를 더 자세히 적어주세요.',
				) ), false );
				return;
			}
			$hit = $i;
		}
	}

	$new_block = trim( $STELLA_PATCH_BLOCK );

	if ( $hit < 0 ) {
		if ( 'append' !== STELLA_PATCH_MISSING ) {
			$say( array_merge( $log, array(
				'"' . STELLA_PATCH_FIND . '" 이 들어 있는 블록을 찾지 못했습니다.',
				'페이지 ' . $page_id . ' 의 블록 수 : ' . count( $blocks ),
				'아무것도 고치지 않았습니다.',
			) ), false );
			return;
		}
		$log[]   = '찾는 블록이 없어 맨 뒤에 붙입니다.';
		$updated = rtrim( $content ) . "\n\n" . $new_block . "\n";
		$where   = '맨 뒤 (' . count( $blocks ) . '번째)';
	} else {
		$old       = serialize_block( $blocks[ $hit ] );
		$log[]     = $hit . '번째 블록을 바꿉니다. (지금 ' . number_format( strlen( $old ) ) . ' 바이트)';
		$parsed = array_values( array_filter(
			parse_blocks( $new_block ),
			function ( $b ) { return ! empty( $b['blockName'] ); }
		) );
		if ( 1 !== count( $parsed ) ) {
			$say( array_merge( $log, array(
				'붙여넣은 새 블록이 <!-- wp:html --> … <!-- /wp:html --> 한 덩어리가 아닙니다.',
				'읽어낸 블록 수 : ' . count( $parsed ),
			) ), false );
			return;
		}
		$blocks[ $hit ] = $parsed[0];
		$updated   = serialize_blocks( $blocks );
		$where     = $hit . '번째';
	}

	$log[] = '자리   : ' . $where;
	$log[] = '지금   : ' . number_format( strlen( $content ) ) . ' 바이트';
	$log[] = '바뀐 뒤 : ' . number_format( strlen( $updated ) ) . ' 바이트';

	/* ---- 안전장치 : 페이지가 갑자기 반토막 나면 멈춥니다 ---- */
	if ( strlen( $updated ) < strlen( $content ) * 0.5 ) {
		$say( array_merge( $log, array(
			'바뀐 내용이 원래의 절반도 안 됩니다. 뭔가 잘못된 것 같아 멈췄습니다.',
		) ), false );
		return;
	}

	if ( $dry ) {
		$say( array_merge( $log, array(
			'',
			'※ 미리보기였습니다. 아무것도 고치지 않았습니다.',
			'진짜로 고치려면 주소 끝을 ?stella_patch=go 로 바꿔서 다시 여세요.',
		) ) );
		return;
	}

	/* ---- 진짜로 고치기 ---- */
	update_option( $back_opt, $content, false );

	$ok = $wpdb->update(
		$wpdb->posts,
		array(
			'post_content'      => $updated,
			'post_modified'     => current_time( 'mysql' ),
			'post_modified_gmt' => current_time( 'mysql', 1 ),
		),
		array( 'ID' => $page_id )
	);

	if ( false === $ok ) {
		$say( array_merge( $log, array( '저장에 실패했습니다. ' . $wpdb->last_error ) ), false );
		return;
	}

	clean_post_cache( $page_id );
	update_option( $done_opt, current_time( 'mysql' ), false );

	$say( array_merge( $log, array(
		'',
		'다 됐습니다.',
		'1) WPCode 에서 이 스니펫을 지우세요. (꼭)',
		'2) 호스팅 → 성능 → 캐시 비우기',
		'3) 시크릿 창에서 https://stellasaju.com/reading-book/ 확인',
		'',
		'되돌리려면 : /wp-admin/?stella_patch=undo',
	) ) );
} );
