# -*- coding: utf-8 -*-
"""labindex.html 을 워드프레스 **페이지**에 들어갈 블록으로 바꿉니다.

왜 페이지인가 —
  지금은 조각(snip_lab_index)이 /lab/ 주소를 가로채서 그립니다.
  조각 하나만 꺼지면 옛 목록이 나옵니다. 2026-09-16 에 실제로
  그렇게 됐습니다. 페이지로 두면 조각과 무관하게 남습니다.

무엇을 손보나 (lab/README.md 의 규칙 그대로) —
  · <!DOCTYPE> · <html> · <head> · <body> 를 걷어냅니다
  · 글꼴 <link> 를 <style> 안의 @import 로 옮깁니다
    (워드프레스는 <link> 를 지웁니다)
  · 겉모습 규칙을 전부 .stq-lab 안쪽으로 묶습니다
    (안 그러면 .card · .nav 같은 흔한 이름이 테마를 덮습니다)
  · 두 겹 앰퍼샌드가 있는지 셉니다 (워드프레스가 바꿔치기해 죽입니다)
"""
import io, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, 'labindex.html')
DST  = os.path.join(HERE, 'index.block.html')

FONTS = ("@import url('https://fonts.googleapis.com/css2"
         "?family=Gaegu:wght@400;700"
         "&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');")


def split_rules(css):
    """중괄호를 세어 위 층 덩어리로 가릅니다. @media 는 안으로 들어갑니다."""
    out, buf, depth = [], '', 0
    for ch in css:
        buf += ch
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                out.append(buf)
                buf = ''
    if buf.strip():
        out.append(buf)
    return out


def scope_sel(sel):
    s = sel.strip()
    if not s:
        return s
    if s.startswith('.stq-lab'):
        return s
    if s == '*':
        return '.stq-lab *'
    if s in ('html', 'body', 'html,body'):
        return '.stq-lab'
    return '.stq-lab ' + s


def scope(css):
    out = []
    for rule in split_rules(css):
        m = re.match(r'^(\s*)([^{]+)\{([\s\S]*)\}\s*$', rule)
        if not m:
            out.append(rule)
            continue
        pre, sel, body = m.group(1), m.group(2).strip(), m.group(3)
        if sel.startswith('@media'):
            out.append(pre + sel + '{' + scope(body) + '}\n')
            continue
        if sel.startswith('@'):
            out.append(rule)
            continue
        if sel == ':root':
            # 낱말값은 .stq-lab 에 담아 밖으로 안 새게 합니다
            out.append(pre + '.stq-lab{' + body + '}\n')
            continue
        parts = [scope_sel(x) for x in sel.split(',')]
        # html,body 처럼 둘이 같은 것으로 접히면 하나만 남깁니다
        seen, keep = {}, []
        for p in parts:
            if p in seen:
                continue
            seen[p] = 1
            keep.append(p)
        out.append(pre + ','.join(keep) + '{' + body + '}\n')
    return ''.join(out)


def main():
    s = io.open(SRC, encoding='utf-8').read()

    css = re.findall(r'<style>([\s\S]*?)</style>', s)
    js  = re.findall(r'<script>([\s\S]*?)</script>', s)
    if len(css) != 1:
        print('★ <style> 가 하나가 아닙니다 : %d' % len(css)); sys.exit(1)
    if len(js) != 1:
        print('★ <script> 가 하나가 아닙니다 : %d' % len(js)); sys.exit(1)

    body = s[s.index('<body'):]
    body = body[body.index('>') + 1:]
    body = body[:body.index('</body>')]
    body = re.sub(r'<style>[\s\S]*?</style>', '', body)
    body = re.sub(r'<script>[\s\S]*?</script>', '', body)

    stamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')

    # ★★ 테마가 같은 이름을 쓰면 **우리 쪽으로 새어듭니다.**
    #   크로미움으로 그려 보고 찾았습니다 — 테마에
    #   .card{border:6px solid red} 를 넣었더니 우리 카드에도
    #   빨간 테두리가 그려졌습니다. .card 는 아주 흔한 이름입니다.
    #   우리 CSS 가 border 를 안 정하니 테마 것이 그대로 이깁니다.
    #   그래서 **우리 규칙보다 먼저** 한 번 비워 둡니다.
    #   (뒤에 오는 우리 규칙이 필요한 값을 다시 얹습니다)
    names = sorted(set(re.findall(r'class=["\']([^"\']+)["\']', body)))
    cls = sorted(set(c for row in names for c in row.split() if c))
    reset = (',\n'.join('.stq-lab .' + c for c in cls)
             + '{border:0;margin:0;padding:0;background:none;box-shadow:none;'
               'float:none;max-width:none;min-height:0;min-width:0;'
               'text-transform:none;letter-spacing:normal;list-style:none;}')

    out = (
        '<!-- 스텔라 랩 목록 · 페이지 블록 · 판 ' + stamp + ' -->\n'
        '<!-- /lab/ 페이지 → 블록 추가 → 「사용자 정의 HTML」 → 이 파일 통째로 -->\n'
        '<style>\n' + FONTS + '\n'
        + '/* 테마가 같은 이름을 쓸 때를 대비해 먼저 비웁니다 */\n'
        + reset + '\n' + scope(css[0]).strip() + '\n</style>\n\n'
        '<div class="stq-lab">\n' + body.strip() + '\n</div>\n\n'
        '<script>\n' + js[0].strip() + '\n</script>\n'
    )

    io.open(DST, 'w', encoding='utf-8').write(out)

    # ── 검사 ────────────────────────────────────────────
    bad = []
    if '<!DOCTYPE' in out: bad.append('DOCTYPE 가 남았습니다')
    if '<html' in out:     bad.append('<html> 이 남았습니다')
    if '<body' in out:     bad.append('<body> 가 남았습니다')
    if '<link' in out:     bad.append('<link> 가 남았습니다 (워드프레스가 지웁니다)')
    jsout = re.findall(r'<script>([\s\S]*?)</script>', out)[0]
    if ('&' + '&') in jsout: bad.append('스크립트에 두 겹 앰퍼샌드가 있습니다')
    if chr(92) in jsout:     bad.append('스크립트에 홑 역빗금이 있습니다')
    cssout = re.findall(r'<style>([\s\S]*?)</style>', out)[0]

    # ★ 검사도 중괄호를 세어야 합니다. 줄바꿈이 든 선택자
    #   (.stq-lab .wrap,\n.stq-lab .hello{ …) 를 정규식으로 보면
    #   마지막 줄만 잡혀 「울타리 밖」이라고 거짓말을 합니다.
    loose = []
    def walk(css):
        for rule in split_rules(css):
            m = re.match(r'^(\s*)([^{]+)\{([\s\S]*)\}\s*$', rule)
            if not m:
                continue
            sel, inner = m.group(2).strip(), m.group(3)
            if sel.startswith('@media'):
                walk(inner)
                continue
            if sel.startswith('@'):
                continue
            loose.append(sel)
            for one in sel.split(','):
                if not one.strip().startswith('.stq-lab'):
                    bad.append('울타리 밖 규칙 : ' + one.strip()[:40])
    walk(cssout)

    print('%s · %d바이트' % (os.path.basename(DST), len(out.encode('utf-8'))))
    print('규칙 %d개 · 모두 .stq-lab 안' % len(loose))
    if bad:
        print('\n★ 걸린 것 %d :' % len(bad))
        for b in bad:
            print('   ' + b)
        sys.exit(1)
    print('검사 통과')


if __name__ == '__main__':
    main()
