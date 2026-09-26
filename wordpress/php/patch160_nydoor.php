<?php
/* ══════════════════════════════════════════════════════════
   문으로 바로 보내기 + 신년운세 주제 둘
                                        ★ 2026-09-14 · 소희 님께
                                        판 NYDOOR-1

   두 가지를 합니다.

   ① 홈 배너에서 주제를 달아 보내면, 문에서 그 주제가 미리 골라집니다
      지금은 「결혼운」 배너를 눌러도 /door-love/ 로만 가서 손님이
      문에서 결혼운을 다시 골라야 합니다. 배너 일곱 개가 전부
      /door-love/ 로만 갑니다.
        홈   /door-love/?topic=결혼운
        문   결혼운 단추가 미리 눌려 있습니다
      ★ 문 여섯 곳 어디서나 됩니다 — 연애 · 직업 · 건강 · 운세 ·
        별자리 · 타로. 주제 이름이 단추 글과 같기만 하면 됩니다.

   ② door-fortune 의 「신년운세」를 해마다 갈라 둘로 만듭니다
        신년운세  →  2026년 운세 · 2027년 운세
      두 해를 따로 팔 수 있고, 손님도 무엇을 보는지 압니다.

   ── 앵커를 안 잡습니다 ────────────────────────────────
   쪽 글을 한 글자도 안 바꿉니다. 그려진 뒤에 자바스크립트로 단추를
   갈아끼우고 주소를 읽습니다. 그래서 「0군데」가 날 일이 없습니다.
   되돌리기도 없습니다 — 스니펫을 끄면 원래대로입니다.

   ── 홈 배너에 쓸 주소 ─────────────────────────────────
       /door-fortune/?topic=2026년 운세
       /door-fortune/?topic=2027년 운세
       /door-love/?topic=결혼운        (이미 있는 주제도 같은 꼴)
   ★ 한글이 주소에 들어가면 브라우저가 알아서 바꿔 적습니다.
     조각이 decodeURIComponent 로 풀어 읽습니다.

   ── 붙이는 법 ─────────────────────────────────────────
   ★ 새 조각입니다. WPCode -> 새 스니펫 -> PHP Snippet -> 저장 -> Active
   ★ 위치(Location)를 「어디서나 실행 / Run Everywhere」로.
   ★ 크롬 번역을 끄고 붙여넣으세요.

   넣으신 뒤 이 주소를 열어 보세요 —
       stellasaju.com/door-fortune/
         → 단추가 「2026년 운세 · 2027년 운세 · 대운 · …」로 바뀝니다
       stellasaju.com/door-love/?topic=결혼운
         → 결혼운이 미리 눌려 있습니다

   ── 검사한 것 ─────────────────────────────────────────
   php -l           문법
   앰퍼샌드 세기      0 이어야 합니다 (URL 가를 때도 fromCharCode(38))
   node --check     스크립트 문법
   jsdom 으로 실제 단추를 만들어 놓고 돌려봄
   ══════════════════════════════════════════════════════════ */

add_action( 'wp_head', function () {
	/* ★ 이 조각은 문 여섯 쪽에서만 씁니다.
	   2026-09-14 · 소희 님 : 「스니펫이 많아서 그거 읽느라 사주가
	   문제있다고 햇었는데」 — 울타리가 없으면 모든 쪽에 실립니다.
	   슬러그는 워드프레스에서 직접 확인했습니다. */
	if ( ! is_page( array( 'door-love', 'door-career', 'door-health',
	                       'door-fortune', 'door-astro', 'door-tarot' ) ) ) { return; }
	?>
<script>
(function(){
  if(window.StellaNyDoor){ return; }
  window.StellaNyDoor = 1;

  /* ── 이 쪽이 문인가 ──────────────────────────────────── */
  function doorSlug(){
    var p = String(location.pathname || '');
    var m = p.match(/door-([a-z]+)/);
    if(!m){ return ''; }
    return 'door-' + m[1];
  }

  /* ── 주소에서 topic 읽기 (앰퍼샌드를 글자로 만들어 씁니다) ── */
  function topicFromUrl(){
    var q = String(location.search || '');
    if(q.charAt(0) === '?'){ q = q.slice(1); }
    if(!q){ return ''; }
    var AMP = String.fromCharCode(38);
    var parts = q.split(AMP), i, kv;
    for(i = 0; i < parts.length; i++){
      kv = parts[i].split('=');
      if(kv[0] === 'topic'){
        if(kv.length < 2){ return ''; }
        try{ return decodeURIComponent(kv[1].replace(/\+/g, ' ')); }
        catch(e){ return kv[1]; }
      }
    }
    return '';
  }

  /* ── 주제 단추 묶음 찾기 ─────────────────────────────── */
  function topicInputs(){
    return document.querySelectorAll('input[name="ssg-topic"]');
  }

  /* ── ② door-fortune 의 「신년운세」를 두 해로 가릅니다 ─── */
  var NEW_YEARS = ['2026년 운세', '2027년 운세'];

  function splitNewYear(){
    if(doorSlug() !== 'door-fortune'){ return; }
    var list = topicInputs();
    if(!list.length){ return; }
    var i, inp, lab, old = null;
    for(i = 0; i < list.length; i++){
      if(list[i].value === '신년운세'){ old = list[i]; }
    }
    if(!old){ return; }
    lab = old.closest ? old.closest('label') : old.parentNode;
    if(!lab){ return; }
    if(lab.getAttribute('data-nysplit') === '1'){ return; }

    var made = [], j, node, span, cloneLab;
    for(j = 0; j < NEW_YEARS.length; j++){
      cloneLab = lab.cloneNode(true);
      node = cloneLab.querySelector('input[name="ssg-topic"]');
      span = cloneLab.querySelector('span');
      if(!node){ continue; }
      node.value = NEW_YEARS[j];
      node.checked = (j === 0);
      if(span){ span.textContent = NEW_YEARS[j]; }
      cloneLab.setAttribute('data-nysplit', '1');
      made.push(cloneLab);
    }
    if(!made.length){ return; }
    /* 차례대로 끼웁니다 — 뒤에서부터 넣으면 2027 이 앞에 섭니다 */
    for(j = 0; j < made.length; j++){
      lab.parentNode.insertBefore(made[j], lab);
    }
    lab.parentNode.removeChild(lab);
  }

  /* ── ① 주소로 온 주제를 미리 골라둡니다 ───────────────── */
  function preselect(){
    var want = topicFromUrl();
    if(!want){ return false; }
    var list = topicInputs();
    if(!list.length){ return false; }
    var i, hit = null;
    for(i = 0; i < list.length; i++){
      if(String(list[i].value).replace(/\s+/g, '') === want.replace(/\s+/g, '')){
        hit = list[i];
      }
    }
    if(!hit){ return false; }
    hit.checked = true;
    /* 쪽이 change 를 듣고 있을 수 있으니 알려 줍니다 */
    try{
      var ev = document.createEvent('HTMLEvents');
      ev.initEvent('change', true, false);
      hit.dispatchEvent(ev);
    }catch(e){}
    /* 골라진 자리를 눈에 보이게 */
    try{
      var lab = hit.closest ? hit.closest('label') : hit.parentNode;
      if(lab){ lab.scrollIntoView({block:'center'}); }
    }catch(e){}
    return true;
  }

  function run(){
    try{ splitNewYear(); }catch(e){}
    try{ preselect(); }catch(e){}
  }

  /* 지금 당장 한 번 (단추가 이미 그려져 있으면 여기서 끝납니다) */
  run();
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', run);
  }
  /* 쪽이 늦게 단추를 그리는 경우를 위해 몇 번 더 봅니다 */
  var tries = 0;
  var tick = setInterval(function(){
    tries = tries + 1;
    if(tries > 12){ clearInterval(tick); return; }
    run();
  }, 250);
})();
</script>
	<?php
} );
