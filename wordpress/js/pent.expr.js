(function(){
  try{
    var five = chart.five;
    var NM = { '목':'나무', '화':'불', '토':'흙', '금':'쇠', '수':'물' };
    var ORDER = ['목','화','토','금','수'];   /* 상생 차례로 시계방향 */
    var by = {}, i, j;
    for(i=0; i<five.length; i++){ by[five[i].element] = five[i]; }

    var max = 0;
    for(i=0; i<ORDER.length; i++){
      var f0 = by[ORDER[i]];
      if(!f0){ continue; }
      if(f0.count > max){ max = f0.count; }
    }
    if(max < 1){ return ''; }

    var CX = 170, CY = 130, R = 88;
    function pt(k, m){
      var a = (-90 + k * 72) * Math.PI / 180;
      return [ CX + Math.cos(a) * R * m, CY + Math.sin(a) * R * m ];
    }
    function poly(m){
      var s = [], p;
      for(j=0; j<5; j++){ p = pt(j, m); s.push(p[0].toFixed(1) + ',' + p[1].toFixed(1)); }
      return s.join(' ');
    }

    /* 거미줄 — 네 겹의 오각형과 다섯 갈래 */
    var web = '';
    var rings = [0.25, 0.5, 0.75, 1];
    for(i=0; i<rings.length; i++){
      var op = '.16';
      if(rings[i] === 1){ op = '.34'; }
      web += '<polygon points="' + poly(rings[i]) + '" fill="none" '
           + 'stroke="currentColor" stroke-width="1" opacity="' + op + '"/>';
    }
    for(i=0; i<5; i++){
      var e1 = pt(i, 1);
      web += '<line x1="' + CX + '" y1="' + CY + '" x2="' + e1[0].toFixed(1)
           + '" y2="' + e1[1].toFixed(1) + '" stroke="currentColor" '
           + 'stroke-width="1" opacity=".16"/>';
    }

    /* 내 모양 */
    var pts = [], dots = '', labs = '';
    for(i=0; i<5; i++){
      var el = ORDER[i];
      var f1 = by[el];
      var n = 0;
      if(f1){ n = f1.count; }
      var p1 = pt(i, n / max);
      pts.push(p1[0].toFixed(1) + ',' + p1[1].toFixed(1));
      dots += '<circle data-el="' + el + '" cx="' + p1[0].toFixed(1)
            + '" cy="' + p1[1].toFixed(1) + '" r="4.5" fill="currentColor"/>';

      var lp = pt(i, 1.24);
      var an = 'middle';
      if(i === 1){ an = 'start'; }
      if(i === 2){ an = 'start'; }
      if(i === 3){ an = 'end'; }
      if(i === 4){ an = 'end'; }
      labs += '<text data-el="' + el + '" class="pent-l" x="' + lp[0].toFixed(1)
            + '" y="' + lp[1].toFixed(1) + '" text-anchor="' + an + '" '
            + 'dominant-baseline="middle" fill="currentColor">'
            + el + ' ' + NM[el]
            + '<tspan class="pent-n" dx="6">' + n + '</tspan></text>';
    }

    var css = '<style>'
      + '#ssb .pent{ margin:24px 0 2px; }'
      + '#ssb .pent svg{ display:block; width:100%; max-width:440px; height:auto;'
      + ' margin:0 auto; color:var(--dim); overflow:visible; }'
      + '#ssb .pent-area{ fill:rgba(138,106,36,.15); stroke:var(--gold);'
      + ' stroke-width:2; stroke-linejoin:round; }'
      + '#ssb .pent-l{ font-family:var(--serif); font-size:13px; font-weight:700; }'
      + '#ssb .pent-n{ font-family:var(--mono); font-size:16px; font-weight:700; }'
      + '#ssb .pent-cap{ text-align:center; font-size:.8rem; color:var(--dim);'
      + ' margin:8px 0 0; }'
      + '#ssb .scale{ display:none; }'   /* 오각형이 막대를 대신합니다 */
      + '@media(max-width:640px){ #ssb .pent-l{ font-size:12px; }'
      + ' #ssb .pent-n{ font-size:14px; } }'
      + '</style>';

    return css
      + '<div class="pent"><!-- STELLA-PENT-v1 -->'
      + '<svg viewBox="0 0 340 240" role="img" aria-label="오행 오각형">'
      + '<g>' + web + '</g>'
      + '<polygon class="pent-area" points="' + pts.join(' ') + '"/>'
      + dots + labs
      + '</svg>'
      + '<p class="pent-cap">가운데에 가까울수록 그 기운이 적습니다</p>'
      + '</div>';
  }catch(err){
    return '';
  }
})()
