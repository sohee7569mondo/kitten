# -*- coding: utf-8 -*-
"""낱말표를 조각 둘에 박아 넣습니다.

    uandme_1_engine.WPCODE.txt   화면과 캔버스 그림이 쓰는 자바스크립트
    uandme_4_card.WPCODE.txt     카톡에 갈 그림을 그리는 PHP

  둘이 같은 표를 써야 카톡 그림과 화면이 같은 말을 합니다.
  고칠 때는 원고(drafts/유앤미-낱말표.md)만 고치고 이것을 돌립니다.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uandme_words as W

END = '/* ───── 낱말표 끝 ───── */'

PHP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'php')


def q(x):
    return "'" + x + "'"


def js_block():
    L = []
    L.append('/* ───── uandme-words.js ───── */')
    L.append('/* 낱말표 — 두 층입니다.')
    L.append('     BAND  점수 구간 스무 칸. 요약 · 이모지 · 별명.')
    L.append('           관계를 안 가립니다 — 실과 바늘은 어느 사이에나 맞습니다.')
    L.append('     TALK  관계 일곱 × 큰 칸 다섯. 훅 · 본문 세 문장.')
    L.append('           여기가 관계를 맡습니다.')
    L.append('   ★ 손으로 고치지 않습니다 — drafts/유앤미-낱말표.md 를 고치고')
    L.append('     tools/emit_uandme_words.py 를 돌립니다. */')
    L.append('window.UANDME_BAND_MIN = [' + ', '.join(str(x) for x in W.BAND_MIN) + '];')
    L.append('window.UANDME_BAND = [')
    for row in W.BAND:
        a, b, c = row[0], row[1], row[2]
        body = row[3] if len(row) > 3 else []
        L.append('  [' + q(a) + ', ' + q(b) + ', ' + q(c) + ', [' +
                 ', '.join(q(x) for x in body) + ']],')
    L.append('];')
    L.append('window.UANDME_STEP_MIN = [' + ', '.join(str(x) for x in W.STEP_MIN) + '];')
    L.append('window.UANDME_TALK = {')
    for k, rel in enumerate(W.RELS):
        L.append('  ' + rel + ': [')
        for hook, lines in W.TALK[rel]:
            L.append('    [' + q(hook) + ', [' + ', '.join(q(x) for x in lines) + ']],')
        L.append('  ]' + (',' if k < len(W.RELS) - 1 else ''))
    L.append('};')
    L.append('')
    L.append('window.UANDME_TIER = function (score, rel) {')
    L.append('  var i, b = null, t = null;')
    L.append('  var BM = window.UANDME_BAND_MIN, BD = window.UANDME_BAND;')
    L.append('  var SM = window.UANDME_STEP_MIN, TK = window.UANDME_TALK;')
    L.append('  for (i = 0; i < BM.length; i++) {')
    L.append('    if (score >= BM[i]) { b = BD[i]; break; }')
    L.append('  }')
    L.append('  if (!b) { b = BD[BD.length - 1]; }')
    L.append('  var rows = TK[rel] ? TK[rel] : TK.lover;')
    L.append('  for (i = 0; i < SM.length; i++) {')
    L.append('    if (score >= SM[i]) { t = rows[i]; break; }')
    L.append('  }')
    L.append('  if (!t) { t = rows[rows.length - 1]; }')
    L.append('  /* 결과 화면의 긴 글은 예전 표를 그대로 씁니다 */')
    L.append("  var say = '';")
    L.append('  var old = window.UANDME_TIERS, j;')
    L.append('  if (old) {')
    L.append('    for (j = 0; j < old.length; j++) {')
    L.append('      if (score >= old[j].min) { if (score <= old[j].max) {')
    L.append('        say = old[j].c[rel] || old[j].c.lover; break;')
    L.append('      } }')
    L.append('    }')
    L.append('  }')
    L.append('  /* 카드에 나가는 글(요약·별명·본문)은 점수 칸이 맡고,')
    L.append('     훅과 긴 글은 관계가 맡습니다 — 2026-09-15 */')
    L.append('  return { sum: b[0], emoji: b[1], title: b[2], lines: b[3],')
    L.append('           hook: t[0], talk: t[1], plain: b[2], comment: say };')
    L.append('};')
    L.append(END)
    return '\n'.join(L) + '\n'


def php_block():
    L = []
    L.append("/* ── 점수와 관계로 낱말 알아내기 ─────────────────────")
    L.append("   자바스크립트 쪽 uandme-words.js 와 한 글자도 다르면 안 됩니다.")
    L.append("   돌려주는 것 :")
    L.append("     0 별명   1 훅   2·3 본문 두 문장   4 (안 씀)   5 요약   6 이모지")
    L.append("   ★ 고칠 때는 drafts/유앤미-낱말표.md 를 고치고")
    L.append("     tools/emit_uandme_words.py 를 돌립니다. */")
    L.append("if ( ! function_exists( 'stella_um_nick' ) ) {")
    L.append("\tfunction stella_um_nick( $n, $rel ) {")
    L.append("\t\t$bmin = array( " + ', '.join(str(x) for x in W.BAND_MIN) + " );")
    L.append("\t\t$band = array(")
    for row in W.BAND:
        a, b, c = row[0], row[1], row[2]
        body = row[3] if len(row) > 3 else ['', '']
        while len(body) < 2:
            body.append('')
        L.append("\t\t\tarray( '" + a + "', '" + b + "', '" + c + "', '" +
                 body[0] + "', '" + body[1] + "' ),")
    L.append("\t\t);")
    L.append("\t\t$smin = array( " + ', '.join(str(x) for x in W.STEP_MIN) + " );")
    L.append("\t\t$talk = array(")
    for rel in W.RELS:
        L.append("\t\t\t'" + rel + "' => array(")
        for hook, lines in W.TALK[rel]:
            L.append("\t\t\t\tarray( '" + hook + "', '" + lines[0] + "', '" +
                     lines[1] + "', '" + lines[2] + "' ),")
        L.append("\t\t\t),")
    L.append("\t\t);")
    L.append("\t\t$b = $band[ count( $band ) - 1 ];")
    L.append("\t\t$i = 0;")
    L.append("\t\twhile ( $i < count( $bmin ) ) {")
    L.append("\t\t\tif ( $n >= $bmin[ $i ] ) { $b = $band[ $i ]; break; }")
    L.append("\t\t\t$i++;")
    L.append("\t\t}")
    L.append("\t\t$rows = isset( $talk[ $rel ] ) ? $talk[ $rel ] : $talk['lover'];")
    L.append("\t\t$t = $rows[ count( $rows ) - 1 ];")
    L.append("\t\t$i = 0;")
    L.append("\t\twhile ( $i < count( $smin ) ) {")
    L.append("\t\t\tif ( $n >= $smin[ $i ] ) { $t = $rows[ $i ]; break; }")
    L.append("\t\t\t$i++;")
    L.append("\t\t}")
    L.append("\t\t/* 0 별명  1 훅  2·3·4 본문  5 요약  6 이모지")
    L.append("\t\t   본문은 점수 칸에서 꺼냅니다 — 이름이 스무 가지인데 글이")
    L.append("\t\t   다섯 가지면 아래쪽 여덟 칸이 전부 같은 글이 나옵니다. */")
    L.append("\t\treturn array( $b[2], $t[0], $b[3], $b[4], '', $b[0], $b[1] );")
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


def swap(path, head_marks, tail_mark, block, what):
    s = io.open(path, encoding='utf-8').read()
    a = -1
    for m in head_marks:
        if m in s:
            a = s.index(m)
            break
    if a < 0:
        raise SystemExit('★ ' + what + ' — 머리를 못 찾았습니다')
    b = s.index(tail_mark, a) + len(tail_mark)
    s2 = s[:a] + block + s[b:]
    io.open(path, 'w', encoding='utf-8').write(s2)
    print(what + '  ' + str(len(s)) + ' -> ' + str(len(s2)))


def main():
    swap(os.path.join(PHP, 'uandme_1_engine.WPCODE.txt'),
         ['/* ───── uandme-words.js ───── */',
          '/* ───── uandme-nick.js ───── */',
          END,
          'window.UANDME_TIER = function (score, rel) {'],
         END + '\n', js_block(), '자바스크립트')

    p = os.path.join(PHP, 'uandme_4_card.WPCODE.txt')
    s = io.open(p, encoding='utf-8').read()
    for m in ('/* ── 점수와 관계로 낱말 알아내기',
              '/* ── 점수와 관계로 별명 알아내기',
              '/* ── 점수로 등급 이름 알아내기'):
        if m in s:
            a = s.index(m)
            break
    else:
        raise SystemExit('★ PHP — 머리를 못 찾았습니다')
    end = s.index("\n}\n", s.index("function stella_um_tier", a)) + 3
    s2 = s[:a] + php_block() + s[end:]
    io.open(p, 'w', encoding='utf-8').write(s2)
    print('PHP           ' + str(len(s)) + ' -> ' + str(len(s2)))


if __name__ == '__main__':
    main()
