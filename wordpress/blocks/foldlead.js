<!-- wp:html -->
<script>
/* 접힘 상자 첫 줄을 쉬운 말로  FOLD-1  2026-09-02
   두 번째 책부터 나오는 접힘 상자의 첫 줄이
   「시각을 먼저 바로잡습니다 · 여덟 글자 · … 외 2장 — 모두 6장」처럼
   장 제목을 늘어놓아서 손님이 무슨 말인지 알기 어려웠습니다.
   한 줄로 바꿉니다. 9번 조각은 건드리지 않고 그려진 글자만 고칩니다.
   이 안에서 두 글자짜리 논리기호를 쓰지 않습니다. */
(function(){
  'use strict';

  function fix(){
    var bars=document.getElementsByClassName('foldbar');
    var i, bar, lead, m, n, txt;
    for(i=0;i<bars.length;i++){
      bar=bars[i];
      if(bar.className.indexOf('skipbar')>=0){ continue; }
      if(bar.getAttribute('data-lead')==='1'){ continue; }
      lead=bar.getElementsByClassName('foldlead')[0];
      if(!lead){ continue; }
      txt=String(lead.textContent||'');
      m=txt.match(/모두\s*(\d+)\s*장/);
      n=m?m[1]:'';
      lead.innerHTML = n
        ? ('지난 책에서 보신 계산 '+n+'장입니다. 태어난 날은 바뀌지 않으니 내용도 그대로예요.')
        : '지난 책에서 보신 계산입니다. 태어난 날은 바뀌지 않으니 내용도 그대로예요.';
      bar.setAttribute('data-lead','1');
    }
  }

  var tries = 0;
  function tick(){
    tries += 1;
    try{ fix(); }catch(e){}
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
