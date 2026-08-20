<?php
/**
 * STELLA SAJU — 회원가입 + 구슬(잔액) 엔진
 * ------------------------------------------------------------------
 * 넣는 곳 : WPCode  →  + Add Snippet  →  Add Your Custom Code
 *            Code Type = PHP Snippet / Location = Run Everywhere / Active
 *            (여는 <?php 태그는 빼고 붙여넣으세요)
 *
 * 하는 일
 *   1) /wp-json/stella/v1/signup  으로 들어온 첫 방문자를 실제로 회원가입시킵니다.
 *   2) 생년월일시·출생지를 회원 정보에 저장합니다 (다음부터 자동 입력).
 *   3) 구슬을 "충전 묶음" 단위로 관리합니다 — 각 묶음은 충전일로부터 1년간 유효.
 *   4) 매일 한 번 만료된 구슬을 정리하고, 잔액이 10개 미만이면 안내 메일을 보냅니다.
 *   5) 로그인한 회원 화면에 window.STELLA_USER 를 심어 폼이 자동으로 채워지게 합니다.
 * ------------------------------------------------------------------
 */

/* ===== 설정 — 여기만 고치면 됩니다 =============================== */
define( 'STELLA_ORB_TTL_DAYS',   365 );  // 구슬 유효기간 (일)
define( 'STELLA_LOW_ORB_LIMIT',  10  );  // 이 개수 미만이면 안내 메일
define( 'STELLA_LOW_MAIL_GAP',   30  );  // 같은 사람에게 다시 보내기까지 최소 일수
define( 'STELLA_WELCOME_ORBS',   0   );  // 가입 축하 구슬 (0 이면 안 줌)
/* ================================================================ */


/* ---------------------------------------------------------------
 * 1. 구슬 장부
 *    사용자 메타 stella_orb_lots 에 묶음 배열로 저장합니다.
 *    한 묶음 = array( 'left' => 남은개수, 'at' => 충전시각, 'exp' => 만료시각, 'why' => 사유 )
 * --------------------------------------------------------------- */

function stella_orb_lots( $uid ) {
	$lots = get_user_meta( $uid, 'stella_orb_lots', true );
	return is_array( $lots ) ? $lots : array();
}

function stella_orb_save_lots( $uid, $lots ) {
	update_user_meta( $uid, 'stella_orb_lots', array_values( $lots ) );
}

/** 만료된 묶음을 걷어냅니다. 걷어낸 개수를 돌려줍니다. */
function stella_orb_prune( $uid ) {
	$now     = time();
	$lots    = stella_orb_lots( $uid );
	$dropped = 0;
	$keep    = array();

	foreach ( $lots as $lot ) {
		if ( empty( $lot['left'] ) ) {
			continue;                       // 다 쓴 묶음은 버립니다
		}
		if ( $lot['exp'] <= $now ) {
			$dropped += (int) $lot['left']; // 기간이 지난 묶음
			continue;
		}
		$keep[] = $lot;
	}

	if ( count( $keep ) !== count( $lots ) ) {
		stella_orb_save_lots( $uid, $keep );
	}
	return $dropped;
}

/** 지금 쓸 수 있는 구슬 개수 */
function stella_orb_balance( $uid ) {
	stella_orb_prune( $uid );
	$sum = 0;
	foreach ( stella_orb_lots( $uid ) as $lot ) {
		$sum += (int) $lot['left'];
	}
	return $sum;
}

/** 가장 먼저 만료되는 묶음의 만료일 (없으면 0) */
function stella_orb_next_expiry( $uid ) {
	$exp = 0;
	foreach ( stella_orb_lots( $uid ) as $lot ) {
		if ( ! $exp || $lot['exp'] < $exp ) {
			$exp = (int) $lot['exp'];
		}
	}
	return $exp;
}

/** 구슬 충전 — 오늘부터 1년짜리 묶음 하나가 생깁니다. */
function stella_orb_add( $uid, $n, $why = '' ) {
	$n = (int) $n;
	if ( $n <= 0 ) {
		return stella_orb_balance( $uid );
	}
	$lots   = stella_orb_lots( $uid );
	$lots[] = array(
		'left' => $n,
		'at'   => time(),
		'exp'  => time() + ( STELLA_ORB_TTL_DAYS * DAY_IN_SECONDS ),
		'why'  => sanitize_text_field( $why ),
	);
	stella_orb_save_lots( $uid, $lots );

	// 충전했으니 "잔액 부족" 알림 기록을 지웁니다.
	delete_user_meta( $uid, 'stella_low_mailed_at' );

	return stella_orb_balance( $uid );
}

/**
 * 구슬 사용 — 먼저 만료되는 묶음부터 씁니다 (선입선출).
 * 잔액이 모자라면 false 를 돌려주고 아무것도 차감하지 않습니다.
 */
function stella_orb_spend( $uid, $n, $why = '' ) {
	$n = (int) $n;
	if ( $n <= 0 ) {
		return true;
	}
	if ( stella_orb_balance( $uid ) < $n ) {
		return false;
	}

	$lots = stella_orb_lots( $uid );
	usort( $lots, function ( $a, $b ) {
		return $a['exp'] - $b['exp'];      // 먼저 사라질 것부터
	} );

	$need = $n;
	foreach ( $lots as $i => $lot ) {
		if ( $need <= 0 ) {
			break;
		}
		$take            = min( $need, (int) $lot['left'] );
		$lots[ $i ]['left'] = (int) $lot['left'] - $take;
		$need           -= $take;
	}
	stella_orb_save_lots( $uid, $lots );

	// 사용 내역 남기기 (최근 100건)
	$log   = get_user_meta( $uid, 'stella_orb_log', true );
	$log   = is_array( $log ) ? $log : array();
	$log[] = array( 'n' => -$n, 'at' => time(), 'why' => sanitize_text_field( $why ) );
	update_user_meta( $uid, 'stella_orb_log', array_slice( $log, -100 ) );

	// 쓰고 나서 잔액이 적으면 바로 안내
	stella_orb_maybe_warn( $uid );

	return true;
}


/* ---------------------------------------------------------------
 * 2. 잔액 부족 안내 메일
 * --------------------------------------------------------------- */

function stella_orb_maybe_warn( $uid ) {
	$balance = stella_orb_balance( $uid );
	if ( $balance >= STELLA_LOW_ORB_LIMIT ) {
		return false;
	}

	$last = (int) get_user_meta( $uid, 'stella_low_mailed_at', true );
	if ( $last && ( time() - $last ) < ( STELLA_LOW_MAIL_GAP * DAY_IN_SECONDS ) ) {
		return false;                      // 너무 자주 보내지 않기
	}

	$user = get_userdata( $uid );
	if ( ! $user || ! is_email( $user->user_email ) ) {
		return false;
	}

	$name = get_user_meta( $uid, 'stella_name', true );
	$name = $name ? $name : $user->display_name;
	$exp  = stella_orb_next_expiry( $uid );

	$subject = '[스텔라사주] 남은 구슬이 ' . $balance . '개예요';

	$lines   = array();
	$lines[] = $name . '님, 안녕하세요.';
	$lines[] = '';
	$lines[] = '명성의 신이 잠깐 들렀습니다. 지금 남으신 구슬이 ' . $balance . '개예요.';
	if ( $balance > 0 && $exp ) {
		$lines[] = '이 구슬은 ' . wp_date( 'Y년 n월 j일', $exp ) . '까지 쓰실 수 있어요.';
	}
	$lines[] = '';
	$lines[] = '여섯 개의 문 중 아직 열어보지 않으신 문이 있다면,';
	$lines[] = '구슬을 채우고 다시 찾아와 주세요.';
	$lines[] = '';
	$lines[] = '구슬 충전하기 : ' . home_url( '/mypage/' );
	$lines[] = '';
	$lines[] = '— 스텔라사주';

	$sent = wp_mail( $user->user_email, $subject, implode( "\n", $lines ) );
	update_user_meta( $uid, 'stella_low_mailed_at', time() );

	return $sent;
}


/* ---------------------------------------------------------------
 * 3. 하루 한 번 — 만료 정리 + 잔액 안내
 * --------------------------------------------------------------- */

add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'stella_daily_orbs' ) ) {
		wp_schedule_event( time() + 300, 'daily', 'stella_daily_orbs' );
	}
} );

add_action( 'stella_daily_orbs', function () {
	$users = get_users( array(
		'meta_key' => 'stella_orb_lots',
		'fields'   => 'ID',
		'number'   => 500,
	) );

	foreach ( $users as $uid ) {
		$dropped = stella_orb_prune( $uid );

		if ( $dropped > 0 ) {
			$user = get_userdata( $uid );
			if ( $user && is_email( $user->user_email ) ) {
				wp_mail(
					$user->user_email,
					'[스텔라사주] 구슬 ' . $dropped . '개의 기한이 지났어요',
					"안녕하세요.\n\n" .
					"1년이 지나 구슬 " . $dropped . "개가 사라졌습니다.\n" .
					"지금 남으신 구슬은 " . stella_orb_balance( $uid ) . "개예요.\n\n" .
					home_url( '/mypage/' ) . "\n\n— 스텔라사주"
				);
			}
		}

		stella_orb_maybe_warn( $uid );
	}
} );


/* ---------------------------------------------------------------
 * 4. 회원가입 REST 엔드포인트
 * --------------------------------------------------------------- */

add_action( 'rest_api_init', function () {
	register_rest_route( 'stella/v1', '/signup', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => 'stella_rest_signup',
	) );
} );

function stella_rest_signup( WP_REST_Request $req ) {

	/* 너무 잦은 요청 막기 — 같은 아이피는 1분에 5번까지 */
	$ip  = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '0';
	$key = 'stella_su_' . md5( $ip );
	$hit = (int) get_transient( $key );
	if ( $hit >= 5 ) {
		return new WP_Error( 'stella_slow', '요청이 너무 잦습니다. 잠시 후 다시 시도해주세요.', array( 'status' => 429 ) );
	}
	set_transient( $key, $hit + 1, MINUTE_IN_SECONDS );

	$body    = $req->get_json_params();
	$profile = isset( $body['profile'] ) ? $body['profile'] : array();

	$email = isset( $profile['email'] ) ? sanitize_email( $profile['email'] ) : '';
	$name  = isset( $profile['name'] )  ? sanitize_text_field( $profile['name'] ) : '';

	if ( ! is_email( $email ) ) {
		return new WP_Error( 'stella_email', '이메일을 정확히 적어주세요.', array( 'status' => 400 ) );
	}
	if ( $name === '' ) {
		return new WP_Error( 'stella_name', '이름을 적어주세요.', array( 'status' => 400 ) );
	}

	$y = isset( $profile['year'] )  ? (int) $profile['year']  : 0;
	$m = isset( $profile['month'] ) ? (int) $profile['month'] : 0;
	$d = isset( $profile['day'] )   ? (int) $profile['day']   : 0;

	if ( $y < 1900 || $y > 2049 || $m < 1 || $m > 12 || $d < 1 || $d > 31 ) {
		return new WP_Error( 'stella_birth', '생년월일을 다시 확인해주세요.', array( 'status' => 400 ) );
	}

	/* 이미 가입된 이메일이면 새로 만들지 않습니다 */
	$existing = get_user_by( 'email', $email );
	if ( $existing ) {
		if ( ! is_user_logged_in() ) {
			return new WP_Error(
				'stella_exists',
				'이미 가입된 이메일이에요. 로그인 후 이용해주세요.',
				array( 'status' => 409 )
			);
		}
		$uid = $existing->ID;
	} else {
		$login = stella_unique_login( $email );
		$pass  = wp_generate_password( 16, true, false );
		$uid   = wp_insert_user( array(
			'user_login'   => $login,
			'user_email'   => $email,
			'user_pass'    => $pass,
			'display_name' => $name,
			'first_name'   => $name,
			'role'         => 'subscriber',
		) );
		if ( is_wp_error( $uid ) ) {
			return new WP_Error( 'stella_create', '가입 처리 중 문제가 생겼어요.', array( 'status' => 500 ) );
		}

		if ( STELLA_WELCOME_ORBS > 0 ) {
			stella_orb_add( $uid, STELLA_WELCOME_ORBS, '가입 축하' );
		}
		stella_send_welcome( $uid, $name );
	}

	/* 사주 정보 저장 */
	stella_save_profile( $uid, $profile );

	/* 주문 내용 임시 보관 — 결제 붙이면 여기서 이어집니다 */
	$order = array(
		'guardian' => isset( $body['guardian'] ) ? sanitize_text_field( $body['guardian'] ) : '',
		'slug'     => isset( $body['guardian_slug'] ) ? sanitize_title( $body['guardian_slug'] ) : '',
		'topic'    => isset( $body['topic'] ) ? sanitize_text_field( $body['topic'] ) : '',
		'oneline'  => isset( $body['oneline'] ) ? mb_substr( sanitize_text_field( $body['oneline'] ), 0, 30 ) : '',
		'memo'     => isset( $body['memo'] ) ? mb_substr( sanitize_textarea_field( $body['memo'] ), 0, 200 ) : '',
		'deeps'    => isset( $body['deeps'] ) ? array_map( 'sanitize_text_field', (array) $body['deeps'] ) : array(),
		'orbs'     => isset( $body['orbs'] ) ? (int) $body['orbs'] : 0,
		'at'       => time(),
		'status'   => 'pending',
	);
	$orders   = get_user_meta( $uid, 'stella_orders', true );
	$orders   = is_array( $orders ) ? $orders : array();
	$orders[] = $order;
	update_user_meta( $uid, 'stella_orders', array_slice( $orders, -50 ) );

	/* 바로 로그인 */
	wp_clear_auth_cookie();
	wp_set_current_user( $uid );
	wp_set_auth_cookie( $uid, true );

	return rest_ensure_response( array(
		'ok'      => true,
		'user_id' => $uid,
		'balance' => stella_orb_balance( $uid ),
		'needed'  => $order['orbs'],
		'next'    => home_url( '/mypage/?order=new' ),
	) );
}

function stella_unique_login( $email ) {
	$base  = sanitize_user( current( explode( '@', $email ) ), true );
	$base  = $base ? $base : 'stella';
	$login = $base;
	$i     = 2;
	while ( username_exists( $login ) ) {
		$login = $base . $i;
		$i++;
	}
	return $login;
}

function stella_save_profile( $uid, $profile ) {
	$hour = isset( $profile['hour'] ) && $profile['hour'] !== null ? (int) $profile['hour'] : -1;

	update_user_meta( $uid, 'stella_name',     sanitize_text_field( $profile['name'] ) );
	update_user_meta( $uid, 'stella_year',     (int) $profile['year'] );
	update_user_meta( $uid, 'stella_month',    (int) $profile['month'] );
	update_user_meta( $uid, 'stella_day',      (int) $profile['day'] );
	update_user_meta( $uid, 'stella_hour',     $hour );                 // -1 = 시간 모름
	update_user_meta( $uid, 'stella_calendar', ( isset( $profile['calendar'] ) && $profile['calendar'] === 'lunar' ) ? 'lunar' : 'solar' );
	update_user_meta( $uid, 'stella_leap',     ! empty( $profile['leap'] ) ? 1 : 0 );
	update_user_meta( $uid, 'stella_country',  isset( $profile['country'] ) ? sanitize_text_field( $profile['country'] ) : '' );
	update_user_meta( $uid, 'stella_city',     isset( $profile['city'] ) ? sanitize_text_field( $profile['city'] ) : '' );
}

function stella_send_welcome( $uid, $name ) {
	$user = get_userdata( $uid );
	if ( ! $user ) {
		return;
	}
	$key  = get_password_reset_key( $user );
	$link = is_wp_error( $key )
		? wp_login_url()
		: network_site_url( 'wp-login.php?action=rp&key=' . $key . '&login=' . rawurlencode( $user->user_login ), 'login' );

	$lines   = array();
	$lines[] = $name . '님, 스텔라사주에 오신 것을 환영합니다.';
	$lines[] = '';
	$lines[] = '알려주신 생년월일시는 안전하게 보관했어요.';
	$lines[] = '다음부터는 다시 적지 않으셔도 여섯 개의 문을 열어보실 수 있습니다.';
	$lines[] = '';
	$lines[] = '아래 주소에서 비밀번호를 정해주세요.';
	$lines[] = $link;
	$lines[] = '';
	$lines[] = '로그인 아이디 : ' . $user->user_login;
	$lines[] = '';
	$lines[] = '— 명성의 신 드림';

	wp_mail( $user->user_email, '[스텔라사주] 가입을 환영합니다', implode( "\n", $lines ) );
}


/* ---------------------------------------------------------------
 * 5. 로그인한 회원 화면에 정보 심어주기
 *    가디언 페이지의 window.STELLA_USER 가 이걸 읽습니다.
 * --------------------------------------------------------------- */

add_action( 'wp_head', function () {
	if ( ! is_user_logged_in() ) {
		return;
	}
	$uid  = get_current_user_id();
	$y    = (int) get_user_meta( $uid, 'stella_year', true );
	if ( ! $y ) {
		return;                                  // 아직 사주 정보가 없는 회원
	}

	$hour   = (int) get_user_meta( $uid, 'stella_hour', true );
	$hours  = array( '자시', '축시', '인시', '묘시', '진시', '사시', '오시', '미시', '신시', '유시', '술시', '해시' );
	$hourKr = ( $hour >= 0 && $hour < 12 ) ? $hours[ $hour ] : '시간 모름';
	$cal    = get_user_meta( $uid, 'stella_calendar', true ) === 'lunar' ? '음력' : '양력';
	$leap   = get_user_meta( $uid, 'stella_leap', true ) ? ' 윤달' : '';

	$data = array(
		'name'    => (string) get_user_meta( $uid, 'stella_name', true ),
		'birth'   => sprintf(
			'%s %d년 %d월 %d일%s · %s',
			$cal,
			$y,
			(int) get_user_meta( $uid, 'stella_month', true ),
			(int) get_user_meta( $uid, 'stella_day', true ),
			$leap,
			$hourKr
		),
		'place'   => trim( get_user_meta( $uid, 'stella_country', true ) . ' ' . get_user_meta( $uid, 'stella_city', true ) ),
		'balance' => stella_orb_balance( $uid ),
		'expires' => stella_orb_next_expiry( $uid ) ? wp_date( 'Y-m-d', stella_orb_next_expiry( $uid ) ) : '',
	);

	echo '<script>window.STELLA_USER=' . wp_json_encode( $data ) . ';</script>' . "\n";
}, 5 );
