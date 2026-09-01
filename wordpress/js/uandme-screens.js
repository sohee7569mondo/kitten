/* ══════════════════════════════════════════════════════════════
   유앤미 — 화면 다섯과 공유
   주의 · 이 파일 안에서 앰퍼샌드 두 개 연산자를 쓰지 않습니다.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var U = window.UandMe, X = window.UandMeUI, st = U.state;
  var el = X.el, esc = X.esc, IC = X.IC;
  var root = null;

  /* ── 들어올 때의 장막 ────────────────────────────────────
     워드프레스가 자기 화면을 먼저 그리고 나서야 우리 코드가 도는
     탓에, 그 사이 스텔라사주 첫 화면이 깜빡 비칩니다. 들어오는
     즉시 파스텔 여백으로 덮어두었다가 우리 화면이 다 그려지면
     걷습니다. 혹시 무슨 일이 나도 4초 뒤에는 반드시 걷힙니다. */
  function veilOn() {
    if (document.getElementById('um-veil')) { return; }
    var st2 = document.createElement('style');
    st2.id = 'um-veil';
    st2.textContent = 'html.um-load::before{content:"";position:fixed;left:0;top:0;' +
      'right:0;bottom:0;background:#F7F2FC;z-index:2147483646;pointer-events:none}';
    (document.head || document.documentElement).appendChild(st2);
    document.documentElement.className += ' um-load';
    setTimeout(veilOff, 4000);
  }
  function veilOff() {
    var d = document.documentElement;
    d.className = d.className.replace(/\s*\bum-load\b/g, '');
  }
  veilOn();

  function go(v) { st.view = v; render(); window.scrollTo(0, 0); }

  /* ── 공유 ────────────────────────────────────────────── */
  function inviteUrl() { return X.base() + '?i=' + U.packLink(st.rel, st.me); }
  function resultUrl() {
    var u = X.base() + '?r=' + U.packLink(st.rel, st.me, st.you);
    /* 점수를 같이 실어 둡니다. 이러면 링크를 스레드·X·디스코드 어디에
       붙여도 그쪽에서 우리 점수 카드를 미리 보여줍니다.
       생년월일은 앞의 r 안에만 있고 여기에는 점수뿐입니다. */
    if (st.result) {
      var r = st.result, t = '';
      try { t = window.UANDME_TIER(r.total, st.rel).title || ''; } catch (e) { t = ''; }
      /* 「s」 는 워드프레스가 검색어로 알아듣는 이름이라 페이지가 404 가
         됩니다. 크롤러는 404 페이지의 og 를 버리므로 「sc」 로 씁니다. */
      u += '&sc=' + r.total +
           '&a=' + r.blocks.saju.score +
           '&b=' + r.blocks.zodiac.score +
           '&c=' + r.blocks.animal.score +
           '&t=' + encodeURIComponent(t);
    }
    return u;
  }

  function shareText() {
    if (!st.result) { return '우리 궁합 몇 점일까?'; }
    var t = window.UANDME_TIER(st.result.total, st.rel);
    return '우리 ' + st.result.total + '점 · ' + t.title;
  }

  function nativeShare(url, text) {
    if (navigator.share) {
      navigator.share({ title: '유앤미', text: text, url: url })
        .catch(function () {});
      return true;
    }
    return false;
  }
  function copy(url) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(function () { toast('링크를 복사했어요'); },
        function () { prompt('이 주소를 복사하세요', url); });
    } else { prompt('이 주소를 복사하세요', url); }
  }
  function threads(url, text) {
    var q = 'text=' + encodeURIComponent(text + '\n' + url);
    window.open('https://www.threads.net/intent/post?' + q, '_blank', 'noopener');
  }
  function xpost(url, text) {
    /* 물음표 뒤에 값 하나만 넘깁니다 — 주소에 앰퍼샌드를 안 쓰려고요 */
    var q = 'text=' + encodeURIComponent(text + '\n' + url);
    window.open('https://twitter.com/intent/tweet?' + q, '_blank', 'noopener');
  }
  /* 카카오 SDK — 설정에 키가 있을 때만 불러옵니다 */
  function kakaoKey() {
    if (!window.UM_SET) { return ''; }
    if (!window.UM_SET.설정) { return ''; }
    return window.UM_SET.설정.카카오키 || '';
  }
  function kakaoPic() {
    /* 점수가 나왔으면 그 점수로 그린 카드를 보냅니다.
       주소를 부르면 서버가 그 자리에서 800x400 그림을 그려 줍니다
       (④번 스니펫). 아무것도 남기지 않고 이름도 담기지 않습니다. */
    if (st.result) {
      var u = cardCdn();
      if (u) { return u; }
    }
    if (!window.UM_SET) { return ''; }
    if (!window.UM_SET.설정) { return ''; }
    return window.UM_SET.설정.카톡그림 || '';
  }
  function cardName() {
    if (!st.result) { return ''; }
    var r = st.result;
    return r.total + '-' + st.rel + '-' + r.blocks.saju.score + '-' +
      r.blocks.zodiac.score + '-' + r.blocks.animal.score;
  }
  /* 우리 서버가 그 자리에서 그려 주는 주소 */
  function cardUrl() {
    var n = cardName();
    return n ? (location.origin + '/um-card/' + n) : '';
  }
  /* 워드프레스닷컴 그림 CDN 주소 — 카카오가 우리 서버에서는 그림을
     못 가져가는 듯하여 이쪽을 알려줍니다. 위 주소를 한 번 부르면
     서버가 파일로 남겨 두므로 CDN 이 그것을 나릅니다. */
  function cardCdn() {
    var n = cardName();
    if (!n) { return ''; }
    var host = location.host;
    if (!host) { return cardUrl(); }
    return 'https://i0.wp.com/' + host +
      '/wp-content/uploads/uandme/card/' + n + '.png?ssl=1';
  }
  /* 결과가 나오면 카드를 미리 한 번 그려 둡니다 (파일로 남게) */
  function cardWarm() {
    var u = cardUrl();
    if (!u) { return; }
    try { var im = new Image(); im.src = u; } catch (e) {}
  }

  function kakaoReady() {
    if (!window.Kakao) { return false; }
    if (!window.Kakao.Share) { return false; }
    try { return window.Kakao.isInitialized(); } catch (e) { return false; }
  }
  function loadKakao() {
    var key = kakaoKey();
    if (!key) { return; }
    function boot() {
      try { if (!window.Kakao.isInitialized()) { window.Kakao.init(key); } } catch (e) {}
    }
    if (window.Kakao) { boot(); return; }
    var sc = document.createElement('script');
    sc.src = 'https://t1.kakaocdn.net/kakao_js_sdk/2.7.2/kakao.min.js';
    sc.onload = boot;
    document.head.appendChild(sc);
  }

  /* 카톡 카드에 들어갈 속 이야기 — 점수가 있으면 알맹이를 넣습니다 */
  function kakaoDesc() {
    if (!st.result) {
      return '사주 · 별자리 · 띠 셋을 함께 봅니다. 생일만 넣으면 바로 나와요';
    }
    var r = st.result;
    return '사주 ' + r.blocks.saju.score + '/40 · 별자리 ' + r.blocks.zodiac.score +
      '/30 · 띠 ' + r.blocks.animal.score + '/30\n' +
      '성격 ' + r.categories.personality + ' 연애 ' + r.categories.love +
      ' 결혼 ' + r.categories.marriage + ' 금전 ' + r.categories.money;
  }

  function kakao(url, text) {
    if (kakaoReady()) {
      try {
        window.Kakao.Share.sendDefault({
          objectType: 'feed',
          content: {
            title: text || '우리 궁합 몇 점일까?',
            description: kakaoDesc(),
            imageUrl: kakaoPic(),
            imageWidth: 800,
            imageHeight: 400,
            link: { mobileWebUrl: url, webUrl: url }
          },
          buttons: [{ title: st.result ? '나도 해보기' : '내 생일 넣기',
                      link: { mobileWebUrl: url, webUrl: url } }]
        });
        return;
      } catch (e) {}
    }
    copy(url);
    toast('링크를 복사했어요. 카카오톡에 붙여넣어 보내세요');
  }

  function toast(msg) {
    var t = el('<div style="position:fixed;left:50%;bottom:34px;transform:translateX(-50%);' +
      'background:#3F3A52;color:#fff;padding:13px 20px;border-radius:16px;font-size:14px;' +
      'z-index:99999;box-shadow:0 10px 24px -10px rgba(0,0,0,.5)">' + esc(msg) + '</div>');
    document.body.appendChild(t);
    setTimeout(function () { t.remove(); }, 2200);
  }

  /* ── 자랑용 그림 만들기 ──────────────────────────────── */
  function makeImage(cb) {
    /* 결과가 아직 없으면(초대 화면) 초대용 그림을 그립니다 */
    if (!st.result) { makeInvite(cb); return; }
    /* 캐릭터를 먼저 받아두고 나서 그립니다 */
    var slotA = REL_PIC[st.rel] || '연인';
    loadPics([slotA, '__lucky'], function (P) { drawResult(P, cb); });
  }
  function drawResult(P, cb) {
    var W = 1080, H = 1350;
    var c = document.createElement('canvas');
    c.width = W; c.height = H;
    var g = c.getContext('2d');

    var bg = g.createLinearGradient(0, 0, W, H);
    bg.addColorStop(0, '#FBF6FF'); bg.addColorStop(0.55, '#F0E6FB'); bg.addColorStop(1, '#FFEDE2');
    g.fillStyle = bg; g.fillRect(0, 0, W, H);

    var r = st.result, tier = window.UANDME_TIER(r.total, st.rel);
    g.textAlign = 'center';

    g.fillStyle = '#A79BC4'; g.font = '600 34px "Noto Sans KR",sans-serif';
    g.fillText('유앤미 · ' + U.relKo(st.rel) + ' 궁합', W / 2, 130);

    var who = (st.me.name || '나') + ' × ' + (st.you.name || '너');
    g.fillStyle = '#8C82A6'; g.font = '500 38px "Noto Sans KR",sans-serif';
    g.fillText(who, W / 2, 205);

    /* 큰 점수 좌우로 둘이 마주봅니다 */
    var slotA2 = REL_PIC[st.rel] || '연인';
    drawPic(g, P[slotA2], 166, 448, 280, 250);
    drawPic(g, P['__lucky'], 914, 448, 280, 250);

    g.fillStyle = '#6B5BA8'; g.font = '700 300px Jua,"Noto Sans KR",sans-serif';
    g.fillText(String(r.total), W / 2, 520);
    g.fillStyle = '#A79BC4'; g.font = '500 44px "Noto Sans KR",sans-serif';
    g.fillText('점', W / 2, 585);

    g.fillStyle = '#3F3A52'; g.font = '700 76px Jua,"Noto Sans KR",sans-serif';
    g.fillText(tier.title, W / 2, 700);

    /* 세 덩어리 막대 */
    var blocks = [['사주', r.blocks.saju.score, 40], ['별자리', r.blocks.zodiac.score, 30],
                  ['띠', r.blocks.animal.score, 30]];
    var y = 800, i;
    for (i = 0; i < blocks.length; i++) {
      var b = blocks[i];
      g.textAlign = 'left';
      g.fillStyle = '#8C82A6'; g.font = '700 32px "Noto Sans KR",sans-serif';
      g.fillText(b[0], 120, y - 14);
      g.textAlign = 'right';
      g.fillStyle = '#6B5BA8'; g.font = '700 32px "Noto Sans KR",sans-serif';
      g.fillText(b[1] + ' / ' + b[2], 960, y - 14);
      g.fillStyle = '#EAE0F7';
      rr(g, 120, y, 840, 22, 11); g.fill();
      var gg = g.createLinearGradient(120, 0, 960, 0);
      gg.addColorStop(0, '#C3B2F0'); gg.addColorStop(1, '#F4B9D4');
      g.fillStyle = gg;
      rr(g, 120, y, Math.max(24, 840 * (b[1] / b[2])), 22, 11); g.fill();
      y += 92;
    }

    /* 네 항목 */
    var cats = [['성격', r.categories.personality], ['연애', r.categories.love],
                ['결혼', r.categories.marriage], ['금전', r.categories.money]];
    var bx = 120, bw = (840 - 3 * 18) / 4;
    for (i = 0; i < 4; i++) {
      g.fillStyle = 'rgba(255,255,255,.85)';
      rr(g, bx, 1090, bw, 130, 32); g.fill();
      g.textAlign = 'center';
      g.fillStyle = '#A79BC4'; g.font = '500 28px "Noto Sans KR",sans-serif';
      g.fillText(cats[i][0], bx + bw / 2, 1138);
      g.fillStyle = '#6B5BA8'; g.font = '700 54px Jua,"Noto Sans KR",sans-serif';
      g.fillText(String(cats[i][1]), bx + bw / 2, 1196);
      bx += bw + 18;
    }

    g.textAlign = 'center';
    g.fillStyle = '#A79BC4'; g.font = '500 30px "Noto Sans KR",sans-serif';
    g.fillText('너도 해볼래? · stellasaju.com/uandme', W / 2, 1290);

    c.toBlob(function (blob) { cb(blob, c); }, 'image/png');
  }
  /* 초대 화면에서 나갈 그림 — 아직 점수가 없으니 물음표를 크게 */
  function makeInvite(cb) {
    var slotB = REL_PIC[st.rel] || '연인';
    loadPics([slotB, '__lucky'], function (P) { drawInvite(P, cb); });
  }
  function drawInvite(P, cb) {
    var W = 1080, H = 1350;
    var c = document.createElement('canvas');
    c.width = W; c.height = H;
    var g = c.getContext('2d');
    var bg = g.createLinearGradient(0, 0, W, H);
    bg.addColorStop(0, '#FBF6FF'); bg.addColorStop(0.55, '#F0E6FB'); bg.addColorStop(1, '#FFEDE2');
    g.fillStyle = bg; g.fillRect(0, 0, W, H);
    g.textAlign = 'center';
    g.fillStyle = '#A79BC4'; g.font = '600 34px "Noto Sans KR",sans-serif';
    g.fillText('유앤미 · ' + U.relKo(st.rel) + ' 궁합', W / 2, 150);
    var slotB2 = REL_PIC[st.rel] || '연인';
    drawPic(g, P[slotB2], 166, 466, 280, 250);
    drawPic(g, P['__lucky'], 914, 466, 280, 250);

    g.fillStyle = '#6B5BA8'; g.font = '700 300px Jua,"Noto Sans KR",sans-serif';
    g.fillText('?', W / 2, 540);
    g.fillStyle = '#3F3A52'; g.font = '700 84px Jua,"Noto Sans KR",sans-serif';
    g.fillText('우리 둘,', W / 2, 700);
    g.fillText('몇 점일까?', W / 2, 810);
    g.fillStyle = '#7C7392'; g.font = '500 40px "Noto Sans KR",sans-serif';
    g.fillText('사주 · 별자리 · 띠 셋을 함께 봅니다', W / 2, 915);
    g.fillText('생일만 넣으면 바로 나와요', W / 2, 980);
    g.fillStyle = 'rgba(255,255,255,.85)';
    rr(g, 140, 1070, 800, 120, 34); g.fill();
    g.fillStyle = '#6B5BA8'; g.font = '700 42px "Noto Sans KR",sans-serif';
    g.fillText('가입도 앱 설치도 없어요', W / 2, 1146);
    g.fillStyle = '#A79BC4'; g.font = '500 32px "Noto Sans KR",sans-serif';
    g.fillText('stellasaju.com/uandme', W / 2, 1290);
    c.toBlob(function (blob) { cb(blob, c); }, 'image/png');
  }

  function rr(g, x, y, w, h, r) {
    g.beginPath();
    g.moveTo(x + r, y);
    g.arcTo(x + w, y, x + w, y + h, r);
    g.arcTo(x + w, y + h, x, y + h, r);
    g.arcTo(x, y + h, x, y, r);
    g.arcTo(x, y, x + w, y, r);
    g.closePath();
  }

  /* 그림 저장 ─────────────────────────────────────────────
     예전에는 곧바로 내려받기를 시켰는데, 아이폰 사파리는 내려받기를
     아예 안 하고 안드로이드도 가끔 막습니다. 그래서 그림을 화면에
     띄워 드리고 거기서 저장하시게 합니다. 어느 기기에서나 됩니다. */
  function shareImage() {
    makeImage(function (blob, canvas) { imageSheet(blob, canvas); });
  }

  function saveBlob(blob, canvas) {
    var name = st.result ? 'uandme.png' : 'uandme-invite.png';
    var url = '';
    try { url = URL.createObjectURL(blob); } catch (e) { url = ''; }
    if (!url) { try { url = canvas.toDataURL('image/png'); } catch (e2) { url = ''; } }
    if (!url) { return false; }
    var a = document.createElement('a');
    a.href = url;
    a.download = name;
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    /* 주소를 너무 일찍 거두면 안 됩니다. 「저장할 곳을 물어보기」가 켜져
       있는 컴퓨터에서는 사람이 폴더를 고르는 동안 내려받기가 이어지는데,
       그 사이에 거두면 파일이 잘려 열리지 않습니다. */
    setTimeout(function () {
      if (a.parentNode) { a.parentNode.removeChild(a); }
    }, 2000);
    setTimeout(function () {
      try { URL.revokeObjectURL(url); } catch (e3) {}
    }, 120000);
    return true;
  }

  function shareFile(blob) {
    var file = null;
    try { file = new File([blob], 'uandme.png', { type: 'image/png' }); } catch (e) { return false; }
    if (!navigator.canShare) { return false; }
    try { if (!navigator.canShare({ files: [file] })) { return false; } } catch (e2) { return false; }
    try { navigator.share({ files: [file], text: shareText() }).catch(function () {}); } catch (e3) { return false; }
    return true;
  }

  /* ── 연예인 고르기 ──────────────────────────────────────
     UM_CELEB 은 사람 목록을 짧은 글로 눌러 담아 둔 것입니다.
     처음 한 번만 풀어서 씁니다. */
  var CELEB = null;
  function celebList() {
    if (CELEB) { return CELEB; }
    if (!window.UM_CELEB) { return []; }
    var G = window.UM_CELEB.g, out = [], rows = window.UM_CELEB.p.split(';'), i;
    for (i = 0; i < rows.length; i++) {
      var f = rows[i].split('|');
      if (f.length < 5) { continue; }
      var gg = (G[parseInt(f[3], 10)] || '|').split('|');
      out.push({
        n: f[0], e: f[1],
        y: parseInt(f[2].slice(0, 4), 10),
        m: parseInt(f[2].slice(4, 6), 10),
        d: parseInt(f[2].slice(6, 8), 10),
        g: gg[0], ge: gg[1] || '', s: f[4],
        c: cho(f[0]), l: (f[1] + gg[1]).toLowerCase()
      });
    }
    CELEB = out;
    return out;
  }
  /* 한글 첫소리 — 장원영 → ㅈㅇㅇ */
  var CHO = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'];
  function cho(str) {
    var out = '', i, c;
    for (i = 0; i < str.length; i++) {
      c = str.charCodeAt(i);
      if (c >= 0xAC00) { if (c <= 0xD7A3) { out += CHO[Math.floor((c - 0xAC00) / 588)]; continue; } }
      if (str.charAt(i) !== ' ') { out += str.charAt(i); }
    }
    return out;
  }
  function celebHit(p, q) {
    if (!q) { return true; }
    if (p.n.indexOf(q) >= 0) { return true; }
    if (p.g.indexOf(q) >= 0) { return true; }
    if (p.c.indexOf(q) >= 0) { return true; }
    if (p.l.indexOf(q.toLowerCase()) >= 0) { return true; }
    return false;
  }
  function pad2n(n) { return n < 10 ? '0' + n : '' + n; }

  function celebSheet() {
    var all = celebList();
    if (!all.length) { toast('연예인 목록을 아직 못 받았어요'); return; }

    var old = document.getElementById('um-celeb');
    if (old) { if (old.parentNode) { old.parentNode.removeChild(old); } }

    var wrap = el('<div id="um-celeb" style="position:fixed;left:0;top:0;right:0;bottom:0;' +
      'background:#F7F2FC;z-index:2147483644;display:flex;flex-direction:column"></div>');

    var top = el('<div style="padding:16px 18px 12px;background:#F7F2FC;flex:0 0 auto"></div>');
    var row = el('<div style="display:flex;gap:9px;align-items:center"></div>');
    var inp = el('<input id="um-cq" placeholder="이름 · 그룹 · ㅈㅇㅇ" ' +
      'style="flex:1;min-width:0;border:1.6px solid #E4DAF6;background:#fff;border-radius:15px;' +
      'padding:13px 15px;font-size:15px;color:#3F3A52;font-family:inherit;outline:none">');
    var xb = el('<button style="flex:0 0 auto;background:none;border:0;padding:8px;' +
      'font-size:15px;color:#8C82A6;font-family:inherit">닫기</button>');
    row.appendChild(inp); row.appendChild(xb);
    top.appendChild(el('<div class="jua" style="font-size:22px;color:#3F3A52;margin-bottom:12px">' +
      '누구랑 볼까요?</div>'));
    top.appendChild(row);
    top.appendChild(el('<div style="font-size:11.5px;color:#A79BC4;margin-top:9px">' +
      all.length + '명 · 태어난 시각은 알려진 것이 없어 빼고 봅니다</div>'));

    var body = el('<div style="flex:1 1 auto;overflow-y:auto;padding:4px 18px 30px"></div>');
    wrap.appendChild(top); wrap.appendChild(body);

    function draw(q) {
      var i, cur = '', out = [], n = 0;
      for (i = 0; i < all.length; i++) {
        var p = all[i];
        if (!celebHit(p, q)) { continue; }
        if (n >= 220) { break; }
        if (p.g !== cur) {
          cur = p.g;
          out.push('<div style="font-size:12px;font-weight:700;color:#A79BC4;' +
            'margin:18px 0 8px;letter-spacing:.02em">' + esc(p.g) + '</div>');
        }
        out.push('<button class="um-cb" data-i="' + i + '" style="width:100%;text-align:left;' +
          'background:#fff;border:0;border-radius:16px;padding:13px 15px;margin-bottom:7px;' +
          'display:flex;align-items:center;gap:10px;font-family:inherit">' +
          '<span style="flex:1;min-width:0;font-size:15px;font-weight:600;color:#3F3A52">' +
          esc(p.n) + '</span>' +
          '<span style="font-size:11.5px;color:#B3A9C9">' + p.y + '.' + pad2n(p.m) + '.' + pad2n(p.d) +
          '</span></button>');
        n++;
      }
      if (!n) {
        out.push('<div style="text-align:center;color:#A79BC4;font-size:14px;padding:50px 0">' +
          '그런 사람은 없어요<br><span style="font-size:12px">초성으로도 찾아보세요 — ㅈㅇㅇ</span></div>');
      }
      body.innerHTML = out.join('');
      var bs = body.querySelectorAll('.um-cb'), k;
      for (k = 0; k < bs.length; k++) {
        bs[k].addEventListener('click', function () {
          pickCeleb(all[parseInt(this.getAttribute('data-i'), 10)]);
        });
      }
    }
    function shut() { if (wrap.parentNode) { wrap.parentNode.removeChild(wrap); } }
    xb.addEventListener('click', shut);
    var tmr = null;
    inp.addEventListener('input', function () {
      var v = this.value;
      if (tmr) { clearTimeout(tmr); }
      tmr = setTimeout(function () { draw(v.replace(/\s+/g, '')); }, 120);
    });

    (X.getRoot() || document.body).appendChild(wrap);
    draw('');
    window.__umPick = shut;
  }

  function pickCeleb(p) {
    if (window.__umPick) { window.__umPick(); }
    st.you = { sex: p.s, y: p.y, m: p.m, d: p.d, h: 0, mi: 0, known: false, name: p.n };
    st.celeb = p;
    try { U.compute(); } catch (e) { toast('계산이 안 됐어요'); return; }
    history.replaceState(null, '', X.base());
    go('result');
  }

  function imageSheet(blob, canvas) {
    var url = '';
    try { url = URL.createObjectURL(blob); } catch (e) { url = ''; }
    if (!url) { try { url = canvas.toDataURL('image/png'); } catch (e2) { url = ''; } }

    var old = document.getElementById('um-sheet');
    if (old) { if (old.parentNode) { old.parentNode.removeChild(old); } }

    var wrap = el('<div id="um-sheet" style="position:fixed;left:0;top:0;right:0;bottom:0;' +
      'background:rgba(28,22,45,.95);z-index:2147483645;display:flex;align-items:center;' +
      'justify-content:center;padding:18px;overflow:auto"></div>');
    var box = el('<div style="max-width:340px;width:100%;text-align:center"></div>');
    box.appendChild(el('<img src="' + url + '" alt="유앤미 궁합" ' +
      'style="width:100%;border-radius:20px;display:block;box-shadow:0 18px 50px rgba(0,0,0,.35)">'));
    box.appendChild(el('<div style="color:#fff;font-size:13px;line-height:1.7;margin-top:14px;opacity:.92">' +
      '카톡·X·스레드로 보내면 <b>이 그림과 링크가 함께</b> 갑니다<br>' +
      '<span style="opacity:.72">인스타는 그림을 저장해서 올려주세요</span></div>'));

    /* 보내는 곳들 — 화면 아래쪽과 같은 아이콘 줄입니다 */
    var link = st.result ? resultUrl() : inviteUrl();
    var row = el('<div id="um-shsheet" style="margin-top:15px"></div>');
    row.innerHTML = shareRow(link, shareText(), false);
    var bs = row.querySelectorAll('[data-s]'), bi;
    for (bi = 0; bi < bs.length; bi++) {
      bs[bi].addEventListener('click', function () {
        var k = this.getAttribute('data-s');
        if (k === 'kakao') { kakao(link, shareText()); return; }
        if (k === 'x') { tweet(link, shareText()); return; }
        if (k === 'threads') { threads(link, shareText()); return; }
        if (k === 'copy') { copy(link); toast('링크를 복사했어요'); return; }
        if (k === 'image') {
          if (saveBlob(blob, canvas)) { toast('그림을 저장했어요. 인스타에 올려보세요'); }
          else { toast('그림을 꾹 눌러 저장해 주세요'); }
        }
      });
    }
    var bSave = el('<button style="width:100%;background:#fff;color:#3F3A52;border:0;border-radius:15px;' +
      'padding:14px 0;margin-top:11px;font-size:14.5px;font-weight:700;font-family:inherit">' +
      '그림 저장하기</button>');
    var bClose = el('<button style="width:100%;background:none;color:#fff;border:0;margin-top:9px;' +
      'padding:11px 0;font-size:13.5px;opacity:.8;font-family:inherit">닫기</button>');

    bSave.addEventListener('click', function () {
      if (saveBlob(blob, canvas)) { toast('사진첩이나 다운로드 폴더를 봐주세요'); }
      else { toast('그림을 꾹 눌러 저장해 주세요'); }
    });
    function shut() {
      if (wrap.parentNode) { wrap.parentNode.removeChild(wrap); }
      try { URL.revokeObjectURL(url); } catch (e) {}
    }
    bClose.addEventListener('click', shut);
    wrap.addEventListener('click', function (ev) { if (ev.target === wrap) { shut(); } });

    box.appendChild(row); box.appendChild(bSave); box.appendChild(bClose);
    wrap.appendChild(box);
    (X.getRoot() || document.body).appendChild(wrap);
  }

  /* ── 화면 ────────────────────────────────────────────── */
  function relChips() {
    return U.RELS.map(function (r) {
      return '<button class="chip' + (st.rel === r.key ? ' on' : '') +
        '" data-rel="' + r.key + '">' + r.ko + '</button>';
    }).join('');
  }

  function form(who) {
    var p = who === 'me' ? st.me : st.you;
    p = p || {};
    return [
      '<div class="pad" style="margin-top:22px"><div class="lbl">부를 이름 <span style="font-weight:400;color:#B3A9C9">(안 넣어도 돼요)</span></div>',
      '<input class="fld" id="f-name" maxlength="8" placeholder="지은" value="' + esc(p.name || '') + '"></div>',
      '<div class="pad" style="margin-top:18px"><div class="lbl">생년월일</div><div class="row">',
      '<input class="fld" id="f-y" inputmode="numeric" maxlength="4" placeholder="1994" value="' + (p.y || '') + '" style="flex:1.7">',
      '<input class="fld" id="f-m" inputmode="numeric" maxlength="2" placeholder="03" value="' + (p.m || '') + '">',
      '<input class="fld" id="f-d" inputmode="numeric" maxlength="2" placeholder="21" value="' + (p.d || '') + '">',
      '</div></div>',
      '<div class="pad" style="margin-top:18px"><div class="lbl">태어난 시각</div>',
      '<div class="row">',
      '<button class="seg' + (draft.ampm !== '오후' ? ' on' : '') + '" data-ampm="오전">오전</button>',
      '<button class="seg' + (draft.ampm === '오후' ? ' on' : '') + '" data-ampm="오후">오후</button>',
      '</div>',
      '<div class="row" style="margin-top:7px">',
      '<input class="fld" id="f-h" inputmode="numeric" maxlength="2" placeholder="9시">',
      '<input class="fld" id="f-mi" inputmode="numeric" maxlength="2" placeholder="30분">',
      '<button class="seg' + (draft.known === false ? ' on' : '') + '" id="f-unk" style="flex:0 0 92px">모름</button>',
      '</div>',
      '<div class="note" style="margin-top:9px">낮 12시는 <b>오후 12시</b>, 밤 12시는 <b>오전 12시</b>입니다.<br>',
      '모르셔도 됩니다. 시각 없이도 나오고, 있으면 조금 더 정확해집니다.</div></div>',
      '<div class="pad" style="margin-top:18px"><div class="lbl">성별</div><div class="row">',
      '<button class="seg' + (p.sex !== 'M' ? ' on' : '') + '" data-sex="F">여성</button>',
      '<button class="seg' + (p.sex === 'M' ? ' on' : '') + '" data-sex="M">남성</button>',
      '</div></div>'
    ].join('');
  }

  var draft = { sex: 'F', known: true, ampm: '오전' };

  function readForm() {
    function v(id) { var n = root.querySelector('#' + id); return n ? n.value.trim() : ''; }
    var y = +v('f-y'), m = +v('f-m'), d = +v('f-d');
    if (!y || !m || !d) { toast('생년월일을 넣어주세요'); return null; }
    if (y < 1900 || y > 2100) { toast('연도를 다시 봐주세요'); return null; }
    if (m < 1 || m > 12) { toast('월을 다시 봐주세요'); return null; }
    if (d < 1 || d > 31) { toast('일을 다시 봐주세요'); return null; }
    var h = +v('f-h'), mi = +v('f-mi');
    var known = draft.known;
    if (known) { if (!v('f-h')) { known = false; } }
    if (known) {
      if (h < 1 || h > 12) { toast('시각은 1시부터 12시까지 넣어주세요'); return null; }
      /* 오전 12시는 밤 0시, 오후 12시는 낮 12시입니다 */
      if (draft.ampm === '오후') { if (h < 12) { h = h + 12; } }
      else { if (h === 12) { h = 0; } }
      if (mi < 0 || mi > 59) { toast('분은 0부터 59까지 넣어주세요'); return null; }
    }
    return { sex: draft.sex, y: y, m: m, d: d, h: known ? h : 12,
             mi: known ? (mi || 0) : 0, known: known, name: v('f-name') };
  }

  function bar(label, sc, mx) {
    return '<div style="margin-top:14px"><div style="display:flex;justify-content:space-between;' +
      'font-size:12.5px;font-weight:700;color:#8C82A6;margin-bottom:6px"><span>' + label +
      '</span><span style="color:#6B5BA8">' + sc + ' / ' + mx + '</span></div>' +
      '<div class="bar"><i style="width:' + Math.round(sc / mx * 100) + '%"></i></div></div>';
  }

  function shareRow(url, text, withImage) {
    var row = '<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px">' +
      shareBtn('kakao',   '카카오톡',  '#FAE100', IC.talk) +
      shareBtn('x',       'X',        '#000000', IC.ex) +
      shareBtn('threads', '스레드',    '#1A1A1A', IC.at) +
      shareBtn('image',   '인스타',    '#D9578C', IC.cam) +
      shareBtn('copy',    '링크 복사', '#E7DEFA', IC.link) +
      '</div>';
    if (withImage) {
      row += '<button class="btnG" data-s="save" style="margin-top:12px;background:#fff">' +
        '그림으로 저장하기</button>';
    }
    return row;
  }

  function shareBtn(k, name, bg, icon) {
    return '<button class="sh" data-s="' + k + '">' +
      '<i style="background:' + bg + '">' + icon + '</i>' +
      '<span>' + name + '</span></button>';
  }

  /* ── 유앤미만의 머리말과 꼬리말 ───────────────────────
     스텔라사주의 검은 머리띠는 이 페이지에서만 감춰집니다(옷 쪽에서). */
  var C = window.UM_CHARS || {};
  function ch(k) { return C[k] || ''; }

  /* 설정(um-settings.js)에 그림 주소가 들어 있으면 그 그림을,
     비어 있으면 그려진 동물을 씁니다. 소희 님이 주소만 넣으면 바뀝니다. */
  /* 그림 자리 이름 → 실제 주소. art 와 같은 규칙입니다. */
  /* 관계마다 쓰는 그림 자리 (설정의 이름과 같습니다) */
  var REL_PIC = { lover: '연인', married: '부부', friend: '친구', sibling: '형제자매',
                  parent_child: '부모자녀', boss_sub: '상사부하', partner: '동업자' };

  function picUrl(slot) {
    var u = '';
    if (slot === '__lucky') { u = luckyPic(); }
    else if (window.UM_SET) { if (window.UM_SET.그림) { u = window.UM_SET.그림[slot] || ''; } }
    if (u === '없음') { return ''; }
    if (u) { if (u.indexOf('/') < 0) {
      if (window.UM_PIC) { u = window.UM_PIC[u] || ''; }
    } }
    return u;
  }
  /* 그림 한 장 미리 받아둡니다. 못 받으면 없는 대로 갑니다. */
  function loadPic(slot, cb) {
    var u = picUrl(slot);
    if (!u) { cb(null); return; }
    var im = new Image();
    im.crossOrigin = 'anonymous';
    im.onload = function () { cb(im); };
    im.onerror = function () { cb(null); };
    im.src = u;
  }
  /* 여러 장을 다 받고 나서 한 번에 부릅니다 */
  function loadPics(slots, cb) {
    var out = {}, left = slots.length;
    if (!left) { cb(out); return; }
    var done = function () { left = left - 1; if (left === 0) { cb(out); } };
    var i;
    for (i = 0; i < slots.length; i++) {
      (function (nm) {
        loadPic(nm, function (im) { out[nm] = im; done(); });
      })(slots[i]);
    }
    setTimeout(function () { if (left > 0) { left = 0; cb(out); } }, 3000);
  }
  /* 그림 둘레의 빈 곳을 재 둡니다.
     아이마다 여백이 달라서, 그냥 상자에 맞추면 어떤 아이는 작아 보입니다.
     실제로 그려진 데만 재서 쓰면 다들 고르게 큼직해집니다. */
  var TRIM = {};
  function trimBox(im) {
    var key = im.src;
    if (TRIM[key]) { return TRIM[key]; }
    var w = im.naturalWidth || im.width, h = im.naturalHeight || im.height;
    var box = { x: 0, y: 0, w: w, h: h };
    if (w) { if (h) {
      try {
        var c = document.createElement('canvas');
        c.width = w; c.height = h;
        var g2 = c.getContext('2d');
        g2.drawImage(im, 0, 0);
        var d = g2.getImageData(0, 0, w, h).data;
        var x0 = w, y0 = h, x1 = -1, y1 = -1, x, y, i;
        for (y = 0; y < h; y++) {
          for (x = 0; x < w; x++) {
            i = (y * w + x) * 4 + 3;
            if (d[i] > 12) {
              if (x < x0) { x0 = x; }
              if (x > x1) { x1 = x; }
              if (y < y0) { y0 = y; }
              if (y > y1) { y1 = y; }
            }
          }
        }
        if (x1 >= 0) { box = { x: x0, y: y0, w: x1 - x0 + 1, h: y1 - y0 + 1 }; }
      } catch (e) {}
    } }
    TRIM[key] = box;
    return box;
  }
  /* 캔버스에 그림을 넣습니다 — 빈 곳은 빼고, 키를 맞춰 그립니다.
     상자에 맞추면 세로로 긴 아이가 작아 보여서, 키(높이)를 기준으로
     맞춥니다. 대신 너무 옆으로 퍼지지 않게 너비에 울타리를 둡니다. */
  function drawPic(g, im, cx, cy, tall, wide) {
    if (!im) { return; }
    var t = trimBox(im);
    if (!t.w) { return; }
    if (!wide) { wide = tall; }
    var k = Math.min(tall / t.h, wide / t.w);
    var dw = t.w * k, dh = t.h * k;
    g.drawImage(im, t.x, t.y, t.w, t.h, cx - dw / 2, cy - dh / 2, dw, dh);
  }
  /* 그림 곳간에서 아무거나 한 장 — 들어올 때 한 번 정하고 그대로 씁니다 */
  var LUCKY = null;
  function luckyPic() {
    if (LUCKY) { return LUCKY; }
    if (!window.UM_PIC) { return ''; }
    var keys = [], k;
    for (k in window.UM_PIC) {
      if (!window.UM_PIC.hasOwnProperty(k)) { continue; }
      if (k === '로고그림') { continue; }
      keys.push(k);
    }
    if (!keys.length) { return ''; }
    LUCKY = keys[Math.floor(Math.random() * keys.length)];
    return LUCKY;
  }

  function art(slot, fb) {
    var u = '';
    if (window.UM_SET) { if (window.UM_SET.그림) { u = window.UM_SET.그림[slot] || ''; } }
    /* 「없음」이라고 적으면 그 자리에 아무것도 안 그립니다 */
    if (u === '없음') { return ''; }
    /* 「가1」 「다7」 같은 이름표면 그림 목록에서 주소를 찾습니다 */
    if (u) { if (u.indexOf('/') < 0) {
      if (window.UM_PIC) { u = window.UM_PIC[u] || ''; }
    } }
    if (u) {
      return '<img class="um-img" src="' + esc(u) + '" alt="">';
    }
    return ch(fb);
  }

  /* 설정에 글이 들어 있으면 그것을, 없으면 원래 글을 */
  function T(k, fb) {
    var v = '';
    if (window.UM_SET) { if (window.UM_SET.글) { v = window.UM_SET.글[k] || ''; } }
    return v || fb || '';
  }

  var BUN = art('로고', 'bunny_white');

  /* 카드 뒤에서 머리만 내미는 「빼꼼」 */
  /* 카드 뒤로 숨기지 않고 통째로 얹습니다 */
  function pop(slot, w, css) {
    var a = art(slot, '');
    if (!a) { return ''; }
    return '<div class="pop" style="width:' + w + 'px;height:' + w + 'px;' + css + '">' +
      a + '</div>';
  }

  function peek(slot, fb, w, css) {
    var a = art(slot, fb);
    if (!a) { return ''; }          /* 「없음」이면 빈 칸도 안 만듭니다 */
    return '<div class="peek" style="width:' + w + 'px;height:' + w + 'px;' + css + '">' +
      a + '</div>';
  }

  function chrome() {
    if (!document.getElementById('um-top')) {
      var top = X.el('<div id="um-top"><div class="in">' +
        '<a class="lg" href="/uandme/">' +
        '<span class="lgi">' + BUN + '</span>' +
        '<b>유앤미</b></a>' +
        '<a class="st" href="/">스텔라사주</a>' +
        '</div></div>');
      root.parentNode.insertBefore(top, root);
    }
    if (!document.getElementById('um-foot')) {
      var foot = X.el('<div id="um-foot">' +
        '<div class="lk">' +
        '<a href="/uandme/">유앤미</a>' +
        '<a href="/">스텔라사주</a>' +
        '<a href="/privacy/">개인정보</a>' +
        '</div>' +
        '<p>' + T('꼬리말') + '</p>' +
        '<p style="margin-top:10px">stellasaju.com</p></div>');
      root.parentNode.insertBefore(foot, root.nextSibling);
    }
  }

  function render() {
    root = X.getRoot();
    chrome();
    var h = [];
    if (st.view === 'home') {
      h.push(
      /* 히어로 — 오른쪽에서 둘이 빼꼼 */
      '<div class="pad" style="padding-top:26px;padding-bottom:18px;position:relative">' +
        peek('히어로큰', 'bunny_pink', 134, 'right:-10px;top:8px') +
        peek('히어로작은', 'bunny_white', 78, 'right:60px;top:78px;transform:rotate(-11deg)') +
        '<div class="front" style="display:inline-block;background:#E7DEFA;color:#6B5BA8;' +
        'border-radius:999px;padding:7px 15px;font-size:12px;font-weight:500">' + T('제목위') + '</div>' +
        '<div class="h1 front" style="margin-top:16px;max-width:215px">' + T('제목') + '</div>' +
        '<div class="sub front" style="max-width:235px">' + T('제목설명') + '</div>' +
      '</div>',

      /* 보기 카드 — 카드 위 테두리에서 머리만 */
      '<div class="pad" style="padding-top:40px;position:relative">' +
        peek('카드왼쪽', 'bunny_happy', 78, 'left:38px;top:12px;transform:rotate(-9deg)') +
        peek('카드오른쪽', 'cat_cream', 78, 'right:38px;top:12px;transform:rotate(9deg)') +
        '<div class="card front">' +
          '<div style="display:flex;align-items:center;justify-content:space-between">' +
            '<div style="background:#FFE2D6;color:#C4674A;font-size:11.5px;font-weight:700;padding:6px 13px;border-radius:999px">연인 궁합</div>' +
            '<div style="font-size:11.5px;color:#B3A9C9;font-weight:500">이런 식으로 나와요</div></div>' +
          '<div style="margin-top:16px">' + ring(92, 'umRingA') + '</div>' +
          '<div class="jua" style="font-size:27px;text-align:center;margin-top:10px;color:#3F3A52">완전 찰떡궁합</div>' +
          '<div style="font-size:13.5px;line-height:1.8;color:#7C7392;margin-top:10px;text-align:center">' +
          '갑돌이가 갑순이 시집가도 여전히 못 잊었다는데, 두 분은 그럴 걱정 없을 궁합이에요.</div>' +
          bar('사주', 34, 40) + bar('별자리', 27, 30) + bar('띠', 26, 30) +
          '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin-top:20px">' +
          cat('성격', 90, '#F1EBFA', '#6B5BA8', '#A79BC4') +
          cat('연애', 85, '#FCE8F1', '#C4658F', '#C58AA8') +
          cat('결혼', 70, '#FFEFE2', '#C4784A', '#C99578') +
          cat('금전', 95, '#E2F5EE', '#4F937A', '#7FAE9C') +
          '</div></div></div>',

      /* 관계 고르기 — 여기서는 얼굴이 다 보여야 고를 수 있습니다 */
      '<div class="pad" style="margin-top:46px">' +
        '<div class="jua" style="font-size:25px;color:#3F3A52">' + T('관계제목') + '</div>' +
        '<div style="font-size:13px;color:#A79BC4;margin-top:7px">' + T('관계설명') + '</div>' +
        '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:18px">' +
      '<button class="tile' + (st.rel==='lover' ? ' on' : '') + '" data-rel="lover">' +
        '<div class="im" style="background:#FCE8F1">' + art('연인', 'bunny_pink') + '</div><b>연인</b></button>' +
      '<button class="tile' + (st.rel==='married' ? ' on' : '') + '" data-rel="married">' +
        '<div class="im" style="background:#E7DEFA">' + art('부부', 'bunny_white') + '</div><b>부부</b></button>' +
      '<button class="tile' + (st.rel==='friend' ? ' on' : '') + '" data-rel="friend">' +
        '<div class="im" style="background:#E2F5EE">' + art('친구', 'cat_cream') + '</div><b>친구</b></button>' +
      '<button class="tile' + (st.rel==='sibling' ? ' on' : '') + '" data-rel="sibling">' +
        '<div class="im" style="background:#FFEFE2">' + art('형제자매', 'bunny_happy') + '</div><b>형제자매</b></button>' +
      '<button class="tile' + (st.rel==='parent_child' ? ' on' : '') + '" data-rel="parent_child">' +
        '<div class="im" style="background:#DCEEF9">' + art('부모자녀', 'cow') + '</div><b>부모자녀</b></button>' +
      '<button class="tile' + (st.rel==='boss_sub' ? ' on' : '') + '" data-rel="boss_sub">' +
        '<div class="im" style="background:#F1EBFA">' + art('상사부하', 'bunny_peek') + '</div><b>상사부하</b></button>' +
      '<button class="tile' + (st.rel==='partner' ? ' on' : '') + '" data-rel="partner">' +
        '<div class="im" style="background:#FCF3DA">' + art('동업자', 'cat_cream') + '</div><b>동업자</b></button>' +
      '<button class="tile" id="tile-celeb">' +
        '<div class="im" style="background:#F1EBFA">' + art('연예인', 'bunny_happy') + '</div><b>연예인</b></button>' +
        '</div></div>',

      '<div class="pad" style="margin-top:30px"><button class="btnP" id="go-mine">' + T('시작버튼') + '</button></div>',

      /* 초대 설명 */
      '<div class="pad" style="margin-top:104px;position:relative">' +
        pop('초대그림', 124, 'right:8px;top:-108px') +
        peek('초대위', 'cow', 84, 'right:28px;top:-44px;transform:rotate(8deg)') +
        '<div class="front" style="background:#E7DEFA;border-radius:28px;padding:26px 22px">' +
          '<div class="jua" style="font-size:25px;line-height:1.3;color:#3F3A52">' + T('초대제목') + '</div>' +
          step(1, T('초대1')) +
          step(2, T('초대2')) +
          step(3, T('초대3'), true) +
        '</div>' +
        peek('초대아래', 'bunny_peek', 70, 'left:38px;bottom:-28px;transform:rotate(-10deg);z-index:2') +
      '</div>',

      /* 무료라는 것 */
      '<div class="pad" style="margin-top:100px;position:relative">' +
        pop('공짜카드', 118, 'right:10px;top:-104px') +
        '<div class="card front">' +
          '<div class="jua" style="font-size:22px;color:#3F3A52">' + T('공짜제목') + '</div>' +
          '<div style="font-size:13.5px;line-height:1.8;color:#7C7392;margin-top:9px">' +
          T('공짜설명') + '</div>' +
        '</div></div>',

      /* 스텔라사주로 */
      '<div class="pad" style="margin-top:44px">' +
        '<a href="/" style="text-decoration:none"><div style="display:flex;align-items:center;' +
        'justify-content:space-between;padding:20px 22px;background:#100B22;border-radius:24px">' +
        '<div><div style="font-size:11px;color:#B9A2F2;font-weight:700;margin-bottom:5px">스텔라사주</div>' +
        '<div style="font-size:16px;font-weight:700;color:#F6F1E7">' + T('스텔라띠') + '</div></div>' +
        '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#C99A55" stroke-width="2" ' +
        'stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>' +
        '</div></a></div>');
    } else if (st.view === 'mine') {
      var celebFirst = (st.want === 'celeb');
      h.push('<div class="pad" style="padding-top:30px"><div class="h1">먼저<br>내 것부터</div>',
        '<div class="sub">' + (celebFirst
          ? '내 생일만 넣으면 연예인을 고를 수 있어요.'
          : '상대 생일은 몰라도 됩니다. 링크를 보내면 그쪽이 직접 넣어요.') + '</div></div>',
        form('me'),
        '<div class="pad" style="margin-top:28px">' +
        (celebFirst
          ? '<button class="btnP" id="celeb">연예인 고르기</button>' +
            '<div style="height:9px"></div><button class="btnG" id="mk-link">궁합 링크 만들기</button>' +
            '<div style="height:9px"></div><button class="btnG" id="both">상대 생일도 내가 알아요</button>'
          : '<button class="btnP" id="mk-link">궁합 링크 만들기</button>' +
            '<div style="height:9px"></div><button class="btnG" id="both">상대 생일도 내가 알아요</button>' +
            '<div style="height:9px"></div><button class="btnG" id="celeb" style="background:#F3ECFF;color:#6B5BA8">연예인이랑 볼래요</button>') +
        '</div>');
    } else if (st.view === 'both') {
      h.push('<div class="pad" style="padding-top:30px"><div class="h1">상대는<br>언제 태어났나요</div></div>',
        form('you'),
        '<div class="pad" style="margin-top:28px"><button class="btnP" id="calc">우리 점수 보기</button></div>');
    } else if (st.view === 'invite') {
      var iu = inviteUrl();
      h.push('<div class="pad" style="padding-top:30px"><div class="h1">링크가<br>만들어졌어요</div>',
        '<div class="sub">보내기만 하면 됩니다. 그 사람이 생일을 넣으면 그쪽 화면에 점수가 뜨고, 거기서 「결과 보내기」를 누르면 돌아옵니다.</div></div>',
        '<div class="pad" style="margin-top:28px"><div class="lbl">어디로 보낼까요</div>',
        shareRow(iu, '', false), '</div>',
        '<div class="pad" style="margin-top:22px"><div style="background:#fff;border-radius:20px;padding:14px 16px;display:flex;align-items:center;gap:11px">',
        '<div style="flex:1;font-size:12.5px;color:#8C82A6;overflow:hidden;white-space:nowrap;text-overflow:ellipsis">' + esc(iu) + '</div>',
        '<button class="chip on" data-s="copy" style="padding:9px 15px">복사</button></div></div>',
        '<div class="pad" style="margin-top:26px"><button class="btnG" id="both2">아니면 내가 상대 생일을 넣을게요</button></div>',
        '<div class="pad" style="margin-top:22px"><div class="mini">링크에는 당신의 생년월일이 담깁니다. 아무에게나 보내지 마세요.</div></div>');
    } else if (st.view === 'joined') {
      var nm = st.me.name || '상대';
      h.push('<div class="pad" style="padding-top:34px;text-align:center"><div class="h1">' +
        esc(nm) + '님이<br>궁합 보자고 했어요</div>',
        '<div class="sub">생일만 넣으면 둘 다 점수를 봅니다.</div></div>',
        '<div class="pad" style="margin-top:24px"><div class="card" style="padding:18px">',
        '<div style="font-size:11.5px;color:#A79BC4;font-weight:700">' + esc(nm) + ' · ' +
        st.me.y + '년생 ' + (st.me.sex === 'M' ? '남성' : '여성') + '</div>',
        '<div style="font-size:14px;color:#3F3A52;margin-top:4px;font-weight:500">' +
        U.relKo(st.rel) + ' 궁합으로 물어봤어요</div></div></div>',
        form('you'),
        '<div class="pad" style="margin-top:28px"><button class="btnP" id="calc">우리 점수 보기</button></div>');
    } else if (st.view === 'result') {
      var r = st.result, tier = window.UANDME_TIER(r.total, st.rel);
      var ru = resultUrl();
      if (st.celeb) {
        h.push('<div class="pad" style="padding-top:22px"><div style="background:#F3ECFF;' +
          'border-radius:18px;padding:13px 16px;display:flex;align-items:center;gap:10px">' +
          '<div style="flex:1;min-width:0">' +
          '<div style="font-size:11.5px;color:#8C82A6;font-weight:700">연예인 궁합</div>' +
          '<div style="font-size:14.5px;color:#3F3A52;font-weight:600;margin-top:3px">' +
          esc(st.celeb.n) + (st.celeb.g === '배우' ? '' : ' · ' + esc(st.celeb.g)) +
          '</div></div>' +
          '<div style="font-size:11px;color:#A79BC4;text-align:right;line-height:1.5">' +
          '태어난 시각은<br>빼고 봤어요</div></div></div>');
      }
      h.push('<div class="pad" style="padding-top:26px"><div class="card">',
        '<div style="display:flex;align-items:center;justify-content:space-between">',
        '<div style="background:#FFE2D6;color:#C4674A;font-size:11.5px;font-weight:700;padding:6px 13px;border-radius:999px">' +
        U.relKo(st.rel) + ' 궁합</div>',
        '<div style="font-size:11.5px;color:#B3A9C9;font-weight:500">' +
        esc(st.me.name || '나') + ' × ' + esc(st.you.name || '너') + '</div></div>',
        '<div style="margin-top:16px">' + ring(r.total, 'umRingB') + '</div>',
        '<div class="jua" style="font-size:28px;text-align:center;margin-top:12px;color:#3F3A52">' + esc(tier.title) + '</div>',
        '<div style="font-size:13.5px;line-height:1.8;color:#7C7392;margin-top:10px;text-align:center">' + esc(tier.comment) + '</div>',
        bar('사주', r.blocks.saju.score, 40),
        bar('별자리 · ' + esc(r.blocks.zodiac.pair), r.blocks.zodiac.score, 30),
        bar(esc(r.blocks.animal.pair), r.blocks.animal.score, 30),
        '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin-top:20px">',
        cat('성격', r.categories.personality, '#F1EBFA', '#6B5BA8', '#A79BC4'),
        cat('연애', r.categories.love, '#FCE8F1', '#C4658F', '#C58AA8'),
        cat('결혼', r.categories.marriage, '#FFEFE2', '#C4784A', '#C99578'),
        cat('금전', r.categories.money, '#E2F5EE', '#4F937A', '#7FAE9C'),
        '</div></div></div>',
        '<div class="pad" style="margin-top:20px"><div class="lbl">왜 이 점수인지</div><div class="card" style="padding:20px">',
        '<div style="font-size:13.5px;line-height:1.85;color:#57506E">' + esc(r.blocks.zodiac.note) + '</div>',
        '<div style="font-size:13.5px;line-height:1.85;color:#57506E;margin-top:12px">' + esc(r.blocks.animal.note) + '</div>',
        '<div style="font-size:13.5px;line-height:1.85;color:#57506E;margin-top:12px">' + esc(r.parts.ji.note) + '</div>',
        '<div style="font-size:13.5px;line-height:1.85;color:#57506E;margin-top:12px">' + esc(r.parts.god.note) + '</div>',
        '</div></div>',
        '<div class="pad" style="margin-top:24px"><div class="lbl">자랑하기</div>',
        shareRow(ru, shareText(), true), '</div>',
        '<div class="pad" style="margin-top:26px"><button class="btnG" id="again">다른 사람과도 보기</button>',
        '<div style="height:9px"></div><button class="btnG" id="celeb2" style="background:#F3ECFF;color:#6B5BA8">연예인이랑도 볼래요</button></div>',
        '<div class="pad" style="margin-top:26px"><a href="/" style="text-decoration:none"><div style="display:flex;align-items:center;justify-content:space-between;padding:20px 22px;background:#100B22;border-radius:24px">',
        '<div><div style="font-size:11px;color:#B9A2F2;font-weight:700;margin-bottom:5px">스텔라사주</div>',
        '<div style="font-size:16px;font-weight:700;color:#F6F1E7">내 사주 제대로 읽어보기</div></div>',
        '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#C99A55" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>',
        '</div></a></div>');
    }
    root.innerHTML = h.join('');
    wire();
    veilOff();
    if (st.view === 'result') { cardWarm(); }
  }

  function step(n, txt, last) {
    return '<button class="stp" data-goto="mine" style="display:flex;gap:12px;align-items:center;' +
      'background:#fff;border-radius:20px;padding:13px 15px;margin-top:9px;width:100%;text-align:left">' +
      '<span style="width:26px;height:26px;border-radius:999px;' +
      'background:' + (last ? '#B8A6E8' : '#E7DEFA') + ';color:' + (last ? '#fff' : '#6B5BA8') + ';' +
      'font-family:Jua,sans-serif;font-size:13px;display:flex;align-items:center;justify-content:center;' +
      'flex:0 0 26px">' + n + '</span>' +
      '<span style="font-size:14px;color:#57506E;flex:1">' + txt + '</span>' +
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#C3BAD6" stroke-width="2.4" ' +
      'stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>' +
      '</button>';
  }

  /* 도넛 게이지 — 시안에 있던 그것입니다.
     둘레는 2 x 3.14159 x 70 = 439.8. 점수만큼 칠하고 나머지는 비웁니다. */
  function ring(score, id) {
    var C = 439.8;
    var on = C * (score / 100);
    return '<div style="position:relative;width:168px;height:168px;margin:0 auto">' +
      '<svg width="168" height="168" viewBox="0 0 168 168">' +
      '<defs><linearGradient id="' + id + '" x1="0" y1="0" x2="1" y2="1">' +
      '<stop offset="0%" stop-color="#C3B2F0"/>' +
      '<stop offset="50%" stop-color="#F4B9D4"/>' +
      '<stop offset="100%" stop-color="#FFCBA8"/></linearGradient></defs>' +
      '<circle cx="84" cy="84" r="70" fill="none" stroke="#F1EBFA" stroke-width="17"/>' +
      '<circle cx="84" cy="84" r="70" fill="none" stroke="url(#' + id + ')" stroke-width="17" ' +
      'stroke-linecap="round" stroke-dasharray="' + on.toFixed(1) + ' ' + (C - on + 60).toFixed(1) + '" ' +
      'transform="rotate(-90 84 84)"/></svg>' +
      '<div style="position:absolute;inset:0;display:flex;flex-direction:column;' +
      'align-items:center;justify-content:center">' +
      '<div class="jua" style="font-size:58px;line-height:1;color:#6B5BA8">' + score + '</div>' +
      '<div style="font-size:12.5px;color:#A79BC4;font-weight:500;margin-top:2px">점</div>' +
      '</div></div>';
  }

  function cat(name, v, bg, fg, sub) {
    return '<div style="background:' + bg + ';border-radius:18px;padding:13px 6px;text-align:center">' +
      '<div style="font-size:10.5px;color:' + sub + ';font-weight:500">' + name + '</div>' +
      '<div class="jua" style="font-size:21px;color:' + fg + ';margin-top:2px">' + v + '</div></div>';
  }

  function wire() {
    X.on('[data-rel]', 'click', function () {
      st.rel = this.getAttribute('data-rel'); render();
    });
    X.on('[data-ampm]', 'click', function () {
      draft.ampm = this.getAttribute('data-ampm');
      var n = root.querySelectorAll('[data-ampm]'), i;
      for (i = 0; i < n.length; i++) { n[i].classList.remove('on'); }
      this.classList.add('on');
    });
    X.on('[data-sex]', 'click', function () {
      draft.sex = this.getAttribute('data-sex');
      var n = root.querySelectorAll('[data-sex]'), i;
      for (i = 0; i < n.length; i++) { n[i].classList.remove('on'); }
      this.classList.add('on');
    });
    var unk = root.querySelector('#f-unk');
    if (unk) {
      unk.addEventListener('click', function () {
        draft.known = !draft.known;
        this.classList.toggle('on', !draft.known);
        var a = root.querySelector('#f-h'), b = root.querySelector('#f-mi');
        if (a) { a.disabled = !draft.known; a.style.opacity = draft.known ? 1 : .45; }
        if (b) { b.disabled = !draft.known; b.style.opacity = draft.known ? 1 : .45; }
      });
    }
    bind('#go-mine', function () { draft = { sex: 'F', known: true, ampm: '오전' }; st.want = ''; go('mine'); });
    X.on('[data-goto]', 'click', function () {
      draft = { sex: 'F', known: true, ampm: '오전' };
      st.want = '';
      go(this.getAttribute('data-goto'));
    });
    bind('#mk-link', function () {
      var p = readForm(); if (!p) { return; }
      st.me = p; U.saveMe(); go('invite');
    });
    bind('#both', function () {
      var p = readForm(); if (!p) { return; }
      st.me = p; U.saveMe(); draft = { sex: 'M', known: true, ampm: '오전' }; go('both');
    });
    bind('#both2', function () { draft = { sex: 'M', known: true, ampm: '오전' }; go('both'); });
    bind('#celeb', function () {
      var p = readForm(); if (!p) { return; }
      st.me = p; U.saveMe(); celebSheet();
    });
    bind('#celeb2', function () { celebSheet(); });
    bind('#tile-celeb', function () {
      draft = { sex: 'F', known: true, ampm: '오전' };
      st.want = 'celeb'; go('mine');
    });
    bind('#calc', function () {
      var p = readForm(); if (!p) { return; }
      st.you = p;
      try { U.compute(); } catch (e) { toast('계산이 안 됐어요. 날짜를 다시 봐주세요'); return; }
      history.replaceState(null, '', resultUrl());
      go('result');
    });
    bind('#again', function () {
      st.you = null; st.result = null; st.celeb = null;
      history.replaceState(null, '', X.base());
      draft = { sex: 'M', known: true, ampm: '오전' }; go('both');
    });
    X.on('[data-s]', 'click', function () {
      var k = this.getAttribute('data-s');
      var url = st.result ? resultUrl() : inviteUrl();
      var text = st.result ? shareText() :
        ((st.me.name || '친구') + '님이 궁합 보자고 해요');
      if (k === 'kakao')   { kakao(url, text); }
      if (k === 'x')       { xpost(url, text); }
      if (k === 'threads') { threads(url, text); }
      if (k === 'copy')    { copy(url); }
      if (k === 'image')   { shareImage(); }
      if (k === 'save')    { shareImage(); }
    });
  }
  function bind(sel, fn) {
    var n = root.querySelector(sel);
    if (n) { n.addEventListener('click', fn); }
  }

  /* ── 스텔라사주의 머리띠와 꼬리말 감추기 ──────────────
     테마가 어떤 이름을 쓰는지 몰라도 되게, 이름이 아니라 구조로 찾습니다.
     페이지에 있는 모든 header · footer 가운데 우리 화면을 품고 있지 않은
     것만 감춥니다. 워드프레스 관리 막대(#wpadminbar)는 div 라서 안 걸립니다. */
  /* 우리 화면 말고는 전부 감춥니다.
     #um 에서 body 까지 한 층씩 올라가면서, 우리를 품고 있지 않은 형제를
     이름과 상관없이 감춥니다. 테마가 무엇을 쓰든 통합니다.
     관리 막대(#wpadminbar)와 우리 머리말·꼬리말, 그리고 script/style 은
     건드리지 않습니다. */
  function isolate(host) {
    var node = host, parent = host.parentNode, i, k, t, hops = 0;
    while (parent) {
      if (hops > 12) { break; }
      for (i = 0; i < parent.children.length; i++) {
        k = parent.children[i];
        if (k === node) { continue; }
        if (k.id === 'wpadminbar') { continue; }
        if (k.id === 'um-top') { continue; }
        if (k.id === 'um-foot') { continue; }
        if (k.contains(host)) { continue; }
        t = k.tagName;
        if (t === 'SCRIPT') { continue; }
        if (t === 'STYLE') { continue; }
        if (t === 'LINK') { continue; }
        if (t === 'NOSCRIPT') { continue; }
        if (t === 'TEMPLATE') { continue; }
        k.style.setProperty('display', 'none', 'important');
      }
      if (parent === document.body) { break; }
      node = parent;
      parent = parent.parentNode;
      hops++;
    }
  }

  function hideTheme(host) {
    isolate(host);
    var i, n;
    /* 워드프레스는 머리띠를 <header> 로 낼 때도 있고 그냥
       <div class="wp-block-template-part"> 로 낼 때도 있습니다.
       태그를 가리지 않고 「템플릿 조각」이면 다 잡습니다. */
    n = document.querySelectorAll(
      'header, footer, .wp-block-template-part, .site-header, .site-footer, ' +
      '#masthead, #colophon, .wp-block-site-logo, .wp-block-navigation');
    for (i = 0; i < n.length; i++) {
      if (n[i].id === 'um-top') { continue; }
      if (n[i].id === 'um-foot') { continue; }
      if (n[i].contains(host)) { continue; }
      if (host.contains(n[i])) { continue; }
      n[i].style.setProperty('display', 'none', 'important');
    }
    /* 워드프레스가 붙이는 페이지 제목도 감춥니다 */
    n = document.querySelectorAll('.wp-block-post-title, .entry-title, h1.entry-title');
    for (i = 0; i < n.length; i++) {
      if (!host.contains(n[i])) { n[i].style.setProperty('display', 'none', 'important'); }
    }
    /* 본문 칸의 여백과 최대 너비를 풀어 화면 전체를 씁니다 */
    var box = host.parentNode, hop = 0;
    while (box) {
      if (box === document.body) { break; }
      if (hop > 4) { break; }
      box.style.setProperty('max-width', 'none', 'important');
      box.style.setProperty('margin', '0', 'important');
      box.style.setProperty('padding', '0', 'important');
      box = box.parentNode; hop++;
    }
    document.body.style.setProperty('background', '#F7F2FC', 'important');
  }

  /* 무엇을 감췄는지 보고 싶을 때 : /uandme/?umdebug=1 */
  function debugPanel(host) {
    var out = ['<b>유앤미 진단</b>'];
    out.push('body 표시 : ' + (document.body.classList.contains('um-page') ? 'um-page 붙음' : '안 붙음'));
    out.push('유앤미 머리말 : ' + (document.getElementById('um-top') ? '있음' : '없음'));
    out.push('유앤미 꼬리말 : ' + (document.getElementById('um-foot') ? '있음' : '없음'));
    /* 화면에 아직 보이는 것이 무엇인지 그대로 보여줍니다 */
    var all = document.querySelectorAll('body *'), i, L = [], seen = 0;
    for (i = 0; i < all.length; i++) {
      var e = all[i];
      if (e.closest('#wpadminbar')) { continue; }
      if (e.closest('#um')) { continue; }
      if (e.closest('#um-top')) { continue; }
      if (e.closest('#um-foot')) { continue; }
      if (e.contains(host)) { continue; }
      if (getComputedStyle(e).display === 'none') { continue; }
      var r = e.getBoundingClientRect();
      if (r.height < 24) { continue; }
      if (r.width < 120) { continue; }
      if (e.parentNode) { if (e.parentNode.__um) { continue; } }
      e.__um = 1;
      seen++;
      if (seen > 14) { break; }
      L.push(e.tagName.toLowerCase() +
        (e.id ? '#' + e.id : '') +
        (e.className ? '.' + String(e.className).trim().split(/\s+/).slice(0, 3).join('.') : '') +
        '  [' + Math.round(r.width) + 'x' + Math.round(r.height) + ']');
    }
    out.push('아직 화면에 남아 있는 것 ' + seen + '개');
    out.push(L.length ? L.join('<br>') : '없음 — 깨끗합니다');
    var d = X.el('<div style="position:fixed;left:8px;right:8px;bottom:8px;z-index:99999;' +
      'background:#111;color:#9fd;font:12px/1.7 monospace;padding:14px;border-radius:12px;' +
      'max-height:52vh;overflow:auto">' + out.join('<br>') + '</div>');
    document.body.appendChild(d);
  }

  /* 그림 스물아홉 장을 번호와 함께 봅니다 : /uandme/?umall=1
     「연인을 다9로 바꿔줘」처럼 말씀하시면 그대로 옮깁니다. */
  function picSheet(host) {
    var P = window.UM_PIC || {}, S = (window.UM_SET || {}).그림 || {};
    var used = {}, k;
    for (k in S) { if (S[k]) { used[S[k]] = (used[S[k]] ? used[S[k]] + ' · ' : '') + k; } }
    var keys = Object.keys(P), i, cells = '';
    for (i = 0; i < keys.length; i++) {
      var n = keys[i], u = used[n] || '';
      cells += '<div style="text-align:center">' +
        '<div style="background:#fff;border-radius:18px;padding:6px;' +
        (u ? 'outline:3px solid #B8A6E8;outline-offset:2px' : '') + '">' +
        '<img src="' + esc(P[n]) + '" alt="" style="width:100%;aspect-ratio:1;object-fit:contain;display:block">' +
        '</div>' +
        '<div style="font-family:Jua,sans-serif;font-size:16px;color:#6B5BA8;margin-top:6px">' + n + '</div>' +
        '<div style="font-size:10.5px;color:' + (u ? '#B8A6E8' : '#C9C2DA') + ';line-height:1.5;min-height:26px">' +
        (u ? esc(u) : '안 씀') + '</div></div>';
    }
    host.innerHTML =
      '<div class="pad" style="padding-top:24px">' +
      '<div class="h1" style="font-size:26px">그림 ' + keys.length + '장</div>' +
      '<div class="sub">보라색 테두리가 지금 쓰이는 그림입니다.<br>' +
      '「연인을 다9로 바꿔줘」처럼 말씀해 주세요.</div></div>' +
      '<div class="pad" style="margin-top:22px;display:grid;' +
      'grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">' + cells + '</div>' +
      '<div class="pad" style="margin-top:28px"><a class="btnG" href="?">유앤미로 돌아가기</a></div>';
  }

  /* ── 시작 ────────────────────────────────────────────── */
  function boot() {
    var host = document.getElementById('um');
    if (!host) { return; }
    X.css(); X.setRoot(host); root = host;
    if (!document.getElementById('um-peek-css')) {
      var pc = document.createElement('style');
      pc.id = 'um-peek-css';
      pc.textContent = '#um .peek{position:absolute;z-index:0;' +
        'filter:drop-shadow(0 5px 8px rgba(107,91,168,.22))}' +
        '#um .front{position:relative;z-index:1}' +
        '#um .pop{position:absolute;z-index:3;pointer-events:none;' +
        'filter:drop-shadow(0 6px 10px rgba(107,91,168,.2))}' +
        '#um .tile{display:flex;flex-direction:column;align-items:center;gap:7px}' +
        '#um .tile .im{width:100%;aspect-ratio:1;border-radius:22px;padding:5px;cursor:pointer}' +
        '#um .tile.on .im{outline:3px solid #B8A6E8;outline-offset:2px}' +
        '#um .tile b{font-size:12px;font-weight:500;color:#57506E}' +
        '#um .tile.on b{font-weight:700;color:#6B5BA8}';
      document.head.appendChild(pc);
    }
    document.body.classList.add('um-page');
    hideTheme(host);
    setTimeout(function () { hideTheme(host); }, 400);
    setTimeout(function () { hideTheme(host); }, 1500);
    U.setEngines(window.StellaSaju, window.StellaMatch);
    loadKakao();

    if (location.search.indexOf('umall') >= 0) {
      chrome(); picSheet(host);
      return;
    }

    var q = new URLSearchParams(location.search);
    var i = q.get('i'), r = q.get('r');
    if (r) {
      var d2 = U.unpackLink(r);
      if (d2) { if (d2.b) {
        st.rel = d2.rel; st.me = d2.a; st.you = d2.b;
        try { U.compute(); st.view = 'result'; } catch (e) { st.view = 'home'; }
      } }
    } else if (i) {
      var d1 = U.unpackLink(i);
      if (d1) { st.rel = d1.rel; st.me = d1.a; st.view = 'joined'; draft = { sex: 'M', known: true, ampm: '오전' }; }
    }
    render();
    if (location.search.indexOf('umdebug') >= 0) {
      setTimeout(function () { debugPanel(host); }, 900);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }
})();
