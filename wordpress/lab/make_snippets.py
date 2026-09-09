# -*- coding: utf-8 -*-
"""블록 파일을 WPCode 스니펫으로 감쌉니다.
   글자가 제 손을 거치지 않고 파일에서 파일로 바로 옮겨갑니다."""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, 'snippets')
os.makedirs(OUT, exist_ok=True)

TESTS = [
    ('night-snack', '편의점 야식 유형',      '밤 11시 42분, 계산대까지 다섯 걸음'),
    ('cafe',        '카페에서 나는',          '들어선 순간부터 나가는 순간까지'),
    ('camping',     '캠핑 갔을 때',           '텐트 자리 잡는 순간부터 철수까지'),
    ('grocery',     '장보기 스타일',          '코스트코 입구부터 집에 와서 정리할 때까지'),
    ('money',       '나의 돈 씀씀이 스타일',  '월급날 아침부터 월말 잔고 확인까지'),
    ('breakup',     '헤어지고 나서 나는',     '끝난 뒤 한 달, 여덟 번의 선택'),
]

HEAD = '''/* ════════════════════════════════════════════════════════════
   스텔라 랩 · {title}   ★ 2026-09-09 · 소희 님께

   주소   https://stellasaju.com/lab/{slug}/

   랩 본체(804)를 건드리지 않습니다. 이 주소만 따로 맡습니다.
   본체보다 먼저(우선순위 5) 돌아서 서로 부딪히지 않습니다.

   붙여넣기 : WPCode -> 새 스니펫 -> PHP Snippet -> 저장 -> Active
   ★ 위치(Location)를 반드시 「어디서나 실행 / Run Everywhere」로.
   ★ 이 스니펫 하나가 검사 하나입니다. 여섯 개를 다 넣으셔야
     목록의 여섯 장이 모두 열립니다.
{extra}   ════════════════════════════════════════════════════════════ */

add_action( 'init', function () {{

	$uri = isset( $_SERVER['REQUEST_URI'] ) ? $_SERVER['REQUEST_URI'] : '';
	if ( false === strpos( $uri, '/lab/{slug}' ) ) {{ return; }}

	$path = parse_url( $uri, PHP_URL_PATH );
	$path = rtrim( (string) $path, '/' );
	if ( '/lab/{slug}' !== $path ) {{ return; }}

	status_header( 200 );
	nocache_headers();
	header( 'Content-Type: text/html; charset=utf-8' );

	echo <<<'STELLA_LAB_HTML'
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — 스텔라 랩</title>
<meta name="description" content="{dek}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title} — 스텔라 랩">
<meta property="og:description" content="{dek}">
<meta property="og:url" content="https://stellasaju.com/lab/{slug}/">
<link rel="canonical" href="https://stellasaju.com/lab/{slug}/">
</head>
<body style="margin:0">
'''

FOOT = '''
</body>
</html>
STELLA_LAB_HTML;

	exit;
}}, 5 );
'''

made = []
for slug, title, dek in TESTS:
    src = os.path.join(HERE, slug + '.block.html')
    body = io.open(src, encoding='utf-8').read()

    # 붙여넣기 안내용 주석은 화면에 필요 없습니다
    if body.lstrip().startswith('<!--'):
        end = body.index('-->') + 3
        body = body[end:].lstrip('\n')

    if 'STELLA_LAB_HTML' in body:
        print('!! 끝말이 글 안에 있습니다:', slug); sys.exit(1)

    extra = ''
    if slug == 'breakup':
        extra = ('   ★ 랩 안(806 MORE2)에 열두 문항짜리 옛 판이 있습니다.\n'
                 '     이 스니펫이 먼저 돌아서 새 여덟 문항 판이 나옵니다.\n'
                 '     끄면 옛 판으로 돌아갑니다.\n')

    txt = HEAD.format(slug=slug, title=title, dek=dek, extra=extra) + body + FOOT.format()
    dst = os.path.join(OUT, 'snip_lab_%s.WPCODE.txt' % slug)
    io.open(dst, 'w', encoding='utf-8').write(txt)
    made.append((dst, len(txt)))

for d, n in made:
    print('%-46s %7d' % (os.path.basename(d), n))
