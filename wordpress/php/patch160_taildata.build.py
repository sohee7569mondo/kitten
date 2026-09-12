#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
덤 두 쪽의 글 504칸을 담는 짝 조각(B)을 원고에서 만듭니다.

  원고  wordpress/drafts/별자리-맺음앞-원고.md   → 별자리 표 (21 주제 × 12 자리)
  원고  wordpress/drafts/띠-원고.md              → 띠 표   (21 주제 × 12 띠)

이 조각은 책 쪽에서 한 글자도 내보내지 않습니다.
가벼운 조각(A)이 물어볼 때만 그 두 칸을 돌려줍니다.

    python3 wordpress/php/patch160_taildata.build.py

★ 집 규칙 — 홑따옴표·앰퍼샌드·역슬래시가 원고에 있으면 멈추고 어디인지 알려줍니다.
"""
import importlib.util, pathlib, sys

HERE  = pathlib.Path(__file__).resolve().parent
DRAFT = HERE.parent / 'drafts'
OUT   = HERE / 'patch160_taildata.WPCODE.txt'

# 원고 읽는 법은 한 곳에만 둡니다.
spec = importlib.util.spec_from_file_location('tailrun_build', HERE / 'patch160_tailrun.build.py')
tb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tb)

HEAD = """/* ══════════════════════════════════════════════════════════
   맺음말 앞 두 쪽 — 글을 담아두는 짝 조각
   ★ 2026-09-12 · 소희 님께      BUILD: TAIL-DATA-1

   ── 이 조각이 하는 일 ─────────────────────────────────
   덤 두 쪽의 글 504칸을 가지고 있습니다.

       별자리  21 주제 × 12 자리 = 252 칸
       띠      21 주제 × 12 띠   = 252 칸

   ★ 책 쪽에서는 한 글자도 나가지 않습니다.
     가벼운 조각(A)이 손님의 별자리와 띠를 알아낸 뒤
     필요한 두 칸만 물어봅니다. 그때만 그 두 칸을 돌려줍니다.
     오가는 글은 2KB 남짓입니다.

   책 쪽에 300KB를 얹었다가 하얗게 죽었습니다. 그래서 나눴습니다.

   ── 짝이 있어야 돕니다 ────────────────────────────────
       A  patch160_tailfetch   책 쪽에 나가는 가벼운 조각
       B  이 조각              글을 담아두는 조각
   둘 다 Active 여야 덤 두 쪽이 나옵니다.

   ── 글은 원고에서 바로 옵니다 ─────────────────────────
       wordpress/drafts/별자리-맺음앞-원고.md
       wordpress/drafts/띠-원고.md
   손으로 옮기지 않습니다. 원고를 고치신 뒤
       python3 wordpress/php/patch160_taildata.build.py
   를 돌리면 이 조각이 새로 만들어집니다.

   ── 확인하고 싶으실 때 ────────────────────────────────
   이 주소를 여시면 두 칸이 글자로 보입니다.

       https://stellasaju.com/?stella_tailx=1[그리고]tp=연애운[그리고]sg=양자리[그리고]ji=쥐띠

   대괄호 자리에는 주소에 쓰는 「그리고」 기호를 넣으세요.
   ⑨ 취업운처럼 번호는 넣지 않습니다. 주제 이름만 넣습니다.

   붙여넣기 : WPCode -> 새 스니펫 -> PHP Snippet -> 저장 -> Active
   ★ 위치(Location)를 반드시 「어디서나 실행 / Run Everywhere」로.
   ★ 두 번 붙여도 안전합니다. 같은 이름이 이미 있으면 물러납니다.
   ══════════════════════════════════════════════════════════ */

if ( ! function_exists( 'stella_tailx_zo' ) ) {

/* ── 물어보면 두 칸만 돌려줍니다 ─────────────────────────
   표는 함수 안에 있습니다. 물어보지 않는 쪽(책 쪽을 포함해)에서는
   표를 펼치지 않습니다. 그래서 다른 쪽의 메모리가 늘지 않습니다. */
add_action( 'init', function () {

	if ( ! isset( $_GET['stella_tailx'] ) ) { return; }

	$t = '';
	$s = '';
	$j = '';
	/* 이름을 tp·sg·ji 로 씁니다. s 는 워드프레스가 검색어로 쓰는 이름이라 피했습니다. */
	if ( isset( $_GET['tp'] ) ) { $t = sanitize_text_field( wp_unslash( $_GET['tp'] ) ); }
	if ( isset( $_GET['sg'] ) ) { $s = sanitize_text_field( wp_unslash( $_GET['sg'] ) ); }
	if ( isset( $_GET['ji'] ) ) { $j = sanitize_text_field( wp_unslash( $_GET['ji'] ) ); }

	$zo = stella_tailx_zo();
	$dd = stella_tailx_dd();

	$t = stella_tailx_norm( $t, $zo, $dd );

	$out = array( 'q' => '', 'zo' => null, 'dd' => null, 'topic' => $t );

	if ( isset( $zo[ $t ] ) ) {
		$out['q'] = $zo[ $t ]['q'];
		if ( isset( $zo[ $t ]['c'][ $s ] ) ) { $out['zo'] = $zo[ $t ]['c'][ $s ]; }
	}
	if ( isset( $dd[ $t ] ) ) {
		if ( isset( $dd[ $t ][ $j ] ) ) { $out['dd'] = $dd[ $t ][ $j ]; }
	}

	/* 같은 손님이 다시 열어도 빠르게. 하루 동안 담아둡니다. */
	header( 'Cache-Control: public, max-age=86400' );
	wp_send_json( $out );
}, 1 );

/* 책의 주제 이름과 원고의 주제 이름을 맞춥니다.
   「~운」으로 오든 「~운세」로 오든 다 받습니다. */
function stella_tailx_norm( $t, $zo, $dd ) {
	if ( '' === $t ) { return ''; }

	$map = array(
		'직업운'   => '직장운',   '직업운세' => '직장운', '직장운세' => '직장운',
		'짝사랑'   => '짝사랑운', '짝사랑운세' => '짝사랑운',
		'신년운'   => '신년운세', '자녀운'   => '자식운', '자녀운세' => '자식운'
	);
	if ( isset( $map[ $t ] ) ) { return $map[ $t ]; }
	if ( isset( $zo[ $t ] ) ) { return $t; }
	if ( isset( $dd[ $t ] ) ) { return $t; }

	/* 「연애운세」처럼 뒤에 「세」가 붙어 오면 떼고 다시 찾습니다 */
	if ( '운세' === substr( $t, -6 ) ) {
		$s = substr( $t, 0, -3 );
		if ( isset( $map[ $s ] ) ) { return $map[ $s ]; }
		if ( isset( $zo[ $s ] ) ) { return $s; }
		if ( isset( $dd[ $s ] ) ) { return $s; }
	}
	/* 「신년운」처럼 왔는데 원고가 「신년운세」인 경우 */
	if ( '운' === substr( $t, -3 ) ) {
		$w = $t . '세';
		if ( isset( $zo[ $w ] ) ) { return $w; }
		if ( isset( $dd[ $w ] ) ) { return $w; }
	}
	return $t;
}

"""

TAILEND = """
}
"""


def pstr(s):
    return "'" + s + "'"


def emit(func, table, with_q, title):
    out = ['/* ── %s ─────────────────────────────────────── */' % title,
           'function %s() {' % func,
           '\treturn array(']
    tl = list(table.items())
    for ti, (topic, v) in enumerate(tl):
        comma = ',' if ti < len(tl) - 1 else ''
        if with_q:
            out.append('\t' + pstr(topic) + ' => array( ' + pstr('q') + ' => ' + pstr(v['q']) + ', ' + pstr('c') + ' => array(')
            close = '\t) )'
        else:
            out.append('\t' + pstr(topic) + ' => array(')
            close = '\t)'
        cl = list(v['c'].items())
        for ci, (k, (sub, html)) in enumerate(cl):
            tail = ',' if ci < len(cl) - 1 else ''
            out.append('\t\t' + pstr(k) + ' => array(' + pstr(sub) + ', ' + pstr(html) + ')' + tail)
        out.append(close + comma)
    out.append('\t);')
    out.append('}')
    return '\n'.join(out)


def main():
    zo = tb.parse(DRAFT / '별자리-맺음앞-원고.md')
    dd = tb.parse(DRAFT / '띠-원고.md')

    for name, table in (('별자리', zo), ('띠', dd)):
        for t in [t for t, v in table.items() if not v['c']]:
            print('표에서 뺐습니다 (칸 없음) :', name, t)
            del table[t]

    bad = tb.guard('별자리', zo) + tb.guard('띠', dd)
    if bad:
        print('멈춥니다 — 원고에 손볼 곳이 있습니다')
        for b in bad:
            print('  ·', b)
        sys.exit(1)

    body = (HEAD
            + emit('stella_tailx_zo', zo, True, '별자리 스물한 주제 × 열두 자리') + '\n\n'
            + emit('stella_tailx_dd', dd, False, '띠 스물한 주제 × 열두 띠')
            + TAILEND)
    OUT.write_text(body, encoding='utf-8')

    print('별자리 %2d 주제 %3d 칸' % (len(zo), sum(len(v['c']) for v in zo.values())))
    print('띠     %2d 주제 %3d 칸' % (len(dd), sum(len(v['c']) for v in dd.values())))
    print('만들었습니다 :', OUT.name, '%.0f KB' % (OUT.stat().st_size / 1024))


if __name__ == '__main__':
    main()
