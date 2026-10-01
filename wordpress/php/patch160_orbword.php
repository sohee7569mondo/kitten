<?php
/* ═══════════════════════════════════════════════════════
   「충전」이라는 말 걷어내기        patch160_orbword
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   왜
   소희 님이 KG이니시스에 「저희는 포인트를 유료로 충전하는 구조가
   아닙니다」로 회신하셨습니다. 심사관은 사이트를 직접 열어 봅니다.
   지난번 카카오페이 심사 때도 「구슬은 어디서 사나요?」를 물었습니다.

   살아 있는 쪽을 뒤져 보니 문 쪽에 이 한 줄이 남아 있었습니다 —

       구슬은 충전일로부터 1년간 유효합니다.

   「충전일」이라는 말이 있으면 충전이 있다는 뜻으로 읽힙니다.
   가격 안내와 이용약관은 이미 「따로 구매할 수 없으며」,
   「미리 금액을 충전해 두는 방식이 아니며」로 잘 적혀 있습니다.
   그 결에 맞춥니다.

   무엇을 하나
   ① 화면에 보이는 글에서 아래 말을 바꿉니다 (아래 표)
   ② ?stella_orbword=1 로 열면 그 쪽에 남은 「충전」을 다 찍어 줍니다
      — 제가 못 보는 쪽까지 소희 님이 화면만 찍어 보내주시면 됩니다

   왜 앵커를 안 잡나
   쪽마다 어디에 있는지 제가 다 알 수 없습니다. 그래서 글자를 찾아
   바꾸지 않고, 다 그려진 화면의 글마디만 바꿉니다. 코드·주소·입력칸은
   건드리지 않습니다.

   되돌리기
   이 스니펫을 끄면 원래대로 돌아옵니다. 쪽을 안 건드립니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_footer', function () {
	?>
<script>
(function(){
  if(window.StellaOrbWord){ return; }
  window.StellaOrbWord = 1;

  /* [ 바꿀 말, 바뀐 말 ] — 긴 것부터 놓습니다 */
  var MAP = [
    ['구슬은 충전일로부터', '구슬은 받으신 날로부터'],
    ['충전일로부터', '받으신 날로부터'],
    ['충전한 날로부터', '받으신 날로부터'],
    ['구슬 충전하기', '풀이 보러 가기'],
    ['구슬로 먼저 충전하기', '결제하고 바로 보기'],
    ['구슬 충전', '결제'],
    ['충전 내역', '결제 내역'],
    ['충전하기', '결제하기']
  ];

  /* 글자만 있는 마디를 훑습니다 — script · style · 입력칸은 뺍니다 */
  function walk(fn){
    var SKIP = { SCRIPT:1, STYLE:1, TEXTAREA:1, INPUT:1, CODE:1, PRE:1 };
    var stack = [document.body], node, i, kids;
    while(stack.length){
      node = stack.pop();
      if(!node){ continue; }
      kids = node.childNodes;
      for(i = 0; i < kids.length; i++){
        var c = kids[i];
        if(c.nodeType === 3){ fn(c); continue; }
        if(c.nodeType !== 1){ continue; }
        if(SKIP[c.nodeName]){ continue; }
        stack.push(c);
      }
    }
  }

  function fix(){
    var n = 0;
    walk(function(t){
      var v = t.nodeValue;
      if(!v){ return; }
      if(v.indexOf('충전') < 0){ return; }
      var i, out = v;
      for(i = 0; i < MAP.length; i++){
        out = out.split(MAP[i][0]).join(MAP[i][1]);
      }
      if(out !== v){ t.nodeValue = out; n++; }
    });
    return n;
  }

  /* 남은 자리를 찍어 주는 띠 — ?stella_orbword=1 */
  function report(){
    var hits = [];
    walk(function(t){
      var v = String(t.nodeValue || '');
      if(v.indexOf('충전') < 0){ return; }
      /* 빈칸 줄이기 — 정규식도 역빗금도 안 씁니다.
         역빗금은 편집기 저장에 벗겨져 탈이 납니다 (집 규칙). */
      var NL = String.fromCharCode(10), CR = String.fromCharCode(13),
          TB = String.fromCharCode(9);
      var s = v.split(NL).join(' ').split(CR).join(' ').split(TB).join(' ');
      while(s.indexOf('  ') >= 0){ s = s.split('  ').join(' '); }
      while(s.charAt(0) === ' '){ s = s.slice(1); }
      while(s.length){ if(s.charAt(s.length - 1) !== ' '){ break; } s = s.slice(0, -1); }
      if(s){ hits.push(s.slice(0, 120)); }
    });
    var box = document.createElement('div');
    box.setAttribute('style',
      'margin:24px auto;max-width:820px;padding:16px 18px;'
      + 'border:1px solid #E2DACB;border-radius:10px;background:#FBF8F2;'
      + 'color:#221C33;font:14px/1.8 -apple-system,sans-serif;');
    var html = '<b>「충전」이 남은 자리 — ' + hits.length + '군데</b>';
    if(!hits.length){
      html += '<div style="color:#2F7D4A;margin-top:8px">이 쪽에는 없습니다.</div>';
    } else {
      var i;
      for(i = 0; i < hits.length; i++){
        html += '<div style="margin-top:8px;color:#C4453A">· '
              + hits[i].split('<').join(' ') + '</div>';
      }
    }
    html += '<div style="margin-top:12px;color:#8B849C;font-size:.86rem">'
          + '주소 ' + location.pathname + '</div>';
    box.innerHTML = html;
    document.body.appendChild(box);
  }

  var tries = 0;
  function run(){
    fix();
    tries++;
    if(tries > 24){ clearInterval(t); }
  }
  fix();
  document.addEventListener('DOMContentLoaded', function(){ fix(); });
  var t = setInterval(run, 300);

  if(String(location.search).indexOf('stella_orbword=1') >= 0){
    setTimeout(report, 1800);
  }
})();
</script>
	<?php
} );
