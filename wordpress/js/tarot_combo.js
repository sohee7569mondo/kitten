  /* ═══ 셋을 겹쳐 놓으면 ═══════════════════════════════════════
     2026-09-09 · 소희 님 : 「세 장 그림 설명만 있어. 예전엔 세 장에
     대한 설명이 있었는데」

     한 장씩 읽는 것과 셋을 겹쳐 읽는 것은 다릅니다. 조합이 수만
     가지라 하나하나 쓸 수 없으므로 세 잣대로만 읽습니다 —
     큰 카드가 몇 장인가 · 숫자가 오르는가 내리는가 · 뒤집힌 것이 몇 장인가.
     책에서 이미 쓰는 방식이라 손님이 낯설어하지 않습니다.

     ★ 이 안에서 두 글자짜리 논리기호를 쓰지 않습니다 (워드프레스가 망가뜨림) */
  var TCOMBO_STYLE =
      '<style>'
    + '#ssa .combo{ margin-top:28px; padding:26px 28px; border-radius:12px;'
    + ' background:var(--nebula-soft); border:1px solid var(--line); }'
    + '@media(max-width:700px){ #ssa .combo{ padding:22px 18px; } }'
    + '#ssa .combo h3{ font-size:1.14rem; margin-bottom:6px; }'
    + '#ssa .combo-lead{ font-size:.88rem; color:var(--ink-dim); line-height:1.85;'
    + ' margin-bottom:18px; }'
    + '#ssa .combo-row{ display:grid; grid-template-columns:88px 1fr; gap:18px;'
    + ' padding:16px 0; border-top:1px solid var(--line); }'
    + '@media(max-width:560px){ #ssa .combo-row{ grid-template-columns:1fr; gap:6px; } }'
    + '#ssa .combo-k{ font-family:"IBM Plex Mono",monospace; font-size:.7rem;'
    + ' letter-spacing:.16em; color:var(--g-accent); padding-top:5px; }'
    + '#ssa .combo-v p{ margin:0 0 9px; font-size:.98rem; line-height:1.9;'
    + ' color:var(--ink-soft); }'
    + '#ssa .combo-v p:last-child{ margin-bottom:0; }'
    + '#ssa .combo-v em{ font-style:normal; color:var(--star); font-weight:700; }'
    + '</style>';

  var TCOMBO = {
    m0: '<p>세 장이 모두 <em>작은 카드</em>입니다. 큰 카드가 한 장도 없어요.</p>'
      + '<p>큰 사건이 판을 뒤집는 때가 아니라 <em>매일의 선택이 결과를 만드는 때</em>입니다.'
      + ' 갑자기 달라지는 일은 없습니다. 대신 오늘 하시는 것이 그대로 쌓여요.</p>',
    m1: '<p>큰 카드가 <em>한 장</em> 섞여 있습니다.</p>'
      + '<p>세 자리 가운데 하나는 <em>당신 뜻과 상관없이 움직입니다.</em>'
      + ' 나머지 둘은 정하시는 대로 가요. 그 한 자리에서만 힘을 빼고 지켜보셔도 됩니다.</p>',
    m2: '<p>큰 카드가 <em>{N} 장</em>이나 됩니다.</p>'
      + '<p><em>조용히 지나가지 않는 때</em>입니다. 좋은 쪽이든 아닌 쪽이든 지금과 같은'
      + ' 모양으로 끝나지는 않아요. 계획을 너무 촘촘히 잡아두시면 오히려 어긋납니다.</p>',

    up: '<p>숫자가 <em>올라갑니다.</em> 지금이 가장 낮고 뒤로 갈수록 커지는 모양이에요.</p>'
      + '<p>지금 답답한 것이 바닥입니다. <em>여기서 더 나빠지지는 않습니다.</em>'
      + ' 다만 올라가는 속도가 느려서 한동안은 티가 안 나요.</p>',
    down: '<p>숫자가 <em>내려갑니다.</em> 지금이 가장 크고 뒤로 갈수록 작아지는 모양이에요.</p>'
      + '<p>나빠진다는 뜻이 아닙니다. <em>벌여둔 것을 정리하고 매듭짓는 때</em>라는 뜻이에요.'
      + ' 새로 크게 벌이시면 이번에는 결론이 안 납니다.</p>',
    flat: '<p>숫자가 <em>크게 오르지도 내리지도 않습니다.</em> 평평한 모양이에요.</p>'
      + '<p>당분간 비슷하게 흘러갑니다. 답답하실 수 있는데 <em>흔들리지 않는다는 뜻</em>이기도'
      + ' 합니다. 이런 때에 정해둔 것이 제일 오래 갑니다.</p>',

    r0: '<p>세 장이 모두 <em>바로 놓였습니다.</em> 뒤집힌 것이 하나도 없어요.</p>'
      + '<p>보이는 대로 가는 때입니다. 숨은 뜻을 찾으실 것 없어요.'
      + ' <em>지금 눈에 보이는 것이 그대로 답</em>입니다.</p>',
    r3: '<p>세 장이 <em>모두 뒤집혀</em> 나왔습니다. 흔한 일이 아닙니다.</p>'
      + '<p><em>제자리에서 한 번 멈춰 있는 때</em>라는 뜻이에요. 나쁜 것이 아니라'
      + ' 방향을 바꾸기 직전입니다. 이럴 때 밀어붙이면 더 안 갑니다.</p>',
    rs: '<p>세 장 가운데 <em>{N} 장</em>이 뒤집혀 나왔습니다.</p>'
      + '<p>뒤집힌 자리는 <em>아직 때가 안 됐다</em>는 뜻입니다. 없던 일이 되는 것이 아니라'
      + ' 늦는 거예요. 당기려 하시면 그 자리만 어긋납니다.</p>'
  };

  /* 카드의 「숫자」 — 작은 카드는 spd, 큰 카드는 놓인 차례를 씁니다.
     둘 다 0~21 사이라 그대로 견줄 수 있습니다. */
  function tcRank(c){
    if(c.spd){ return c.spd; }
    var i = TAROT.indexOf(c);
    if(i < 0){ return 0; }
    if(i <= 21){ return i; }
    return 0;
  }
  function tcIsMajor(c){
    var i = TAROT.indexOf(c);
    if(i < 0){ return false; }
    if(i <= 21){ return true; }
    return false;
  }

  function comboHtml(got){
    if(!got){ return ''; }
    if(got.length < 3){ return ''; }

    var i, majorN = 0, revN = 0;
    for(i = 0; i < 3; i++){
      if(tcIsMajor(got[i].card)){ majorN++; }
      if(got[i].rev){ revN++; }
    }
    var flow = tcRank(got[2].card) - tcRank(got[0].card);

    var mKey = 'm2';
    if(majorN === 0){ mKey = 'm0'; }
    if(majorN === 1){ mKey = 'm1'; }

    var fKey = 'flat';
    if(flow >= 4){ fKey = 'up'; }
    if(flow <= -4){ fKey = 'down'; }

    var rKey = 'rs';
    if(revN === 0){ rKey = 'r0'; }
    if(revN === 3){ rKey = 'r3'; }

    var KO = ['','한','두','세'];
    function put(k, n){
      var t = TCOMBO[k];
      if(!t){ return ''; }
      var w = KO[n];
      if(!w){ w = '' + n; }
      return t.split('{N}').join(w);
    }

    return TCOMBO_STYLE
      + '<section class="combo"><!-- STELLA-TCOMBO-v1 -->'
      + '<h3>셋을 겹쳐 놓으면</h3>'
      + '<p class="combo-lead">한 장씩 읽는 것과 셋을 겹쳐 읽는 것은 다릅니다.'
      + ' 조합이 너무 많아 하나하나 적을 수 없으니, 세 가지만 봅니다.</p>'
      + '<div class="combo-row"><div class="combo-k">큰 카드</div>'
      + '<div class="combo-v">' + put(mKey, majorN) + '</div></div>'
      + '<div class="combo-row"><div class="combo-k">흐름</div>'
      + '<div class="combo-v">' + put(fKey, 0) + '</div></div>'
      + '<div class="combo-row"><div class="combo-k">뒤집힘</div>'
      + '<div class="combo-v">' + put(rKey, revN) + '</div></div>'
      + '</section>';
  }

