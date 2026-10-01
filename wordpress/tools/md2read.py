# -*- coding: utf-8 -*-
# 원고(.md) 를 읽기 쪽(.html) 으로 바꿉니다.
# 소희 님이 폰에서도 읽으시려고 만든 것입니다 (2026-10-01).
#   python3 wordpress/tools/md2read.py wordpress/drafts/투자운-원고.md wordpress/drafts/투자운-원고.html
#
# 하는 일 —
#   # 장 / ## 꼭지 로 차례를 만듭니다 (왼쪽에 붙어 따라다님)
#   들여쓴 문단은 들여쓰기를 떼어 보통 문단으로
#   공백으로 줄을 맞춘 표는 그대로 (가로로 밀 수 있게)
#   ★ ☞ × ○ 로 시작하는 줄은 「벼리 메모」로 색을 달리
#   **굵게** `코드` 만 바꿉니다
import io, re, sys, html, datetime

src = sys.argv[1]
dst = sys.argv[2]
raw = io.open(src, encoding='utf-8').read().replace('\r\n', '\n')

def inline(t):
    t = html.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]', r'<em class="tag">[\1]</em>', t)
    return t

MEMO = ('★', '☞', '×', '○')

lines = raw.split('\n')
out, toc = [], []
n_h1 = 0
n_h2 = 0
i = 0
buf = []        # 모으고 있는 문단
pre = []        # 모으고 있는 표

def flush_p():
    global buf
    if buf:
        rows = [x for x in buf if x.strip()]
        if rows:
            cls = ' class="memo"' if rows[0][:1] in MEMO else ''
            out.append('<p' + cls + '>' + '<br>'.join(inline(x) for x in rows) + '</p>')
        buf = []

def flush_pre():
    global pre
    if pre:
        while pre and not pre[-1].strip():
            pre.pop()
        out.append('<pre>' + html.escape('\n'.join(pre)) + '</pre>')
        pre = []

while i < len(lines):
    ln = lines[i]
    s = ln.strip()

    # 공백으로 맞춘 표 — 줄 안에 공백 세 칸 덩어리가 있고 글자가 둘 이상
    is_tbl = bool(re.search(r'\S {3,}\S', ln)) and not s.startswith('#')

    if is_tbl:
        flush_p()
        pre.append(re.sub(r'^ {0,2}', '', ln))
        i += 1
        continue

    if pre:
        # 표 안의 빈 줄 한 줄은 품습니다
        if not s and i + 1 < len(lines) and re.search(r'\S {3,}\S', lines[i + 1]):
            pre.append('')
            i += 1
            continue
        flush_pre()

    if not s:
        flush_p()
        i += 1
        continue

    if s.startswith('# '):
        flush_p()
        if i == 0:
            i += 1
            continue
        n_h1 += 1
        n_h2 = 0
        hid = 'c' + str(n_h1)
        ttl = s[2:].strip()
        toc.append((1, hid, re.sub(r'\s*\[[^\]]*\]\s*$', '', ttl)))
        out.append('<h2 id="' + hid + '">' + inline(ttl) + '</h2>')
        i += 1
        continue

    if s.startswith('## '):
        flush_p()
        n_h2 += 1
        hid = 'c' + str(n_h1) + '_' + str(n_h2)
        ttl = s[3:].strip()
        toc.append((2, hid, re.sub(r'\s*\[[^\]]*\]\s*$', '', ttl)))
        out.append('<h3 id="' + hid + '">' + inline(ttl) + '</h3>')
        i += 1
        continue

    if s.startswith('#'):
        flush_p()
        out.append('<h4>' + inline(s.lstrip('#').strip()) + '</h4>')
        i += 1
        continue

    if set(s) <= set('-') and len(s) >= 3:
        flush_p()
        out.append('<hr>')
        i += 1
        continue

    if s.startswith('> '):
        flush_p()
        q = []
        while i < len(lines) and lines[i].strip().startswith('> '):
            q.append(lines[i].strip()[2:])
            i += 1
        out.append('<blockquote>' + '<br>'.join(inline(x) for x in q) + '</blockquote>')
        continue

    # 번호 목록 · 점 목록은 한 줄씩 그대로 둡니다 (줄이 뜻을 가집니다)
    if re.match(r'^(\d+\.|[-*·])\s', s):
        flush_p()
        out.append('<p class="item">' + inline(s) + '</p>')
        i += 1
        continue

    # 메모 줄은 이어지는 들여쓴 줄까지 한 덩어리로
    if s[:1] in MEMO:
        flush_p()
        buf.append(s)
        i += 1
        while i < len(lines) and lines[i].startswith('  ') and lines[i].strip() \
                and lines[i].strip()[:1] not in MEMO and not re.search(r'\S {3,}\S', lines[i]):
            buf.append(lines[i].strip())
            i += 1
        flush_p()
        continue

    buf.append(s)
    i += 1

flush_p()
flush_pre()

tochtml = []
for lv, hid, ttl in toc:
    tochtml.append('<a class="t' + str(lv) + '" href="#' + hid + '">' + html.escape(ttl) + '</a>')

title = re.sub(r'^#\s*', '', raw.split('\n')[0]).strip()
stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
chars = len(re.sub(r'\s', '', raw))

page = u'''<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>''' + html.escape(title) + u'''</title>
<style>
:root{ --ink:#241F1A; --soft:#6B6054; --line:#E6DFD3; --bg:#FBF8F3;
       --memo:#8A6A3B; --memobg:#FAF3E6; --gold:#9C7B3F; }
*{ box-sizing:border-box; }
html{ scroll-behavior:smooth; }
body{ margin:0; background:var(--bg); color:var(--ink);
  font-family:'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  font-size:17px; line-height:1.95; }
.wrap{ max-width:1180px; margin:0 auto; display:flex; gap:40px; padding:0 22px; }
nav{ width:280px; flex:0 0 280px; position:sticky; top:0; align-self:flex-start;
  max-height:100vh; overflow-y:auto; padding:28px 0 60px; }
nav .navttl{ font-size:.78rem; letter-spacing:.14em; color:var(--gold);
  font-weight:700; padding:0 0 10px; }
nav a{ display:block; text-decoration:none; color:var(--soft);
  border-left:2px solid transparent; }
nav a:hover{ color:var(--ink); border-left-color:var(--gold); background:#FFFFFF; }
nav a.t1{ font-weight:700; color:var(--ink); font-size:.92rem;
  padding:9px 10px 7px; margin-top:8px; line-height:1.45; }
nav a.t2{ font-size:.82rem; padding:3px 10px 3px 20px; line-height:1.5; }
nav a.on{ color:var(--ink); border-left-color:var(--gold); background:#FFFFFF;
  font-weight:700; }
main{ flex:1 1 auto; min-width:0; padding:30px 0 140px; }
h1{ font-size:1.9rem; line-height:1.4; margin:10px 0 6px; letter-spacing:-.01em; }
.sub{ color:var(--soft); font-size:.86rem; margin:0 0 34px; }
h2{ font-size:1.42rem; line-height:1.45; margin:62px 0 18px;
  padding-top:16px; border-top:2px solid var(--ink); letter-spacing:-.01em; }
h3{ font-size:1.08rem; margin:40px 0 12px; color:var(--gold); }
h4{ font-size:.98rem; margin:26px 0 8px; }
p{ margin:0 0 16px; }
p.item{ margin:0 0 8px; padding-left:4px; }
p.memo{ background:var(--memobg); border-left:3px solid var(--memo);
  color:var(--memo); padding:12px 16px; margin:0 0 18px;
  font-size:.92rem; line-height:1.8; border-radius:0 6px 6px 0; }
strong{ font-weight:700; }
code{ font-size:.86em; background:#F0EBE1; padding:1px 5px; border-radius:4px; }
em.tag{ font-style:normal; font-size:.8em; color:var(--soft); }
pre{ background:#FFFFFF; border:1px solid var(--line); border-radius:8px;
  padding:16px 18px; overflow-x:auto; margin:0 0 20px;
  font-family:'Menlo','Consolas',monospace; font-size:.84rem; line-height:1.85;
  color:#352E26; }
blockquote{ margin:0 0 20px; padding:4px 0 4px 18px;
  border-left:3px solid var(--gold); color:#3A3229; }
hr{ border:0; border-top:1px solid var(--line); margin:34px 0; }
#top{ position:fixed; right:18px; bottom:18px; background:var(--ink);
  color:#FFFFFF; text-decoration:none; padding:10px 15px; border-radius:22px;
  font-size:.82rem; box-shadow:0 6px 18px -8px rgba(0,0,0,.5); }
@media(max-width:900px){
  .wrap{ display:block; padding:0 18px; }
  nav{ width:auto; flex:none; position:static; max-height:none;
    border-bottom:1px solid var(--line); padding:20px 0 16px; margin-bottom:6px; }
  nav .tocbox{ max-height:220px; overflow-y:auto; }
  nav a.t2{ display:none; }
  main{ padding-top:10px; }
  h2{ font-size:1.26rem; margin-top:46px; }
}
</style>
<div class="wrap">
<nav><div class="navttl">차례</div><div class="tocbox">
''' + '\n'.join(tochtml) + u'''
</div></nav>
<main>
<h1>''' + html.escape(title) + u'''</h1>
<p class="sub">''' + format(chars, ',') + u'''자 · 읽기 쪽 만든 시각 ''' + stamp + u'''</p>
''' + '\n'.join(out) + u'''
</main></div>
<a id="top" href="#">↑ 맨 위</a>
<script>
(function(){
  var links = {};
  var as = document.querySelectorAll('nav a');
  for (var i = 0; i < as.length; i++) {
    links[as[i].getAttribute('href').slice(1)] = as[i];
  }
  var hs = document.querySelectorAll('h2[id],h3[id]');
  var cur = null;
  function mark(el){
    if (el === cur) { return; }
    if (cur) { cur.className = cur.className.replace(' on', ''); }
    cur = el;
    if (cur) {
      cur.className = cur.className + ' on';
      var nav = document.querySelector('nav');
      var rn = nav.getBoundingClientRect();
      var rc = cur.getBoundingClientRect();
      if (rc.top < rn.top + 40) { nav.scrollTop = nav.scrollTop + (rc.top - rn.top) - 56; }
      if (rc.bottom > rn.bottom - 30) { nav.scrollTop = nav.scrollTop + (rc.bottom - rn.bottom) + 60; }
    }
  }
  function tick(){
    var best = null;
    for (var i = 0; i < hs.length; i++) {
      if (hs[i].getBoundingClientRect().top < 140) { best = hs[i]; }
    }
    mark(best ? links[best.id] : null);
  }
  var wait = 0;
  window.addEventListener('scroll', function(){
    if (wait) { return; }
    wait = setTimeout(function(){ wait = 0; tick(); }, 120);
  });
  tick();
})();
</script>
'''

io.open(dst, 'w', encoding='utf-8').write(page)
print(dst, len(page), 'bytes ·', len(toc), 'items in toc')
