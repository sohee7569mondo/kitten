<?php
/* ═══════════════════════════════════════════════════════
   지금 값이 얼마로 잡혀 있나 — 진단   patch160_money
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   붙이신 뒤 주소창에 이렇게 여세요 —

       https://stellasaju.com/?stella_money=1

   왜 이것부터 만들었나
   체험판을 끄시기 전에 「끄면 손님이 무슨 값을 보게 되는가」를
   먼저 봐야 합니다. 제 사본에는 이렇게 적혀 있습니다 —

       STELLA_PRICE_BASE     5   ← 풀이 한 편
       STELLA_PRICE_ONELINE  5   ← 한 줄 질문
       STELLA_PRICE_DEEP     5   ← 심화 질문 한 개

   그런데 화면 글은 어디나 「3구슬 · 3,000원」이고, 가격 안내 쪽에는
   「한 줄 질문과 더 깊이 세 꼭지는 따로 값을 받지 않습니다」라고
   적혀 있습니다. 제 사본이 맞다면 체험판을 끄는 순간 손님은
   5,000원 — 한 줄 질문까지 적으면 10,000원을 보게 됩니다.

   제 사본은 낡았을 수 있습니다. 그래서 짐작하지 않고 봅니다.

   이 조각은 아무것도 바꾸지 않습니다. 읽기만 합니다.
   다 보시고 나면 꺼두셔도 됩니다.

   ★ 2026-09-14 · 비밀 열쇠를 가립니다
     처음 판은 STELLA 로 시작하는 설정을 전부 그대로 찍었습니다.
     그 바람에 포트원 비밀키가 화면에 통째로 나왔습니다. 이름에
     SECRET · KEY · TOKEN · PASS · PW · REST · CHANNEL · STORE · HOOK 이
     들어가면 앞 네 글자만 보이고 나머지는 ● 로 가립니다.
     진단 도구가 비밀을 흘리면 안 됩니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'template_redirect', function () {

	if ( ! isset( $_GET['stella_money'] ) ) { return; }

	$KRW = 1000;
	if ( defined( 'STELLA_ORB_KRW' ) ) { $KRW = (int) constant( 'STELLA_ORB_KRW' ); }
	if ( $KRW < 1 ) { $KRW = 1000; }

	$won = function ( $n ) use ( $KRW ) {
		return number_format( (int) $n * $KRW ) . '원';
	};

	nocache_headers();
	header( 'Content-Type: text/html; charset=utf-8' );

	echo '<!doctype html><meta charset="utf-8">';
	echo '<meta name="viewport" content="width=device-width,initial-scale=1">';
	echo '<title>지금 값이 얼마인가</title>';
	echo '<style>
body{margin:0;padding:26px 18px 80px;background:#F1EDE3;color:#221C33;
  font:16px/1.8 -apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;}
.w{max-width:760px;margin:0 auto;}
h1{font-size:1.4rem;margin:0 0 6px;}
.dek{color:#8B849C;font-size:.92rem;margin:0 0 24px;}
h2{font-size:1.06rem;margin:30px 0 10px;padding-top:18px;border-top:1px solid #E2DACB;}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #E2DACB;
  border-radius:9px;overflow:hidden;}
td,th{padding:11px 13px;border-bottom:1px solid #EFE9DC;text-align:left;
  font-size:.94rem;vertical-align:top;}
th{background:#FAF7F0;color:#8B849C;font-weight:600;font-size:.86rem;}
tr:last-child td{border-bottom:0;}
.k{font-family:"IBM Plex Mono",monospace;color:#4E4763;}
.v{font-family:"IBM Plex Mono",monospace;font-weight:700;}
.ok{color:#2F7D4A;}
.no{color:#C4453A;font-weight:700;}
.note{margin-top:10px;font-size:.9rem;color:#8B849C;line-height:1.75;}
.big{margin-top:14px;padding:16px 18px;border-radius:10px;
  background:#FBEFEE;border:1px solid #EBC7C3;color:#C4453A;font-weight:700;}
.big.fine{background:#EDF7F0;border-color:#BFE0C9;color:#2F7D4A;}
</style>';
	echo '<div class="w">';
	echo '<h1>지금 값이 얼마로 잡혀 있나</h1>';
	echo '<p class="dek">읽기만 합니다. 아무것도 바꾸지 않습니다.</p>';

	/* ── 읽는 부분은 통째로 감쌉니다. 여기서 멈춰도 위의 글은 남습니다 ── */
	try {

		/* ① 설정값 ------------------------------------------------- */
		echo '<h2>① 스니펫에 적힌 설정</h2>';
		echo '<table><tr><th>이름</th><th>지금 값</th><th>뜻</th></tr>';

		$all  = get_defined_constants();
		$mine = array();
		foreach ( $all as $k => $v ) {
			if ( 0 === strpos( $k, 'STELLA' ) ) { $mine[ $k ] = $v; }
		}
		ksort( $mine );

		$say = array(
			'STELLA_TRIAL'         => '체험판 — true 면 무엇을 열어도 0원입니다',
			'STELLA_WELCOME_ORBS'  => '가입하면 그냥 드리는 구슬',
			'STELLA_EVENT_ORBS'    => '오픈 기념으로 더 드리는 구슬',
			'STELLA_EVENT_UNTIL'   => '그 기념을 언제까지',
			'STELLA_PRICE_BASE'    => '풀이 한 편',
			'STELLA_PRICE_ONELINE' => '한 줄 질문 — 가격 안내 쪽엔 「값 안 받음」이라 적혀 있습니다',
			'STELLA_PRICE_DEEP'    => '심화 질문 한 개 — 위와 같습니다',
			'STELLA_PRICE_FULL'    => '인생길잡이 종합본 (아직 못 파는 것)',
			'STELLA_REF_ORBS'      => '친구 한 명 데려오면',
			'STELLA_ORB_TTL_DAYS'  => '드린 구슬이 살아 있는 날 수',
			'STELLA_ORB_KRW'       => '구슬 한 개가 몇 원인가',
		);

		if ( empty( $mine ) ) {
			echo '<tr><td colspan="3" class="no">★ STELLA 로 시작하는 설정이 하나도 없습니다 '
				. '— stella-signup 조각이 꺼져 있는 것 같습니다.</td></tr>';
		}
		/* ★ 비밀 열쇠는 절대로 찍지 않습니다 (2026-09-14 · 한 번 새어나갔습니다)
		   이름에 아래 낱말이 들어가면 앞 네 글자만 보이고 나머지는 가립니다. */
		$hide = array( 'SECRET', 'KEY', 'TOKEN', 'PASS', 'PW', 'REST', 'CHANNEL', 'STORE', 'HOOK' );

		foreach ( $mine as $k => $v ) {
			$show = $v;
			if ( true === $v )  { $show = 'true'; }
			if ( false === $v ) { $show = 'false'; }
			if ( '' === $v )    { $show = '(비어 있음)'; }

			$secret = false;
			foreach ( $hide as $w ) {
				if ( false !== strpos( $k, $w ) ) { $secret = true; }
			}
			if ( $secret ) {
				$t = (string) $v;
				if ( '' === $t ) {
					$show = '(비어 있음)';
				} else {
					$show = mb_substr( $t, 0, 4 ) . str_repeat( '●', 8 )
						. ' (' . mb_strlen( $t ) . '자 · 가렸습니다)';
				}
			}
			$d = isset( $say[ $k ] ) ? $say[ $k ] : '';
			echo '<tr><td class="k">' . esc_html( $k ) . '</td>'
				. '<td class="v">' . esc_html( (string) $show ) . '</td>'
				. '<td>' . esc_html( $d ) . '</td></tr>';
		}
		echo '</table>';

		/* ② 실제로 값을 세어 봅니다 ------------------------------- */
		echo '<h2>② 실제로 세어 본 값</h2>';

		if ( ! function_exists( 'stella_price' ) ) {
			echo '<p class="no">★ stella_price() 가 없습니다 — 값을 셀 수 없습니다.</p>';
		} else {
			$cases = array(
				'문 하나 · 주제 하나 (손님 대부분)' => array(
					'guardian' => '미르', 'guardian_slug' => 'door-fortune',
					'topic' => '2026년 운세', 'oneline' => '', 'memo' => '', 'deeps' => array(),
				),
				'거기에 한 줄 질문을 적으면' => array(
					'guardian' => '미르', 'guardian_slug' => 'door-fortune',
					'topic' => '2026년 운세', 'oneline' => '올해 이직해도 될까요',
					'memo' => '', 'deeps' => array(),
				),
				'거기에 더 깊이 두 꼭지까지' => array(
					'guardian' => '미르', 'guardian_slug' => 'door-fortune',
					'topic' => '2026년 운세', 'oneline' => '올해 이직해도 될까요',
					'memo' => '', 'deeps' => array( '가', '나' ),
				),
			);

			echo '<table><tr><th>손님이 고른 것</th><th>구슬</th><th>돈으로</th></tr>';
			$base = null;
			foreach ( $cases as $name => $body ) {
				$o = function_exists( 'stella_clean_order' )
					? stella_clean_order( $body )
					: $body;
				$p = (int) stella_price( $o );
				if ( null === $base ) { $base = $p; }
				echo '<tr><td>' . esc_html( $name ) . '</td>'
					. '<td class="v">' . $p . '개</td>'
					. '<td class="v">' . esc_html( $won( $p ) ) . '</td></tr>';
			}
			echo '</table>';

			/* ③ 화면 글과 맞나 ---------------------------------
			   체험판이면 stella_price() 가 무조건 0 이라 견줄 것이 없습니다.
			   그때는 설정값(STELLA_PRICE_BASE)으로 견줍니다 — 체험판을
			   끈 뒤에 손님이 보게 될 값이 그것이기 때문입니다. */
			if ( defined( 'STELLA_TRIAL' ) ) {
				if ( constant( 'STELLA_TRIAL' ) ) {
					$base = defined( 'STELLA_PRICE_BASE' )
						? (int) constant( 'STELLA_PRICE_BASE' ) : 0;
				}
			}
			echo '<h2>③ 화면에 적힌 글과 맞나</h2>';
			if ( defined( 'STELLA_TRIAL' ) ) {
				if ( constant( 'STELLA_TRIAL' ) ) {
					echo '<p class="note">체험판일 때는 설정값(STELLA_PRICE_BASE)으로 견줍니다 '
						. '— 체험판을 끈 뒤에 손님이 보게 될 값이 그것이라서요.</p>';
				}
			}
			echo '<table><tr><th>어디</th><th>그 쪽에 적힌 값</th><th>실제</th><th></th></tr>';

			$where = array(
				'가격 안내 (/price/)'   => 3,
				'로그인 쪽 (/login/)'   => 3,
				'문 여섯 쪽 · 결제창'   => 3,
			);
			$bad = false;
			foreach ( $where as $w => $claim ) {
				$same = ( (int) $claim === (int) $base );
				if ( ! $same ) { $bad = true; }
				echo '<tr><td>' . esc_html( $w ) . '</td>'
					. '<td class="v">' . $claim . '구슬 · ' . esc_html( $won( $claim ) ) . '</td>'
					. '<td class="v">' . $base . '구슬 · ' . esc_html( $won( $base ) ) . '</td>'
					. '<td class="' . ( $same ? 'ok' : 'no' ) . '">'
					. ( $same ? '맞습니다' : '★ 다릅니다' ) . '</td></tr>';
			}
			echo '</table>';

			$trial = defined( 'STELLA_TRIAL' ) ? (bool) constant( 'STELLA_TRIAL' ) : false;
			if ( $trial ) {
				echo '<div class="big">지금은 체험판이라 무엇을 열어도 0원입니다. '
					. '결제창이 뜨지 않습니다 — 심사에서 결제 화면을 보여드릴 수 없습니다.</div>';
				echo '<p class="note">위 ②의 값은 체험판을 끈 뒤에 손님이 보게 될 값입니다. '
					. 'stella_price() 가 체험판일 때 0 을 돌려주므로, 여기서는 설정값으로 '
					. '직접 세어 보여드립니다.</p>';
			}
			if ( $bad ) {
				echo '<div class="big">★ 화면 글과 실제 값이 다릅니다. '
					. '체험판을 끄기 전에 설정값을 먼저 맞춰야 합니다.</div>';
			} else {
				echo '<div class="big fine">화면 글과 실제 값이 같습니다.</div>';
			}
		}

		/* ④ 체험판일 때는 설정값으로 손수 세어 봅니다 ------------- */
		if ( defined( 'STELLA_TRIAL' ) ) {
			if ( constant( 'STELLA_TRIAL' ) ) {
				echo '<h2>④ 체험판을 끄면 이렇게 됩니다</h2>';
				$b  = defined( 'STELLA_PRICE_BASE' ) ? (int) constant( 'STELLA_PRICE_BASE' ) : 0;
				$o1 = defined( 'STELLA_PRICE_ONELINE' ) ? (int) constant( 'STELLA_PRICE_ONELINE' ) : 0;
				$dp = defined( 'STELLA_PRICE_DEEP' ) ? (int) constant( 'STELLA_PRICE_DEEP' ) : 0;
				echo '<table><tr><th>손님이 고른 것</th><th>구슬</th><th>돈으로</th></tr>';
				$rows = array(
					'문 하나 · 주제 하나'        => $b,
					'거기에 한 줄 질문'          => $b + $o1,
					'거기에 더 깊이 두 꼭지까지' => $b + $o1 + ( $dp * 2 ),
				);
				foreach ( $rows as $n => $p ) {
					echo '<tr><td>' . esc_html( $n ) . '</td>'
						. '<td class="v">' . $p . '개</td>'
						. '<td class="v">' . esc_html( $won( $p ) ) . '</td></tr>';
				}
				echo '</table>';
				if ( 3 !== (int) $b ) {
					echo '<div class="big">★ 풀이 한 편이 ' . $b . '구슬('
						. esc_html( $won( $b ) ) . ')로 잡혀 있습니다. '
						. '화면 글은 어디나 3구슬 · 3,000원입니다.</div>';
				}
				if ( $o1 > 0 ) {
					echo '<div class="big">★ 한 줄 질문에 ' . $o1 . '구슬을 더 받습니다. '
						. '가격 안내 쪽에는 「따로 값을 받지 않습니다」라고 적혀 있습니다.</div>';
				}
				if ( $dp > 0 ) {
					echo '<div class="big">★ 더 깊이 한 꼭지마다 ' . $dp . '구슬을 더 받습니다. '
						. '가격 안내 쪽에는 「따로 값을 받지 않습니다」라고 적혀 있습니다.</div>';
				}
			}
		}

		/* ⑤ 지금 들어와 계신 분 ---------------------------------- */
		echo '<h2>⑤ 지금 이 화면을 보시는 분</h2>';
		echo '<table>';
		if ( is_user_logged_in() ) {
			$uid = get_current_user_id();
			$u   = get_userdata( $uid );
			echo '<tr><td>들어와 계신가</td><td class="v ok">예</td></tr>';
			echo '<tr><td>이메일</td><td class="v">' . esc_html( $u ? $u->user_email : '' ) . '</td></tr>';
			if ( function_exists( 'stella_orb_balance' ) ) {
				echo '<tr><td>가지고 계신 구슬</td><td class="v">'
					. (int) stella_orb_balance( $uid ) . '개</td></tr>';
			} else {
				echo '<tr><td>가지고 계신 구슬</td><td class="no">stella_orb_balance() 가 없습니다</td></tr>';
			}
		} else {
			echo '<tr><td>들어와 계신가</td><td class="v">아니요 (손님으로 보고 계십니다)</td></tr>';
		}
		echo '</table>';

		/* ⑥ 있어야 할 함수들 ------------------------------------- */
		echo '<h2>⑥ 있어야 할 것들</h2>';
		echo '<table><tr><th>이름</th><th></th></tr>';
		$fns = array(
			'stella_price', 'stella_clean_order', 'stella_place_order',
			'stella_orb_add', 'stella_orb_spend', 'stella_orb_balance',
		);
		foreach ( $fns as $f ) {
			$has = function_exists( $f );
			echo '<tr><td class="k">' . esc_html( $f ) . '()</td>'
				. '<td class="' . ( $has ? 'ok' : 'no' ) . '">'
				. ( $has ? '있습니다' : '★ 없습니다' ) . '</td></tr>';
		}
		echo '</table>';

	} catch ( Throwable $e ) {
		echo '<div class="big">★ 읽다가 멈췄습니다 — ' . esc_html( $e->getMessage() )
			. ' (' . esc_html( basename( $e->getFile() ) ) . ' ' . (int) $e->getLine() . '줄)</div>';
	}

	echo '<p class="note">이 조각은 patch160_money 입니다. '
		. '다 보시고 나면 꺼두셔도 됩니다.</p>';
	echo '</div>';
	exit;
}, 1 );
