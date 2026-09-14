<?php
/* ═══════════════════════════════════════════════════════
   「가입」 단추 바로잡기            patch160_join
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   소희 님 : 「모바일에서 가입 눌렀는데 마루의 정보입력창으로 가네」
             「우리가 회원가입폼이 따로 없나?」

   없습니다 — 일부러 없앤 구조입니다. 이용약관 제4조에 이렇게
   적혀 있습니다.

     스텔라사주는 별도의 가입 절차를 두지 않습니다. 여섯 개의 문
     가운데 하나를 골라 생년월일시를 넣으시면 그 자리에서 계정이
     만들어집니다.

   그런데 머리글에는 「가입」 단추가 있고, 그것이 /door-career/ 로
   갑니다. 손님은 「가입」을 눌렀는데 마루의 직업운 입력창을 만납니다.
   가입 폼을 찾다가 생년월일을 넣으라니 어리둥절합니다.

   그리고 마이페이지의 「가입하기」는 /signin/ 으로 가는데
   그런 쪽이 아예 없습니다 (쪽 38개를 워드프레스에서 직접 확인했습니다).
   누르면 404 입니다.

   무엇을 하나
   ① 머리글 「가입」 → 글씨 「시작하기」 · 홈의 문 고르는 자리(/#saju)
      가입 폼이 없으니 「가입」이라는 말을 안 씁니다. 손님이 문을 고르면
      그 자리에서 계정이 생깁니다 — 약관과 말이 맞습니다.
   ② /signin/ 으로 가는 링크를 모두 /login/ 로 돌립니다 (404 막기)

   왜 앵커를 안 잡나
   머리글은 테마라 제 사본이 낡을 수 있습니다. 그래서 글자를 잡지 않고
   주소(href)로 찾아 고칩니다. 마이페이지 링크는 스크립트가 나중에
   그리므로 한동안 지켜보며 고칩니다.

   되돌리기
   이 스니펫을 끄면 원래대로 돌아옵니다. 쪽을 안 건드립니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_footer', function () {
	?>
<script>
(function(){
  if(window.StellaJoinFix){ return; }
  window.StellaJoinFix = 1;

  var JOIN_TO   = '/#saju';        /* 홈의 「스텔라사주보기」 줄 */
  var JOIN_TEXT = '시작하기';
  var LOGIN_TO  = '/login/';

  function tail(h){
    var s = String(h === null ? '' : h);
    var q = s.indexOf('?');
    if(q >= 0){ s = s.slice(0, q); }
    var g = s.indexOf('#');
    if(g >= 0){ s = s.slice(0, g); }
    if(s.length){ if(s.charAt(s.length - 1) !== '/'){ s = s + '/'; } }
    return s;
  }
  function ends(s, t){
    if(s.length < t.length){ return false; }
    return s.slice(s.length - t.length) === t;
  }
  function txt(a){
    return String(a.textContent || '').split(' ').join('').split(' ').join('');
  }

  function run(){
    var n = 0, links = document.querySelectorAll('a[href]'), i, a, h, t;
    for(i = 0; i < links.length; i++){
      a = links[i];
      if(a.getAttribute('data-joinfix') === '1'){ continue; }
      h = tail(a.getAttribute('href'));
      t = txt(a);

      /* ① 「가입」이라 적힌 단추가 문으로 가고 있으면 돌립니다 */
      if(t === '가입' || t === '가입하기' || t === '가입하기→'){
        if(ends(h, '/door-career/') || ends(h, '/signin/')){
          a.setAttribute('href', JOIN_TO);
          a.textContent = JOIN_TEXT;
          a.setAttribute('data-joinfix', '1');
          n++;
          continue;
        }
      }

      /* ② 없는 쪽 /signin/ 으로 가는 것은 모두 /login/ 으로 */
      if(ends(h, '/signin/')){
        a.setAttribute('href', LOGIN_TO);
        a.setAttribute('data-joinfix', '1');
        n++;
        continue;
      }
    }
    return n;
  }

  run();
  document.addEventListener('DOMContentLoaded', function(){ run(); });
  var done = 0;
  var t2 = setInterval(function(){
    done++;
    run();
    if(done > 40){ clearInterval(t2); }
  }, 300);
})();
</script>
	<?php
} );
