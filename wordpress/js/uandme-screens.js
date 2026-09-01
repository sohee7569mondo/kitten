/* ══════════════════════════════════════════════════════════════
   유앤미 — 화면 다섯과 공유
   주의 · 이 파일 안에서 앰퍼샌드 두 개 연산자를 쓰지 않습니다.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var U = window.UandMe, X = window.UandMeUI, st = U.state;
  var el = X.el, esc = X.esc, IC = X.IC;
  var root = null;

  function go(v) { st.view = v; render(); window.scrollTo(0, 0); }

  /* ── 공유 ────────────────────────────────────────────── */
  function inviteUrl() { return X.base() + '?i=' + U.packLink(st.rel, st.me); }
  function resultUrl() { return X.base() + '?r=' + U.packLink(st.rel, st.me, st.you); }

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
  function kakao(url, text) {
    if (window.Kakao) { if (window.Kakao.Share) {
      try {
        window.Kakao.Share.sendDefault({
          objectType: 'feed',
          content: { title: text, description: '생일만 넣으면 우리 둘 점수가 바로 나와요',
                     imageUrl: location.origin + '/wp-content/uploads/uandme-share.png',
                     link: { mobileWebUrl: url, webUrl: url } },
          buttons: [{ title: '나도 보기', link: { mobileWebUrl: url, webUrl: url } }]
        });
        return;
      } catch (e) {}
    } }
    if (!nativeShare(url, text)) { copy(url); }
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
  function rr(g, x, y, w, h, r) {
    g.beginPath();
    g.moveTo(x + r, y);
    g.arcTo(x + w, y, x + w, y + h, r);
    g.arcTo(x + w, y + h, x, y + h, r);
    g.arcTo(x, y + h, x, y, r);
    g.arcTo(x, y, x + w, y, r);
    g.closePath();
  }

  function shareImage() {
    makeImage(function (blob, canvas) {
      var file = null;
      try { file = new File([blob], 'uandme.png', { type: 'image/png' }); } catch (e) {}
      if (file) { if (navigator.canShare) { if (navigator.canShare({ files: [file] })) {
        navigator.share({ files: [file], text: shareText() }).catch(function () {});
        return;
      } } }
      var a = document.createElement('a');
      a.href = canvas.toDataURL('image/png');
      a.download = 'uandme.png';
      a.click();
      toast('그림을 저장했어요. 인스타에 올려보세요');
    });
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
      '<input class="fld" id="f-y" inputmode="numeric" maxlength="4" placeholder="1994" value="' + (p.y || '') + '" style="flex:1.3">',
      '<input class="fld" id="f-m" inputmode="numeric" maxlength="2" placeholder="03" value="' + (p.m || '') + '">',
      '<input class="fld" id="f-d" inputmode="numeric" maxlength="2" placeholder="21" value="' + (p.d || '') + '">',
      '</div></div>',
      '<div class="pad" style="margin-top:18px"><div class="lbl">태어난 시각</div><div class="row">',
      '<input class="fld" id="f-h" inputmode="numeric" maxlength="2" placeholder="14" style="flex:1">',
      '<input class="fld" id="f-mi" inputmode="numeric" maxlength="2" placeholder="30" style="flex:1">',
      '<button class="seg' + (p.known === false ? ' on' : '') + '" id="f-unk" style="flex:0 0 96px">모름</button>',
      '</div><div class="note" style="margin-top:9px">모르셔도 됩니다. 시각 없이도 나오고, 있으면 조금 더 정확해집니다.</div></div>',
      '<div class="pad" style="margin-top:18px"><div class="lbl">성별</div><div class="row">',
      '<button class="seg' + (p.sex !== 'M' ? ' on' : '') + '" data-sex="F">여성</button>',
      '<button class="seg' + (p.sex === 'M' ? ' on' : '') + '" data-sex="M">남성</button>',
      '</div></div>'
    ].join('');
  }

  var draft = { sex: 'F', known: true };

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
    if (known) { if (h < 0 || h > 23) { toast('시각을 다시 봐주세요'); return null; } }
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
    var b = ['<button class="sh" data-s="kakao"><i style="background:#FAE100">' + IC.talk + '</i><span>카카오톡</span></button>',
             '<button class="sh" data-s="threads"><i style="background:#1A1A1A">' + IC.at + '</i><span>스레드</span></button>'];
    if (withImage) {
      b.push('<button class="sh" data-s="image"><i style="background:#D9578C">' + IC.cam + '</i><span>인스타</span></button>');
      b.push('<button class="sh" data-s="save"><i style="background:#E2F5EE">' + IC.save + '</i><span>그림 저장</span></button>');
    }
    b.push('<button class="sh" data-s="copy"><i style="background:#E7DEFA">' + IC.link + '</i><span>링크 복사</span></button>');
    return '<div style="display:flex;gap:8px">' + b.join('') + '</div>';
  }

  /* ── 유앤미만의 머리말과 꼬리말 ───────────────────────
     스텔라사주의 검은 머리띠는 이 페이지에서만 감춰집니다(옷 쪽에서). */
  var BUN = '<svg viewBox="0 0 120 120" width="32" height="32" style="display:block">' +
    '<g stroke="#5A4038" stroke-width="4.5" stroke-linejoin="round">' +
    '<ellipse cx="45" cy="31" rx="9" ry="25" fill="#fff" transform="rotate(-9 45 31)"/>' +
    '<ellipse cx="75" cy="31" rx="9" ry="25" fill="#fff" transform="rotate(9 75 31)"/>' +
    '<ellipse cx="60" cy="88" rx="31" ry="26" fill="#fff"/>' +
    '<circle cx="60" cy="63" r="27" fill="#fff"/></g>' +
    '<ellipse cx="45" cy="30" rx="4" ry="15" fill="#F7C6D3" transform="rotate(-9 45 30)"/>' +
    '<ellipse cx="75" cy="30" rx="4" ry="15" fill="#F7C6D3" transform="rotate(9 75 30)"/>' +
    '<circle cx="50" cy="61" r="3.6" fill="#5A4038"/><circle cx="70" cy="61" r="3.6" fill="#5A4038"/>' +
    '<ellipse cx="40" cy="70" rx="6.5" ry="4.5" fill="#F7A8BC"/>' +
    '<ellipse cx="80" cy="70" rx="6.5" ry="4.5" fill="#F7A8BC"/>' +
    '<ellipse cx="60" cy="69" rx="4" ry="3" fill="#EE8FA8"/></svg>';

  function chrome() {
    if (!document.getElementById('um-top')) {
      var top = X.el('<div id="um-top"><div class="in">' +
        '<a class="lg" href="/uandme/">' + BUN + '<b>유앤미</b></a>' +
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
        '<p>재미로 보는 궁합입니다. 생년월일은 결과를 만드는 동안에만 쓰이고 ' +
        '서버로 보내지 않습니다. 링크를 지우면 함께 사라집니다.</p>' +
        '<p style="margin-top:10px">stellasaju.com</p></div>');
      root.parentNode.insertBefore(foot, root.nextSibling);
    }
  }

  function render() {
    root = X.getRoot();
    chrome();
    var h = [];
    if (st.view === 'home') {
      h.push('<div class="pad" style="padding-top:34px"><div class="h1">우리 둘,<br>몇 점일까?</div>',
        '<div class="sub">사주 · 별자리 · 띠 셋을 함께 봅니다.<br>가입도 앱 설치도 없어요.</div></div>',
        '<div class="pad" style="margin-top:34px"><div class="lbl">누구와 보나요</div>',
        '<div style="display:flex;flex-wrap:wrap;gap:7px">' + relChips() + '</div></div>',
        '<div class="pad" style="margin-top:30px"><button class="btnP" id="go-mine">시작하기</button></div>',
        '<div class="pad" style="margin-top:22px"><div class="mini">생년월일은 이 기기에만 남습니다. 서버로 보내지 않습니다.</div></div>');
    } else if (st.view === 'mine') {
      h.push('<div class="pad" style="padding-top:30px"><div class="h1">먼저<br>내 것부터</div>',
        '<div class="sub">상대 생일은 몰라도 됩니다. 링크를 보내면 그쪽이 직접 넣어요.</div></div>',
        form('me'),
        '<div class="pad" style="margin-top:28px"><button class="btnP" id="mk-link">궁합 링크 만들기</button>',
        '<div style="height:9px"></div><button class="btnG" id="both">상대 생일도 내가 알아요</button></div>');
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
      h.push('<div class="pad" style="padding-top:26px"><div class="card">',
        '<div style="display:flex;align-items:center;justify-content:space-between">',
        '<div style="background:#FFE2D6;color:#C4674A;font-size:11.5px;font-weight:700;padding:6px 13px;border-radius:999px">' +
        U.relKo(st.rel) + ' 궁합</div>',
        '<div style="font-size:11.5px;color:#B3A9C9;font-weight:500">' +
        esc(st.me.name || '나') + ' × ' + esc(st.you.name || '너') + '</div></div>',
        '<div style="text-align:center;margin-top:16px"><div class="jua" style="font-size:82px;line-height:1;color:#6B5BA8">' +
        r.total + '</div><div style="font-size:12.5px;color:#A79BC4;font-weight:500;margin-top:2px">점</div></div>',
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
        '<div class="pad" style="margin-top:26px"><button class="btnG" id="again">다른 사람과도 보기</button></div>',
        '<div class="pad" style="margin-top:26px"><a href="/" style="text-decoration:none"><div style="display:flex;align-items:center;justify-content:space-between;padding:20px 22px;background:#100B22;border-radius:24px">',
        '<div><div style="font-size:11px;color:#B9A2F2;font-weight:700;margin-bottom:5px">스텔라사주</div>',
        '<div style="font-size:16px;font-weight:700;color:#F6F1E7">내 사주 제대로 읽어보기</div></div>',
        '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#C99A55" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>',
        '</div></a></div>');
    }
    root.innerHTML = h.join('');
    wire();
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
    bind('#go-mine', function () { draft = { sex: 'F', known: true }; go('mine'); });
    bind('#mk-link', function () {
      var p = readForm(); if (!p) { return; }
      st.me = p; U.saveMe(); go('invite');
    });
    bind('#both', function () {
      var p = readForm(); if (!p) { return; }
      st.me = p; U.saveMe(); draft = { sex: 'M', known: true }; go('both');
    });
    bind('#both2', function () { draft = { sex: 'M', known: true }; go('both'); });
    bind('#calc', function () {
      var p = readForm(); if (!p) { return; }
      st.you = p;
      try { U.compute(); } catch (e) { toast('계산이 안 됐어요. 날짜를 다시 봐주세요'); return; }
      history.replaceState(null, '', resultUrl());
      go('result');
    });
    bind('#again', function () {
      st.you = null; st.result = null;
      history.replaceState(null, '', X.base());
      draft = { sex: 'M', known: true }; go('both');
    });
    X.on('[data-s]', 'click', function () {
      var k = this.getAttribute('data-s');
      var url = st.result ? resultUrl() : inviteUrl();
      var text = st.result ? shareText() :
        ((st.me.name || '친구') + '님이 궁합 보자고 해요');
      if (k === 'kakao')   { kakao(url, text); }
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

  /* ── 시작 ────────────────────────────────────────────── */
  function boot() {
    var host = document.getElementById('um');
    if (!host) { return; }
    X.css(); X.setRoot(host); root = host;
    document.body.classList.add('um-page');
    U.setEngines(window.StellaSaju, window.StellaMatch);

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
      if (d1) { st.rel = d1.rel; st.me = d1.a; st.view = 'joined'; draft = { sex: 'M', known: true }; }
    }
    render();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }
})();
