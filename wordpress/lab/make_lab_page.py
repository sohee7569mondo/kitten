# -*- coding: utf-8 -*-
"""index.block.html 을 /lab/ **페이지**로 만드는 한 번짜리 조각으로 감쌉니다.

유앤미 ③(uandme_3_page)과 같은 결입니다 — 미리보기 먼저, 그다음 만들기.
한 번 쓰고 끄시면 됩니다. 페이지는 남습니다.
"""
import io, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, 'index.block.html')
DST  = os.path.join(HERE, 'snippets', 'snip_lab_page.WPCODE.txt')
TAG  = 'STELLA_LAB_PAGE_BODY'

HEAD = '''/* ════════════════════════════════════════════════════════════
   스텔라 랩 목록을 **페이지로 못박습니다**     판 %(S)s

   소희 님 : 「snip_lab_index 이걸 스텔라 랩의 첫화면으로
              못박아줘 페이지를 만드는 방식으로 하기로 햇잖아」

   ── 왜 페이지인가 ───────────────────────────────────
   지금은 조각(snip_lab_index)이 /lab/ 주소를 가로채서 그립니다.
   **조각 하나만 꺼지면 옛 목록이 나옵니다.** 오늘 실제로 그랬습니다.
   페이지로 두면 조각과 무관하게 남습니다.

   ── 쓰는 법 (한 번만) ───────────────────────────────
   ① 미리보기   https://stellasaju.com/?stella_labpage=1
                무엇이 바뀌는지 보여만 줍니다. 아무것도 안 건드립니다.
   ② 만들기     미리보기 화면 맨 아래의 「→ 이대로 만들기」를 누르세요.
   ③ 그다음     WPCode 에서 **snip_lab_index 를 끕니다**
                (그 조각이 켜져 있으면 페이지보다 먼저 돌아 가로챕니다)
   ④ 이 조각도 끄셔도 됩니다. 페이지는 그대로 남습니다.

   ── 무엇이 들어가나 ─────────────────────────────────
   labindex.html 을 페이지에 넣을 수 있게 손본 것입니다.
   크로미움으로 원본과 나란히 그려 값이 똑같은 것을 확인했습니다
   (카드 18장 · 그림 6장 · 폭 540 · 카드 폭 263).

   붙여넣기 : WPCode → 새 스니펫 → PHP Snippet → 저장 → Active
   ★ 위치(Location)를 반드시 「어디서나 실행 / Run Everywhere」로.
   ★ 크롬 번역을 끄고 붙여넣으세요.
   ════════════════════════════════════════════════════════════ */

add_action( 'init', function () {

	if ( ! isset( $_GET['stella_labpage'] ) ) { return; }

	header( 'Content-Type: text/html; charset=utf-8' );
	echo '<meta charset="utf-8"><body style="font:15px/1.9 system-ui;'
		. 'background:#141018;color:#eee;padding:24px;max-width:860px">';

	if ( ! current_user_can( 'manage_options' ) ) {
		echo '<h1 style="color:#ff7b7b">관리자만 볼 수 있습니다.</h1>';
		exit;
	}

	$slug = 'lab';
	$body = <<<'%(T)s'
'''

FOOT = '''
%(T)s;

	$content = '<!-- wp:html -->' . "\\n" . $body . "\\n" . '<!-- /wp:html -->';
	$go   = isset( $_GET['go'] );
	$page = get_page_by_path( $slug, OBJECT, 'page' );

	printf( '<h1 style="color:#ffd76a">스텔라 랩 목록 — %%s</h1>',
		$go ? '만들기' : '<span style="color:#9fd">미리보기 · 아무것도 안 바뀝니다</span>' );

	echo '<table cellpadding="7" style="border-collapse:collapse;font-size:14px">';
	printf( '<tr><td>주소</td><td><b>/%%s/</b></td></tr>', $slug );
	printf( '<tr><td>이미 있나</td><td>%%s</td></tr>',
		$page
			? '<span style="color:#9fd">있음 · 번호 ' . $page->ID . ' · 지금 '
				. number_format( strlen( $page->post_content ) ) . '자</span>'
			: '없음 · 새로 만듭니다' );
	printf( '<tr><td>넣을 글</td><td><b>%%s자</b> · 카드 %%d장 · 그림 %%d장</td></tr>',
		number_format( strlen( $content ) ),
		substr_count( $body, 'class="card' ),
		substr_count( $body, 'background-image' ) + substr_count( $body, '<img' ) );
	echo '</table>';

	/* 이미 있던 글이 통째로 바뀌면 그대로 보여드립니다 (되돌리기 대비) */
	if ( $page ) {
		if ( strlen( $page->post_content ) > 400 ) {
			echo '<h2 style="color:#ffb4b4;margin-top:22px">★ 지금 들어 있는 글이 지워집니다</h2>';
			echo '<pre style="white-space:pre-wrap;word-break:break-all;max-height:260px;'
				. 'overflow:auto;background:#0b0810;padding:12px;border-radius:8px;'
				. 'font-size:12px;color:#c9c3d6">'
				. esc_html( substr( $page->post_content, 0, 2000 ) ) . '</pre>';
		}
	}

	if ( ! $go ) {
		echo '<p style="margin-top:22px;font-size:18px">'
			. '<a style="color:#ffd76a" href="?stella_labpage=1&amp;go=1">'
			. '→ 이대로 만들기</a></p>';
		exit;
	}

	if ( $page ) {
		$id = $page->ID;
		wp_update_post( array(
			'ID'           => $id,
			'post_content' => $content,
			'post_status'  => 'publish',
		) );
		echo '<h2 style="color:#7bff9b">있던 페이지를 고쳤습니다.</h2>';
	} else {
		$id = wp_insert_post( array(
			'post_title'     => '스텔라 랩',
			'post_name'      => $slug,
			'post_content'   => $content,
			'post_status'    => 'publish',
			'post_type'      => 'page',
			'comment_status' => 'closed',
			'ping_status'    => 'closed',
		) );
		echo '<h2 style="color:#7bff9b">페이지를 만들었습니다.</h2>';
	}

	if ( is_wp_error( $id ) ) {
		echo '<h2 style="color:#ff7b7b">못 만들었습니다 — '
			. esc_html( $id->get_error_message() ) . '</h2>';
		exit;
	}

	clean_post_cache( $id );
	if ( function_exists( 'wp_cache_flush' ) ) { wp_cache_flush(); }

	printf( '<p>페이지 번호 <b>%%d</b> · 넣은 글 <b>%%s자</b></p>',
		$id, number_format( strlen( $content ) ) );
	printf( '<p style="font-size:18px"><a style="color:#ffd76a" href="%%s">→ 스텔라 랩 열어보기</a></p>',
		esc_url( get_permalink( $id ) ) );
	echo '<h3 style="color:#ffd76a;margin-top:24px">다음 한 가지만 더</h3>';
	echo '<p>WPCode 에서 <b>snip_lab_index</b>(「스텔라 랩 목록」)를 <b>끄세요</b>.<br>'
		. '그 조각이 켜져 있으면 페이지보다 먼저 돌아 주소를 가로챕니다.</p>';
	echo '<p style="color:#888">이 조각도 이제 꺼두셔도 됩니다. 페이지는 남습니다.</p>';
	exit;
}, 1 );
'''


def main():
    body = io.open(SRC, encoding='utf-8').read()
    if TAG in body:
        print('★ 본문에 nowdoc 꼬리표가 들어 있습니다'); sys.exit(1)

    stamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    out = (HEAD % {'S': stamp, 'T': TAG}) + body + (FOOT % {'T': TAG})

    os.makedirs(os.path.dirname(DST), exist_ok=True)
    io.open(DST, 'w', encoding='utf-8').write(out)
    print('%s · %d바이트' % (os.path.basename(DST), len(out.encode('utf-8'))))
    print('본문 %d바이트 · 카드 %d장' % (len(body.encode('utf-8')), body.count('class="card')))


if __name__ == '__main__':
    main()
