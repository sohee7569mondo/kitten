<?php
/**
 * STELLA SAJU — 페이지 160 · 2부 저울 다섯 개 주제별로 갈라놓기   PATCH: AXIS-TOPIC-1
 * ------------------------------------------------------------------
 * 한 번만 돌리는 스니펫입니다. 돌린 뒤에는 반드시 지우세요.
 *
 * [무엇을 고치나]
 *   연성의 신 전자책 2부 「어긋나는 자리」의 저울 다섯 개(혼자·실물·하나·안정·정답)가
 *   결혼운·연애운·재회운·이별운·짝사랑 어느 것을 골라도 똑같은 문장을 냈습니다.
 *   메인 엔진 안쪽 지역변수 AXIS_WARM 이 가디언 단위로만 갈라져 있고
 *   주제(topic)를 아예 안 보기 때문입니다.
 *
 * [어떻게 고치나]
 *   메인 엔진(페이지160 섹션 index 10) 본문 두 군데만 건드립니다.
 *     1) function gapBlock(key, title){ 바로 앞에 AXIS_WARM_TOPIC 표를 끼워넣습니다
 *     2) W 를 찾는 두 줄을 "주제 먼저 보고, 없으면 예전대로" 로 바꿉니다
 *   나머지 25만 자는 한 글자도 건드리지 않습니다.
 *
 * 넣는 곳 : WPCode → + Add Snippet → Add Your Custom Code
 *           Code Type = PHP Snippet / Location = Run Everywhere / Active
 *           (맨 윗줄 <?php 은 빼고 붙여넣으세요)
 *
 * 돌리는 법 :
 *   1) 저장하고 Active 로 켠 다음, 관리자로 로그인한 채 아래를 엽니다
 *        미리보기 (아무것도 안 고침) : https://stellasaju.com/wp-admin/?stella_patch=dry
 *        진짜로 고치기               : https://stellasaju.com/wp-admin/?stella_patch=go
 *        되돌리기                    : https://stellasaju.com/wp-admin/?stella_patch=undo
 *   2) 화면 위쪽에 결과가 뜹니다
 *   3) 확인했으면 WPCode 에서 이 스니펫을 지웁니다
 *   4) 호스팅 → 성능 → 캐시 비우기
 *
 * [왜 wp_update_post 를 안 쓰나]
 *   워드프레스가 kses 로 <script> 를 통째로 지웁니다. 페이지 160 은 거의 전부가
 *   <script> 라 그러면 전자책이 죽습니다. 그래서 $wpdb 로 직접 씁니다.
 * ------------------------------------------------------------------
 */

defined( 'STELLA_AXIS_PAGE' ) || define( 'STELLA_AXIS_PAGE', 160 );
defined( 'STELLA_AXIS_KEY' )  || define( 'STELLA_AXIS_KEY',  'axis_topic_1' );

/* 이미 들어가 있으면 다시 하지 않게 하는 표시 */
defined( 'STELLA_AXIS_STAMP' ) || define( 'STELLA_AXIS_STAMP', 'AXIS_WARM_TOPIC' );


/* ===== 끼워넣을 JS ============================================== */
$STELLA_AXIS_TABLE = <<<'JS'
  /* ═══ AXIS_WARM_TOPIC (2026-08-30) ═══════════════════════════════
     2부 저울 다섯 개가 주제를 안 보고 가디언 공용 문구만 쓰던 문제를 고칩니다.
     door-love 의 다섯 주제마다 저울(solo·form·many·risk·make) 본문을 따로 씁니다.
     여는 문장("사주는 OO 쪽으로 기울어 있습니다 — a 대 b.")은 gapBlock 이 붙이므로
     여기엔 넣지 않습니다. 없는 조합은 AXIS_WARM[slug] 로 자동 폴백합니다. */
  var AXIS_WARM_TOPIC = {
    '결혼운': {
      solo: { '함께': { what: '혼자 참고 견디기보다, 사람과 부딪히고 이야기하면서 풀어가는 쪽이 조금 더 편한 분이에요. 부부싸움 뒤에도 혼자 방에 들어가 삭이기보다, 어떻게든 그 자리에서 풀고 넘어가는 쪽이 당신에게는 더 편합니다. 화해 없이 며칠을 같은 집에서 냉랭하게 지내는 시간이 생각보다 많이 지치실 거예요. 꼭 큰 대화를 해야 한다는 뜻은 아니에요. 「나는 이게 조금 서운했어」 하고 마음을 조금씩 꺼내놓는 것만으로도 충분합니다.' } },
      form: { '무형': { what: '생활비를 벌어오고 살림을 하는 것만큼이나, 서로 마음을 말로 확인하는 것이 당신에게는 중요합니다. 아무리 살림을 잘 꾸려도 말 한마디가 없으면 「나만 애쓰나」 싶은 생각이 들 수 있어요. 꼭 거창하게 표현할 필요는 없어요. 「고마워」 「네가 있어서 좋아」 이런 짧은 말 한마디가 생각보다 큰 힘이 됩니다.' } },
      many: { '여럿': { what: '결혼생활 하나에 모든 의미를 두기보다, 일이나 취미처럼 마음이 향할 다른 곳이 있을 때 관계도 오히려 더 편안해지는 쪽입니다. 배우자에게 모든 걸 걸지 않는 게 오히려 결혼을 오래가게 합니다. 마음이 향할 수 있는 곳이 여러 군데 있을수록 결혼생활에서도 조금 더 여유를 가질 수 있어요.' } },
      risk: { flat: '안정적이고 편안한 결혼생활도, 가끔은 신선한 자극이 있는 결혼생활도 둘 다 받아들일 수 있는 분이에요. 너무 오래 똑같기만 한 일상보다는, 가끔 작은 변화가 섞여 있을 때 관계가 더 오래 생기 있게 유지됩니다.' },
      make: { '정답': { what: '남들처럼 무난하게 흘러가는 결혼생활, 검증된 방식에 마음이 편한 분이에요. 굳이 남들과 다른 방식을 무리해서 만들기보다, 기본적인 틀 안에서 두 분만의 색을 조금씩 더해가는 쪽이 당신에게는 더 잘 맞습니다.' } }
    },
    '연애운': {
      solo: { '함께': { what: '혼자 참고 견디기보다, 사람과 부딪히고 이야기하면서 풀어가는 쪽이 조금 더 편한 분이에요. 마음이 상했을 때 아무 말 없이 혼자 삭이는 시간이 길어지면, 생각보다 마음이 많이 지칠 수 있습니다. 꼭 큰 대화를 해야 한다는 뜻은 아니에요. 「나는 이게 조금 서운했어」 하고 마음을 조금씩 꺼내놓는 것만으로도 충분합니다.' } },
      form: { '무형': { what: '무언가를 챙겨주는 것만큼이나, 마음을 표현하고 서로의 마음을 확인하는 것이 중요한 분이에요. 아무리 많은 것을 해주더라도 그 마음이 말로 전달되지 않으면, 서로의 마음을 충분히 느끼지 못할 수 있어요. 꼭 거창하게 표현할 필요는 없어요. 「고마워」 「보고 싶었어」 이런 짧은 말 한마디가 생각보다 큰 힘이 됩니다.' } },
      many: { '여럿': { what: '한 가지에만 마음을 오래 집중하기보다, 관심과 마음의 방향을 여러 영역으로 나누어 둘 때 조금 더 편안한 성향이에요. 사람이 아니어도 괜찮아요. 일일 수도 있고, 취미일 수도 있습니다. 마음이 향할 수 있는 곳이 여러 군데 있을수록 한 사람과의 관계에서도 조금 더 여유를 가질 수 있어요.' } },
      risk: { flat: '편안함과 긴장감, 어느 한쪽만을 원하는 성향이라기보다 두 가지 관계의 온도를 모두 받아들일 수 있는 자리예요. 지금 관계의 상황과 서로의 상태에 따라 필요한 온도가 달라질 수 있는 사람에 가깝습니다.' },
      make: { '정답': { what: '이미 많은 사람들이 선택해왔거나, 어느 정도 검증된 방식과 분명한 기준이 있을 때 마음이 편한 분이에요. 관계에서도 서로가 지켜야 할 기본적인 약속과 신뢰가 분명할 때 안정감을 느끼기 쉽습니다.' } }
    },
    '재회운': {
      solo: { '함께': { what: '헤어진 이유를 혼자 곱씹기보다, 만나서든 연락해서든 직접 이야기로 풀고 싶은 쪽입니다. 아무 설명도 없이 끝난 관계일수록 오래 마음에 남으실 거예요. 다시 만난다면 그때 못다 한 이야기부터 짚고 넘어가는 편이 당신에게는 훨씬 편합니다.' } },
      form: { '무형': { what: '예전 관계에서 물질적으로는 부족함이 없었어도, 마음을 확인하는 말이 부족했다면 그게 헤어짐의 진짜 이유였을 가능성이 있습니다. 다시 만난다면 그 부분부터 채워야 오래갑니다. 「고마워」 「네가 필요해」 같은 말을 아끼지 마세요.' } },
      many: { '여럿': { what: '헤어진 뒤 그 사람 생각만 붙잡고 있기보다, 다른 데로 마음을 돌릴 자리가 있어야 오히려 회복이 빠른 쪽입니다. 다시 만나더라도 그 사람 하나에만 몰두하지 않는 편이 당신에게는 더 건강합니다.' } },
      risk: { flat: '다시 만난다면 예전처럼 편안한 관계로 돌아가고 싶은 마음과, 뭔가는 달라져야 한다는 마음이 함께 있는 쪽이에요. 둘 다 맞습니다 — 편안함은 그대로 가져가되, 예전과 똑같은 방식만 반복하지 않는 게 중요합니다.' },
      make: { '정답': { what: '다시 만난다면 예전과 완전히 다른 새로운 방식보다, 검증된 안정적인 방식으로 관계를 다시 쌓고 싶은 쪽이에요. 급격한 변화보다는 익숙한 기반 위에서 천천히 다시 신뢰를 쌓는 게 당신에게 맞습니다.' } }
    },
    '이별운': {
      solo: { '함께': { what: '말없이 조용히 정리되는 이별보다, 어떤 식으로든 서로 이야기를 나누고 끝내는 쪽이 당신에게는 덜 힘듭니다. 아무 말 없이 연락이 끊기는 이별이 유난히 오래가는 상처가 됩니다.' } },
      form: { '무형': { what: '헤어짐이 아쉬운 건 물질적으로 못 받은 게 아니라, 마음을 확인할 말이 부족했기 때문일 가능성이 큽니다. 「그 사람이 나한테 뭘 해줬나」보다 「그 사람이 나한테 뭐라고 말해줬나」가 더 오래 남으실 거예요.' } },
      many: { '여럿': { what: '이별 후 그 사람 생각에만 갇혀 있기보다, 마음을 나눠 쓸 다른 곳이 있어야 조금씩 회복되는 쪽입니다. 일이든 취미든 마음 둘 곳을 하나 만들어두시면 이 시기가 덜 힘드실 거예요.' } },
      risk: { flat: '이 관계가 너무 편안해서 안주하고 있었는지, 아니면 계속되는 긴장에 지쳐 있었는지 — 둘 다 이별의 이유가 될 수 있는 쪽이에요. 어느 쪽이었는지 돌아보면 다음 관계에서 무엇을 다르게 할지가 보입니다.' },
      make: { '정답': { what: '이별을 정리하는 방식도 무리해서 튀는 방식보다, 조용하고 무난한 방식이 당신에게는 더 편합니다. 극적으로 끝내기보다 담담하게 정리하는 쪽이 회복도 더 빠릅니다.' } }
    },
    '짝사랑': {
      solo: { '함께': { what: '혼자 마음을 삭이며 끝내는 것보다, 누군가에게라도 이 마음을 털어놓아야 조금은 편해지는 쪽입니다. 아무한테도 말 못 하고 혼자 삼키는 짝사랑이 유난히 무겁게 느껴지실 거예요.' } },
      form: { '무형': { what: '뭔가를 해주고 챙겨주는 것보다, 그 사람이 나에게 건네는 말 한마디에 더 크게 흔들리는 쪽입니다. 짧은 한마디에도 며칠을 곱씹으실 거예요.' } },
      many: { '여럿': { what: '그 사람 하나에만 마음을 다 쏟기보다, 다른 곳에도 마음 둘 자리가 있어야 이 짝사랑이 덜 버겁습니다. 마음이 그 사람으로만 꽉 차 있다면, 다른 관심사를 하나 만들어두는 게 도움이 될 수 있어요.' } },
      risk: { flat: '그 사람 앞에서 편안한 게 좋은지, 설레고 긴장되는 게 좋은지 — 둘 다 당신에게는 괜찮은 감정이에요. 어느 한쪽만 정답이라고 여기지 않으셔도 됩니다.' },
      make: { '정답': { what: '마음을 표현할 때도 파격적인 방식보다, 무난하고 검증된 방식이 당신에게는 더 편합니다. 남들 다 하는 평범한 방식으로 다가가는 것이 오히려 당신답고 자연스럽습니다.' } }
    }
  };

  /* 어떤 주제를 고르셨는지 — 가디언이 연성의 신일 때만 봅니다.
     엔진 안의 slug 를 그대로 쓰므로 가디언 판별은 틀릴 수 없고,
     주제는 접수 내역(localStorage.stella_demo)에서 읽습니다.
     못 읽거나 모르는 주제면 빈 값을 돌려주고, 그러면 예전 문구로 갑니다. */
  function loveTopicOf(slug){
    if(slug!=='door-love'){ return ''; }
    try{
      var raw=localStorage.getItem('stella_demo');
      if(!raw){ return ''; }
      var o=JSON.parse(raw);
      var t=(o&&o.topic)?String(o.topic).trim():'';
      return AXIS_WARM_TOPIC[t] ? t : '';
    }catch(e){ return ''; }
  }
JS;

/* ===== W 를 찾는 부분을 이렇게 바꿉니다 ========================= */
$STELLA_AXIS_LOOKUP = <<<'JS'
if(AXIS_WARM[slug]){ if(AXIS_WARM[slug][key]){ W=AXIS_WARM[slug][key]; } }
    /* 주제별 문구가 있으면 그 자리만 덮어씁니다.
       통째로 갈아끼우지 않는 이유 — 새 표에 없는 쪽(예: solo 의 '혼자')까지
       같이 사라져서, 그쪽으로 기운 분은 문단을 통째로 잃게 됩니다. */
    var __lt = loveTopicOf(slug);
    if(__lt && AXIS_WARM_TOPIC[__lt] && AXIS_WARM_TOPIC[__lt][key]){
      var __over = AXIS_WARM_TOPIC[__lt][key], __merged = {}, __k;
      if(W){ for(__k in W){ if(Object.prototype.hasOwnProperty.call(W,__k)){ __merged[__k]=W[__k]; } } }
      for(__k in __over){ if(Object.prototype.hasOwnProperty.call(__over,__k)){ __merged[__k]=__over[__k]; } }
      W = __merged;
    }
JS;


/* ------------------------------------------------------------------
 * 아래는 손대지 않으셔도 됩니다.
 * ---------------------------------------------------------------- */

add_action( 'admin_init', function () use ( $STELLA_AXIS_TABLE, $STELLA_AXIS_LOOKUP ) {

	if ( ! isset( $_GET['stella_patch'] ) || ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$mode     = sanitize_key( wp_unslash( $_GET['stella_patch'] ) );
	$page_id  = (int) STELLA_AXIS_PAGE;
	$done_opt = 'stella_patch_' . STELLA_AXIS_KEY . '_done';
	$back_opt = 'stella_patch_' . STELLA_AXIS_KEY . '_backup';
	$log      = array();

	$say = function ( $lines, $ok = true ) {
		add_action( 'admin_notices', function () use ( $lines, $ok ) {
			printf(
				'<div class="notice notice-%s"><p><strong>스텔라 패치 · 2부 저울</strong></p><pre style="white-space:pre-wrap;margin:0">%s</pre></div>',
				$ok ? 'success' : 'error',
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
	if ( false !== strpos( $content, STELLA_AXIS_STAMP ) ) {
		$say( array(
			'페이지에 이미 ' . STELLA_AXIS_STAMP . ' 이(가) 들어 있습니다. 아무것도 하지 않았습니다.',
			'WPCode 에서 이 스니펫을 지우셔도 됩니다.',
		) );
		return;
	}

	/* ---- 고칠 곳 1 : gapBlock 앞에 표를 끼워넣기 ---- */
	$re_gap = '/function\s+gapBlock\s*\(\s*key\s*,\s*title\s*\)\s*\{/';
	$n_gap  = preg_match_all( $re_gap, $content );

	/* ---- 고칠 곳 2 : W 를 찾는 두 줄 ---- */
	$re_w = '/if\s*\(\s*AXIS_WARM\s*\[\s*slug\s*\]\s*\)\s*\{\s*'
	      . 'if\s*\(\s*AXIS_WARM\s*\[\s*slug\s*\]\s*\[\s*key\s*\]\s*\)\s*\{\s*'
	      . 'W\s*=\s*AXIS_WARM\s*\[\s*slug\s*\]\s*\[\s*key\s*\]\s*;\s*\}\s*\}/';
	$n_w  = preg_match_all( $re_w, $content );

	$log[] = 'gapBlock 정의를 찾은 횟수 : ' . (int) $n_gap . ' (1 이어야 함)';
	$log[] = 'W 찾는 부분을 찾은 횟수   : ' . (int) $n_w . ' (1 이어야 함)';

	if ( 1 !== $n_gap || 1 !== $n_w ) {
		$say( array_merge( $log, array(
			'',
			'찾는 자리가 하나씩이 아닙니다. 엔진이 그 사이에 바뀐 것 같습니다.',
			'아무것도 고치지 않았습니다. 이 화면을 그대로 알려주세요.',
		) ), false );
		return;
	}

	$table  = rtrim( $STELLA_AXIS_TABLE ) . "\n\n";
	$lookup = trim( $STELLA_AXIS_LOOKUP );

	$updated = preg_replace_callback(
		$re_gap,
		function ( $m ) use ( $table ) { return $table . '  ' . $m[0]; },
		$content,
		1
	);
	if ( null === $updated ) {
		$say( array_merge( $log, array( '표를 끼워넣다가 실패했습니다. (preg 오류)' ) ), false );
		return;
	}

	$updated = preg_replace_callback(
		$re_w,
		function ( $m ) use ( $lookup ) { return $lookup; },
		$updated,
		1
	);
	if ( null === $updated ) {
		$say( array_merge( $log, array( 'W 찾는 부분을 바꾸다가 실패했습니다. (preg 오류)' ) ), false );
		return;
	}

	$grew  = strlen( $updated ) - strlen( $content );
	$log[] = '';
	$log[] = '지금    : ' . number_format( strlen( $content ) ) . ' 바이트';
	$log[] = '바뀐 뒤 : ' . number_format( strlen( $updated ) ) . ' 바이트  (' . ( $grew >= 0 ? '+' : '' ) . number_format( $grew ) . ')';

	/* ---- 안전장치 ---- */
	if ( $grew < 8000 || $grew > 20000 ) {
		$say( array_merge( $log, array(
			'',
			'늘어난 크기가 예상 범위(8,000~20,000 바이트)를 벗어났습니다. 뭔가 잘못된 것 같아 멈췄습니다.',
		) ), false );
		return;
	}
	if ( false === strpos( $updated, 'AXIS_WARM_TOPIC[__lt][key]' ) ) {
		$say( array_merge( $log, array( '', '바뀐 내용에 새 조회 코드가 없습니다. 멈췄습니다.' ) ), false );
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
		'3) 시크릿 창에서 연성의 신 → 결혼운 / 연애운 각각 전자책까지 가서',
		'   「어긋나는 자리」 저울 다섯 개가 서로 다른지 확인',
		'',
		'되돌리려면 : /wp-admin/?stella_patch=undo',
	) ) );
} );
