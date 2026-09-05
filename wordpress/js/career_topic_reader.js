
    /* ═══ 주제별로 갈라 쓰기 (2026-08-31) ═══
       이 아래 세 꼭지는 여섯 주제가 모두 같은 글을 쓰고 있었습니다.
       지금 주제를 읽어 표의 몇 칸만 갈아끼웁니다.
       주의 · 이 안에서 앰퍼샌드를 쓰지 않습니다. */
    var __ct=(function(){
      try{
        var o=JSON.parse(localStorage.getItem('stella_demo'));
        var t=(o?o.topic:'')||'';
        t=String(t).trim();
        var A={'직업운':'직장운'};
        return A[t]?A[t]:t;
      }catch(e){ return ''; }
    })();
    function __over(tbl, base){
      var m=tbl[__ct];
      if(!m){ return; }
      var k;
      for(k in m){ if(Object.prototype.hasOwnProperty.call(m,k)){ base[k]=m[k]; } }
    }
