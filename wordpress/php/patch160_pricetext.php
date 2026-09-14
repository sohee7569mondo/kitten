<?php
/* ═══════════════════════════════════════════════════════
   가격 안내 쪽 글 다듬기   patch160_pricetext
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   결제대행 심사에서 보는 쪽입니다. 세 군데가 걸립니다.

   ① 「미리 충전해 두는 것이 없습니다」
      없다는 말이라도 「충전」이라는 낱말이 쪽 맨 위에 있습니다.
      소희 님 : 「우리 사이트 충전 이런말이 있으면 안되는데」
      → 「미리 사두는 것이 없습니다」

   ② 「값을 치르지 않고도 두 편을 보실 수 있습니다」
      바로 아래 본문은 「첫 한 편은 값을 치르지 않으셔도 됩니다」
      입니다. 한 쪽 안에서 두 편과 한 편이 어긋나 있었습니다.
      실제 값으로 세어 보면 — 가입 축하 2 + 여는 기념 1 = 구슬 3개,
      풀이 한 편이 3구슬이니 **한 편**이 맞습니다.
      → 「첫 한 편은 값을 치르지 않으셔도 됩니다」

   ③ 「구슬 한 개가 1,000원이에요」
      소희 님 : 「구슬 1개가 1000원이라는 문구도 뺴자」
      구슬을 돈으로 바꾸는 값을 적어두면 환금성이 있는 것으로
      읽힙니다. 표에 「3,000원 / 구슬 3개」가 나란히 있으니
      손님이 헤아리시는 데는 모자라지 않습니다.
      → 그 문장만 덜어냅니다.

   왜 쪽을 안 고치고 조각으로 하나
   워드프레스 편집기로 열어 저장하면 역빗금이 벗겨집니다.
   그래서 고칠 것은 늘 조각으로 합니다. 끄면 원래 글로 돌아갑니다.

   무엇이 바뀌었는지 보시려면 —
       /price/?pricewhy=1
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_footer', function () {

	if ( ! is_page( 'price' ) ) { return; }
	?>
<style id="stella-pricetext-css">
#stellaPriceWhy{ margin:14px auto; padding:14px 16px; max-width:700px;
  background:#FFFDF9; border:1px solid #E2DACB; border-radius:10px;
  font:13px/1.8 "IBM Plex Mono",monospace; color:#4E4763;
  white-space:pre-wrap; }
</style>
<script>
(function(){
  if(window.StellaPriceText){ return; }
  window.StellaPriceText = 1;

  var NL = String.fromCharCode(10);
  var WHY = (location.search.indexOf('pricewhy=1') > -1);
  var log = [];

  /* ① ② — 문장을 통째로 갈아 끼웁니다 */
  var SWAP = [
    ['미리 충전해 두는 것이 없습니다.', '미리 사두는 것이 없습니다.'],
    ['값을 치르지 않고도 두 편을 보실 수 있습니다.',
     '첫 한 편은 값을 치르지 않으셔도 됩니다.']
  ];

  function walk(root, fn){
    var w = document.createTreeWalker(root, 4, null, false);
    var list = [], node;
    while((node = w.nextNode())){ list.push(node); }
    var i;
    for(i = 0; i < list.length; i++){ fn(list[i]); }
  }

  function swapText(){
    var box = document.getElementById('ssp');
    if(!box){ return 0; }
    var hit = 0;
    walk(box, function(t){
      var v = String(t.nodeValue === null ? '' : t.nodeValue);
      if(!v){ return; }
      var i;
      for(i = 0; i < SWAP.length; i++){
        if(v.indexOf(SWAP[i][0]) > -1){
          t.nodeValue = v.split(SWAP[i][0]).join(SWAP[i][1]);
          hit++;
          log.push('갈아끼움 · ' + SWAP[i][0] + '  →  ' + SWAP[i][1]);
        }
      }
    });
    return hit;
  }

  /* ③ — 「구슬 한 개가 1,000원」이 든 <b> 와 바로 뒤의 「이에요.」를 덜어냅니다 */
  function dropRate(){
    var box = document.getElementById('ssp');
    if(!box){ return 0; }
    var bs = box.querySelectorAll('b');
    var i, gone = 0;
    for(i = 0; i < bs.length; i++){
      var v = String(bs[i].textContent).split(' ').join('');
      if(v.indexOf('구슬한개가') < 0){ continue; }
      if(v.indexOf('원') < 0){ continue; }
      var nx = bs[i].nextSibling;
      if(nx){
        if(nx.nodeType === 3){
          var t = String(nx.nodeValue);
          var head = t.slice(0, 6);
          if(head.indexOf('이에요') > -1){ nx.nodeValue = t.slice(t.indexOf('이에요') + 4); }
          else if(head.indexOf('입니다') > -1){ nx.nodeValue = t.slice(t.indexOf('입니다') + 4); }
        }
      }
      log.push('덜어냄 · ' + bs[i].textContent);
      bs[i].parentNode.removeChild(bs[i]);
      gone++;
    }
    return gone;
  }

  function tell(){
    var box = document.getElementById('stellaPriceWhy');
    if(!box){
      box = document.createElement('div');
      box.id = 'stellaPriceWhy';
      var p = document.getElementById('ssp');
      if(p){ p.parentNode.insertBefore(box, p); }
      else { document.body.insertBefore(box, document.body.firstChild); }
    }
    box.textContent = 'patch160_pricetext — 손댄 자리 ' + log.length + '군데' + NL + NL
      + (log.length ? log.join(NL) : '★ 한 군데도 못 찾았습니다. 쪽 글이 바뀌었을 수 있어요.');
  }

  function run(){
    if(!document.getElementById('ssp')){ return 0; }
    var n = swapText() + dropRate();
    if(WHY){ tell(); }
    return 1;
  }

  if(!run()){
    var k = 0;
    var t = setInterval(function(){
      k++;
      if(run()){ clearInterval(t); return; }
      if(k > 40){ clearInterval(t); }
    }, 250);
  }
})();
</script>
	<?php
} );
