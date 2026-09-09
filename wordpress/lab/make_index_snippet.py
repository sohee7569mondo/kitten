# -*- coding: utf-8 -*-
"""labindex.html 을 /lab/ 을 맡는 WPCode 스니펫으로 감쌉니다."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
body = io.open(os.path.join(HERE, 'labindex.html'), encoding='utf-8').read()
assert 'STELLA_LAB_INDEX' not in body

HEAD = '''/* ════════════════════════════════════════════════════════════
   스텔라 랩 목록   ★ 2026-09-09 · 소희 님께

   주소   https://stellasaju.com/lab/

   ★ 반드시 검사 스니펫 일곱 개를 먼저 넣으신 뒤에 이것을 넣으세요.
     먼저 넣으면 새 카드를 눌러도 빈 쪽으로 갑니다.

   랩 본체(804)가 그리던 옛 목록 대신 이 목록을 내놓습니다.
   본체는 안 건드립니다. 우선순위 5 로 먼저 돌 뿐입니다.
   이 스니펫을 끄면 옛 목록으로 그대로 돌아갑니다.

   /lab/mbti/ · /lab/ohaeng/ 처럼 본체가 맡는 검사 주소는
   건드리지 않습니다. 이 스니펫은 목록 한 장만 맡습니다.

   붙여넣기 : WPCode -> 새 스니펫 -> PHP Snippet -> 저장 -> Active
   ★ 위치(Location)를 반드시 「어디서나 실행 / Run Everywhere」로.
   ════════════════════════════════════════════════════════════ */

add_action( 'init', function () {

	$uri = isset( $_SERVER['REQUEST_URI'] ) ? $_SERVER['REQUEST_URI'] : '';
	if ( false === strpos( $uri, '/lab' ) ) { return; }

	$path = parse_url( $uri, PHP_URL_PATH );
	$path = rtrim( (string) $path, '/' );
	if ( '/lab' !== $path ) { return; }

	status_header( 200 );
	nocache_headers();
	header( 'Content-Type: text/html; charset=utf-8' );

	echo <<<'STELLA_LAB_INDEX'
'''

FOOT = '''
STELLA_LAB_INDEX;

	exit;
}, 5 );
'''

os.makedirs(os.path.join(HERE,'snippets'), exist_ok=True)
dst = os.path.join(HERE, 'snippets', 'snip_lab_index.WPCODE.txt')
io.open(dst,'w',encoding='utf-8').write(HEAD + body + FOOT)
print(os.path.basename(dst), len(HEAD+body+FOOT))
