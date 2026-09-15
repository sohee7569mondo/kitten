<style>
#ssb .sjkeep{ font-weight:600; }
#ssb .mini{ font-size:.86rem; color:#6a6a78; }
#ssb .sjbox{ font-family:IBM Plex Mono,monospace; font-size:.74rem; line-height:1.9;
  background:#faf8f4; border:1px solid #ece6dc; border-radius:8px;
  padding:12px 14px; margin:10px 0; white-space:pre-wrap; color:#4a4a58; }
/* 인용 한 마디 — 2026-09-14 · 소희 님 : 「강조부분이 이상해 오류같아
   보여. 그냥 배경없이 앞에 바만 있는 형태가 어떨까?」
   흰 상자가 본문 바탕(아이보리) 위에 떠서 덜 그려진 것처럼 보였습니다.
   바탕을 없애고 왼쪽 바만 남깁니다. 글은 본문과 같은 자리에서 시작하되
   바 두께만큼만 들여씁니다. */
/* ★ padding-left 에 !important 가 꼭 있어야 합니다.
   아래 폭 울타리가 `.page > *` 의 좌우 여백을 0 으로 누릅니다.
   그것이 이기면 바가 글에 딱 붙어 버립니다 (크로미움으로 재서 잡음). */
#ssb .sjsay{ margin:22px 0; padding:2px 0 2px 18px !important;
  border-left:3px solid #9E2B50; background:none; border-radius:0;
  line-height:1.9; }
#ssb .sjmark{ font-family:IBM Plex Mono,monospace; font-size:.62rem;
  letter-spacing:.18em; color:#9E2B50; margin:0 0 6px; }

/* ── 쪽 폭 울타리 ──────────────────────────────────────────
   2026-09-14 · 소희 님 : 「중간에 폭이 달라짐」
                          「폭잡는것도 여러번 있던일이라서 찾아보면
                            답이 있을거야」 — 있었습니다.

   ★ 책 전체 폭은 patch160_width (WIDTH-7) 하나가 정합니다.
     그 조각 머리말에 「책의 모양 — 이 조각 하나가 정합니다」라고
     적혀 있습니다. 쪽 900px · 좌우 여백 78px · 글줄 744px.
     제가 여기에 max-width 를 또 걸어 두어 둘이 싸우고 있었습니다.
     그래서 우리 쪽에서는 폭을 아예 정하지 않습니다.

   ★ 이기는 규칙으로 씁니다 — 앞에 #ssb 를 붙입니다.
       WIDTH-7   #ssb .page                      (아이디+클래스)
       전에 우리    [data-samjae="1"] > .page      → 힘이 모자라 집니다
       지금 우리  #ssb .book[data-samjae="1"] > .page  → 이깁니다
     가족운 책(FAMILY-1)이 같은 탈을 겪고 이 꼴로 고쳤습니다.
     그 책과 똑같이 적어 두 책이 같은 자리에서 시작합니다.

   깃발이 .book 에 달릴 수도, #bkBook 에만 달릴 수도 있어 둘 다 겁니다. */
/* ══ 폭은 책 상자 한 곳에서만 정합니다 ═══════════════════════
   2026-09-14 · 소희 님 : 「신년운세 폭이 안맞는건」
                          「여러번 언급했음 찾아봐」
   찾아보니 제가 같은 날 두 번 고치면서 한 번은 되돌려 놓았습니다 —

     a711f94  「책이 왼쪽으로 쏠려 글이 잘렸습니다. 살아 있는 쪽에 제
               사본에 없는 여백 규칙이 얹혀 있어서입니다」
               → 쪽을 max-width 760px · margin auto 로 못 박음
     405b0a2  「flex 안에서 auto margin 이 stretch 를 끕니다」
               → 그 못을 빼고 margin 0 · max-width none 으로 바꿈
               (쪽마다 폭이 달라지던 탈은 이걸로 고쳐졌습니다)

   둘 다 맞는 말이었는데 **같은 자리에 걸었기 때문에** 하나를 고치면
   다른 하나가 되살아났습니다. 자리를 갈라 놓습니다 —

     책 상자(.book)  폭을 정합니다   max-width · margin auto · padding
     쪽(.page)       늘어나게 둡니다 margin 0 · max-width none

   auto margin 이 stretch 를 끄는 것은 **flex 아이템**에서 생기는 일이라,
   상자 자신에 걸면 쪽은 그대로 늘어납니다. 그리고 상자에 못을 박아
   두면 살아 있는 쪽이 무슨 여백을 얹든 우리 책은 안 밀립니다. */
@media screen{
  #ssb .book[data-samjae="1"],
  #ssb [data-samjae="1"]{
    max-width:900px !important;
    margin-left:auto !important; margin-right:auto !important;
    /* ★★ 좌우 여백 78px — 2026-09-15
       소희 님 「왼쪽에 여백이 너무 없고」
       까닭 : 쪽(.page)에 padding-left:0 을 못 박으면서, 원래 책이
       갖고 있던 좌우 78px(patch160_spacerun)까지 같이 날아갔습니다.
       크로미움으로 재 보니 1280px 화면에서 글줄이 744px 이 아니라
       860px 이었습니다 — 116px 더 넓게 퍼져 있었습니다.
       여백을 쪽이 아니라 **상자**에 줍니다. 그래야 flex 의 stretch 를
       끄지 않으면서 900 - 156 = 744px 로 원래 폭과 같아집니다.
       휴대폰은 spacerun 과 같은 22px. */
    padding-left:78px !important; padding-right:78px !important;
    box-sizing:border-box !important; }
}
@media screen{
  /* ★ 왜 쪽마다 폭이 달랐나 — 2026-09-14 크로미움으로 재현해서 잡았습니다
     소희 님 : 「중간에 폭이 달라짐」 · 「폭잡는것도 여러번 있던일이라서
                찾아보면 답이 있을거야」 — 있었습니다.

     책(.book)은 display:flex · flex-direction:column 입니다.
     WIDTH-7 은 쪽을 `width:auto` + `margin-left/right:auto` 로 가운데
     놓습니다. 그런데 flex 안에서 좌우 margin 이 auto 면 stretch 가
     꺼집니다 — 쪽이 글 길이만큼 줄어들고 가운데로 몰립니다.
     재 보니 239px 부터 780px 까지 제각각이었고 글 시작 자리가
     세 가지(210 · 283 · 320)였습니다. 소희 님이 보신 그 모습입니다.

     그래서 auto margin 을 0 으로 눌러 stretch 가 살아나게 합니다.
     가족운 책(FAMILY-1)이 같은 탈을 겪고 똑같이 고쳤습니다 —
     그래서 두 책이 같은 자리에서 시작합니다.

     ★ 앞에 #ssb 를 꼭 붙입니다. WIDTH-7 이 `#ssb .page` 로 걸어서,
       전에 쓰던 `[data-samjae="1"] > .page` 는 힘이 모자라 졌습니다.
       이것이 어떤 쪽은 제 규칙이, 어떤 쪽은 WIDTH-7 이 이기던 까닭입니다. */
  #ssb .book[data-samjae="1"] > .page,
  #ssb [data-samjae="1"] > .page{
    margin-left:0 !important; margin-right:0 !important;
    padding-left:0 !important; padding-right:0 !important;
    max-width:none !important; width:auto !important; }
  #ssb .book[data-samjae="1"] > .page:not(.divider):not(.cover):not([data-part="cover"]) > *,
  #ssb [data-samjae="1"] > .page:not(.divider):not(.cover):not([data-part="cover"]) > *{
    padding-left:0 !important; padding-right:0 !important;
    margin-left:0 !important; margin-right:0 !important;
    max-width:none !important; }
  /* ★ 인용 한 마디는 왼쪽 바 옆에 여백이 있어야 합니다.
     바로 위 못이 `.page > *` 의 좌우 여백을 0 으로 누르는데, 그 못이
     뒤에 있고 선택자도 더 세서 `.sjsay` 의 !important 까지 이깁니다.
     그래서 같은 세기로 여기서 한 번 더 박습니다
     (크로미움으로 재서 잡았습니다 — 바가 글에 딱 붙어 있었습니다). */
  #ssb .book[data-samjae="1"] > .page > .sjsay,
  #ssb [data-samjae="1"] > .page > .sjsay{
    padding-left:18px !important; }
  /* 장 속표지는 가운데 정렬이라 위 못에서 빼 줍니다 */
  #ssb .book[data-samjae="1"] > .page.divider > *,
  #ssb [data-samjae="1"] > .page.divider > *{
    margin-left:auto !important; margin-right:auto !important; }
}
/* ★★ 좁은 화면 좌우 여백 — 2026-09-14 · 소희 님 「폭이 안맞아」
   제가 없앤 것을 되살립니다. 저장소를 찾아보니 답이 있었습니다.

     2026-09-14  a711f94  「폭 — 책이 왼쪽으로 쏠려 글이 잘렸습니다」
                 그때 넣은 것 : @media(max-width:820px){ padding 16px }
     같은 날      405b0a2  flex 의 auto margin 을 잡으면서 여백 규칙을
                 통째로 걷어냈습니다. 좁은 화면 여백까지 같이 사라졌습니다.

   ★ 여백(padding)은 flex 의 stretch 를 끄지 않습니다 — auto margin 만
     끕니다. 그래서 되살려도 쪽마다 폭이 달라지는 탈은 안 납니다.
   ★ 넓은 화면에서는 책 상자(.book)가 여백을 대므로 0 이 맞습니다. */
@media screen and (max-width:820px){
  #ssb .book[data-samjae="1"],
  #ssb [data-samjae="1"]{
    padding-left:22px !important; padding-right:22px !important; }
  /* ★ 2026-09-14 · 소희 님 : 「2026년 폭이 안맞아」
     가족운 책(FAMILY-1)에는 있는데 여기만 빠져 있던 못입니다.
     살아 있는 쪽에 글을 가운데로 미는 규칙이 얹혀 있으면
     쪽은 제 폭인데 글줄만 안쪽으로 몰려 「폭이 좁다」로 보입니다.
     두 책이 똑같이 보이도록 같은 못을 박습니다. */
  #ssb .book[data-samjae="1"] > .page.divider > h2,
  #ssb .book[data-samjae="1"] > .page.divider > p,
  #ssb [data-samjae="1"] > .page.divider > h2,
  #ssb [data-samjae="1"] > .page.divider > p{
    text-align:center !important; }
  #ssb .book[data-samjae="1"] > .page > h2,
  #ssb .book[data-samjae="1"] > .page > h3,
  #ssb .book[data-samjae="1"] > .page > p,
  #ssb [data-samjae="1"] > .page > h2,
  #ssb [data-samjae="1"] > .page > h3,
  #ssb [data-samjae="1"] > .page > p{ text-align:left; }
}
/* ══ 장 속표지의 얼굴 — 우리가 직접 박습니다 ═════════════
   2026-09-15 · 소희 님 「중간에 미르 사진 안들어가고」
                        「중간에 중간에 사진없음」

   까닭 : 동그라미(.dvmark.dvface)의 크기를 정하는 규칙이 우리
   조각에 없었습니다. 남의 조각(patch160_face)이 살아 있는 쪽에
   넣어둔 CSS 에 기대고 있었는데, 우리가 갈아끼운 책에는 그것이
   안 닿았습니다. 크로미움으로 재 보니 사진이 0 x 0 이었습니다 —
   자리는 있는데 크기가 없어 한 점도 안 그려집니다.

   그래서 남에게 기대지 않고 우리 울타리 안에 크기를 박습니다.
   화면과 인쇄 둘 다에 걸리도록 @media 밖에 둡니다. */
#ssb .book[data-samjae="1"] > .page.divider > .dvmark.dvface,
#ssb [data-samjae="1"] > .page.divider > .dvmark.dvface{
  display:block !important;
  width:132px !important; height:132px !important;
  max-width:132px !important; min-width:0 !important;
  margin:0 auto 16px !important; padding:0 !important;
  border-radius:50% !important; overflow:hidden !important;
  box-sizing:border-box !important; }
#ssb .book[data-samjae="1"] > .page.divider > .dvmark.dvface img,
#ssb [data-samjae="1"] > .page.divider > .dvmark.dvface img{
  width:100% !important; height:100% !important; display:block !important;
  max-width:none !important; object-fit:cover !important;
  object-position:center 16% !important; }
@media (max-width:640px){
  #ssb .book[data-samjae="1"] > .page.divider > .dvmark.dvface,
  #ssb [data-samjae="1"] > .page.divider > .dvmark.dvface{
    width:108px !important; height:108px !important; max-width:108px !important;
    margin-bottom:14px !important; }
}
@media print{
  #ssb .book[data-samjae="1"] > .page.divider > .dvmark.dvface img,
  #ssb [data-samjae="1"] > .page.divider > .dvmark.dvface img{
    -webkit-print-color-adjust:exact; print-color-adjust:exact; }
}
</style>
