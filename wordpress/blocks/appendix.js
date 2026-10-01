/* ═══ 계산 다섯 장을 부록으로 뒤로 보냅니다 ═══  APPX-4  2026-09-02
   손님은 자기 이야기를 보러 오는데 여덟 번째 장까지 가야 나옵니다.
   그 앞 다섯 장이 전부 계산 설명입니다 — 진태양시 · 원국 · 오행 ·
   대운 · 태어나던 밤의 하늘. 친구분들이 어렵다고 한 자리가 여기입니다.

   지우지 않고 옮깁니다. 궁금한 분은 그대로 다 보실 수 있습니다.
   글은 한 자도 안 씁니다. 순서만 바꿉니다.

   미리보기 — 주소 뒤에 #appendix 를 붙였을 때만 돕니다.
   이 안에서 두 글자짜리 논리기호를 쓰지 않습니다. */
(function(){
  'use strict';

  var GATE = '';

  function two(n){ return (n<10?'0':'')+n; }

  function move(){
    var book=document.getElementById('bkBook');
    if(!book){ return; }
    if(book.getAttribute('data-appx')==='1'){ return; }
    if(GATE){
      if(String(location.hash).indexOf(GATE)<0){ return; }
    }

    /* 접는 조각이 일을 마친 뒤에 손댑니다 */
    if(book.getAttribute('data-folded')!=='1'){ return; }

    var pages=[].slice.call(book.getElementsByClassName('page'));
    if(pages.length<6){ return; }

    /* 1부가 시작하는 자리를 찾습니다 */
    var i, eb, at=-1;
    for(i=0;i<pages.length;i++){
      eb=pages[i].getElementsByClassName('eyebrow')[0];
      if(!eb){ continue; }
      if(String(eb.textContent).indexOf('1부')===0){ at=i; break; }
    }
    if(at<3){ return; }

    /* 표지와 여는 글은 그대로 두고, 그 뒤부터 1부 앞까지를 옮깁니다 */
    var take=pages.slice(2, at);
    if(!take.length){ return; }

    var holder=take[0].parentNode;
    if(!holder){ return; }

    /* 부록 표지 한 장 */
    var cover=document.createElement('div');
    cover.className='page';
    cover.innerHTML=
      '<p class="eyebrow">부록</p>'+
      '<h2>이 책이 어떻게 나왔는지</h2>'+
      '<p class="dek">궁금하실 때만 펴보시면 됩니다</p>'+
      '<p>여기서부터는 계산입니다. 태어난 시각을 어떻게 바로잡았는지, '+
      '여덟 글자가 무엇인지, 오행과 대운이 무엇인지 — 앞에서 읽으신 이야기가 '+
      '전부 여기서 나왔습니다.</p>'+
      '<p>몰라도 앞의 이야기를 읽는 데에는 아무 지장이 없습니다. 다만 '+
      '<em>왜 그런 말이 나왔지</em> 싶으실 때 여기를 펴보시면 답이 있습니다.</p>'+
      '<div class="folio"></div>';

    holder.appendChild(cover);
    for(i=0;i<take.length;i++){ holder.appendChild(take[i]); }

    /* 쪽 번호를 다시 매깁니다 (표지는 번호가 없습니다) */
    var all=book.getElementsByClassName('page'), f, n=0;
    for(i=0;i<all.length;i++){
      n+=1;
      f=all[i].getElementsByClassName('folio')[0];
      if(f){ f.textContent=two(n); }
    }
    var bkN=document.getElementById('bkN');
    if(bkN){ bkN.textContent=n+'쪽'; }

    /* 낱장 높이를 다시 맞춥니다 */
    var sheets=[].slice.call(book.getElementsByClassName('page'));
    sheets.forEach(function(el){ el.style.minHeight=''; });
    var tall=0;
    sheets.forEach(function(el){
      var h=el.getBoundingClientRect().height;
      if(h>tall){ tall=h; }
    });
    tall=Math.ceil(tall);
    sheets.forEach(function(el){ el.style.minHeight=tall+'px'; });

    book.setAttribute('data-appx','1');
  }

  function go(){
    setTimeout(move, 1200);
    setTimeout(move, 2600);
    setTimeout(move, 4500);
    setTimeout(move, 7000);
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', go);
  } else { go(); }
})();
