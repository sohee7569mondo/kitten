/* ══════════════════════════════════════════════════════════════
   유앤미 — 두 사람 궁합 (stellasaju.com/uandme/)

   서버에 아무것도 저장하지 않습니다. 두 사람의 생년월일은 링크 안에만
   담겨 돌고, 링크를 지우면 함께 사라집니다.

   화면 다섯
     home    첫 화면 — 관계 고르고 시작
     mine    내 생년월일 넣기
     invite  링크 만들어 보내기
     joined  상대가 링크를 열었을 때
     result  결과 · 돌려보내기 · 자랑하기

   주소
     /uandme/            처음부터
     /uandme/?i=…        초대 링크 (한 사람 정보)
     /uandme/?r=…        결과 링크 (두 사람 정보)

   주의 · 이 파일 안에서 앰퍼샌드 두 개 연산자를 쓰지 않습니다.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var ROOT = null;
  var S = null, M = null;

  /* ── 링크에 담고 푸는 법 ─────────────────────────────── */
  function b64enc(s) {
    return btoa(unescape(encodeURIComponent(s)))
      .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }
  function b64dec(s) {
    s = String(s).replace(/-/g, '+').replace(/_/g, '/');
    while (s.length % 4) { s += '='; }
    try { return decodeURIComponent(escape(atob(s))); } catch (e) { return ''; }
  }
  /* 한 사람 = 성별.생년월일.시각.시각앎.이름 */
  function packOne(p) {
    return [p.sex, p.y + pad2(p.m) + pad2(p.d),
            p.known ? pad2(p.h) + pad2(p.mi) : '',
            p.known ? '1' : '0', p.name || ''].join('~');
  }
  function unpackOne(s) {
    var a = String(s).split('~');
    if (a.length < 5) { return null; }
    var ymd = a[1];
    if (ymd.length !== 8) { return null; }
    var known = a[3] === '1';
    return {
      sex: a[0] === 'M' ? 'M' : 'F',
      y: +ymd.slice(0, 4), m: +ymd.slice(4, 6), d: +ymd.slice(6, 8),
      h: known ? +a[2].slice(0, 2) : 12,
      mi: known ? +a[2].slice(2, 4) : 0,
      known: known,
      name: a[4] || ''
    };
  }
  function packLink(rel, a, b) {
    var parts = ['1', rel, packOne(a)];
    if (b) { parts.push(packOne(b)); }
    return b64enc(parts.join('|'));
  }
  function unpackLink(t) {
    var raw = b64dec(t);
    if (!raw) { return null; }
    var a = raw.split('|');
    if (a[0] !== '1') { return null; }
    var one = unpackOne(a[2]);
    if (!one) { return null; }
    return { rel: a[1] || 'lover', a: one, b: a[3] ? unpackOne(a[3]) : null };
  }
  function pad2(n) { return (n < 10 ? '0' : '') + n; }

  /* ── 관계 이름표 ─────────────────────────────────────── */
  var RELS = [
    { key: 'lover',        ko: '연인' },
    { key: 'married',      ko: '부부' },
    { key: 'friend',       ko: '친구' },
    { key: 'sibling',      ko: '형제자매' },
    { key: 'parent_child', ko: '부모와 자녀' },
    { key: 'boss_sub',     ko: '상사와 부하' },
    { key: 'partner',      ko: '동업자' }
  ];
  function relKo(k) {
    var i;
    for (i = 0; i < RELS.length; i++) { if (RELS[i].key === k) { return RELS[i].ko; } }
    return '연인';
  }

  /* ── 사주 세우기 ─────────────────────────────────────── */
  function chartOf(p) {
    return S.compute({
      year: p.y, month: p.m, day: p.d,
      hour: p.known ? p.h : 12, minute: p.known ? p.mi : 0,
      sex: p.sex, lat: 37.5665, lon: 126.9780, hourKnown: p.known
    });
  }

  /* ── 상태 ────────────────────────────────────────────── */
  var st = {
    view: 'home',
    rel: 'lover',
    me: null,
    you: null,
    result: null
  };

  function saveMe() {
    try { localStorage.setItem('uandme_me', JSON.stringify(st.me)); } catch (e) {}
  }
  function loadMe() {
    try {
      var v = localStorage.getItem('uandme_me');
      return v ? JSON.parse(v) : null;
    } catch (e) { return null; }
  }

  /* ── 화면 그리기는 render.js 쪽에서 이어집니다 ────────── */
  window.UandMe = {
    packLink: packLink, unpackLink: unpackLink,
    packOne: packOne, unpackOne: unpackOne,
    chartOf: chartOf, relKo: relKo, RELS: RELS,
    state: st, saveMe: saveMe, loadMe: loadMe,
    setEngines: function (saju, match) { S = saju; M = match; },
    compute: function () {
      var A = chartOf(st.me), B = chartOf(st.you);
      st.result = M.match(A, B, st.rel);
      st.result.chartA = A;
      st.result.chartB = B;
      return st.result;
    },
    b64enc: b64enc, b64dec: b64dec
  };
})();
