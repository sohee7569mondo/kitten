#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
덤 두 쪽(별자리·띠)의 글 표를 원고에서 바로 만들어
patch160_tailrun.WPCODE.txt 의 var ZO / var DD 자리에 넣습니다.

  원고  wordpress/drafts/별자리-맺음앞-원고.md   → ZO   (21 주제 × 12 자리)
  원고  wordpress/drafts/띠-원고.md              → DD   (21 주제 × 12 띠)

손으로 표를 옮기지 않습니다. 원고를 고치고 이 파일을 돌리면 조각이 새로 만들어집니다.

    python3 wordpress/php/patch160_tailrun.build.py

★ 집 규칙 세 가지를 여기서 지킵니다.
  · 홑따옴표를 쓰지 않습니다 (JS 글자값을 홑따옴표로 감싸므로)
  · 「&」를 쓰지 않습니다 (워드프레스가 &#038; 로 바꿉니다)
  · 역슬래시를 쓰지 않습니다 (저장할 때 벗겨집니다)
  셋 중 하나라도 원고에 있으면 여기서 멈추고 어디인지 알려줍니다.
"""
import json, re, sys, pathlib

HERE  = pathlib.Path(__file__).resolve().parent
ROOT  = HERE.parent                      # wordpress/
DRAFT = ROOT / 'drafts'
OUT   = HERE / 'patch160_tailrun.WPCODE.txt'

NUM = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑'


def parse(path):
    """원고 한 편을 { 주제 : {q:질문, c:{ 자리 : [부제, html] } } } 로 읽습니다.

    원고의 모양 —
        # ⑨ 취업운 · 어떤 자리에서 내 장점이 먼저 보이는가   ← 주제 (질문은 있을 때만)
        ### 양자리 · 먼저 해보는 사람                        ← 한 칸 (부제는 있을 때만)
        본문 문단                                            → <p>…</p>
        **맺음 한 줄**                                       → <p class="cl"><strong>…</strong></p>
    맨 위 제목과 「## …」로 적은 집필 지침은 읽지 않습니다.
    """
    text = path.read_text(encoding='utf-8')
    table, topic, key, sub, buf = {}, None, None, '', []

    def flush():
        if topic is None or key is None:
            return
        html = []
        for para in [x.strip() for x in buf if x.strip()]:
            if para.startswith('**') and para.endswith('**'):
                html.append('<p class="cl"><strong>' + para[2:-2].strip() + '</strong></p>')
            else:
                html.append('<p>' + para + '</p>')
        table[topic]['c'][key] = [sub, ''.join(html)]

    def split_dot(head):
        if ' · ' in head:
            a, b = head.split(' · ', 1)
            return a.strip(), b.strip()
        return head.strip(), ''

    for raw in text.splitlines():
        line = raw.rstrip()

        m = re.match(r'^###\s+(.+)$', line)
        if m:
            flush(); buf = []
            key, sub = split_dot(m.group(1))
            continue

        m = re.match(r'^#\s+(.+)$', line)
        if m:
            head = m.group(1).strip()
            if not head or head[0] not in NUM:
                continue                      # 맨 위 제목
            flush(); buf = []; key = None; sub = ''
            topic, q = split_dot(head[1:].strip())
            table[topic] = {'q': q, 'c': {}}
            continue

        if re.match(r'^##\s', line):         # 집필 지침 — 표에 넣지 않습니다
            flush(); buf = []; key = None; topic = None
            continue

        if key is not None:
            buf.append(line)

    flush()
    return table


def jstr(s):
    return "'" + s + "'"


def emit(name, table, with_q):
    """JS 표로 적습니다.

    ZO 는 질문을 함께 답니다 :  '연애운':{q:'…',long:1,c:{ '양자리':[부제,글], … }}
    DD 는 질문이 없어 평평합니다 :  '연애운':{ '쥐띠':[부제,글], … }
    ★ 책의 코드가 ZO[주제].c[자리] · DD[주제][띠] 로 찾습니다. 모양을 바꾸면 안 됩니다.
    """
    lines = ['  var %s={' % name]
    tl = list(table.items())
    for ti, (topic, v) in enumerate(tl):
        if with_q:
            lines.append('  ' + jstr(topic) + ':{q:' + jstr(v['q']) + ',long:1,c:{')
            close = '  }}'
        else:
            lines.append('  ' + jstr(topic) + ':{')
            close = '  }'
        cl = list(v['c'].items())
        for ci, (k, (sub, html)) in enumerate(cl):
            tail = ',' if ci < len(cl) - 1 else ''
            lines.append('    ' + jstr(k) + ':[' + jstr(sub) + ',' + jstr(html) + ']' + tail)
        lines.append(close + (',' if ti < len(tl) - 1 else ''))
    lines.append('};')
    return '\n'.join(lines)


def guard(name, table):
    bad = []
    for t, v in table.items():
        if len(v['c']) != 12:
            bad.append('%s %s 칸이 %d개' % (name, t, len(v['c'])))
        for k, (sub, html) in v['c'].items():
            for ch, why in (("'", '홑따옴표'), ('&', '앰퍼샌드'), ('\\', '역슬래시')):
                if ch in sub or ch in html:
                    bad.append('%s %s %s 에 %s' % (name, t, k, why))
            if 'class="cl"' not in html:
                bad.append('%s %s %s 맺음말 없음' % (name, t, k))
    return bad


def splice(src, name, block):
    start = src.index('  var %s={\n' % name)
    end = src.index('\n};\n', start) + len('\n};\n')
    return src[:start] + block + '\n' + src[end:]


def main():
    zo = parse(DRAFT / '별자리-맺음앞-원고.md')
    dd = parse(DRAFT / '띠-원고.md')

    # 칸이 하나도 없는 목(아직 책에 안 넣은 글)은 표에서 뺍니다.
    for name, table in (('별자리', zo), ('띠', dd)):
        for t in [t for t, v in table.items() if not v['c']]:
            print('표에서 뺐습니다 (칸 없음) :', name, t)
            del table[t]

    bad = guard('별자리', zo) + guard('띠', dd)
    if bad:
        print('멈춥니다 — 원고에 손볼 곳이 있습니다')
        for b in bad:
            print('  ·', b)
        sys.exit(1)

    src = OUT.read_text(encoding='utf-8')
    src = splice(src, 'ZO', emit('ZO', zo, True))
    src = splice(src, 'DD', emit('DD', dd, False))
    OUT.write_text(src, encoding='utf-8')

    print('별자리 %2d 주제 %3d 칸' % (len(zo), sum(len(v['c']) for v in zo.values())))
    print('띠     %2d 주제 %3d 칸' % (len(dd), sum(len(v['c']) for v in dd.values())))
    print('만들었습니다 :', OUT.name, '%.0f KB' % (OUT.stat().st_size / 1024))
    json.dump(zo, open('/tmp/ZO.json', 'w'), ensure_ascii=False)
    json.dump(dd, open('/tmp/DD.json', 'w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
