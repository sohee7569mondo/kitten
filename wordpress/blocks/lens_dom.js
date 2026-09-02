<!-- wp:html -->
<script>
/* 1부 긴 글을 화면에 실제로 올립니다  LENSDOM-1  2026-09-02
   찾아낸 것 — 전자책 본체(12번 조각)는 자기 자리에서 곧바로 1부를 그립니다.
   그래서 그 뒤에 놓인 조각들(19 · 21 · 23~27)이 아무리 긴 글을 넣어도
   화면에는 이미 짧은 글이 그려진 뒤였습니다. 손님은 계속 짧은 글을 봤습니다.
   조각 차례를 바꾸는 대신, 다 그려진 뒤에 그 세 문단만 긴 글로 갈아끼웁니다.
   글은 window.StellaGuide[문].lens 에서 그대로 가져오므로
   여기에는 글이 한 줄도 들어 있지 않습니다.
   직성의 신은 갈아끼우는 함수를 한 번 불러 줘야 lens 가 채워집니다.
   이 안에서 두 글자짜리 논리기호를 쓰지 않습니다. */
(function(){
  'use strict';

  var KEYS = ['비겁','식상','재성','관성','인성'];

  function ord(){
    try{ return JSON.parse(localStorage.getItem('stella_demo')); }catch(e){ return null; }
  }
  function lensOf(){
    var o = ord();
    if(!o){ return null; }
    var G = window.StellaGuide;
    if(!G){ return null; }
    var g = G[o.guardian_slug];
    if(!g){ return null; }
    return g.lens || null;
  }
  /* 직성의 신은 갈아끼우는 함수가 아직 안 불렸을 수 있습니다 */
  function warm(){
    if(!window.__stellaCareerLens){ return; }
    try{ window.__stellaCareerLens(); }catch(e){}
  }

  function pageOf(node){
    var n = node;
    while(n){
      if(n.className){ if(String(n.className).indexOf('page') >= 0){ return n; } }
      n = n.parentNode;
    }
    return null;
  }

  function fix(){
    var box = document.getElementById('ssb');
    if(!box){ return false; }
    var lens = lensOf();
    if(!lens){ return false; }

    /* 1부는 「… 의 언어로 다시 읽습니다」 라는 줄이 있는 낱장입니다 */
    var ps = box.getElementsByTagName('p'), i, hit = null;
    for(i=0;i<ps.length;i++){
      if(String(ps[i].textContent||'').indexOf('언어로 다시 읽습니다') >= 0){ hit = ps[i]; break; }
    }
    if(!hit){ return false; }
    var pg = pageOf(hit);
    if(!pg){ return false; }

    var h3 = pg.getElementsByTagName('h3');
    if(!h3.length){ return false; }

    var done = 0, j, k, t, key, p, box2, kid;
    for(j=0;j<h3.length;j++){
      if(h3[j].getAttribute('data-lens') === '1'){ done += 1; continue; }
      t = String(h3[j].textContent || '');
      key = '';
      for(k=0;k<KEYS.length;k++){
        if(t.indexOf(KEYS[k] + '이') >= 0){ key = KEYS[k]; }
      }
      if(!key){ continue; }
      if(t.indexOf('자리') < 0){ continue; }
      if(!lens[key]){ continue; }
      p = h3[j].nextElementSibling;
      if(!p){ continue; }
      if(p.tagName !== 'P'){ continue; }
      /* 이미 긴 글이면 놔둡니다 */
      if(String(p.textContent||'').length > 300){
        h3[j].setAttribute('data-lens','1'); done += 1; continue;
      }
      box2 = document.createElement('div');
      box2.innerHTML = '<p>' + lens[key] + '</p>';
      while(box2.firstChild){
        kid = box2.firstChild;
        box2.removeChild(kid);
        p.parentNode.insertBefore(kid, p);
      }
      p.parentNode.removeChild(p);
      h3[j].setAttribute('data-lens','1');
      done += 1;
    }
    return done > 0;
  }

  var tries = 0;
  function tick(){
    tries += 1;
    var ok = false;
    try{ ok = fix(); }catch(e){ ok = true; }
    if(ok){ return; }
    if(tries > 40){ return; }
    setTimeout(tick, 500);
  }
  function go(){ warm(); setTimeout(tick, 500); }
  warm();
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', go);
  } else { go(); }
})();
</script>
<!-- /wp:html -->
