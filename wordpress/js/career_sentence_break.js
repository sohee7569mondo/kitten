/* ═══ 문장이 끝나면 줄을 바꿉니다 (2026-08-31) ═══
   한 문단 안에서 문장이 어중간하게 이어져 붙어 보였습니다.
   마침표 뒤에서 줄을 바꿔 문장 하나가 한 줄로 서게 합니다.
   글자는 하나도 바꾸지 않고 줄만 바꿉니다.
   두 번 돌아도 안전합니다 — 이미 바꾼 자리는 마침표 뒤가 여백이 아니라
   태그라서 다시 잡히지 않습니다.
   주의 · 이 안에서 앰퍼샌드를 쓰지 않습니다. */
(function(){
  var root=null;

  function fix(){
    if(!root){ return; }
    var ps=root.getElementsByTagName('p');
    var i, h, n;
    for(i=0;i<ps.length;i++){
      h=ps[i].innerHTML;
      if(!h){ continue; }
      /* 링크가 든 문단은 건드리지 않습니다 */
      if(h.indexOf('<a ')>=0){ continue; }
      /* 마침표 뒤에 여백이 있고 그다음에 글자가 오면 줄을 바꿉니다.
         마침표 앞이 여백이나 마침표나 닫는 꺾쇠면 건너뜁니다 (1. 2. 같은 번호 매김 보호) */
      n=h.replace(/([^\s.>0-9][.])\s+(?=[^\s<])/g, '$1<br>');
      if(n!==h){ ps[i].innerHTML=n; }
    }
  }

  function start(){
    root=document.getElementById('bkBook');
    if(!root){ setTimeout(start, 300); return; }
    fix();
    if(window.MutationObserver){
      var mo=new MutationObserver(function(){
        mo.disconnect();
        fix();
        mo.observe(root, {childList:true, subtree:true});
      });
      mo.observe(root, {childList:true, subtree:true});
    }
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
