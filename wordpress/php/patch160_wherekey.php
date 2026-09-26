<?php
/* ═══════════════════════════════════════════════════════
   포트원 열쇠가 어디에 적혀 있나 찾기   patch160_wherekey
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」
   ★ 관리자로 로그인한 창에서만 열립니다.

       https://stellasaju.com/?stella_wherekey=1

   소희 님 : 「어디에 넣어야 해?」

   「STELLA - 포트원 백엔드」 스니펫을 여시면 define 이 보이는데
   그건 여는 빗금별표와 닫는 별표빗금 사이에 든 **설명**입니다.
   PHP 가 읽지 않아요. (이 글 안에 그 기호를 그대로 쓰면 설명이
   거기서 끝나버려 조각이 깨집니다 — 방금 한 번 그랬습니다.)
   진짜 열쇠는 다른 자리에 적혀 있습니다 —
   wp-config.php 이거나 다른 스니펫입니다.

   이 조각이 그 자리를 찾아 줍니다. 찾은 뒤에는 꺼두셔도 됩니다.

   ★ 열쇠 값은 한 자도 찍지 않습니다.
     define 줄을 보여드릴 때 따옴표 안은 통째로 가립니다.
     길이와 앞 네 글자만 냅니다 — 새 열쇠와 대보시라고요.
   ═══════════════════════════════════════════════════════ */

add_action( 'template_redirect', function () {

	if ( ! isset( $_GET['stella_wherekey'] ) ) { return; }
	if ( ! is_user_logged_in() ) {
		wp_die( '관리자로 로그인한 창에서 열어주세요.', '스텔라', array( 'response' => 200 ) );
	}
	if ( ! current_user_can( 'manage_options' ) ) {
		wp_die( '관리자만 볼 수 있습니다.', '스텔라', array( 'response' => 200 ) );
	}

	nocache_headers();
	header( 'Content-Type: text/html; charset=utf-8' );

	$NAMES = array( 'STELLA_PORTONE_SECRET', 'STELLA_PORTONE_STORE',
		'STELLA_PORTONE_CHANNEL', 'STELLA_UM_KAKAO_REST' );

	/* ── define 을 토큰으로 찾습니다 ───────────────────────────
	   글자로 'define' 을 찾으면 **defined** 까지 걸립니다.
	   2026-09-14 · 소희 님 화면에 tool_portone 의
	       if ( '' === $secret ) { if ( defined( 'STELLA_PORTONE_SECRET' ) ) {
	   가 「여기 고치세요」로 잘못 나왔습니다. 거기는 읽는 곳이지
	   적는 곳이 아닙니다.

	   PHP 자신에게 물어보면 틀릴 일이 없습니다 —
	     · 설명(주석) 안의 define 은 T_COMMENT 한 덩어리로 묶여
	       아예 안 잡힙니다
	     · defined 는 T_STRING 값이 'defined' 라 저절로 걸러집니다
	     · 값은 따옴표 토큰이라 정규식으로 자를 일이 없습니다 */
	$scan = function ( $code ) use ( $NAMES ) {
		$rows = array();
		$src  = (string) $code;
		if ( false === strpos( $src, '<' . '?php' ) ) {
			$src = '<' . "?php\n" . $src;
		}
		$toks = @token_get_all( $src );
		if ( ! is_array( $toks ) ) { return $rows; }
		$n = count( $toks );
		$i = 0;
		while ( $i < $n ) {
			$t = $toks[ $i ];
			$i++;
			if ( ! is_array( $t ) ) { continue; }
			if ( T_STRING !== $t[0] ) { continue; }
			if ( 'define' !== strtolower( $t[1] ) ) { continue; }

			/* 다음에 여는 괄호가 와야 합니다 */
			$j = $i;
			while ( $j < $n ) {
				if ( is_array( $toks[ $j ] ) ) {
					if ( T_WHITESPACE === $toks[ $j ][0] ) { $j++; continue; }
				}
				break;
			}
			if ( $j >= $n ) { continue; }
			if ( '(' !== $toks[ $j ] ) { continue; }

			/* 첫 칸 — 상수 이름 */
			$k = $j + 1;
			while ( $k < $n ) {
				if ( is_array( $toks[ $k ] ) ) {
					if ( T_WHITESPACE === $toks[ $k ][0] ) { $k++; continue; }
				}
				break;
			}
			if ( $k >= $n ) { continue; }
			if ( ! is_array( $toks[ $k ] ) ) { continue; }
			if ( T_CONSTANT_ENCAPSED_STRING !== $toks[ $k ][0] ) { continue; }
			$nm = trim( (string) $toks[ $k ][1], "'" . '"' );
			if ( ! in_array( $nm, $NAMES, true ) ) { continue; }

			/* 둘째 칸 — 값 */
			$v = $k + 1;
			while ( $v < $n ) {
				if ( is_array( $toks[ $v ] ) ) {
					if ( T_WHITESPACE === $toks[ $v ][0] ) { $v++; continue; }
				}
				if ( ',' === $toks[ $v ] ) { $v++; continue; }
				break;
			}
			$val  = null;
			if ( $v < $n ) {
				if ( is_array( $toks[ $v ] ) ) {
					if ( T_CONSTANT_ENCAPSED_STRING === $toks[ $v ][0] ) {
						$val = trim( (string) $toks[ $v ][1], "'" . '"' );
					}
				}
			}
			$rows[] = array( 'line' => (int) $t[2], 'name' => $nm, 'val' => $val );
		}
		return $rows;
	};

	/* 찾은 줄을 사람이 읽게 — 값은 길이와 앞 네 글자만 */
	$show = function ( $r ) {
		$v = $r['val'];
		if ( null === $v ) { $tail = '값이 글자가 아닙니다 (다른 상수를 가리킵니다)'; }
		elseif ( '' === $v ) { $tail = '값이 비어 있습니다'; }
		else {
			$tail = '값 ' . mb_strlen( $v ) . '자 · 앞 네 글자 '
				. mb_substr( $v, 0, 4 ) . '●●●●';
		}
		return $r['line'] . '줄   define( ' . "'" . $r['name'] . "'" . ', … )   ' . $tail;
	};

	echo '<!doctype html><meta charset="utf-8">';
	echo '<meta name="viewport" content="width=device-width,initial-scale=1">';
	echo '<title>열쇠가 어디 있나</title>';
	echo '<style>
body{margin:0;padding:26px 18px 80px;background:#F1EDE3;color:#221C33;
  font:16px/1.85 -apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;}
.w{max-width:820px;margin:0 auto;}
h1{font-size:1.34rem;margin:0 0 6px;}
.dek{color:#8B849C;font-size:.92rem;margin:0 0 24px;}
h2{font-size:1.04rem;margin:28px 0 10px;padding-top:16px;border-top:1px solid #E2DACB;}
.box{background:#fff;border:1px solid #E2DACB;border-radius:9px;padding:14px 16px;margin-top:10px;}
code{font-family:"IBM Plex Mono",monospace;font-size:.9rem;color:#4E4763;
  display:block;white-space:pre-wrap;word-break:break-all;}
.hit{color:#2F7D4A;font-weight:700;}
.no{color:#C4453A;font-weight:700;}
.k{font-family:"IBM Plex Mono",monospace;color:#221C33;font-weight:700;}
.where{margin-top:8px;padding:12px 14px;border-radius:8px;background:#FAF7F0;
  border:1px solid #EAE2D2;font-size:.93rem;}
.big{margin-top:16px;padding:16px 18px;border-radius:10px;
  background:#EDF7F0;border:1px solid #BFE0C9;color:#2F7D4A;font-weight:700;}
.big.no{background:#FBEFEE;border-color:#EBC7C3;color:#C4453A;}
</style>';
	echo '<div class="w"><h1>포트원 열쇠가 어디에 적혀 있나</h1>';
	echo '<p class="dek">찾기만 합니다. 열쇠 값은 한 자도 찍지 않습니다.</p>';

	try {

		/* ① 지금 들어 있는 값 ------------------------------------- */
		echo '<h2>① 지금 사이트가 들고 있는 열쇠</h2><div class="box">';
		foreach ( $NAMES as $n ) {
			if ( ! defined( $n ) ) {
				echo '<div><span class="k">' . esc_html( $n ) . '</span> — <span class="no">없습니다</span></div>';
				continue;
			}
			$v = (string) constant( $n );
			if ( '' === $v ) {
				echo '<div><span class="k">' . esc_html( $n ) . '</span> — (비어 있음)</div>';
				continue;
			}
			echo '<div><span class="k">' . esc_html( $n ) . '</span> — '
				. esc_html( mb_substr( $v, 0, 4 ) ) . '●●●●●●●● ('
				. mb_strlen( $v ) . '자)</div>';
		}
		echo '</div>';
		echo '<p class="where">앞 네 글자를 포트원에서 새로 받으신 열쇠와 대보세요. '
			. '다르면 아직 옛 열쇠입니다.</p>';

		/* ② wp-config.php 에 있나 --------------------------------- */
		echo '<h2>② wp-config.php 에 있나</h2>';
		$paths = array();
		if ( defined( 'ABSPATH' ) ) {
			$paths[] = ABSPATH . 'wp-config.php';
			$paths[] = dirname( ABSPATH ) . '/wp-config.php';
		}
		$found = false;
		foreach ( $paths as $p ) {
			if ( ! @is_readable( $p ) ) { continue; }
			$code = @file_get_contents( $p );
			if ( ! $code ) { continue; }
			$rows = $scan( $code );
			if ( ! $rows ) { continue; }
			$found = true;
			$out = array();
			foreach ( $rows as $r ) { $out[] = $show( $r ); }
			echo '<div class="box"><div class="hit">여기 있습니다 — '
				. esc_html( $p ) . '</div><code>'
				. esc_html( implode( "\n", $out ) ) . '</code></div>';
		}
		if ( ! $found ) {
			echo '<div class="box">wp-config.php 에는 없습니다 '
				. '(또는 읽을 수 없습니다).</div>';
		}

		/* ③ 어느 스니펫에 있나 ------------------------------------ */
		echo '<h2>③ 어느 WPCode 스니펫에 적혀 있나</h2>';
		$snips = get_posts( array(
			'post_type'      => 'wpcode',
			'post_status'    => 'any',
			'posts_per_page' => 500,
		) );
		$any = false;
		foreach ( $snips as $sn ) {
			$rows = $scan( (string) $sn->post_content );
			if ( ! $rows ) { continue; }
			foreach ( $rows as $r ) {
				if ( null !== $r['val'] ) {
					if ( '' !== $r['val'] ) { $any = true; }
				}
			}
			$out  = array();
			$real = 0;
			foreach ( $rows as $r ) {
				$out[] = $show( $r );
				if ( null !== $r['val'] ) {
					if ( '' !== $r['val'] ) { $real++; }
				}
			}
			echo '<div class="box"><div class="' . ( $real ? 'hit' : 'no' ) . '">스니펫 '
				. (int) $sn->ID . ' · ' . esc_html( $sn->post_title )
				. ( $real ? '' : '  — 비워둔 대비값입니다' ) . '</div><code>'
				. esc_html( implode( "\n", $out ) ) . '</code>'
				. '<div class="where">'
				. ( $real
					? '이 스니펫을 열어 위 줄의 둘째 따옴표 안을 새 열쇠로 바꾸시면 됩니다.'
					: '여기는 「값이 없을 때 대신 쓸 것」을 적어두는 자리라 일부러 비어 '
					. '있습니다. 고칠 자리가 아닙니다.' )
				. '</div></div>';
		}
		if ( ! $any ) {
			echo '<div class="box">스니펫 ' . count( $snips )
				. '개 가운데 define 으로 적어둔 곳이 없습니다. '
				. '(설명 안에 적힌 본보기는 세지 않습니다.)</div>';
		}

		if ( $found ) {
			echo '<div class="big">wp-config.php 에 있습니다. '
				. '워드프레스 편집기로는 못 고치고 SFTP 로 열어야 합니다.</div>';
		} elseif ( $any ) {
			echo '<div class="big">위 스니펫을 열어 고치시면 됩니다.</div>';
		} else {
			echo '<div class="big no">적힌 자리를 못 찾았습니다. '
				. '서버 설정(환경변수)에 들어 있을 수 있습니다.</div>';
		}

	} catch ( Throwable $e ) {
		echo '<div class="big no">읽다가 멈췄습니다 — ' . esc_html( $e->getMessage() )
			. ' (' . esc_html( basename( $e->getFile() ) ) . ' ' . (int) $e->getLine() . '줄)</div>';
	}

	echo '<p class="dek" style="margin-top:26px">이 조각은 patch160_wherekey 입니다. '
		. '찾으신 뒤에는 꺼두셔도 됩니다.</p></div>';
	exit;
}, 1 );
