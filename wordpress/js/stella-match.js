/* ══════════════════════════════════════════════════════════════
   스텔라 궁합 — 두 사람의 사주를 견주어 점수를 냅니다
   유앤미(stellasaju.com/uandme)에서 씁니다.

   StellaSaju.compute() 가 뽑아준 두 사람의 사주를 받아
   0~100 점과 네 항목 점수를 돌려줍니다.

   보는 것 셋 — 생년월일 하나로 물어보지 않고 뽑을 수 있는 것들입니다.

     ① 사주   40점  일지(14) · 일간(11) · 오행 보완(8) · 십성(7)
     ② 별자리 30점  두 별자리의 원소와 각도
     ③ 띠     30점  삼합 · 육합 · 충 · 형 · 해 · 원진

   사주가 가장 무겁고, 별자리와 띠가 그 옆을 받칩니다.
   셋을 따로 보여주면 손님이 「사주는 높은데 띠가 낮네」처럼
   읽을 수 있어 이야깃거리가 생깁니다.

   같은 계산이라도 관계(연인 · 부부 · 친구 · 동업 …)에 따라
   사주의 십성 가중치가 달라집니다. 연인에게 좋은 배치와
   동업에 좋은 배치가 다르기 때문입니다.

   주의 · 이 파일 안에서 앰퍼샌드 두 개 연산자를 쓰지 않습니다
          (워드프레스가 엔티티로 바꿔 스크립트를 죽입니다).
   ══════════════════════════════════════════════════════════════ */
(function (root) {
  'use strict';

  var GAN_EL = ['목','목','화','화','토','토','금','금','수','수'];
  var JI_EL  = ['수','토','목','목','토','화','화','토','금','금','토','수'];
  var GAN_H  = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'];
  var JI_H   = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
  var ANIMAL = ['쥐','소','호랑이','토끼','용','뱀','말','양','원숭이','닭','개','돼지'];

  /* 오행 상생 : 목→화→토→금→수→목 */
  var GEN = { '목':'화', '화':'토', '토':'금', '금':'수', '수':'목' };
  /* 오행 상극 : 목→토→수→화→금→목 */
  var OVR = { '목':'토', '토':'수', '수':'화', '화':'금', '금':'목' };

  function pairKey(a, b) { return Math.min(a,b) + '-' + Math.max(a,b); }
  function has(list, a, b) { return list.indexOf(pairKey(a,b)) >= 0; }
  function mk(pairs) { return pairs.map(function (p) { return pairKey(p[0], p[1]); }); }

  /* ── 지지 관계표 ─────────────────────────────────────── */
  var YUKHAP  = mk([[0,1],[2,11],[3,10],[4,9],[5,8],[6,7]]);          /* 육합 */
  var SAMHAP  = [[8,0,4],[11,3,7],[2,6,10],[5,9,1]];                  /* 삼합 */
  var BANGHAP = [[2,3,4],[5,6,7],[8,9,10],[11,0,1]];                  /* 방합 */
  var CHUNG   = mk([[0,6],[1,7],[2,8],[3,9],[4,10],[5,11]]);          /* 충 */
  var HAE     = mk([[0,7],[1,6],[2,5],[3,4],[8,11],[9,10]]);          /* 해 */
  var WONJIN  = mk([[0,7],[1,6],[2,9],[3,8],[4,11],[5,10]]);          /* 원진 */
  var HYUNG   = mk([[2,5],[5,8],[2,8],[1,10],[10,7],[1,7],[0,3]]);    /* 형 */

  function inTri(sets, a, b) {
    var i;
    for (i = 0; i < sets.length; i++) {
      if (sets[i].indexOf(a) >= 0) { if (sets[i].indexOf(b) >= 0) { if (a !== b) { return true; } } }
    }
    return false;
  }

  /* ── ① 일간 관계 ─────────────────────────────────────── */
  function ganScore(a, b) {
    var note, sc;
    if ((a + 5) % 10 === b % 10) {
      sc = 25; note = '두 분의 일간이 서로 손을 잡는 자리입니다(천간합). 처음부터 편하게 느껴지는 조합이에요.';
    } else if (Math.abs(a - b) === 6 || Math.abs(a - b) === 4) {
      var ea = GAN_EL[a], eb = GAN_EL[b];
      if (OVR[ea] === eb || OVR[eb] === ea) {
        sc = 10; note = '일간끼리 부딪히는 자리입니다. 서로 다른 방식이 부딪히니 말로 풀어야 합니다.';
      } else {
        sc = 17; note = '일간이 서로 다른 결입니다. 나쁘지 않지만 맞춰가는 시간이 필요합니다.';
      }
    } else {
      var e1 = GAN_EL[a], e2 = GAN_EL[b];
      if (e1 === e2) {
        sc = 18; note = '두 분의 일간이 같은 기운입니다. 잘 통하는 대신 같은 것을 원해 부딪히기도 합니다.';
      } else if (GEN[e1] === e2 || GEN[e2] === e1) {
        sc = 23; note = '한쪽이 다른 쪽을 밀어주는 자리입니다(상생). 함께 있으면 힘이 붙습니다.';
      } else if (OVR[e1] === e2 || OVR[e2] === e1) {
        sc = 12; note = '한쪽이 다른 쪽을 누르는 자리입니다(상극). 역할이 분명해야 편해집니다.';
      } else {
        sc = 17; note = '일간이 서로 무난한 거리에 있습니다.';
      }
    }
    return { score: sc, note: note };
  }

  /* ── ② 일지 관계 (부부궁) ────────────────────────────── */
  function jiScore(a, b) {
    var sc, note;
    if (has(YUKHAP, a, b)) {
      sc = 30; note = '두 분의 일지가 짝을 이룹니다(육합). 궁합에서 가장 좋게 보는 자리입니다.';
    } else if (inTri(SAMHAP, a, b)) {
      sc = 27; note = '일지가 같은 무리에 듭니다(삼합). 뜻이 잘 맞고 오래 갑니다.';
    } else if (inTri(BANGHAP, a, b)) {
      sc = 24; note = '일지가 같은 계절에 있습니다(방합). 사는 결이 비슷합니다.';
    } else if (has(CHUNG, a, b)) {
      sc = 9;  note = '일지가 정면으로 부딪힙니다(충). 끌리는 힘도 크지만 흔들림도 큽니다.';
    } else if (has(WONJIN, a, b)) {
      sc = 11; note = '일지가 서로 미묘하게 어긋납니다(원진). 이유 없이 서운한 순간이 옵니다.';
    } else if (has(HYUNG, a, b)) {
      sc = 13; note = '일지가 서로를 깎는 자리입니다(형). 가까울수록 말이 날카로워지기 쉽습니다.';
    } else if (has(HAE, a, b)) {
      sc = 15; note = '일지가 살짝 어긋납니다(해). 큰 문제는 아니지만 오해가 쌓이기 쉽습니다.';
    } else if (a === b) {
      sc = 21; note = '일지가 같습니다. 서로를 잘 이해하는 대신 같은 약점도 나눠 갖습니다.';
    } else {
      sc = 19; note = '일지가 특별히 얽히지 않았습니다. 무난하게 흘러가는 자리입니다.';
    }
    return { score: sc, note: note };
  }

  /* ── ③ 오행 보완 ─────────────────────────────────────── */
  function fiveMap(five) {
    var m = {}, i;
    for (i = 0; i < five.length; i++) { m[five[i].element] = five[i].percent; }
    return m;
  }

  function fiveScore(fa, fb) {
    var A = fiveMap(fa), B = fiveMap(fb);
    var els = ['목','화','토','금','수'];
    var filled = 0, thin = 0, i, e, gap;
    for (i = 0; i < els.length; i++) {
      e = els[i];
      var va = A[e] || 0, vb = B[e] || 0;
      if (va < 12) {
        thin++;
        if (vb >= 20) { filled++; }
      }
    }
    /* 두 사람을 합쳤을 때 얼마나 고르게 되는가 */
    var spread = 0;
    for (i = 0; i < els.length; i++) {
      e = els[i];
      var mixed = ((A[e] || 0) + (B[e] || 0)) / 2;
      spread += Math.abs(mixed - 20);
    }
    var even = Math.max(0, 12 - Math.round(spread / 5));      /* 0~12 */
    var help = thin === 0 ? 6 : Math.round((filled / thin) * 8); /* 0~8 */
    var sc = Math.min(20, even + help);

    var note;
    if (filled > 0) {
      note = '한 분에게 얇은 기운을 다른 분이 넉넉히 가지고 있습니다. 서로 채워주는 자리가 ' + filled + '곳 있어요.';
    } else if (thin === 0) {
      note = '두 분 다 다섯 기운이 고르게 들어 있습니다. 크게 기대지 않아도 각자 서는 조합입니다.';
    } else {
      note = '두 분이 같은 기운을 얇게 가지고 있습니다. 그 자리는 서로 채워주기 어려워 바깥에서 구해야 합니다.';
    }
    return { score: sc, note: note };
  }

  /* ── ④ 십성 관계 : 그의 일간이 나에게 무엇인가 ────────── */
  function tenGod(myGan, hisGan) {
    var me = GAN_EL[myGan], his = GAN_EL[hisGan];
    var sameYin = (myGan % 2) === (hisGan % 2);
    if (me === his)      { return sameYin ? '비견' : '겁재'; }
    if (GEN[me] === his) { return sameYin ? '식신' : '상관'; }
    if (OVR[me] === his) { return sameYin ? '편재' : '정재'; }
    if (OVR[his] === me) { return sameYin ? '편관' : '정관'; }
    if (GEN[his] === me) { return sameYin ? '편인' : '정인'; }
    return '비견';
  }

  function group(g) {
    if (g === '비견' || g === '겁재') { return '비겁'; }
    if (g === '식신' || g === '상관') { return '식상'; }
    if (g === '편재' || g === '정재') { return '재성'; }
    if (g === '편관' || g === '정관') { return '관성'; }
    return '인성';
  }

  /* 관계 유형마다 반가운 십성이 다릅니다 */
  var LIKE = {
    lover:        { '재성':15, '관성':14, '인성':11, '식상':10, '비겁':8 },
    married:      { '재성':15, '관성':14, '인성':12, '비겁':10, '식상':8 },
    friend:       { '비겁':15, '식상':13, '인성':11, '재성':9,  '관성':7 },
    sibling:      { '비겁':15, '인성':13, '식상':11, '재성':9,  '관성':7 },
    parent_child: { '인성':15, '식상':13, '비겁':10, '관성':9,  '재성':8 },
    boss_sub:     { '관성':15, '인성':13, '식상':11, '재성':10, '비겁':6 },
    partner:      { '식상':15, '재성':14, '비겁':12, '관성':9,  '인성':8 }
  };

  var GROUP_SAY = {
    lover: {
      '재성':'상대가 당신에게 「챙기고 싶은 사람」으로 옵니다. 잘해주고 싶어지는 자리예요.',
      '관성':'상대가 당신에게 「기준이 되는 사람」으로 옵니다. 어렵고도 끌립니다.',
      '인성':'상대가 당신에게 「기댈 수 있는 사람」으로 옵니다. 편안한 대신 설렘은 덜합니다.',
      '식상':'상대 앞에서 말이 많아지고 표현이 늘어납니다. 같이 있으면 재미있는 조합이에요.',
      '비겁':'상대가 당신과 비슷한 사람입니다. 친구 같은 연애가 되기 쉽습니다.'
    },
    married: {
      '재성':'상대를 건사하고 싶어지는 자리입니다. 살림과 돈에서 역할이 분명해집니다.',
      '관성':'상대가 집안의 기준을 세우는 쪽이 됩니다. 그 기준이 서로 맞으면 아주 단단합니다.',
      '인성':'상대가 당신을 감싸주는 자리입니다. 힘들 때 무너지지 않는 조합이에요.',
      '식상':'같이 있으면 말이 많아지는 부부입니다. 대화가 끊기지 않는 것이 이 조합의 힘입니다.',
      '비겁':'동갑 친구처럼 사는 부부입니다. 편한 대신 서로 양보를 안 하려 들 수 있어요.'
    },
    friend: {
      '비겁':'말이 통하는 자리입니다. 설명하지 않아도 아는 사이가 됩니다.',
      '식상':'같이 있으면 재미있어지는 조합입니다. 노는 합이 잘 맞아요.',
      '인성':'상대가 당신을 챙겨주는 쪽입니다. 힘들 때 먼저 떠오르는 사람이 됩니다.',
      '재성':'상대를 챙기게 되는 자리입니다. 오래 가려면 셈은 분명히 하세요.',
      '관성':'상대가 조금 어렵게 느껴지는 자리입니다. 편한 사이가 되기까지 시간이 걸립니다.'
    },
    sibling: {
      '비겁':'가장 형제다운 자리입니다. 싸워도 금방 돌아옵니다.',
      '인성':'상대가 당신을 돌보는 쪽입니다. 손윗사람 노릇을 하게 되는 조합이에요.',
      '식상':'같이 있으면 시끄럽고 재미있습니다. 명절에 분위기를 살리는 조합입니다.',
      '재성':'상대를 챙기게 되는 자리입니다. 돈 문제만 분명히 하면 오래 갑니다.',
      '관성':'상대가 어렵게 느껴지는 자리입니다. 어릴 때 비교를 많이 받았을 수 있어요.'
    },
    parent_child: {
      '인성':'가장 부모자녀다운 자리입니다. 주고받는 방향이 자연스럽습니다.',
      '식상':'아이가 당신에게 마음을 잘 꺼내놓습니다. 말이 통하는 조합이에요.',
      '비겁':'친구 같은 사이가 됩니다. 편한 대신 어른 노릇 하기가 어려울 수 있어요.',
      '관성':'상대가 당신에게 기준을 세우는 자리입니다. 서로 존중이 필요합니다.',
      '재성':'상대를 건사하는 마음이 큽니다. 다 해주려다 지치지 않게 하세요.'
    },
    boss_sub: {
      '관성':'일에서는 가장 반듯한 자리입니다. 지시와 보고가 깔끔하게 오갑니다.',
      '인성':'상대에게 배우는 것이 많은 자리입니다. 오래 두면 크게 성장합니다.',
      '식상':'아이디어가 잘 나오는 조합입니다. 다만 절차는 따로 챙겨야 합니다.',
      '재성':'성과로 이어지기 좋은 자리입니다. 숫자로 이야기하면 잘 맞습니다.',
      '비겁':'같은 자리를 노리게 되는 조합입니다. 역할을 분명히 나눠야 합니다.'
    },
    partner: {
      '식상':'같이 만들어내는 것이 많은 조합입니다. 새 일을 벌이기에 좋습니다.',
      '재성':'돈이 되는 방향을 함께 봅니다. 사업 파트너로는 반가운 자리예요.',
      '비겁':'힘을 합치기 좋은 자리입니다. 대신 지분과 역할은 종이에 적으세요.',
      '관성':'상대가 기준을 세우는 쪽입니다. 관리와 실행이 나뉘면 잘 굴러갑니다.',
      '인성':'상대에게 배우며 가는 조합입니다. 속도는 느려도 안전합니다.'
    }
  };

  function godScore(myGan, hisGan, rel) {
    var g = tenGod(myGan, hisGan);
    var gr = group(g);
    var tbl = LIKE[rel] || LIKE.lover;
    var say = (GROUP_SAY[rel] || GROUP_SAY.lover)[gr];
    return { score: tbl[gr], god: g, group: gr, note: say };
  }

  /* ── ② 띠 궁합 (30점) ──────────────────────────────── */
  function animalScore(a, b) {
    var sc, note;
    var na = ANIMAL[a], nb = ANIMAL[b];
    if (inTri(SAMHAP, a, b)) {
      sc = 30; note = na + '띠와 ' + nb + '띠는 삼합입니다. 예로부터 가장 잘 맞는 띠로 봅니다.';
    } else if (has(YUKHAP, a, b)) {
      sc = 27; note = na + '띠와 ' + nb + '띠는 육합입니다. 서로를 편하게 하는 띠예요.';
    } else if (inTri(BANGHAP, a, b)) {
      sc = 24; note = na + '띠와 ' + nb + '띠는 같은 계절의 띠입니다. 사는 결이 비슷합니다.';
    } else if (a === b) {
      sc = 20; note = '두 분 다 ' + na + '띠입니다. 서로를 잘 알지만 같은 약점도 나눠 갖습니다.';
    } else if (has(CHUNG, a, b)) {
      sc = 8;  note = na + '띠와 ' + nb + '띠는 충입니다. 끌리면서도 부딪히는 조합이에요.';
    } else if (has(WONJIN, a, b)) {
      sc = 10; note = na + '띠와 ' + nb + '띠는 원진입니다. 이유 없이 서운해지는 순간이 옵니다.';
    } else if (has(HYUNG, a, b)) {
      sc = 13; note = na + '띠와 ' + nb + '띠는 형입니다. 가까울수록 말이 날카로워지기 쉽습니다.';
    } else if (has(HAE, a, b)) {
      sc = 15; note = na + '띠와 ' + nb + '띠는 해입니다. 큰 탈은 없지만 오해가 쌓이기 쉬워요.';
    } else {
      sc = 18; note = na + '띠와 ' + nb + '띠는 특별히 얽히지 않은 사이입니다.';
    }
    return { score: sc, note: note };
  }

  /* ── ③ 별자리 궁합 (30점) ──────────────────────────── */
  var SIGNS = ['양자리','황소자리','쌍둥이자리','게자리','사자자리','처녀자리',
               '천칭자리','전갈자리','사수자리','염소자리','물병자리','물고기자리'];
  var SIGN_EL = ['불','흙','공기','물','불','흙','공기','물','불','흙','공기','물'];

  function signIndex(name) {
    var i = SIGNS.indexOf(name);
    return i < 0 ? 0 : i;
  }

  function zodiacScore(a, b) {
    var d = Math.abs(a - b);
    if (d > 6) { d = 12 - d; }
    var na = SIGNS[a], nb = SIGNS[b];
    var ea = SIGN_EL[a], eb = SIGN_EL[b];
    var sc, note;
    if (d === 4) {
      sc = 30; note = na + '와 ' + nb + '는 같은 ' + ea + ' 기운입니다(120도). 별자리 궁합에서 가장 좋게 보는 자리예요. 말하지 않아도 통합니다.';
    } else if (d === 2) {
      sc = 26; note = na + '와 ' + nb + '는 서로를 북돋우는 자리입니다(60도). ' + ea + '과 ' + eb + '은 함께 있으면 힘이 붙어요.';
    } else if (d === 0) {
      sc = 22; note = '두 분 다 ' + na + '입니다. 같은 방식으로 세상을 보니 편한 대신, 같은 곳에서 같이 막힙니다.';
    } else if (d === 6) {
      sc = 19; note = na + '와 ' + nb + '는 마주 보는 자리입니다(180도). 정반대라서 끌리고, 정반대라서 부딪힙니다.';
    } else if (d === 1) {
      sc = 15; note = na + '와 ' + nb + '는 바로 옆자리입니다. 가까운데 결이 달라 묘하게 안 맞을 때가 있어요.';
    } else if (d === 3) {
      sc = 12; note = na + '와 ' + nb + '는 직각으로 부딪힙니다(90도). 서로를 자극해서 성장시키지만 편하지는 않습니다.';
    } else {
      sc = 10; note = na + '와 ' + nb + '는 서로 어긋난 자리입니다(150도). 이해하려면 설명이 많이 필요합니다.';
    }
    return { score: sc, note: note, elements: ea + ' · ' + eb };
  }

  /* ── 합쳐서 점수 만들기 ──────────────────────────────── */
  function match(chartA, chartB, rel) {
    rel = LIKE[rel] ? rel : 'lover';

    var ga = chartA.pillars.day.gan, gb = chartB.pillars.day.gan;
    var ja = chartA.pillars.day.ji,  jb = chartB.pillars.day.ji;
    var ya = chartA.pillars.year.ji, yb = chartB.pillars.year.ji;
    var za = signIndex(chartA.stars.sun.name), zb = signIndex(chartB.stars.sun.name);

    /* ① 사주 40점 — 네 가지를 각각 제 몫으로 줄입니다 */
    var f1 = ganScore(ga, gb);                     /* /25 → 11 */
    var f2 = jiScore(ja, jb);                      /* /30 → 14 */
    var f3 = fiveScore(chartA.five, chartB.five);  /* /20 →  8 */
    var gA = godScore(ga, gb, rel);                /* 그가 나에게 */
    var gB = godScore(gb, ga, rel);                /* 내가 그에게 */
    var f4raw = (gA.score + gB.score) / 2;         /* /15 →  7 */

    var sGan  = f1.score / 25 * 11;
    var sJi   = f2.score / 30 * 14;
    var sFive = f3.score / 20 * 8;
    var sGod  = f4raw / 15 * 7;
    var saju  = sGan + sJi + sFive + sGod;         /* 0~40 */

    /* ② 별자리 30점 · ③ 띠 30점 */
    var zo = zodiacScore(za, zb);
    var an = animalScore(ya, yb);

    var raw = saju + zo.score + an.score;          /* 이론상 0~100, 실제로는 중간에 모입니다 */

    /* 세 덩어리를 그냥 더하면 3000쌍 기준으로 36~95, 평균 65 에 모입니다.
       그대로 쓰면 「천생연분」도 「이번 생은 예능감」도 거의 안 나와서
       자랑할 맛이 없습니다. 그 폭을 0~100 으로 펴되, 살짝 위로 당깁니다
       (지수 0.7). 운세는 조금 후한 편이 낫고, 낮은 점수는 드물어야
       나왔을 때 웃깁니다. 순서는 그대로라 좋은 궁합이 나쁜 궁합보다
       낮게 나오는 일은 없습니다. */
    var t = (raw - 36) / 59;
    if (t < 0) { t = 0; }
    if (t > 1) { t = 1; }
    var total = Math.round(100 * Math.pow(t, 0.7));
    total = Math.max(1, Math.min(99, total));

    /* 네 항목 — 같은 재료를 다르게 섞습니다 */
    var pGan  = f1.score / 25, pJi = f2.score / 30;
    var pFive = f3.score / 20, pGod = f4raw / 15;
    var pZo   = zo.score / 30, pAn = an.score / 30;

    function clamp(x) { return Math.max(1, Math.min(100, Math.round(x))); }

    var personality = clamp(pGan * 35 + pZo * 40 + pFive * 25);
    var love        = clamp(pJi  * 40 + pGod * 25 + pZo * 25 + pGan * 10);
    var marriage    = clamp(pJi  * 35 + pAn * 30 + pFive * 20 + pGan * 15);
    var money       = clamp(pFive * 35 + pGod * 35 + pJi * 20 + pAn * 10);

    return {
      total: total,
      raw: Math.round(raw),
      relationship: rel,
      categories: {
        personality: personality,
        love: love,
        marriage: marriage,
        money: money
      },
      /* 세 덩어리 — 화면에 막대 셋으로 보여줍니다 */
      blocks: {
        saju:   { score: Math.round(saju),     max: 40 },
        zodiac: { score: zo.score,             max: 30, pair: SIGNS[za] + ' · ' + SIGNS[zb],
                  elements: zo.elements, note: zo.note },
        animal: { score: an.score,             max: 30, pair: ANIMAL[ya] + '띠 · ' + ANIMAL[yb] + '띠',
                  note: an.note }
      },
      /* 사주 안쪽 — 「자세히 보기」에서 풀어줍니다 */
      parts: {
        gan:  { score: Math.round(sGan * 10) / 10,  max: 11, note: f1.note,
                pair: GAN_H[ga] + ' · ' + GAN_H[gb] },
        ji:   { score: Math.round(sJi * 10) / 10,   max: 14, note: f2.note,
                pair: JI_H[ja] + ' · ' + JI_H[jb] },
        five: { score: Math.round(sFive * 10) / 10, max: 8,  note: f3.note },
        god:  { score: Math.round(sGod * 10) / 10,  max: 7,
                aToB: gA.god, bToA: gB.god,
                note: gA.note, noteBack: gB.note }
      }
    };
  }

  root.StellaMatch = { match: match, tenGod: tenGod, ANIMAL: ANIMAL, SIGNS: SIGNS };
})(typeof window !== 'undefined' ? window : globalThis);

if (typeof module !== 'undefined') { module.exports = globalThis.StellaMatch; }
