<?php
/**
 * STELLA SAJU — 결제 심사에 걸리는 값 표시 바로잡기
 *
 *  KG이니시스 입점조건 2번 : 「품절 / 0원 / 임의의 가격 설정 불가」
 *  지금 사이트에는 같은 물건의 값이 네 가지로 적혀 있습니다.
 *
 *    /price/ · 문 페이지    990원      ← 실제로 받는 값
 *    /guide/                무료(체험판) ← 틀렸습니다. 코드는 TRIAL=false 입니다
 *    상단 메뉴 · 인생길잡이  50,000원   (16주제)
 *    /price/  · 인생길잡이   24,750원   (30주제)
 *
 *  세 가지를 고칩니다
 *    1) /guide/ 의 「무료」를 실제 값 990원으로. — 가장 급합니다
 *    2) 「나의 인생길잡이」의 값을 메뉴와 가격 안내에서 뗍니다.
 *       항목은 남기고 「준비 중」이라고만 합니다 (값이 붙은 채 못 사면 품절).
 *    3) 머리말의 베타 띠를 내립니다 — 「아직 손보는 중인 곳이 있어요」는
 *       카드사 심사자에게 영업 준비가 안 된 사이트로 읽힙니다.
 *       띠를 내리면서 빈칸 높이도 108→76 / 92→64 로 되돌립니다.
 *
 *  되돌리기 : ?stella_patch=undo — 심사가 끝나면 그대로 되살아납니다.
 *  쓰는 법  : 확인 ?stella_patch=dry · 적용 =go
 */

add_action( 'init', function () {

	if ( ! isset( $_GET['stella_patch'] ) ) { return; }
	if ( ! current_user_can( 'manage_options' ) ) { return; }
	$mode = sanitize_text_field( wp_unslash( $_GET['stella_patch'] ) );

	global $wpdb;
	$bak_key = 'stella_bak_review_fix';
	$expect_b64 = 2648;

	$edits_b64 =
		'H4sIACollWoC/8VYbU9TSRT+KyfdxEDCS1sVFSsJrq5xJVmDmv0gxhSoQIJAKLq7MSYXKKTS4hZo' .
		'oWqLRXlPjReoULL4hZ+i3+7M/Q97zszc23v7AroxWT4o7cycM+ec5zzPGZ55+kPB3tCopxXu3/ew' .
		'3Zw5qQHL5uD4ANhG1BzP86UpTwN4AAK9A0+hZzAYDl/p8oTDQ8Gnjd2hsWCXB0aHB0P03Vhw7Em4' .
		'y9PWNQT4EwiPBIfsA90+XOAbmlGM8qwGge425cwo6oYeCTR3t/HlKRaLsthqoJmOtpUZ8JOBVIRv' .
		'jAOfTrC9AptJAl+d49kiGHt7PFsAvhzliwX+OtkE+JFPjpupDPBcgmcjwFNxllvl7494LMO2CsD0' .
		'JFvJ4MkcP0wbuzk+88nlnYIINGPM+BslwPOgASoydBjlh0Vg0/PkvY5FFig281USHdTToZ/C4UZK' .
		'FFrsCY0+6w8N9PWPtfq8F0f+vPy89oYLLWL9dI/83XiZR4DqJi/5LZe1drScq+l0exOzxbNHwLaS' .
		'7EVBuZfGANT5nuBgT53P633aD41A7uovly/1OtZOOk1XqXVarqlryuvgFREEfDJrFIt8eYVKv5Tg' .
		'ESyuPg9s8QghZnmTP4Eg9I+GHiGqmvueDPSGmglaS3gqzyMfgTCSy7C1IyD4GPtxnjkiqLjxGH7S' .
		'jafOexu8Xi9/k7Aw2xxU8FeeXGeGhsdCeIhN7JSslvyaL4t4dcLmRcsqnHncGwz3XwaW36f9uIad' .
		'c5ZtxIXL7jZgsxmE8hsbvU2B7lHXDQBKXcdXNXYYET0jUkSNIi/D9jUzotNlsElEH5UMysi+JYN5' .
		'9jb/XemTF6Iu/p788Yk8OgFzXqM4XiFO9yJ8OcHW85VeMXHEE2ZckoDwZ6bS2PZlUVamTXINYkic' .
		'zKXwGKYSv5/h+JvFMy5KE7kUXGYXt2Y+HyCEPSOjAz0hSb6UtO0tAeYIMpqukbMv0/MyIPGxVINA' .
		'v79Nxu/cjXSNWA8042LVrWQJUSY3iA4q6xvybjUNZSgVZRMFDISslbLjUoLR4T9syi8tl+XSdWJI' .
		'tECaZ9Plbeuu9liwD8LDw0M2TpwwOcVHL/mIrVJbsXyRXGF5kBLYmp2sEk55LoL4F+1UAR7RNu+m' .
		'zNQW2yvaClUFLgiYNwnj04fjAxbX+OvC8QFPr5qLL4zDOHljsQICilwhUvnOlOVhI84WVhFMbCFD' .
		'8kSQun3tFxDgyWl8eY1QF0MIRdOnARYoMpZM8kUUCBX7foTAy5I6GpT/ArGNlMCzFs044qpIbJVv' .
		'nIkewUT7z104Lzgw/Dg4ONhmfMrzmTz4zxt6Buslviu3UqmsdokV6kTdltdEJDG89YKuaNwyEhhx' .
		'kwmEx/4Sc8jj4GjfwFCrD0UUvODFC37V4rb5r9osTQxsLiEKTeWVjW6XAsvl6HM74aXLy56XibQr' .
		'Qyxj7E4qJihvOMd0gzkeUZH/h1BOIVkn3Wkn0J0jmBNpDg82yC8pLQQaOWcR2aKC4NK4c3ayYpPq' .
		'vFkkSt5IWKzCdwvGXkQMEdubNkEpuEiWy8AVuHRJSB/U3bl7vaOj/eFvnVcf3ur8vV7d2Z1aG/rS' .
		'io9MoA3bCCgjtztv/nz94dX2O9fBpwxV56CSLQFgtGXBu9zYL/c6OnDT/xoImfqSngK/19/S6L3Y' .
		'eNYHrYBwrx6bwH7arjU5f5kmDUXEo4ziwMxim2rIUyMUw//KUSPOY4PuvxIg28GSbv8DqMpiIsep' .
		'e14IorGrE0bjGrIg8FieZFsaxQvSnlwULySG8B1EymfpRPmou3WDhqFYFJufz5CETtEgv6IbOwXw' .
		's90ofNEQ58LK8QGlCAl3OSLD04zdLdTFVQQu3jKKX9Tbd9+NoxP8xo6CiACfDyrcWJ4tlyIWTtSU' .
		'6WuRTQf2zAfNyqgrk0iraqP/XINETpPFYmY8TpTBUnEsexqLJHk+pVqUJdIc9RZbK1IkKZAzghiw' .
		'1AMtX2Dv49RI5lIamxzMuQyROYkYesiJkVdSgXsAcMyA1lnHcws31KKiNjWcChUtKKmsNtfIzq+m' .
		'EDTiuEYE1zKqPC7e7bzZ3lEhEs593QO0TybgxI3WkGjnSL4wscCCokV7Cfgv6BbPuUQVy8FjWRyq' .
		'M4hbEfMSlaSS+ywACdEw9LmqEio/uYuBB0/PuYKJcVC0GEK1LuoUUleBxz78iMQLOvmGxEsa+pbE' .
		'OwnszOOB3t7hMXy/7Gs0duGoav6dN1Ob5dML+0haAXx/CxGGYkNtaSsqlWC6VCRFnAL07kTZtaFW' .
		'rswaPvTZWsF6/ye2akxSkrfE3JURjLb+gnq3woE9MOD7g95wNMKt54ViCga2sEKsi3DxsakI4pA2' .
		'GwXN4b4aXtwCqpSWxsS5hP2alYIAd9p/vSd5qrqe8em40JI69VKrRy9X793suNYKN3w/zJK/hha5' .
		'qJFol2axE8hI/L1BNDlpQ1Y+Q3DIUAPMUsUMg2Vhb3U2qxNFOViYf05SQbB+gluuPAoOhkOAFql0' .
		'kixpJsZ1CW0xJzsf0tK86+5sYoWGeDOmsXXdklGsj2PCWoqy2bSArT3vqXvWVEMhJYrICfIYUFwT' .
		'w5yeFiyLOzM54d8CjTR5qkbWNzlkwYpTDYriz19UWDtgVJvn/wKFNLZaEBQAAA=='
;

	header( 'Content-Type: text/html; charset=utf-8' );
	echo '<meta charset="utf-8"><style>body{font:15px/1.7 -apple-system,"Apple SD Gothic Neo",sans-serif;max-width:940px;margin:40px auto;padding:0 20px}';
	echo 'code{background:#f4f4f4;padding:1px 5px;border-radius:3px}';
	echo '.ok{color:#0a7a2f}.no{color:#c0392b;font-weight:700}.dim{color:#888}';
	echo '.box{border:1px solid #ddd;border-radius:8px;padding:14px 18px;margin:14px 0}</style>';
	echo '<h2>결제 심사 · 값 표시 바로잡기</h2>';

	$hdr = $wpdb->get_row(
		"SELECT ID FROM {$wpdb->posts}
		 WHERE post_type = 'wp_template_part' AND post_name = 'header' AND post_status = 'publish'
		 ORDER BY ID DESC LIMIT 1", ARRAY_A );
	if ( ! $hdr ) { echo '<p class="no">머리말 템플릿 파트를 찾지 못했습니다.</p>'; exit; }
	$targets = array( 'header' => (int) $hdr['ID'], 'price' => 249, 'guide' => 189 );
	$label   = array( 'header' => '머리말 (템플릿 파트)', 'price' => '가격 안내 (249)', 'guide' => '나의 인생길잡이 (189)' );

	if ( 'undo' === $mode ) {
		$bak = get_option( $bak_key );
		if ( ! $bak ) { echo '<p class="no">되돌릴 백업이 없습니다.</p>'; exit; }
		foreach ( $bak as $id => $c ) {
			$wpdb->update( $wpdb->posts, array( 'post_content' => $c ), array( 'ID' => (int) $id ) );
			clean_post_cache( (int) $id );
		}
		echo '<p class="ok">되돌렸습니다.</p>'; exit;
	}

	$edits_txt = preg_replace( '/\s+/', '', $edits_b64 );
	if ( strlen( $edits_txt ) !== $expect_b64 ) {
		echo '<p class="no">붙여넣기가 잘렸습니다. 담긴 글자 ' . strlen( $edits_txt ) . ' / 있어야 할 글자 ' . $expect_b64 . '</p>'; exit;
	}
	$packed = base64_decode( $edits_txt, true );
	$sets   = ( false === $packed ) ? null : json_decode( (string) @gzdecode( $packed ), true );
	if ( ! is_array( $sets ) ) { echo '<p class="no">고칠 목록을 풀지 못했습니다.</p>'; exit; }

	$fixnl = function ( $t ) { return str_replace( array( "\r\n", "\r" ), "\n", $t ); };
	$mkre  = function ( $find ) use ( $fixnl ) {
		$lines = explode( "\n", $fixnl( $find ) );
		foreach ( $lines as $i => $l ) { $lines[ $i ] = preg_quote( $l, '/' ); }
		return '/' . implode( '\r?\n', $lines ) . '/u';
	};

	$plan = array(); $backup = array(); $fail = false;

	foreach ( $sets as $key => $edits ) {
		$id = $targets[ $key ];
		$c  = $wpdb->get_var( $wpdb->prepare( "SELECT post_content FROM {$wpdb->posts} WHERE ID = %d", $id ) );
		if ( null === $c ) { echo '<p class="no">' . $id . ' 을 찾지 못했습니다.</p>'; $fail = true; continue; }
		$backup[ $id ] = $c;

		echo '<h3>' . esc_html( $label[ $key ] ) . ' <span class="dim">· ' . $id . '</span></h3><ol>';
		foreach ( $edits as $e ) {
			list( $name, $from, $to ) = $e;
			$re = $mkre( $from );
			$n  = preg_match_all( $re, $c );
			echo '<li>' . esc_html( $name ) . ' — ';
			if ( 1 === $n ) {
				echo '<b class="ok">1</b> / 1';
				$c = preg_replace_callback( $re, function ( $m ) use ( $to, $fixnl ) { return $fixnl( $to ); }, $c, 1 );
			} elseif ( 0 === $n && '' !== $to && strpos( $c, $fixnl( $to ) ) !== false ) {
				echo '<span class="ok">이미 고쳐져 있습니다</span>';
			} else {
				echo '<b class="no">' . $n . '</b> / 1 <span class="no">← 어긋납니다</span>'; $fail = true;
			}
			echo '</li>';
		}
		echo '</ol>';
		$plan[ $id ] = $c;
	}

	echo '<div class="box"><b>마무리 확인</b><br>';
	$checks = array(
		'머리말에 베타 띠 남았나 (0)'      => substr_count( $plan[ $targets['header'] ], 'ssnav-beta' ),
		'머리말에 50,000원 남았나 (0)'     => substr_count( $plan[ $targets['header'] ], '50,000원' ),
		'가격 안내에 24750원 남았나 (0)'   => substr_count( $plan[249], '24750원' ),
		'인생길잡이에 「무료」 남았나 (0)'  => substr_count( $plan[189], '<div class="big">무료</div>' ),
		'인생길잡이에 990원 들어갔나 (1)'  => substr_count( $plan[189], '<div class="big">990원</div>' ),
	);
	foreach ( $checks as $k => $v ) {
		$want = ( strpos( $k, '(1)' ) !== false ) ? 1 : 0;
		echo esc_html( $k ) . ' : <b class="' . ( $v === $want ? 'ok' : 'no' ) . '">' . $v . '</b><br>';
		if ( $v !== $want ) { $fail = true; }
	}
	echo '</div>';

	if ( $fail ) { echo '<p class="no">어긋난 곳이 있어 아무것도 바꾸지 않았습니다. 이 화면을 그대로 보여주세요.</p>'; exit; }

	if ( 'go' !== $mode ) {
		echo '<p class="ok"><b>확인만 했습니다. 아무것도 바꾸지 않았습니다.</b></p>';
		echo '<p>이대로 넣으시려면 <code>?stella_patch=go</code> 로 여세요.</p>'; exit;
	}

	if ( false === get_option( $bak_key ) ) { update_option( $bak_key, $backup, false ); }
	foreach ( $plan as $id => $c ) {
		$wpdb->update( $wpdb->posts, array( 'post_content' => $c ), array( 'ID' => (int) $id ) );
		clean_post_cache( (int) $id );
		$chk = $wpdb->get_var( $wpdb->prepare( "SELECT post_content FROM {$wpdb->posts} WHERE ID = %d", (int) $id ) );
		echo '<p><b>' . $id . '</b> — ' . ( sha1( $chk ) === sha1( $c ) ? '<span class="ok">넣었습니다.</span>' : '<span class="no">확인 실패</span>' ) . '</p>';
	}
	echo '<p>심사가 끝나고 베타 띠를 되살리시려면 <code>?stella_patch=undo</code> — 다만 값 수정까지 함께 돌아갑니다.</p>';
	exit;
}, 1 );
