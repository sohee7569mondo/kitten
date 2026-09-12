/* ══════════════════════════════════════════════════════════════
   유앤미 — 화면
   uandme-app.js · uandme-tiers.js · stella-saju.js · stella-match.js
   가 먼저 실려 있어야 합니다.
   주의 · 이 파일 안에서 앰퍼샌드 두 개 연산자를 쓰지 않습니다.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var U = window.UandMe, st = U.state, root = null;
  var BASE = location.origin + location.pathname;

  /* ── 옷 ──────────────────────────────────────────────── */
  var CSS = [
    '#um{--p:#B8A6E8;--pd:#6B5BA8;--bg:#F7F2FC;--ink:#3F3A52;--sub:#7C7392;--soft:#A79BC4;',
    'font-family:"Noto Sans KR","Apple SD Gothic Neo",sans-serif;background:var(--bg);',
    'color:#4A4358;max-width:420px;margin:0 auto;padding:0 0 56px;overflow:hidden;-webkit-text-size-adjust:100%}',
    '#um *{box-sizing:border-box}',
    /* 워드프레스 테마가 button 에 입히는 테두리·배경·그림자를 걷어냅니다.
       「누구랑 볼까요」 칸에 검정 테두리가 나오던 원인입니다. */
    '#um button{border:0;background:none;box-shadow:none;padding:0;margin:0;',
    'font-family:inherit;color:inherit;text-transform:none;letter-spacing:normal;',
    'border-radius:0;-webkit-appearance:none;appearance:none;cursor:pointer}',
    '#um button:hover,#um button:focus{border:0;box-shadow:none;outline:none}',
    '#um img{max-width:100%;height:auto;border:0;border-radius:0;box-shadow:none}',
    '#um .jua{font-family:Jua,"Noto Sans KR",sans-serif}',
    '#um .pad{padding-left:20px;padding-right:20px}',
    '#um .h1{font-family:Jua,"Noto Sans KR",sans-serif;font-size:34px;line-height:1.26;',
    'letter-spacing:-.02em;color:var(--ink)}',
    '#um .sub{font-size:14.5px;line-height:1.8;color:var(--sub);margin-top:12px}',
    '#um .lbl{font-size:12.5px;font-weight:700;color:#8C82A6;margin-bottom:8px}',
    '#um .card{background:#fff;border-radius:28px;padding:26px 22px;',
    'box-shadow:0 18px 34px -20px rgba(107,91,168,.4)}',
    '#um .btnP{display:flex;align-items:center;justify-content:center;height:56px;background:var(--p);',
    'color:#fff;border-radius:20px;font-family:Jua,"Noto Sans KR",sans-serif;font-size:16.5px;',
    'border:0;width:100%;cursor:pointer;box-shadow:0 10px 20px -12px rgba(107,91,168,.8)}',
    '#um .btnG{display:flex;align-items:center;justify-content:center;height:52px;background:#fff;',
    'color:var(--sub);border-radius:20px;font-size:14.5px;font-weight:500;border:0;width:100%;cursor:pointer}',
    '#um .chip{background:#fff;border:0;border-radius:999px;padding:12px 17px;font-size:13.5px;',
    'color:#57506E;cursor:pointer;font-family:inherit}',
    '#um .chip.on{background:var(--p);color:#fff;font-weight:700}',
    '#um .fld{height:54px;background:#fff;border:0;border-radius:18px;padding:0 16px;font-size:15px;',
    'color:var(--ink);width:100%;font-family:inherit;text-align:center}',
    '#um .fld::placeholder{color:#C3BAD6}',
    /* 칸을 누를 때 브라우저 기본 검은 테두리 대신 연보라 테두리 */
    '#um input:focus{outline:none;box-shadow:0 0 0 3px #DCD0F5}',
    '#um button:focus-visible{outline:none;box-shadow:0 0 0 3px #DCD0F5}',
    '#um .row{display:flex;gap:7px}',
    /* 한 줄에 놓인 칸은 폭을 0에서 시작해 고르게 나눠 갖습니다.
       이게 없으면 width:100% 때문에 뒷칸이 폭을 다 먹고 연도 칸이 찌그러집니다. */
    '#um .row>.fld{flex:1 1 0;min-width:0}',
    '#um .seg{flex:1;height:50px;background:#fff;border:0;border-radius:16px;font-size:14px;',
    'color:#57506E;cursor:pointer;font-family:inherit}',
    '#um .seg.on{background:var(--p);color:#fff;font-weight:700}',
    '#um .bar{height:9px;background:#EDE6F8;border-radius:99px;overflow:hidden}',
    '#um .bar i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#C3B2F0,#F4B9D4)}',
    '#um .sh{display:flex;flex-direction:column;align-items:center;gap:7px;flex:1;cursor:pointer;',
    'background:none;border:0;font-family:inherit;padding:0}',
    '#um .sh i{width:56px;height:56px;border-radius:20px;display:flex;align-items:center;justify-content:center}',
    '#um .sh span{font-size:11.5px;font-weight:700;color:#57506E}',
    /* 어두운 덮개 위에 뜨는 시트 안에서는 글씨가 하얘야 보입니다 */
    '#um #um-sheet .sh span{color:#F2EDFA}',
    '#um .stp{cursor:pointer;transition:transform .12s}',
    '#um .stp:active{transform:scale(.98)}',
    '#um .note{font-size:12px;line-height:1.85;color:var(--soft)}',
    '#um .mini{font-size:11.5px;line-height:1.9;color:#B3A9C9}',
    '@media(max-width:400px){#um .h1{font-size:31px}}',

    /* ── 이 페이지에서만 스텔라사주의 머리띠와 꼬리말을 감춥니다 ──
       body 에 um-page 가 붙은 화면에서만 먹으므로 다른 페이지는 그대로입니다. */
    'body.um-page header.wp-block-template-part,',
    'body.um-page footer.wp-block-template-part,',
    'body.um-page .wp-site-blocks>header,',
    'body.um-page .wp-site-blocks>footer,',
    'body.um-page .site-header,body.um-page .site-footer,',
    'body.um-page #masthead,body.um-page #colophon{display:none!important}',
    'body.um-page{background:#F7F2FC!important}',
    'body.um-page .wp-site-blocks{padding:0!important}',
    'body.um-page .entry-content,body.um-page .wp-block-post-content{',
    'margin:0!important;padding:0!important;max-width:none!important}',
    'body.um-page .wp-block-post-title{display:none!important}',

    /* ── 유앤미 머리말 ── */
    '#um-top{position:sticky;top:0;z-index:50;background:rgba(247,242,252,.92);',
    'backdrop-filter:saturate(160%) blur(10px);-webkit-backdrop-filter:saturate(160%) blur(10px)}',
    '#um-top .in{max-width:420px;margin:0 auto;padding:12px 20px;display:flex;',
    'align-items:center;justify-content:space-between}',
    '#um-top .lg{display:flex;align-items:center;gap:7px;text-decoration:none}',
    '#um-top .lg b{font-family:Jua,"Noto Sans KR",sans-serif;font-size:22px;color:#6B5BA8;font-weight:400}',
    '#um-top .lgi{display:block;height:34px;flex:0 0 auto}',
    /* 그림은 칸을 꽉 채우되 비율은 지킵니다. #um 밖(머리말)에서도 먹어야 해서
       #um 을 앞에 안 붙였습니다. */
    '.um-img{width:100%;height:100%;object-fit:contain;display:block}',
    '#um-top .lgi .um-img{height:34px;width:auto}',
    '#um-top .lgi svg{height:34px;width:34px;display:block}',
    '#um-top a.st{font-size:11.5px;font-weight:700;color:#A79BC4;text-decoration:none;',
    'background:#EDE6F8;padding:8px 13px;border-radius:999px}',

    /* ── 유앤미 꼬리말 ── */
    '#um-foot{max-width:420px;margin:0 auto;padding:38px 20px 46px}',
    '#um-foot .lk{display:flex;gap:8px;flex-wrap:wrap}',
    '#um-foot .lk a{flex:1;min-width:90px;text-align:center;background:#fff;border-radius:16px;',
    'padding:14px 10px;font-size:13px;font-weight:700;color:#57506E;text-decoration:none}',
    '#um-foot p{font-size:11.5px;line-height:1.9;color:#B3A9C9;margin:18px 0 0}'
  ].join('');

  function css() {
    if (document.getElementById('um-css')) { return; }
    var s = document.createElement('style');
    s.id = 'um-css'; s.textContent = CSS;
    document.head.appendChild(s);
    var f = document.createElement('link');
    f.rel = 'stylesheet';
    f.href = 'https://fonts.googleapis.com/css2?family=Jua' + '&' + 'display=swap';
    document.head.appendChild(f);
  }

  function el(html) {
    var d = document.createElement('div');
    d.innerHTML = html;
    return d.firstElementChild;
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[<>"']/g, function (c) {
      return { '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function on(sel, ev, fn) {
    var n = root.querySelectorAll(sel), i;
    for (i = 0; i < n.length; i++) { n[i].addEventListener(ev, fn); }
  }

  /* ── 아이콘 ──────────────────────────────────────────── */
  var IC = {
    talk: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#3F2A08" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-9 8.4a9.7 9.7 0 0 1-2.7-.4L3 21l1.6-4.1A8.2 8.2 0 0 1 3 11.5a8.4 8.4 0 0 1 9-8.4a8.4 8.4 0 0 1 9 8.4z"/></svg>',
    at:   '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-4 8"/></svg>',
    cam:  '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/></svg>',
    link: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#6B5BA8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg>',
    ex:   '<svg width="23" height="23" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.3" stroke-linecap="round"><path d="M4.5 4.5l15 15M19.5 4.5l-15 15"/></svg>',
    save: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#4F937A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'
  };

  window.UandMeUI = { css: css, el: el, esc: esc, on: on, IC: IC, CSS: CSS,
                      base: function () { return BASE; },
                      setRoot: function (r) { root = r; },
                      getRoot: function () { return root; } };
})();
