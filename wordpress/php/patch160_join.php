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

  /* ── 로그인 쪽 안내 ────────────────────────────────────
     2026-09-14 · 소희 님
       「그럼 로그인 페이지에 회원가입 안내도 있어야해」
       「로그인에도 풀이 한판은 구슬3개 3000원입니다. 여는값이에요
         안내 문구도 바꿔줘」
     로그인 쪽에 「처음이신가요?」는 있는데, 가입 폼을 찾는 분께는
     설명이 없습니다. 가입 절차가 없다는 것 자체를 말해드려야
     헤매지 않습니다. 값도 여기서 한 번 알려드립니다. */
  /* 「다시 오셨네요」는 처음 오신 분께는 틀린 말입니다.
     2026-09-14 · 소희 님 : 「시크릿모드로 들어갔는데도 돌아오셨군요 하네」
     이 쪽은 누가 오든 같은 제목을 보여줍니다 — 알아본 것이 아닙니다.
     두 분 다 맞는 말로 바꿉니다. */
  function loginTitle(){
    if(!ends(tail(location.pathname), '/login/')){ return; }
    var hs = document.querySelectorAll('h1'), i;
    for(i = 0; i < hs.length; i++){
      var t = String(hs[i].textContent);
      if(t.indexOf('다시 오셨') < 0){ if(t.indexOf('돌아오셨') < 0){ continue; } }
      if(hs[i].getAttribute('data-joinfix') === '1'){ continue; }
      hs[i].textContent = '이메일로 들어오기';
      hs[i].setAttribute('data-joinfix', '1');
    }
  }

  function loginNote(){
    if(!ends(tail(location.pathname), '/login/')){ return 1; }
    if(document.getElementById('joinNote')){ return 1; }

    /* 「처음이신가요」가 적힌 자리를 찾습니다 */
    var all = document.querySelectorAll('p, div, h2, h3'), i, host = null;
    for(i = 0; i < all.length; i++){
      if(String(all[i].textContent).indexOf('처음이신가요') < 0){ continue; }
      if(all[i].children.length > 2){ continue; }   /* 큰 상자 말고 그 줄 */
      host = all[i];
    }
    if(!host){ return 0; }

    var box = document.createElement('div');
    box.id = 'joinNote';
    box.setAttribute('style',
      'margin-top:14px;padding:16px 18px;border-radius:10px;'
      + 'background:rgba(107,79,176,.08);border:1px solid rgba(107,79,176,.22);'
      + 'font-size:.94rem;line-height:1.9;color:#4E4763;');
    box.innerHTML =
      '<b style="color:#221C33">가입 절차가 따로 없습니다.</b><br>'
      + '문 하나를 고르고 생년월일시를 넣으시면 그 자리에서 계정이 '
      + '만들어집니다. 비밀번호도 만들지 않으셔도 됩니다.'
      + '<div style="margin-top:10px;padding-top:10px;'
      + 'border-top:1px solid rgba(107,79,176,.18)">'
      + '풀이 한 편은 <b style="color:#221C33">3구슬 · 3,000원</b>입니다. '
      + '<b style="color:#C4453A">여는 기념 값</b>이고, 10월 31일까지예요. '
      + '그 뒤에는 9구슬 · 9,000원이 됩니다.</div>'
      + '<div style="margin-top:8px;color:#8B849C;font-size:.9rem">'
      + '나의 사주풀이 · 타로 · 띠별운세 · 별자리운세 · 오늘의 운세는 '
      + '값을 받지 않습니다.</div>'
      + '<a href="' + JOIN_TO + '" style="display:inline-block;margin-top:14px;'
      + 'padding:13px 22px;border-radius:8px;text-decoration:none;'
      + 'background:linear-gradient(120deg,#3A2E77,#241C4E);color:#FFFDF9;'
      + 'font-weight:700;font-size:.98rem">처음이신가요? 시작하기</a>';
    if(host.nextSibling){ host.parentNode.insertBefore(box, host.nextSibling); }
    else { host.parentNode.appendChild(box); }
    return 1;
  }

  /* ── 로그인 메일이 안 올 때 ────────────────────────────
     2026-09-14 · 소희 님 : 「로그인 누르면 로그인 링크 받기 나오고
     문제는 링크가 안와 내가 회원이 아닌거지」

     서버(stella-signup 1283줄)가 이렇게 돼 있습니다 —
         $user = get_user_by( 'email', $email );
         if ( $user ) { …메일 보냄… }
         return array( 'ok' => true, 'message' => '메일을 보내드렸어요.' );
     회원이 아니어도 「보내드렸어요」라고 말합니다. 메일은 안 옵니다.
     손님은 스팸함을 뒤지다 포기합니다 — 막다른 길입니다.

     ★ 「그런 계정 없어요」라고 대놓고 말하지는 않습니다.
       남의 이메일을 넣어보며 가입 여부를 캐낼 수 있어서입니다.
       대신 두 길을 같이 보여드립니다 — 기다리거나, 새로 시작하거나. */
  function lateNote(){
    if(!ends(tail(location.pathname), '/login/')){ return; }
    if(document.getElementById('lateNote')){ return; }

    var box = document.createElement('div');
    box.id = 'lateNote';
    box.setAttribute('style',
      'margin-top:16px;padding:16px 18px;border-radius:10px;'
      + 'background:#FBF8F2;border:1px solid #E2DACB;'
      + 'font-size:.94rem;line-height:1.9;color:#4E4763;');
    box.innerHTML =
      '<b style="color:#221C33">메일이 아직 안 오셨나요?</b><br>'
      + '스팸함과 프로모션함을 한 번 봐주세요. 몇 분 걸릴 때가 있어요.'
      + '<div style="margin-top:10px;padding-top:10px;'
      + 'border-top:1px solid #E2DACB">'
      + '그래도 없으면 <b style="color:#221C33">그 이메일로 된 계정이 '
      + '아직 없는 것</b>입니다. 처음이시면 아래에서 시작하세요 — '
      + '문을 고르고 생년월일을 넣으시면 그 자리에서 계정이 만들어집니다.'
      + '</div>'
      + '<a href="' + JOIN_TO + '" style="display:inline-block;margin-top:12px;'
      + 'padding:12px 20px;border-radius:8px;text-decoration:none;'
      + 'background:linear-gradient(120deg,#3A2E77,#241C4E);color:#FFFDF9;'
      + 'font-weight:700">처음부터 시작하기</a>';

    var host = document.getElementById('joinNote');
    if(!host){
      var bs = document.querySelectorAll('button'), i;
      for(i = 0; i < bs.length; i++){
        if(String(bs[i].textContent).indexOf('링크') >= 0){ host = bs[i]; }
      }
    }
    if(!host){ return; }
    if(host.nextSibling){ host.parentNode.insertBefore(box, host.nextSibling); }
    else { host.parentNode.appendChild(box); }
  }

  /* 「링크 받기」를 누르시면 여덟 걸음쯤 뒤에 안내를 띄웁니다 */
  document.addEventListener('click', function(e){
    var t = e.target;
    if(!t){ return; }
    if(!t.textContent){ return; }
    if(String(t.textContent).indexOf('링크') < 0){ return; }
    if(!ends(tail(location.pathname), '/login/')){ return; }
    setTimeout(lateNote, 8000);
  }, true);

  run();
  loginTitle();
  loginNote();
  document.addEventListener('DOMContentLoaded', function(){
    run(); loginTitle(); loginNote();
  });
  var done = 0;
  var t2 = setInterval(function(){
    done++;
    run();
    loginTitle();
    loginNote();
    if(done > 40){ clearInterval(t2); }
  }, 300);
})();
</script>
	<?php
} );
