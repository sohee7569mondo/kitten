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

	/* 따옴표 안을 가립니다 — 다만 상수 **이름**은 남깁니다.
	   이름까지 가리면 어느 줄이 무엇인지 알 수가 없습니다
	   (2026-09-14 · 처음 만들었을 때 그래서 못 알아봤습니다). */
	$mask = function ( $line ) use ( $NAMES ) {
		$keep = array();
		foreach ( $NAMES as $i => $n ) { $keep[ $n ] = '{{K' . $i . '}}'; }
		$out = str_replace( array_keys( $keep ), array_values( $keep ), (string) $line );
		$out = preg_replace( "/'[^']{9,}'/", "'●●●●●●●●'", $out );
		$out = preg_replace( '/"[^"]{9,}"/', '"●●●●●●●●"', $out );
		return str_replace( array_values( $keep ), array_keys( $keep ), $out );
	};

	/* 그 줄이 설명(주석) 안에 있는지 봅니다.
	   소희 님이 여신 「포트원 백엔드」 스니펫의 define 은 설명 안이라
	   PHP 가 읽지 않습니다. 그것을 「여기 고치세요」라고 하면 안 됩니다. */
	$commentLines = function ( $code ) {
		$lines = array();
		try {
			$src = $code;
			if ( false === strpos( $src, '<' . '?php' ) ) { $src = '<' . "?php\n" . $src; }
			$toks = @token_get_all( $src );
			if ( ! is_array( $toks ) ) { return $lines; }
			foreach ( $toks as $t ) {
				if ( ! is_array( $t ) ) { continue; }
				if ( T_COMMENT !== $t[0] ) {
					if ( T_DOC_COMMENT !== $t[0] ) { continue; }
				}
				$from = (int) $t[2];
				$n    = substr_count( (string) $t[1], "\n" );
				$i    = 0;
				while ( $i <= $n ) { $lines[ $from + $i ] = true; $i++; }
			}
		} catch ( Throwable $e ) {
			return array();
		}
		return $lines;
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
			$lines = @file( $p );
			if ( ! $lines ) { continue; }
			$rows = array();
			foreach ( $lines as $i => $line ) {
				foreach ( $NAMES as $n ) {
					if ( false !== strpos( $line, $n ) ) {
						$rows[] = ( $i + 1 ) . '줄  ' . trim( $mask( $line ) );
					}
				}
			}
			if ( $rows ) {
				$found = true;
				echo '<div class="box"><div class="hit">여기 있습니다 — '
					. esc_html( $p ) . '</div><code>'
					. esc_html( implode( "\n", $rows ) ) . '</code></div>';
			}
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
			$code = (string) $sn->post_content;
			$rows  = array();
			$live  = 0;
			$cmt   = $commentLines( $code );
			$lines = explode( "\n", $code );
			foreach ( $lines as $i => $line ) {
				if ( false === strpos( $line, 'define' ) ) { continue; }
				foreach ( $NAMES as $n ) {
					if ( false === strpos( $line, $n ) ) { continue; }
					$no    = $i + 1;
					$inCmt = isset( $cmt[ $no ] );
					if ( ! $inCmt ) { $live++; }
					$rows[] = $no . '줄  ' . trim( $mask( $line ) )
						. ( $inCmt ? '      ← 설명 안입니다 (PHP 가 안 읽습니다)' : '' );
				}
			}
			if ( ! $rows ) { continue; }
			$any = $any || ( $live > 0 );
			echo '<div class="box"><div class="' . ( $live ? 'hit' : 'no' ) . '">스니펫 '
				. (int) $sn->ID . ' · ' . esc_html( $sn->post_title )
				. ( $live ? '' : '  — 설명뿐입니다' ) . '</div><code>'
				. esc_html( implode( "\n", $rows ) ) . '</code>'
				. '<div class="where">'
				. ( $live
					? '이 스니펫을 열어 위 줄의 따옴표 안을 새 열쇠로 바꾸시면 됩니다.'
					: '여기는 고칠 자리가 아닙니다. 설명일 뿐이에요.' )
				. '</div></div>';
		}
		if ( ! $any ) {
			echo '<div class="box">스니펫 ' . count( $snips )
				. '개 가운데 define 으로 적어둔 곳이 없습니다.</div>';
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
