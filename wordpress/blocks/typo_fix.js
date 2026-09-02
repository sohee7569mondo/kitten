<!-- wp:html -->
<script>
/* 글자 깨짐 고치기  TYPO-1  2026-09-02
   세성의 신 1부(FORT-1)를 넣을 때 몇 글자가 깨져 들어갔습니다.
   낛겠는데 · 미뢬 · 쉰 없이 처럼요. 손님 눈에 보이는 자리라 먼저 고칩니다.
   조각을 통째로 다시 넣으면 또 깨질 수 있어서, 화면에 그려진 글자만 바꿉니다.
   앞으로 다른 곳에서 깨진 글자가 나오면 아래 표에 한 줄씩 더하면 됩니다.
   이 안에서 두 글자짜리 논리기호를 쓰지 않습니다. */
(function(){
  'use strict';

  var FIX = [
    ['낛겠는데','낫겠는데'],
    ['미뢬 시기','미룬 시기'],
    ['뭔 원했지','뭘 원했지'],
    ['쉰 없이','쉼 없이'],
    ['자기 힘으로 섬는데','자기 힘으로 섰는데'],
    ['하나쯄은','하나쯤은'],
    ['혼자 버튔 것이','혼자 버틴 것이'],
    ['다툼기 쉽습니다','다투기 쉽습니다'],
    ['갖춰는데','갖춰졌는데'],
    ['유난히 팡팡합니다','유난히 팍팍합니다'],
    ['비우기 쉽은','비우기 쉬운'],
    ['넣넷한','넉넉한'],
    ['내가 빁니다','내가 빕니다'],
    ['엿사를','엿새를'],
    ['안 혼난다고','안 혼낸다고'],
    ['형제가 곳 내','형제가 곧 내'],
    ['다퇠거나','다퉜거나'],
    ['다만 나눈 것이','다만 나눌 것이'],
    ['현실이 얇히는','현실이 얽히는'],
    ['꺼끄러운','껄끄러운'],
    ['형제끼리 무신','형제끼리 무슨'],
    ['받은 것을 늘게','받은 것을 늦게'],
    ['핫김에','홧김에'],
    ['답이 뜼한데도','답이 뜸한데도'],
    ['보낼 말을 썬다','보낼 말을 썼다'],
    ['왜 그러했는지','왜 그랬는지'],
    ['훨씬 가벼지십니다','훨씬 가벼워지십니다'],
    ['더 힘드셔던','더 힘드셨던'],
    ['연락이 뜼해','연락이 뜸해'],
    ['반대로 기대 사람이','반대로 기댈 사람이'],
    ['내놓아야 나는 사람','내놓아야 낫는 사람'],
    ['것이 곳 회복','것이 곧 회복'],
    ['이야기를 나눈 때','이야기를 나눌 때'],
    ['약속을 가벼이 여기면','약속을 가볍게 여기면']
  ];

  function sweep(root){
    if(!root){ return 0; }
    var w, node, t, i, hit=0;
    try{
      w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
    }catch(e){ return 0; }
    while(true){
      node = w.nextNode();
      if(!node){ break; }
      t = node.nodeValue;
      if(!t){ continue; }
      for(i=0;i<FIX.length;i++){
        if(t.indexOf(FIX[i][0])<0){ continue; }
        t = t.split(FIX[i][0]).join(FIX[i][1]);
        hit += 1;
      }
      if(t!==node.nodeValue){ node.nodeValue = t; }
    }
    return hit;
  }

  var tries = 0;
  function tick(){
    tries += 1;
    try{ sweep(document.getElementById('ssb')); }catch(e){}
    if(tries>40){ return; }
    setTimeout(tick, 500);
  }
  function go(){ setTimeout(tick, 600); }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', go);
  } else { go(); }
})();
</script>
<!-- /wp:html -->
