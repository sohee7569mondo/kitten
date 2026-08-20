# -*- coding: utf-8 -*-
"""door-career.html 을 틀로 나머지 다섯 분의 가디언 페이지를 찍어냅니다.
   사용법: python3 build_doors.py   (wordpress/pages 에 덮어씁니다)"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guardians import GUARDIANS

PAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pages')
MASTER = os.path.join(PAGES, 'door-career.html')

def cut(text, start, end, what):
    """start 로 시작해 end 로 끝나는 한 덩어리를 찾아 (앞, 덩어리, 뒤) 로 나눕니다."""
    i = text.index(start)
    j = text.index(end, i) + len(end)
    return text[:i], text[i:j], text[j:]

def replace_block(text, start, end, new, what):
    a, old, b = cut(text, start, end, what)
    return a + new + b

def step2(g):
    opts = '\n'.join(
        '                <option value="%s">%s</option>' % (o, o) for o in g['f2_opts'])
    return (
'''<section class="step">
          <div class="step-head">
            <span class="step-no">STEP 2</span>
            <span class="step-title">%(t)s</span>
            <span class="step-sub">선택</span>
          </div>
          <div class="frow">
            <div class="f"><label for="gJob">%(f1)s</label>
              <input type="text" id="gJob" maxlength="40" placeholder="%(f1p)s"></div>
            <div class="f"><label for="gYears">%(f2)s</label>
              <select id="gYears">
                <option value="">고르기</option>
%(opts)s
              </select></div>
          </div>
          <div class="frow one">
            <div class="f"><label for="gWant">%(f3)s</label>
              <input type="text" id="gWant" maxlength="40" placeholder="%(f3p)s"></div>
          </div>
          <p class="hint">%(hint)s</p>
        </section>''' % dict(t=g['step2_title'], f1=g['f1_label'], f1p=g['f1_ph'],
                             f2=g['f2_label'], opts=opts,
                             f3=g['f3_label'], f3p=g['f3_ph'], hint=g['hint']))

def topics(g):
    rows = []
    for n, t in enumerate(g['topics']):
        chk = ' checked' if n == 0 else ''
        rows.append('            <label class="topic"><input type="radio" name="ssg-topic" '
                    'value="%s"%s><span>%s</span></label>' % (t, chk, t))
    return '<div class="topics">\n' + '\n'.join(rows) + '\n          </div>'

def deeps(g):
    rows = []
    for title, desc in g['deeps']:
        rows.append(
'            <label class="deep"><input type="checkbox" class="deep-c" value="%s">\n'
'              <span><span class="deep-t">%s</span><span class="deep-d">%s</span></span>\n'
'              <span class="deep-p">체험판 무료</span></label>' % (title, title, desc))
    return '<div id="deeps">\n' + '\n'.join(rows) + '\n          </div>'

def build(master, g):
    s = master

    # 머리말 주석
    s = s.replace('  STELLA SAJU — 직성의 신 (THE ARCHITECT) · 일과 돈',
                  '  STELLA SAJU — ' + g['head'])
    s = s.replace('  가디언 상세페이지 공통 틀  BUILD: G9',
                  '  이 파일은 자동 생성됩니다. 여기서 직접 고치지 마세요.\n'
                  '  고칠 일이 있으면 door-career.html(틀) 이나 build/guardians.py(내용) 를\n'
                  '  고친 뒤 build/build_doors.py 를 다시 돌리면 여섯 장이 한꺼번에 맞춰집니다.\n'
                  '  BUILD: G9')
    # 틀에만 필요한 안내(다른 가디언 만드는 법)는 생성본에서 덜어냅니다
    s = replace_block(s, '  [다른 가디언 만들 때]', '(가디언 색)\n', '', 'howto')

    # 색 · 얼굴 · 이름
    s = s.replace('style="--g-accent:#C9A66B"', 'style="--g-accent:%s"' % g['accent'])
    s = s.replace('uploads/2026/08/stellardoorarchitect.jpg',
                  'uploads/2026/08/%s' % g['img'])
    s = s.replace('alt="직성의 신" width="784" height="1168"',
                  'alt="%s" width="%d" height="%d"' % (g['name'], g['img_w'], g['img_h']))
    s = s.replace('<div class="g-theme">The Architect</div>',
                  '<div class="g-theme">%s</div>' % g['theme'])
    s = s.replace('<div class="g-name">직성의 신</div>',
                  '<div class="g-name">%s</div>' % g['name'])
    s = s.replace('<div class="g-en">Career and Wealth</div>',
                  '<div class="g-en">%s</div>' % g['en'])

    s = replace_block(s, '<p class="g-greet">', '</p>',
                      '<p class="g-greet">%s</p>' % g['greet'], 'greet')
    s = replace_block(s, '<p class="g-intro">', '</p>',
                      '<p class="g-intro">%s</p>' % g['intro'], 'intro')
    s = replace_block(s, '<div class="g-method-t">이렇게 읽습니다</div>', '</p>',
                      '<div class="g-method-t">이렇게 읽습니다</div>\n            <p>%s</p>'
                      % g['method'], 'method')

    s = replace_block(s, '<section class="step">\n          <div class="step-head">\n'
                         '            <span class="step-no">STEP 2</span>',
                      '</section>', step2(g), 'step2')
    s = replace_block(s, '<div class="topics">', '</div>', topics(g), 'topics')
    s = replace_block(s, '<div id="deeps">', '</label>\n          </div>', deeps(g), 'deeps')

    s = s.replace('placeholder="예: 올해 안에 이직해도 괜찮을까요?"',
                  'placeholder="%s"' % g['oneline_ph'])
    s = s.replace('<button type="button" class="go" id="goBtn">직성의 신에게 물어보기 →</button>',
                  '<button type="button" class="go" id="goBtn">%s</button>' % g['btn'])
    s = s.replace("guardian:'직성의 신', guardian_slug:'door-career'",
                  "guardian:'%s', guardian_slug:'%s'" % (g['name'], g['slug']))
    return s

def main():
    master = open(MASTER, encoding='utf-8').read()
    for g in GUARDIANS:
        out = build(master, g)
        # 안전장치 — 직성의 신 흔적이 남아 있으면 멈춥니다
        for bad in ['직성의 신', 'door-career', 'stellardoorarchitect', 'The Architect']:
            if bad in out.replace('door-career.html', ''):
                raise SystemExit('!! %s 에 "%s" 가 남아 있습니다' % (g['slug'], bad))
        path = os.path.join(PAGES, g['slug'] + '.html')
        open(path, 'w', encoding='utf-8').write(out)
        print('%-14s %6d bytes' % (g['slug'] + '.html', len(out)))

main()
