# -*- coding: utf-8 -*-
"""별명표를 조각 둘에 박아 넣습니다.

    uandme_1_engine.WPCODE.txt   화면과 캔버스 그림이 쓰는 자바스크립트
    uandme_4_card.WPCODE.txt     카톡에 갈 그림을 그리는 PHP

  둘이 같은 표를 써야 카톡 그림과 화면이 같은 이름을 말합니다.
  별명을 고치면 uandme_nick.py 만 고치고 이것을 다시 돌립니다.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uandme_nick import NICK, RELS, MINS, check

PHP = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', 'php')


def js_block():
    L = []
    L.append('/* ───── uandme-nick.js ───── */')
    L.append('/* 점수 구간마다 붙는 이름 — 관계 일곱 가지 각각 열 칸.')
    L.append('   「좋은 궁합」 같은 설명 대신 이름을 답니다. 카톡에 떴을 때')
    L.append('   그 이름 하나로 눌러보고 싶어야 하기 때문입니다. */')
    L.append('window.UANDME_NICK = {')
    for k, rel in enumerate(RELS):
        rows = NICK[rel]
        L.append('  ' + rel + ': [')
        for name, sub in rows:
            L.append("    ['" + name + "', '" + sub + "'],")
        L.append('  ]' + (',' if k < len(RELS) - 1 else ''))
    L.append('};')
    L.append('')
    L.append('window.UANDME_TIER = function (score, rel) {')
    L.append('  var i, t = window.UANDME_TIERS, N = window.UANDME_NICK;')
    L.append('  for (i = 0; i < t.length; i++) {')
    L.append('    if (score >= t[i].min) { if (score <= t[i].max) {')
    L.append('      var rows = N[rel] ? N[rel] : N.lover;')
    L.append('      var one  = rows[i] ? rows[i] : [t[i].title, 0];')
    L.append('      return { title: one[0] ? one[0] : t[i].title,')
    L.append('               sub: one[1] ? one[1] : 0,')
    L.append('               plain: t[i].title,')
    L.append('               comment: t[i].c[rel] || t[i].c.lover };')
    L.append('    } }')
    L.append('  }')
    L.append("  return { title: '알 수 없음', sub: 0, plain: 0, comment: '' };")
    L.append('};')
    return '\n'.join(L) + '\n'


def php_block():
    L = []
    L.append("/* ── 점수와 관계로 별명 알아내기 ─────────────────────")
    L.append("   주소에 한글을 싣지 않으려고 서버도 같은 표를 갖습니다.")
    L.append("   자바스크립트 쪽 uandme-nick.js 와 한 글자도 다르면 안 됩니다.")
    L.append("   ★ 고칠 때는 wordpress/tools/uandme_nick.py 를 고치고")
    L.append("     emit_uandme_nick.py 를 돌립니다. 손으로 고치지 않습니다. */")
    L.append("if ( ! function_exists( 'stella_um_nick' ) ) {")
    L.append("\tfunction stella_um_nick( $n, $rel ) {")
    L.append("\t\t$mins = array( " + ', '.join(str(m) for m in MINS) + " );")
    L.append("\t\t$tab  = array(")
    for rel in RELS:
        L.append("\t\t\t'" + rel + "' => array(")
        for name, sub in NICK[rel]:
            L.append("\t\t\t\tarray( '" + name + "', '" + sub + "' ),")
        L.append("\t\t\t),")
    L.append("\t\t);")
    L.append("\t\t$rows = isset( $tab[ $rel ] ) ? $tab[ $rel ] : $tab['lover'];")
    L.append("\t\t$i = 0;")
    L.append("\t\twhile ( $i < count( $mins ) ) {")
    L.append("\t\t\tif ( $n >= $mins[ $i ] ) { return $rows[ $i ]; }")
    L.append("\t\t\t$i++;")
    L.append("\t\t}")
    L.append("\t\treturn $rows[ count( $rows ) - 1 ];")
    L.append("\t}")
    L.append("}")
    L.append("/* 옛 이름 — 다른 조각이 아직 부를 수 있어 남겨 둡니다 */")
    L.append("if ( ! function_exists( 'stella_um_tier' ) ) {")
    L.append("\tfunction stella_um_tier( $n ) {")
    L.append("\t\t$one = stella_um_nick( $n, 'lover' );")
    L.append("\t\treturn $one[0];")
    L.append("\t}")
    L.append("}")
    return '\n'.join(L) + '\n'


def cut(text, head, tail, what):
    a = text.find(head)
    if a < 0:
        raise SystemExit('★ ' + what + ' — 머리를 못 찾았습니다: ' + head[:50])
    b = text.find(tail, a)
    if b < 0:
        raise SystemExit('★ ' + what + ' — 꼬리를 못 찾았습니다: ' + tail[:50])
    return a, b + len(tail)


def main():
    bad = check()
    if bad:
        for x in bad:
            print('★ ' + x)
        raise SystemExit('별명표가 규칙에 안 맞습니다.')

    # ── 자바스크립트 ────────────────────────────────
    p = os.path.join(PHP, 'uandme_1_engine.WPCODE.txt')
    s = io.open(p, encoding='utf-8').read()
    a, b = cut(s, 'window.UANDME_TIER = function (score, rel) {',
               '\n};\n', 'engine')
    # 앞에 이미 넣어둔 별명표가 있으면 그것까지 걷어냅니다
    mark = '/* ───── uandme-nick.js ───── */'
    if mark in s:
        a = s.find(mark)
    s2 = s[:a] + js_block() + s[b:]
    io.open(p, 'w', encoding='utf-8').write(s2)
    print('자바스크립트  ' + str(len(s)) + ' -> ' + str(len(s2)))

    # ── PHP ────────────────────────────────────────
    p = os.path.join(PHP, 'uandme_4_card.WPCODE.txt')
    s = io.open(p, encoding='utf-8').read()
    m1 = '/* ── 점수로 등급 이름 알아내기'
    m2 = '/* ── 점수와 관계로 별명 알아내기'
    head = m2 if m2 in s else m1
    a, b = cut(s, head, "\n}\n", 'card')
    # stella_um_tier 까지 통째로 — 마지막 닫는 괄호를 찾습니다
    end = s.find("\n}\n", s.find("function stella_um_tier", a))
    if end > 0:
        b = end + 3
    s2 = s[:a] + php_block() + s[b:]
    io.open(p, 'w', encoding='utf-8').write(s2)
    print('PHP           ' + str(len(s)) + ' -> ' + str(len(s2)))


main()
