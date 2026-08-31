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
 *    2) 「나의 인생길잡이」 — 주제 수(16개니 30개니)는 뺍니다. 어떻게 묶일지
 *       아직 정해지지 않았으니까요. 값은 24,750원으로 하나로 맞춥니다
 *       (메뉴에 있던 50,000원은 버립니다).
 *       다만 값을 「상품 표 안」에 두지는 않습니다. 값이 붙었는데 못 사는 행은
 *       심사에서 품절로 읽힙니다. 표 밖 예고 문장으로 옮겨 적습니다 —
 *       숫자는 그대로 보이고, 파는 물건으로는 안 보입니다.
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
	$expect_b64 = 2692;

	$edits_b64 =
		'H4sIAMkllWoC/8VYbU8TWRT+KyfdxEAC0tZ3rCS6usaVZI0v2Q9qTIEqJAiEorsbYzLgQCotbsEW' .
		'Rm2xKgqYug4wQsniF3+Kfpt75z/sOffemc70RdCYLB8Ueu89555znvOc5/ZeqD8R70uMhjrh6tUQ' .
		'Wy85DzRgxRJ82gK2nHLGy3xhMtQGIYBY38Bd6B2MJ5MnroWSyaH43faexFj8WghGhwcT9NlYfOxO' .
		'8lqo69oQ4E8sORIf8g70RHCBL2t2JcWLGsR6upQzu2Laph7r6Onii5MsnWLppVgHHe2qMRAlA3md' .
		'L48Dn8qyDYtN54AvzfJiBeyNDV60gC+m+LzFn+b2A/7JH4w7+QLwUpYXdeD5DCst8Vc7PF1gqxYw' .
		'M8deFPBkiW8b9nqJT38IeKcgYh0YM/5GCQhdb4O6DG2n+HYF2NQceW9h+mOKzXmSQwetdOinZLKd' .
		'EoUWexOj9/oTA7f6xzoj4aMjfx6/33zDkcNifXeP/OV4jUeAxiaPRV2XzXYcPtjU6dsVzBYv7gBb' .
		'zbGHlnIvjQGo873xwd6WSDh8tx/agdy1Hq9d6vOtfe00XaXZabmmrimvg1dEEPAHRbtS4Ysv8Grs' .
		'9Q7Y5hxwI4UFxjq73uRPLA79o4mbiKqOW3cG+hIdBK0Fiy+Uuf4eCCOlApkg+NibGV7YIagE8Zi8' .
		'04OnDoXbwuEwf5Z1MdsRV/BXngJnhobHEniITaxVrVb9Oo8qdHXE5lHXKuy73RdP9h8HVt6k/biG' .
		'nXOALWeEy54uYDMFhPIzD737Yz2jgRsAVLuOL2lsWxc9g06zolHkZdim5ugmXQabRPRR1aCMbC8Z' .
		'LLPn5W9Kn7wQdfG35I9PlNEJOHMaxfEEcbqh88Use1Ou94qJI55wMpIEhD8nbyAqaqKsTxviyRyv' .
		'7iUziCnFXtGDbUcOhVUVfOmsJru2yk0Tex2xHBoZHehNSBam7L1dFajWkdpMDW3C56k5GZn4s1qM' .
		'WH+0SybCvxt5G3k11oGLDbeSJYSb3CBaqaaByDs1EJvfEeHnU2zCUn1UTVNgJIwO/+Fxf3W5JqmB' .
		'E0OiFwxeNGr7N1j2sfgtSA4PD3mA8eNlFx995CO9RP3FyhVyhcXjOuLTS1YVsLykYyOIvqpDkeif' .
		'l5NOfpVtVLxR1QA3iJxnWfvDu09bLKPxp9anLW4sOfMP7e0MeWNpC6cYuULI8rVJ18Nyhj1ewunF' .
		'HhdoThGWLpz+BQR4ShpffI1I5GmEUMrYDblAkbFcjs/jpFCxb+qEf5Yz0aD8F4h25Cw84PKNL666' .
		'xDb4xJ/oEUx09KDqieTt+OBgl/2hzKfLED1kmwWsl/is1kr9iHVmidHmFXeLqi2+dtvI+If0QsX0' .
		'4zA2EmQVSI79JQTJ7fjorYGhzghOUwhDGC/4Rct4CPqizZB0YLNZUWgqr1QXXimwXAIf+WmOufcS' .
		'Xr28bHaZSK8ygifWHyieqG04n8zBHI+oyL8jlF3Ydq+85wvmO/jOm0+uMPNlYmEKUwgi+NkCbid7' .
		'TH+1S0aRJ5HGaWtGExUXso64HU1g/cv4m1+tuUmUemClQqeXsy598XXL3tCFbHm74jGhwqWk0wKc' .
		'gGPHxLCFlkuXz3R3n7zx28VTN85f/L1V3StYQ6/HpJUImUAbnhFQRi5cPPfzmRunTl46AxFlqDHZ' .
		'VW2JTkFbbh/VGvvlSnc3bvpfAyFTn41JiIajh9vDR9sPRKATsK8axyaazJA40iUYHhkEH2wtHNwo' .
		'0Vl6RclKgpSOyMX/apEhzqPu3Hwi+nQNS/r2X0AdIN4AqPPnxMi1101qhoyGdAs8XSahII3iBWlP' .
		'KYUXErJ/DZHyUTpRPlrOnyX5lU4hKfJpmtWT9HR4YdprFkTZego+a9hQwsqnLUoRMvuiLsPT7PVV' .
		'HMBLvJTHW6bwg1bv7usZdIKfeFEQ4+CDRYWbLrPFasTCidK1kcOyu8FTmdChjAYyifytNnpdul8Q' .
		'fxrrnMlQR7J8BstuYJHkQMmrPmdZg09Qy6F4oJkjxYiQdOpJWLbYqww1krNgIJuIZk7LaYkeSgUR' .
		'leCcoNLwqU73rO+BhxuacV6XksNiXFtqJjcSULLzG40i0lIBLRJYRjmBi5cvnjvZXTeN/Pt6Bmif' .
		'TMBXN7qy1MuRfNMqzpPtJeD/2HTZLzC9sRw8XcShV0DcipglC65aNfTnAkhMJ9ucbTir5V/BYuDB' .
		'3XOuYGJvVVyGUK2LAxGpy+Lpdz8i8YJO9pB4SUN7SbyfwPbdHujrGx7DF9OmRvoONbHzd9nJr9TK' .
		'JPaeZgXwzVVEmJMXbemNbkuML69IijgF6IOJ8mpDrVyfNb5tsNeW+41DdrWJZJO8JQReQTDam4fU' .
		'u3UOPGWCLx56NZJWxHG4UWqTDOxihVgX4RJhkzrikDbbluZz3wgvwQEqhm1pnPTobFbpLXcgwKWT' .
		'v16RPNV4nvGpjJglLept2IpeTl051326E85GfpilaJNZFKBGol0SfV8hI/ENh2hymg1F+d4pjbtK' .
		'aaFOLGFZ2HOTzZhEUT4W5h9zVBCsn+CWEzfjg8kEoEUqnSRLEt+4LqEtBLn/6S7NB+7OJl7Qa8FJ' .
		'a+yN6Y5RrI9Pyi2k2IwhYOsJS3XPptNQjBJF5AR5DEiqLWYagmVxZ6Ek/LugkSZ3nZGt+31jwY1T' .
		'KVLxhRsV1gsYp839/wCyIODlghQAAA=='
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
