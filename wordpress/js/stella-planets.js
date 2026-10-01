/* ═══════════════════════════════════════════════════════════════
   STELLA SAJU — 금성 · 화성 자리 계산기
   ───────────────────────────────────────────────────────────────
   태양과 달은 이미 있습니다. 궁합에 쓸 금성(끌림)과 화성(부딪힘)을
   더합니다.

   방법 — 케플러 궤도요소로 지구·금성·화성의 자리를 각각 구한 뒤,
   지구에서 본 방향으로 바꿉니다. 요소값은 1800~2050년 사이에서
   0.1도 안쪽으로 맞습니다. 별자리 한 칸이 30도라 충분합니다.

   ★ 다만 별자리 경계에서 0.1도 안쪽으로 태어나신 분은 옆 자리로
     나올 수 있습니다. 그런 분은 화면에 「경계에 걸쳐 있습니다」라고
     적어드려야 합니다.

   ★ script 안에 앰퍼샌드를 쓰지 않습니다.
   ═══════════════════════════════════════════════════════════════ */
(function(root){
  'use strict';

  var RAD = Math.PI / 180;

  /* a · e · I · L · 긴꼭짓점 · 오름마디  그리고 백년당 변화량
     (제트추진연구소가 내놓은 1800~2050년용 근사값) */
  var EL = {
    earth: [ 1.00000261,  0.00000562,
             0.01671123, -0.00004392,
            -0.00001531, -0.01294668,
           100.46457166, 35999.37244981,
           102.93768193,  0.32327364,
             0.0,         0.0 ],
    venus: [ 0.72333566,  0.00000390,
             0.00677672, -0.00004107,
             3.39467605, -0.00078890,
           181.97909950, 58517.81538729,
           131.60246718,  0.00268329,
            76.67984255, -0.27769418 ],
    mars:  [ 1.52371034,  0.00001847,
             0.09339410,  0.00007882,
             1.84969142, -0.00813131,
            -4.55343205, 19140.30268499,
           -23.94362959,  0.44441088,
            49.55953891, -0.29257343 ]
  };

  function wrap360(x){ return ((x % 360) + 360) % 360; }
  function wrap180(x){ var v = wrap360(x); return (v > 180) ? v - 360 : v; }

  /* 태양 둘레를 도는 한 천체의 자리 (황도 좌표) */
  function heliocentric(name, T){
    var e = EL[name];
    var a  = e[0]  + e[1]  * T;
    var ec = e[2]  + e[3]  * T;
    var I  = e[4]  + e[5]  * T;
    var L  = e[6]  + e[7]  * T;
    var pi = e[8]  + e[9]  * T;
    var Om = e[10] + e[11] * T;

    var w = pi - Om;                 /* 근일점 인수 */
    var M = wrap180(L - pi);

    /* 케플러 방정식을 되풀이해서 풉니다 */
    var eStar = 180 / Math.PI * ec;
    var E = M + eStar * Math.sin(M * RAD);
    var i, dM, dE;
    for(i = 0; i < 12; i++){
      dM = M - (E - eStar * Math.sin(E * RAD));
      dE = dM / (1 - ec * Math.cos(E * RAD));
      E = E + dE;
      if(Math.abs(dE) < 1e-9){ break; }
    }

    /* 궤도면 위의 자리 */
    var xp = a * (Math.cos(E * RAD) - ec);
    var yp = a * Math.sqrt(1 - ec * ec) * Math.sin(E * RAD);

    /* 황도면으로 돌립니다 */
    var cw = Math.cos(w * RAD),  sw = Math.sin(w * RAD);
    var cO = Math.cos(Om * RAD), sO = Math.sin(Om * RAD);
    var ci = Math.cos(I * RAD),  si = Math.sin(I * RAD);

    return {
      x: (cw * cO - sw * sO * ci) * xp + (-sw * cO - cw * sO * ci) * yp,
      y: (cw * sO + sw * cO * ci) * xp + (-sw * sO + cw * cO * ci) * yp,
      z: (sw * si) * xp + (cw * si) * yp
    };
  }

  /* 지구에서 본 방향 — 황경(도) */
  function geoLon(name, jd){
    var T = (jd - 2451545.0) / 36525.0;
    var p = heliocentric(name, T);
    var e = heliocentric('earth', T);
    var x = p.x - e.x, y = p.y - e.y;
    return wrap360(Math.atan2(y, x) / RAD);
  }

  function venusLon(jd){ return geoLon('venus', jd); }
  function marsLon(jd){  return geoLon('mars',  jd); }

  /* 태양 황경 — 지구 자리의 반대쪽입니다 (검산용) */
  function sunLonFromEarth(jd){
    var T = (jd - 2451545.0) / 36525.0;
    var e = heliocentric('earth', T);
    return wrap360(Math.atan2(-e.y, -e.x) / RAD);
  }

  root.StellaPlanets = {
    venusLon: venusLon,
    marsLon: marsLon,
    sunLonFromEarth: sunLonFromEarth,
    geoLon: geoLon
  };
})(typeof window !== 'undefined' ? window : globalThis);

if (typeof module !== 'undefined') { module.exports = globalThis.StellaPlanets; }
