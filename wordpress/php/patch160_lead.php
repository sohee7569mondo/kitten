<?php
/* ═══════════════════════════════════════════════════════
   듣고 싶은 말을 앞으로 — 자료는 뒤로   patch160_lead
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   소희 님 : 「내가 삼재보려고 열었잖아 그런데 내 사주가 어쨋거나
              여덟자 등등 핸드폰에서 보니 내가 듣고 싶은 말보다
              앞에가 너무 길어…… 쓸데 없는 서사가 길어서 흥미가 급락」

   세어 봤습니다 — 삼재 본론까지 열세 쪽입니다.
   그 가운데 여섯 쪽이 「자료」입니다. 읽을거리가 아니라 근거예요.

       시각을 먼저 바로잡습니다
       여덟 글자
       기운의 저울
       십 년마다 바뀌는 판
       태어나던 밤의 하늘
       여덟 글자가 서로 부딪히는 자리

   이 여섯 쪽을 지우지 않고 뒤로 보냅니다. 맺음말 바로 앞에
   「이 말이 어디서 나왔는지」 속표지를 세우고 그 뒤에 모읍니다.
   「지어내지 않는다」는 약속은 그대로입니다 — 근거를 버리는 게
   아니라 뒤에 두는 것뿐이에요.

   바뀐 뒤 본론까지 — 표지 · 당신이 아무 말도 하기 전에 ·
   사주를 ○○로 풀어보면 · 답해주신 것 · 적어주신 말 ·
   타고난 성향과 어긋난 자리 → 본론. 열세 쪽에서 일곱 쪽으로.

   ★ 앵커를 안 잡습니다
   쪽 글을 한 자도 고치지 않습니다. 다 그려진 책의 쪽 차례만
   바꿉니다. 그래서 제 사본이 낡아도 맞고, 모든 주제 · 모든 문의
   책에 한꺼번에 듣습니다.

   ★ 못 찾으면 아무것도 안 합니다
   여섯 쪽 가운데 하나도 못 찾으면 그냥 물러납니다. 책이 깨지지
   않습니다. 스니펫을 끄면 원래 차례로 돌아갑니다.

   차례가 어떻게 바뀌었는지 보시려면 —

       /reading-book/?leadwhy=1

   책 위에 「옮기기 전 / 옮긴 뒤」 차례를 나란히 찍어드립니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_head', function () {

	if ( ! is_page( 'reading-book' ) ) { return; }
	?>
<style id="stella-lead-css">
#ssb .page.leadsheet{ text-align:center; }
#ssb .page.leadsheet .ls-in{ padding:70px 0 50px; }
#ssb .page.leadsheet .ls-kick{ font-size:.74rem; letter-spacing:.3em;
  color:#A9791F; margin-bottom:18px; }
#ssb .page.leadsheet h2{ font-size:1.34rem; margin-bottom:14px; }
#ssb .page.leadsheet p{ color:#8B849C; font-size:.95rem; line-height:1.9;
  margin:0 auto; max-width:30em; }
#ssb .page.leadsheet .ls-rule{ width:54px; height:1px; background:#D5CCB8;
  margin:26px auto 0; }
/* ★ 폭 울타리 — 책(.book)은 flex 라서 좌우 margin 이 auto 면 stretch 가
   꺼집니다. WIDTH-7(patch160_width)이 #ssb .page 에 auto 를 걸어두어
   글이 짧은 이 속표지가 쪼그라듭니다. #ssb 를 앞에 붙여야 이깁니다. */
@media screen{
  #ssb .book > .page.leadsheet{
    margin-left:0 !important; margin-right:0 !important;
    padding-left:0 !important; padding-right:0 !important;
    max-width:none !important; width:auto !important; }
}
#stellaLeadWhy{ margin:14px auto; padding:16px 18px; max-width:760px;
  background:#FFFDF9; border:1px solid #E2DACB; border-radius:10px;
  font:13px/1.75 "IBM Plex Mono",monospace; color:#4E4763;
  white-space:pre-wrap; word-break:break-all; }
#stellaLeadWhy b{ color:#221C33; }
</style>
<script>
(function(){
  if(window.StellaLead){ return; }
  window.StellaLead = 1;

  /* 뒤로 보낼 쪽 — 제목에 **들어 있으면** 잡습니다.
     2026-09-14 · 처음에는 제목이 똑같아야 잡게 했다가 하나도 못
     찾았습니다. 살아 있는 책은 제목에 이름이 붙습니다
     (「이소희님의 여덟 글자」처럼). 그래서 조각으로 견줍니다. */
  var BACK = [
    '바로잡',        /* 시각을 먼저 바로잡습니다 */
    '여덟글자',      /* 여덟 글자 · 여덟 글자가 서로 부딪히는 자리 */
    '기운의저울',
    '십년마다',      /* 십 년마다 바뀌는 판 */
    '태어나던밤'     /* 태어나던 밤의 하늘 */
  ];

  var WHY = (location.search.indexOf('leadwhy=1') > -1);

  var NL = String.fromCharCode(10);   /* 역빗금을 안 씁니다 */
  var TAB = String.fromCharCode(9);

  function flat(s){
    return String(s === undefined ? '' : s)
      .split(' ').join('').split(' ').join('')
      .split(NL).join('').split(TAB).join('');
  }

  function head(pg){
    var h = pg.querySelector('h2');
    return h ? flat(h.textContent) : '';
  }

  function eyebrow(pg){
    var e = pg.querySelector('.eyebrow');
    return e ? flat(e.textContent) : '';
  }

  function isBack(pg){
    var t = head(pg);
    if(!t){ return false; }
    var i;
    for(i = 0; i < BACK.length; i++){
      if(t.indexOf(BACK[i]) > -1){ return true; }
    }
    return false;
  }

  /* 어디까지가 「자료」인가 — 1부가 시작하는 쪽(class 에 turn)이
     경계입니다. 책에 「여기까지가 기본 풀이였습니다」 띠가 붙는 그 쪽이에요.
     그 뒤는 풀이라 조각으로 견주다 잘못 옮길 일이 없습니다. */
  function edge(pgs){
    var i;
    for(i = 0; i < pgs.length; i++){
      if(pgs[i].className.indexOf('turn') > -1){ return i; }
    }
    for(i = 0; i < pgs.length; i++){
      if(eyebrow(pgs[i]).indexOf('1부') > -1){ return i; }
    }
    return pgs.length;
  }

  /* 맺음말이 시작하는 자리 — 자료를 그 바로 앞에 놓습니다 */
  function endAt(pgs){
    var i;
    for(i = 0; i < pgs.length; i++){
      if(eyebrow(pgs[i]) === '맺음말'){ return i; }
    }
    for(i = 0; i < pgs.length; i++){
      if(pgs[i].className.indexOf('close') > -1){ return i; }
    }
    return pgs.length;
  }

  function sheet(doc){
    var d = doc.createElement('div');
    d.className = 'page leadsheet';
    d.setAttribute('data-lead-sheet', '1');
    d.innerHTML =
      '<div class="ls-in">'
      + '<div class="ls-kick">STELLA SAJU</div>'
      + '<h2>이 말이 어디서 나왔는지</h2>'
      + '<p>여기까지 읽으신 것은 지어낸 이야기가 아닙니다. '
      + '태어나신 때를 계산해 나온 값이에요. '
      + '그 값을 아래에 그대로 펼쳐 두었습니다.</p>'
      + '<div class="ls-rule"></div>'
      + '</div>'
      + '<div class="folio">00</div>';
    return d;
  }

  function names(pgs){
    var out = [], i, t;
    for(i = 0; i < pgs.length; i++){
      t = head(pgs[i]);
      if(!t){ t = eyebrow(pgs[i]); }
      if(!t){ t = '(제목 없음 · ' + pgs[i].className + ')'; }
      out.push((i + 1) + '. ' + t);
    }
    return out.join(NL);
  }

  function tell(before, after, moved){
    var box = document.getElementById('stellaLeadWhy');
    if(!box){
      box = document.createElement('div');
      box.id = 'stellaLeadWhy';
      var bk = document.getElementById('bkBook');
      if(bk){ bk.parentNode.insertBefore(box, bk); }
      else { document.body.insertBefore(box, document.body.firstChild); }
    }
    box.innerHTML = '';
    var b = document.createElement('b');
    b.textContent = 'patch160_lead — 옮긴 쪽 ' + moved + '장' + NL + NL;
    box.appendChild(b);
    box.appendChild(document.createTextNode(
      '［옮기기 전］' + NL + before + NL + NL + '［옮긴 뒤］' + NL + after));
  }

  /* 한 장도 못 찾으면 그 자리 제목을 그대로 찍어 줍니다.
     그래야 왕복이 한 번에 끝납니다 (집 규칙 ⑤). */
  function note(pgs, stop){
    if(document.getElementById('stellaLeadWhy')){ return; }
    var names = [], i, t;
    for(i = 0; i < stop; i++){
      t = head(pgs[i]);
      if(!t){ t = eyebrow(pgs[i]); }
      names.push((i + 1) + '. ' + (t ? t : '(제목 없음)'));
    }
    var box = document.createElement('div');
    box.id = 'stellaLeadWhy';
    box.textContent = 'patch160_lead — 옮길 쪽을 한 장도 못 찾았습니다.' + NL
      + '아래가 1부 앞에 있는 쪽들의 제목입니다. 이대로 벼리에게 보여주세요.'
      + NL + NL + names.join(NL);
    var bk = document.getElementById('bkBook');
    if(bk){ bk.parentNode.insertBefore(box, bk); }
  }

  function run(){
    var bk = document.getElementById('bkBook');
    if(!bk){ return 0; }
    if(bk.getAttribute('data-lead') === '1'){ return 1; }

    var kids = bk.children;
    var pgs = [], i;
    for(i = 0; i < kids.length; i++){
      if(kids[i].className.indexOf('page') > -1){ pgs.push(kids[i]); }
    }
    if(pgs.length < 6){ return 0; }

    var before = WHY ? names(pgs) : '';

    /* 옮길 쪽을 모읍니다 — 1부가 시작하기 전까지만 봅니다 */
    var stop = edge(pgs);
    var move = [];
    for(i = 0; i < stop; i++){
      if(isBack(pgs[i])){ move.push(pgs[i]); }
    }
    if(move.length === 0){
      bk.setAttribute('data-lead', 'none');
      if(WHY){ tell(before, before, 0); }
      note(pgs, stop);
      return 1;
    }

    var cut = endAt(pgs);
    var mark = (cut < pgs.length) ? pgs[cut] : null;

    /* 속표지를 먼저 세우고, 그 뒤에 자료를 차례대로 붙입니다 */
    var sh = sheet(document);
    if(mark){ bk.insertBefore(sh, mark); }
    else { bk.appendChild(sh); }
    for(i = 0; i < move.length; i++){
      if(mark){ bk.insertBefore(move[i], mark); }
      else { bk.appendChild(move[i]); }
    }

    /* 쪽번호를 다시 맵니다 — 표지는 번호가 없습니다 */
    var kids2 = bk.children;
    var no = 0;
    for(i = 0; i < kids2.length; i++){
      if(kids2[i].className.indexOf('page') < 0){ continue; }
      no++;
      var f = kids2[i].querySelector('.folio');
      if(f){ f.textContent = (no < 10 ? '0' : '') + no; }
    }

    bk.setAttribute('data-lead', '1');

    if(WHY){
      var now = [], k;
      for(k = 0; k < kids2.length; k++){
        if(kids2[k].className.indexOf('page') > -1){ now.push(kids2[k]); }
      }
      tell(before, names(now), move.length);
    }
    return 1;
  }

  function watch(){
    if(run()){ return; }
    var n = 0;
    var t = setInterval(function(){
      n++;
      if(run()){ clearInterval(t); return; }
      if(n > 80){ clearInterval(t); }
    }, 300);
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', watch);
  } else {
    watch();
  }
})();
</script>
	<?php
} );
