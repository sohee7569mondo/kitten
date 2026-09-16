# -*- coding: utf-8 -*-
"""NY<해>.json -> WPCode 조각 (신년운세 책 갈아끼우기)

    python3 emit_newyear.py 2026
    python3 emit_newyear.py 2027
"""
import io, json, sys, os, re


def year_luck_names(doc):
    """올해이름 · 대운이름을 원고에서 그대로 뽑습니다.

    2026-09-14 · 소희 님 : 「올해 이름에 값이 들어가야 하는거 아닌가?」
    맞습니다. {올해이름} {대운이름} 은 아무도 안 채우고 있어서 손님 책에
    중괄호 그대로 찍히고 있었습니다.

    손으로 옮겨 적지 않습니다 — 원고의 소제목에서 읽습니다.
      01장  「비겁 · 내가 정하고 내가 서는 해」        → 올해이름
            (2027 은 「비겁 → 식상 · …」 꼴이라 화살표도 흡수합니다)
      02장  「비겁 · 나를 세우는 십 년」                → 대운이름
            문장이 「「…」의 십 년을 지나고 있습니다」라서
            「십 년」을 떼고 「흐름」을 붙입니다.
    """
    G = ('비겁', '식상', '재성', '관성', '인성')
    yn, ln, tn = {}, {}, {}
    # ★ build 가 적어 준 표가 있으면 그것을 먼저 씁니다.
    #   2026-09-14 : ②장에서 대운 다섯 설명을 빼자 여기가 빈손이 되어
    #   2026 이 통째로 안 만들어졌습니다. 원고 구조가 바뀌어도
    #   안 깨지도록 표를 아는 쪽(build)이 적어 줍니다.
    ln.update((doc.get('_names') or {}).get('luck') or {})
    tn.update((doc.get('_names') or {}).get('ten') or {})
    yn.update((doc.get('_names') or {}).get('year') or {})
    for b in doc.get('01', []):
        t = re.sub(r'<[^>]+>', '', str(b.get('t', '')))
        m = re.match(r'^(비겁|식상|재성|관성|인성)\s*(?:→\s*\S+\s*)?·\s*(.+?)\s*$', t)
        if m:
            # ★ 2026-09-14 · 소희 님이 ①장을 다시 쓰시면서 제목을
            #   「{이름}님의 2026년은 「채우고 다음을 준비하는 해」입니다」로
            #   정하셨습니다 — 십성 없이. ②장에서도 십성을 걷어내셨으니
            #   결이 맞습니다. 그래서 뒤 토막만 씁니다.
            yn[m.group(1)] = m.group(2)
    for b in doc.get('02', []):
        t = re.sub(r'<[^>]+>', '', str(b.get('t', '')))
        m = re.match(r'^(비겁|식상|재성|관성|인성)\s*·\s*(.+?)\s*십\s*년\s*$', t)
        if m:
            ln[m.group(1)] = m.group(2) + ' 흐름'
    miss = [g for g in G if g not in yn or g not in ln]
    if miss:
        raise SystemExit('★ 이름표를 못 뽑았습니다: %s' % ', '.join(miss))
    return yn, ln, tn

# ★ 2026-09-14 · 소희 님 「이거 수정안햇어」 — 파일은 고쳐져 있는데
#   화면에는 옛 판이 돌고 있었습니다. 어느 판이 살아 있는지 눈으로
#   확인할 수 있게 만든 시각을 조각에 찍습니다.
#   화면에서 Ctrl+U 로 「stella 2026년 운세 · 판」 을 찾으면 보입니다.
import datetime
STAMP = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

YEAR = sys.argv[1] if len(sys.argv) > 1 else '2026'
HERE = os.path.dirname(os.path.abspath(__file__))
NY = io.open(os.path.join(HERE, 'NY%s.json' % YEAR), encoding='utf-8').read()

# 그 해 세운 천간의 오행 — 2026 병(화) · 2027 정(화)
YEAR_EL = {'2026': '화', '2027': '화'}[YEAR]
YEAR_GAN = {'2026': '병오년', '2027': '정미년'}[YEAR]

HEAD = u'''<?php
/* ══════════════════════════════════════════════════════════
   %(Y)s년 운세 — 열 장짜리 별도 구조 책
                                        ★ 2026-09-14 · 소희 님께
                                        판 %(STAMP)s

   ── 무엇을 하나 ───────────────────────────────────────
   door-fortune 에서 「%(Y)s년 운세」를 고르면 우리 열 장이 나옵니다.
   지금은 그 주제가 DOOR_TOPICS 에 없어서 문 단위 일반판이 나옵니다.

   ★ 먼저 patch160_nydoor 를 넣으셔야 단추가 생깁니다.

   ── 앵커를 안 잡습니다 ────────────────────────────────
   쪽 글을 한 글자도 안 바꿉니다. 책이 다 그려진 뒤, 주제가
   「%(Y)s년 운세」면 책 그릇의 내용을 우리 열 장으로 갈아끼웁니다.
   그래서 「0군데」가 날 일이 없습니다.
   되돌리기도 없습니다 — 스니펫을 끄면 원래대로입니다.

   ── 스물다섯 갈래를 어떻게 고르나 ─────────────────────
   %(Y)s 은 %(YG)s 입니다. 천간이 %(YE)s 이므로 —

       무리(다섯)  = groupOf(일간 오행, %(YE)s)
                     일간 병·정 → 비겁 / 갑·을 → 식상 / 임·계 → 재성
                     경·신 → 관성 / 무·기 → 인성
       대운(다섯)  = groupOf(일간 오행, 그 해 대운 천간의 오행)
       갈래        = 무리 × 대운 = 스물다섯

   ★ 대운은 nowLuck 과 같은 셈입니다 — chart.luck.list 에서
     fromYear 가 %(Y)s 이하인 마지막 칸.
   ★ ②는 축이 넷 더 있습니다 (강도 · 이동 · 대운 · 관계).
     강도는 그 해 오행이 사주에 몇 개인가로 봅니다.

   ── 셈은 전부 책에 이미 있는 것을 씁니다 ──────────────
       window.StellaSaju.locate / compute      원국
       window.StellaRead.interpret             풀이
       chart.pillars.day.han                   일간
       chart.luck.list                         대운
       chart.five                              오행 분포

   ── 붙이는 법 ─────────────────────────────────────────
   ★ 새 조각입니다. WPCode -> 새 스니펫 -> PHP Snippet -> 저장 -> Active
   ★ 위치(Location)를 「어디서나 실행 / Run Everywhere」로.
   ★ 크롬 번역을 끄고 붙여넣으세요.

   넣으신 뒤 door-fortune 에서 「%(Y)s년 운세」를 골라 책을 뽑아보세요.

   ── 검사한 것 ─────────────────────────────────────────
   php -l           문법
   앰퍼샌드 세기      0 이어야 합니다
   node --check     스크립트 문법
   node 로 스물다섯 갈래를 다 그려봄
   ══════════════════════════════════════════════════════════ */

/* ══ 서버가 직접 찍는 한 줄 — 울타리 밖에 둡니다 ═══════════════
   2026-09-14 · 소희 님 「내용도 안보이고 표지도 없어」

   자바스크립트가 아예 안 돌면 자바스크립트로 만든 띠도 안 뜹니다.
   그러면 조각이 켜져 있는지조차 알 수 없습니다.
   그래서 **서버(PHP)가 직접** 한 줄을 찍습니다. 조각이 켜져 있기만
   하면 자바스크립트와 상관없이 무조건 보입니다.
   (CLAUDE.md — 「서버가 발치에 한 줄 찍어 조각이 켜져 있는지를
    따로 알려줍니다」)

   ★ 일부러 울타리(is_page) **밖**에 둡니다. 어느 쪽에서 보시든 뜨므로,
     소희 님이 계신 쪽이 우리가 노리는 쪽인지 한눈에 압니다.
   ★ 관리자에게만 보입니다. 손님 화면에는 한 글자도 안 나갑니다.
   ★ 이 줄이 안 보이면 — 조각이 안 켜졌거나 옛 판이 도는 것입니다. */
add_action( 'wp_footer', function () {
	if ( ! current_user_can( 'manage_options' ) ) { return; }
	global $post;
	$slug = '(쪽 이름 모름)';
	if ( isset( $post ) ) {
		if ( is_object( $post ) ) {
			if ( isset( $post->post_name ) ) { $slug = $post->post_name; }
		}
	}
	$mine = is_page( 'reading-book' ) ? '예 — 우리 쪽입니다' : '아니오 — 여기서는 조각이 안 돕니다';
	echo '<div style="margin:12px;padding:10px 14px;border:2px solid #A9791F;'
	   . 'background:#FFFDF6;border-radius:8px;font:13px/1.8 system-ui;color:#4a3a10">'
	   . '관리자에게만 보입니다 · NY%(Y)s 조각이 켜져 있습니다 · 판 %(STAMP)s'
	   . '<br>지금 쪽 「' . esc_html( $slug ) . '」 · 우리 쪽인가 : ' . $mine
	   . '</div>';
}, 99 );

add_action( 'wp_head', function () {
	/* ★ 이 책은 전자책 쪽에서만 씁니다.
	   2026-09-14 · 소희 님 : 「스니펫이 많아서 그거 읽느라 사주가
	   문제있다고 햇었는데」 — 그 말씀이 맞았습니다.
	   울타리가 없으면 이 조각(수십만 자)이 홈 · 무료 쪽 · 문 쪽까지
	   모든 쪽에 실립니다. 2026 과 2027 두 권이면 반 메가가 넘습니다.
	   reading-book 에서만 내보내면 다른 쪽은 한 글자도 안 받습니다.
	   (쪽 슬러그는 워드프레스에서 직접 확인했습니다 — id 160) */
	if ( ! is_page( 'reading-book' ) ) { return; }
	/* ★★ 사진 주소를 짐작하지 않고 워드프레스에게 묻습니다
	   2026-09-15 · 소희 님 「장표지 글미 없음 — 저거 로고 같은데」

	   동그라미 안에 사진 대신 흐린 로고(책 CSS 의 바탕무늬)만
	   보였습니다. 자리도 크기도 맞으니 **그림을 못 받아온** 것입니다.

	   까닭 : 같은 그림을 다시 올리시면 워드프레스가 파일 이름 끝에
	   -1 을 붙입니다. 미디어를 열어보니 실제로
	       STELLASAJU_FORTUNE-2026.jpg  와  STELLASAJU_FORTUNE-2026-1.jpg
	   이 둘 다 있었습니다. 조각에 박아둔 주소가 살아 있는 쪽이
	   아닐 수 있다는 뜻입니다.

	   그래서 이름으로 미디어를 찾아 **워드프레스가 아는 주소**를
	   씁니다. 못 찾으면 빈 값이 되고, 그때는 아래 박아둔 주소로
	   물러납니다. */
	$pic = '';
	$hit = get_posts( array(
		'post_type'      => 'attachment',
		'post_status'    => 'inherit',
		'post_mime_type' => 'image',
		'posts_per_page' => 1,
		'orderby'        => 'ID',
		'order'          => 'DESC',
		's'              => 'STELLASAJU_FORTUNE-%(Y)s',
	) );
	if ( $hit ) {
		/* ★★ image_url( ..., 'large' ) 를 쓰면 안 됩니다 — 2026-09-15
		   그것은 젯팩 주소에 물음표 뒤 값이 붙은 것을 돌려줍니다
		       i0.wp.com/....jpg?fit=683%%2C1024   <- 앰퍼샌드가 섞입니다
		   집 규칙대로 조각 안에는 앰퍼샌드를 두지 않습니다. 워드프레스가
		   그 글자를 바꿔버리면 주소가 깨져 그림이 안 뜹니다.
		   파라미터 없는 원본 주소를 씁니다. */
		$one = wp_get_attachment_url( $hit[0]->ID );
		if ( $one ) {
			if ( false === strpos( $one, '?' ) ) { $pic = $one; }
		}
	}
	?>
<script>window.StellaPicNy%(Y)s = '<?php echo esc_js( $pic ); ?>';</script>
	<?php
	/* ★ 2026-09-14 · 소희 님 : 「?nycard=1 홈으로 가네」
	   책 쪽은 주소를 건드리면 안 열릴 수 있습니다. 그래서 주소 대신
	   **관리자로 로그인해 계시면 저절로** 한 줄이 뜨게 합니다.
	   손님에게는 안 보입니다. patch160_fit(FIT-2)이 쓰는 길과 같습니다. */
	$stella_admin = current_user_can( 'manage_options' ) ? '1' : '';
	?>
<!-- stella %(Y)s년 운세 · 판 %(STAMP)s -->
<style>
#ssb .keepline{ font-weight:600; }
#ssb .mini{ font-size:.86rem; color:#6a6a78; }
#ssb .nybox{ font-family:IBM Plex Mono,monospace; font-size:.74rem; line-height:1.9;
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
#ssb .nysay{ margin:22px 0; padding:2px 0 2px 18px !important;
  border-left:3px solid #9E2B50; background:none; border-radius:0;
  line-height:1.9; }
#ssb .nymark{ font-family:IBM Plex Mono,monospace; font-size:.62rem;
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
       전에 우리    [data-ny%(Y)s="1"] > .page      → 힘이 모자라 집니다
       지금 우리  #ssb .book[data-ny%(Y)s="1"] > .page  → 이깁니다
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
  #ssb .book[data-ny%(Y)s="1"],
  #ssb [data-ny%(Y)s="1"]{
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
       전에 쓰던 `[data-ny%(Y)s="1"] > .page` 는 힘이 모자라 졌습니다.
       이것이 어떤 쪽은 제 규칙이, 어떤 쪽은 WIDTH-7 이 이기던 까닭입니다. */
  #ssb .book[data-ny%(Y)s="1"] > .page,
  #ssb [data-ny%(Y)s="1"] > .page{
    margin-left:0 !important; margin-right:0 !important;
    padding-left:0 !important; padding-right:0 !important;
    max-width:none !important; width:auto !important; }
    /* ★★ padding 은 누르지 않습니다 — 2026-09-15
       소희 님 「왼쪽에 바가 있을경우 여백이 좁고」
       인용 한 마디(왼쪽 바)와 말상자의 안쪽 여백이 이 못에 눌려
       글이 바에 딱 붙어 있었습니다. 예외를 하나씩 다는 대신
       padding 을 아예 안 건드립니다. 밀려나는 것을 막는 데는
       margin 과 max-width 만으로 충분합니다. */
  #ssb .book[data-ny%(Y)s="1"] > .page:not(.divider):not(.cover):not([data-part="cover"]) > *,
  #ssb [data-ny%(Y)s="1"] > .page:not(.divider):not(.cover):not([data-part="cover"]) > *{
    margin-left:0 !important; margin-right:0 !important;
    max-width:none !important; }
  /* ★ 인용 한 마디는 왼쪽 바 옆에 여백이 있어야 합니다.
     바로 위 못이 `.page > *` 의 좌우 여백을 0 으로 누르는데, 그 못이
     뒤에 있고 선택자도 더 세서 `.nysay` 의 !important 까지 이깁니다.
     그래서 같은 세기로 여기서 한 번 더 박습니다
     (크로미움으로 재서 잡았습니다 — 바가 글에 딱 붙어 있었습니다). */
  #ssb .book[data-ny%(Y)s="1"] > .page > .nysay,
  #ssb [data-ny%(Y)s="1"] > .page > .nysay{
    padding-left:18px !important; }
  /* 장 속표지는 가운데 정렬이라 위 못에서 빼 줍니다 */
  #ssb .book[data-ny%(Y)s="1"] > .page.divider > *,
  #ssb [data-ny%(Y)s="1"] > .page.divider > *{
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
  #ssb .book[data-ny%(Y)s="1"],
  #ssb [data-ny%(Y)s="1"]{
    padding-left:22px !important; padding-right:22px !important; }
  /* ★ 2026-09-14 · 소희 님 : 「2026년 폭이 안맞아」
     가족운 책(FAMILY-1)에는 있는데 여기만 빠져 있던 못입니다.
     살아 있는 쪽에 글을 가운데로 미는 규칙이 얹혀 있으면
     쪽은 제 폭인데 글줄만 안쪽으로 몰려 「폭이 좁다」로 보입니다.
     두 책이 똑같이 보이도록 같은 못을 박습니다. */
  #ssb .book[data-ny%(Y)s="1"] > .page.divider > h2,
  #ssb .book[data-ny%(Y)s="1"] > .page.divider > p,
  #ssb [data-ny%(Y)s="1"] > .page.divider > h2,
  #ssb [data-ny%(Y)s="1"] > .page.divider > p{
    text-align:center !important; }
  #ssb .book[data-ny%(Y)s="1"] > .page > h2,
  #ssb .book[data-ny%(Y)s="1"] > .page > h3,
  #ssb .book[data-ny%(Y)s="1"] > .page > p,
  #ssb [data-ny%(Y)s="1"] > .page > h2,
  #ssb [data-ny%(Y)s="1"] > .page > h3,
  #ssb [data-ny%(Y)s="1"] > .page > p{ text-align:left; }
}

/* ══ 겉표지의 아치문 — 크기와 모양도 우리가 박습니다 ══════
   2026-09-15 · 소희 님 「삼재는 아직 메인에 그림안들어감」
                        「2026 도 비슷하게 메인 사진 없고」
   원본 책은 우리 주제를 몰라 표지 아치를 못 만들거나 비워 둡니다.
   fixCover() 가 없으면 만들어 사진을 넣고, 모양은 여기서 정합니다.
   네 책이 같은 모양이라야 한 세트로 보입니다. */
#ssb .book[data-ny%(Y)s="1"] > .page.cover > .dvmark.dvface,
#ssb [data-ny%(Y)s="1"] > .page.cover > .dvmark.dvface{
  display:block !important;
  width:262px !important; height:360px !important;
  max-width:72%% !important; min-width:0 !important;
  margin:14px auto 30px !important; padding:0 !important;
  border-radius:131px 131px 12px 12px !important;
  overflow:hidden !important; box-sizing:border-box !important; }
#ssb .book[data-ny%(Y)s="1"] > .page.cover > .dvmark.dvface img,
#ssb [data-ny%(Y)s="1"] > .page.cover > .dvmark.dvface img{
  width:100%% !important; height:100%% !important; display:block !important;
  max-width:none !important; object-fit:cover !important;
  object-position:center 34%% !important; }
@media (max-width:640px){
  #ssb .book[data-ny%(Y)s="1"] > .page.cover > .dvmark.dvface,
  #ssb [data-ny%(Y)s="1"] > .page.cover > .dvmark.dvface{
    width:200px !important; height:275px !important;
    border-radius:100px 100px 10px 10px !important;
    margin-bottom:24px !important; }
}
@media print{
  #ssb .book[data-ny%(Y)s="1"] > .page.cover > .dvmark.dvface img,
  #ssb [data-ny%(Y)s="1"] > .page.cover > .dvmark.dvface img{
    -webkit-print-color-adjust:exact; print-color-adjust:exact; }
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
#ssb .book[data-ny%(Y)s="1"] > .page.divider > .dvmark.dvface,
#ssb [data-ny%(Y)s="1"] > .page.divider > .dvmark.dvface{
  display:block !important;
  width:132px !important; height:132px !important;
  max-width:132px !important; min-width:0 !important;
  margin:0 auto 16px !important; padding:0 !important;
  border-radius:50%% !important; overflow:hidden !important;
  box-sizing:border-box !important; }
#ssb .book[data-ny%(Y)s="1"] > .page.divider > .dvmark.dvface img,
#ssb [data-ny%(Y)s="1"] > .page.divider > .dvmark.dvface img{
  width:100%% !important; height:100%% !important; display:block !important;
  max-width:none !important; object-fit:cover !important;
  object-position:center 16%% !important; }
@media (max-width:640px){
  #ssb .book[data-ny%(Y)s="1"] > .page.divider > .dvmark.dvface,
  #ssb [data-ny%(Y)s="1"] > .page.divider > .dvmark.dvface{
    width:108px !important; height:108px !important; max-width:108px !important;
    margin-bottom:14px !important; }
}
@media print{
  #ssb .book[data-ny%(Y)s="1"] > .page.divider > .dvmark.dvface img,
  #ssb [data-ny%(Y)s="1"] > .page.divider > .dvmark.dvface img{
    -webkit-print-color-adjust:exact; print-color-adjust:exact; }
}
</style>
<script>
(function(){
  if(window.StellaNY%(Y)s){ return; }
  window.StellaNY%(Y)s = 1;

  var ADMIN = '<?php echo esc_js( $stella_admin ); ?>';
  var YEAR = %(Y)s;
  var YEAR_EL = '%(YE)s';
  /* 장 표지 얼굴 — 문(door-fortune)의 그 해 사진입니다 */
  var GUARDIAN = '미르';
  var DOORALT  = '%(Y)s년 운세';
  /* ★★ i0.wp.com(젯팩 사진 가속기)을 거치지 않습니다 — 2026-09-15
     소희 님 「중간에 중간에 사진없음」. 파일은 미디어에 다 있는데
     i0.wp.com 주소로는 안 떴습니다. 사이트 주소를 곧장 씁니다. */
    /* ★ 주소는 서버가 미디어에서 찾아 알려준 것을 먼저 씁니다.
       못 찾았으면 아래 박아둔 주소로 갑니다 (2026-09-15). */
  var DOORIMG  = window.StellaPicNy%(Y)s ? window.StellaPicNy%(Y)s
    : 'https://stellasaju.com/wp-content/uploads/2026/09/STELLASAJU_FORTUNE-%(Y)s.jpg';
  COVPIC=DOORIMG; COVALT=DOORALT;   /* 표지에서 쓰려고 옮겨 담습니다 */
  /* ★ 2026-09-14 · 소희 님 : 「2026년이라는 표현은 문장에서 빼세요」
     「원본 데이터에는 {연도}년 … 라고 저장합니다」
     그 말씀대로 해마다 바뀌는 것은 전부 빈칸으로 둡니다. 원고를
     다시 쓰지 않고 해만 갈아끼우면 되도록 하려는 것입니다. */
  var STAMP   = '%(STAMP)s';
  var GANJI   = '%(YG)s';
  var ELNAME  = '%(YE)s';
  var YEARNAME = %(YN)s;
  var LUCKNAME = %(LN)s;
  var TENNAME  = %(TN)s;
  var TOPICS = ['%(Y)s년 운세', '%(Y)s년운세', '%(Y)s 운세'];

  function read(k){
    try{ var r=localStorage.getItem(k); if(!r){ return null; } return JSON.parse(r); }
    catch(e){ return null; }
  }
  function esc(s){
    return String(s===undefined?'':s).split('<').join('').split('>').join('');
  }
  function two(x){ return (x<10?'0':'')+x; }
  /* 이름이 비면 「님」까지 같이 걷어내고 「당신」으로 바꿉니다.
     — 그냥 비워두면 「님의 2026년 운세」가 되고,
       '손님' 을 넣으면 「손님님」이 됩니다. */
  /* 올해이름 · 대운이름 — build() 가 손님 무리를 셈한 뒤 채웁니다.
     2026-09-14 : 그전에는 아무도 안 채워서 손님 책에
     「{올해이름}」이 중괄호째로 찍혔습니다. */
  var YN = '', LN = '', TN = '';
  /* ── 절기 열둘을 책의 계산기로 직접 셉니다 ─────────────────
     2026-09-14 · 소희 님이 ⑤장에 양력 날짜를 적어 주셨습니다.
     그런데 절기는 해마다 하루씩 다릅니다 —
       2026 백로 9월 7일 · 2027 백로 9월 8일
       2026 소서~입추 7월 7일~8월 6일 · 2027 은 7월 7일~8월 7일
     원고에 날짜를 박으면 다음 해에 틀린 날짜를 보여드리게 됩니다.
     그래서 원고에는 {절기1}~{절기12} 만 두고, 책이 이미 가지고 있는
     StellaSaju.terms() 로 그 해 값을 직접 셉니다. 해가 바뀌어도 맞습니다. */
  var TERMLAB = [];
  function fromJD(j){
    var z=Math.floor(j+0.5), f=j+0.5-z, a=z;
    if(z>=2299161){
      var al=Math.floor((z-1867216.25)/36524.25);
      a=z+1+al-Math.floor(al/4);
    }
    var b=a+1524, c=Math.floor((b-122.1)/365.25);
    var d=Math.floor(365.25*c), e=Math.floor((b-d)/30.6001);
    var day=b-d-Math.floor(30.6001*e)+f;
    var mo=(e<14)?e-1:e-13;
    var yr=(mo>2)?c-4716:c-4715;
    return { y:yr, m:mo, d:Math.floor(day) };
  }
  function dayText(j, base){
    var o=fromJD(j+9/24);   /* 한국시 */
    var s=(o.y!==base) ? (o.y+'년 ') : '';
    return s+o.m+'월 '+o.d+'일';
  }
  function termLabels(S){
    var out=[], i;
    try{
      var a=S.terms(YEAR).concat(S.terms(YEAR+1));
      var i0=-1;
      for(i=0;i<a.length;i++){ if(a[i].name==='입춘'){ i0=i; break; } }
      if(i0<0){ return out; }
      for(i=0;i<12;i++){
        var t=a[i0+i], n=a[i0+i+1];
        if(!t){ break; }
        if(!n){ break; }
        out.push(t.name+' · '+dayText(t.jd, YEAR)+' ~ '+dayText(n.jd-1, YEAR));
      }
    }catch(e){ return []; }
    return out;
  }
  function fill(s, nm){
    var t=String(s);
    if(!nm){ t = t.split('{이름}님').join('당신').split('{이름}').join('당신'); }
    else { t = t.split('{이름}').join(nm); }
    if(YN){ t = t.split('{올해이름}').join(YN); }
    if(LN){ t = t.split('{대운이름}').join(LN); }
    if(TN){ t = t.split('{대운십년}').join(TN); }
    t = t.split('{연도}').join(String(YEAR));
    t = t.split('{다음해}').join(String(YEAR + 1));
    t = t.split('{지난해}').join(String(YEAR - 1));
    t = t.split('{간지}').join(GANJI);
    t = t.split('{올해오행}').join(ELNAME);
    var i;
    for(i=0;i<TERMLAB.length;i++){
      t = t.split('{절기'+(i+1)+'}').join(TERMLAB[i]);
    }
    return t;
  }

  /* ── 손님을 무엇이라 부를까 ────────────────────────────
     2026-09-14 · 소희 님 : 「우린 이소희라고 안 부르고 소희님이라고
     부르기로 했어. 성까지 부르면 너무 딱딱해보여」
     그리고 : 「입력폼을 성 따로 이름 따로 넣기로 했었어」

     ★ 폼이 성·이름을 따로 주면 그것을 그대로 씁니다 — 추측이 없습니다.
       남궁민수도 Sohee Lee 도 폼이 갈라준 대로 부릅니다.
     ★ 아직 한 칸으로만 오는 폼(gName)도 있으니, 그때만 뒤로 물러나
       한글 세 글자 이상이면 성을 뗍니다.
     ── 폼이 쓸 수 있는 이름을 두루 봅니다 ───────────────── */
  function firstOf(pr){
    var K=['firstName','first_name','given','givenName','gFirst',
           'name1','nameFirst','이름'];
    var i, v;
    for(i=0;i<K.length;i++){
      v=pr[K[i]];
      if(v){ v=String(v).split(' ').join(''); if(v){ return v; } }
    }
    return '';
  }
  var SURNAME2=['남궁','선우','황보','제갈','사공','서문','독고','동방'];
  function cutSurname(v){
    var i;
    for(i=0;i<SURNAME2.length;i++){
      if(v.indexOf(SURNAME2[i])===0){
        if(v.length>=4){ return v.slice(2); }
        return v;
      }
    }
    if(v.length>=3){ return v.slice(1); }   /* 이소희 → 소희 */
    return v;                                /* 김솔 두 글자는 그대로 */
  }
  function isHangul(v){
    var i, c;
    for(i=0;i<v.length;i++){
      c=v.charCodeAt(i);
      if(c<44032){ return false; }
      if(c>55203){ return false; }
    }
    return v.length>0;
  }
  /* 한 칸 폼에 외국 이름이 오면 앞 토막만 씁니다 — Sohee Lee → Sohee */
  function headWord(v){
    var a=String(v).split(' '), i;
    for(i=0;i<a.length;i++){ if(a[i]){ return a[i]; } }
    return '';
  }
  function callName(pr){
    var f=firstOf(pr);
    if(f){ return f; }                       /* 폼이 갈라줬으면 그대로 */
    var raw=String(pr.name===undefined?'':pr.name);
    var v=raw.split(' ').join('');
    if(!v){ return ''; }                     /* 이름이 없으면 빈 채로 */
    if(!isHangul(v)){ return headWord(raw); }
    return cutSurname(v);
  }

  function isMine(tp){
    var i; for(i=0;i<TOPICS.length;i++){ if(tp===TOPICS[i]){ return true; } }
    return false;
  }

  /* ── 오행 · 십성 무리 (책의 groupOf 와 같은 셈) ──────── */
  var SAENG={'목':'화','화':'토','토':'금','금':'수','수':'목'};
  var GEUK ={'목':'토','토':'수','수':'화','화':'금','금':'목'};
  var GAN_EL_H={'甲':'목','乙':'목','丙':'화','丁':'화','戊':'토',
                '己':'토','庚':'금','辛':'금','壬':'수','癸':'수'};
  var GAN_EL_I=['목','목','화','화','토','토','금','금','수','수'];

  function groupOf(myEl, el){
    if(el===myEl){ return '비겁'; }
    if(SAENG[myEl]===el){ return '식상'; }
    if(GEUK[myEl]===el){ return '재성'; }
    if(GEUK[el]===myEl){ return '관성'; }
    if(SAENG[el]===myEl){ return '인성'; }
    return '';
  }

  /* 그 해에 걸린 대운 한 칸 — 책의 nowLuck 과 같습니다 */
  function nowLuck(chart){
    if(!chart.luck){ return null; }
    var list=chart.luck.list;
    if(!list){ return null; }
    var i, best=null;
    for(i=0;i<list.length;i++){ if(list[i].fromYear<=YEAR){ best=list[i]; } }
    if(best===null){ if(list.length){ best=list[0]; } }
    return best;
  }

  /* 그 해 오행이 사주에 얼마나 있나 — ② 1층 */
  function powerOf(chart){
    var m={'목':0,'화':0,'토':0,'금':0,'수':0}, i;
    if(chart.five){
      for(i=0;i<chart.five.length;i++){ m[chart.five[i].element]=chart.five[i].count; }
    }
    var n=m[YEAR_EL]||0;
    if(n>=3){ return 'much'; }
    if(n<=1){ return 'few'; }
    return 'even';
  }

  var FIVE=['비겁','식상','재성','관성','인성'];
  function nextOf(x){ return FIVE[(FIVE.indexOf(x)+1)%%5]; }
  function relOf(x, d){
    var k=(FIVE.indexOf(d)-FIVE.indexOf(x)+5)%%5;
    return ['겹침','빠져나감','부딪힘','어긋남','받쳐줌'][k];
  }

  var NY = '''

TAIL = u''';

  /* ── 덮기 전에 원본에서 「카드 쪽」을 골라 둡니다 ──────────
     2026-09-14 · 소희 님 : 「비상… 신년운세에 카드 3장 고른거에 대한
     내용이 안들어가」

     우리 조각은 책 그릇을 통째로 갈아끼웁니다(bk.innerHTML). 그래서
     원본이 그려 둔 카드 쪽이 같이 날아갑니다.
     덮기 전에 카드 쪽만 떠서 우리 열 장 뒤에 도로 붙입니다.

     ★ 원본에 카드 쪽이 없으면 아무 일도 안 일어납니다 — 위험이 없습니다.
     ★ 「카드」라는 낱말만 보고 고르면 엉뚱한 쪽이 딸려옵니다. 그래서
       제목(h2)에 카드·아르카나·타로가 있거나, 쪽 안에 카드 칸(.card)이
       실제로 있는 쪽만 고릅니다.
     ★ ?nycard=1 로 몇 쪽을 살렸는지 볼 수 있습니다. */
  var CARDNAMES = [];
  var CARDHTML = '';
  function cardPages(bk){
    var out=[], names=CARDNAMES, ps, i, p, h, t;
    names.length = 0;
    try{ ps=bk.querySelectorAll('.page'); }catch(e){ return out; }
    for(i=0;i<ps.length;i++){
      p=ps[i];
      t='';
      h=p.querySelector('h2');
      if(h){ t=String(h.textContent===undefined?'':h.textContent); }
      /* ★ 2026-09-14 · 소희 님 : 「표지는 있는데 내용이 없어」
         장 속표지(.divider)는 제목만 있고 본문이 없습니다. 제목에
         「아르카나」가 들어 있어서 표지만 딸려오고 있었습니다.
         표지는 거르고, 글이 실제로 든 쪽만 가져옵니다. */
      if(String(p.className).indexOf('divider')>=0){ continue; }
      /* ★ 역빗금을 안 쓰려고 정규식 대신 길이만 봅니다 (집 규칙) */
      var body=String(p.textContent===undefined?'':p.textContent);
      if(body.length<80){ continue; }
      var hit=false;
      if(t.indexOf('카드')>=0){ hit=true; }
      if(t.indexOf('아르카나')>=0){ hit=true; }
      if(t.indexOf('타로')>=0){ hit=true; }
      if(!hit){ if(p.querySelector('.cards')){ hit=true; } }
      if(!hit){ continue; }
      out.push(p.outerHTML);
      names.push(t || '(제목없음)');
    }
    return out;
  }

  /* 쪽번호를 다시 셉니다 — 뒤에 붙인 쪽이 옛 번호를 달고 있습니다 */
  function refolio(bk){
    var ps, i, f;
    try{ ps=bk.querySelectorAll('.page'); }catch(e){ return 0; }
    for(i=0;i<ps.length;i++){
      f=ps[i].querySelector('.folio');
      if(f){ f.textContent=two(i+1); }
    }
    return ps.length;
  }

  /* ── 책 그리기 ──────────────────────────────────────── */
  function build(){
    var S=window.StellaSaju, R=window.StellaRead;
    if(!S){ return null; }
    if(!R){ return null; }
    var o=read('stella_demo');
    if(!o){ return null; }
    var pr=o.profile||o;
    if(!pr.year){ return null; }

    var loc=S.locate(pr.city, pr.country);
    var chart=S.compute({ year:pr.year, month:pr.month, day:pr.day,
      hour:pr.hour, minute:pr.minute||0, sex:pr.sex,
      lon:loc.lon, lat:loc.lat, tz:loc.tz });

    /* 일간 오행 */
    var dayHan='';
    try{ dayHan=String(chart.pillars.day.han).charAt(0); }catch(e){}
    var myEl=GAN_EL_H[dayHan];
    if(!myEl){ return null; }

    /* 무리 = 일간이 그 해 천간을 만나 무엇이 되나 */
    var SP=groupOf(myEl, YEAR_EL);
    if(!SP){ return null; }

    /* 대운 = 일간이 지금 대운 천간을 만나 무엇이 되나 */
    var lk=nowLuck(chart);
    var DAE='';
    if(lk){
      var lel=GAN_EL_I[lk.gan];
      if(!lel){ lel=GAN_EL_H[String(lk.han||'').charAt(0)]; }
      if(lel){ DAE=groupOf(myEl, lel); }
    }
    if(!DAE){ DAE=SP; }

    TERMLAB = termLabels(S);
    var WANT={ move:SP, dae:DAE, power:powerOf(chart), rel:relOf(SP, DAE) };
    YN = YEARNAME[SP] || '';
    LN = LUCKNAME[DAE] || '';
    TN = TENNAME[DAE] || '';
    var nm=esc(callName(pr));

    var pages=[], n=0;
    function page(html, part){
      n++;
      var attr=part?' data-part="'+part+'"':'';
      pages.push('<div class="page"'+attr+'>'+html+
                 '<div class="folio">'+two(n)+'</div></div>');
    }

    /* ── 장 속표지 ────────────────────────────────────────
       2026-09-14 · 소희 님 : 「다른 카테고리처럼 문 사진에 건강운 사진
       넣고 제1장 0000 이렇게만 넣는 장이야. 템플릿 있을거야」
       있었습니다 — patch160_divider 가 만들고 patch160_dvbig 이 키운
       그 틀입니다. 클래스 이름을 그대로 쓰면 책에 이미 있는 CSS 가
       그대로 먹습니다. 새 CSS 를 만들지 않는 까닭입니다.
         .dvmark > img   얼굴 (132px 동그라미)
         .dvwho          가디언 이름
         .dvno dvch      제 N 장   ← 이 쪽이 있는 이유. 제일 큽니다
         h2              장 제목
         .dvrule         밑줄
       소희 님이 「제1장 0000 이렇게만」이라 하셔서 설명(.dvwhat)은
       넣지 않습니다. */
    function sheet(no, title, part){
      n++;
      var attr=part?' data-part="'+part+'"':'';
      return '<div class="page divider"'+attr+'>'+
/* ★ loading="lazy" 를 뺍니다 — 2026-09-16
           소희 님 「장표지의 그림은 안돼?」
           표지 아치에는 사진이 들어가는데 장 속표지 동그라미만
           비어 있었습니다. 진단 띠는 「받았습니다」라고 했는데
           그것은 **표지** 칸을 본 것이었습니다.
           우리는 책을 innerHTML 로 통째로 갈아끼웁니다. 그렇게
           끼운 lazy 그림은 브라우저가 화면에 들어온 줄 모르고
           끝까지 안 받는 일이 있습니다. 장 속표지는 열 장뿐이고
           같은 그림 하나라 한 번만 받으면 됩니다. 미루지 않습니다. */
             '<div class="dvmark dvface"><img decoding="async" '+
             'alt="'+DOORALT+'" src="'+DOORIMG+'"></div>'+
             '<p class="dvwho">'+GUARDIAN+'</p>'+
             '<p class="dvno dvch">'+no+'</p>'+
             '<h2>'+title+'</h2>'+
             '<div class="dvrule"></div>'+
             '<div class="folio">'+two(n)+'</div></div>';
    }
    function bare(t){
      var v=String(t);
      while(v.length){
        var c=v.charCodeAt(0);
        if(c>=9312){ if(c<=9331){ v=v.slice(1); continue; } }
        if(c===32){ v=v.slice(1); continue; }
        break;
      }
      return v;
    }

    /* ── 뽑으신 카드 세 장 ──────────────────────────────────
       2026-09-14 · 소희 님 : 「비상… 신년운세에 카드 3장 고른거에
       대한 내용이 안들어가」 · 「내용도 안보이고 표지도 없어」

       관리자 띠가 「원본에서 살린 카드 쪽 0쪽」이라고 말해 주었습니다.
       원본 신년운세 책에는 카드 대목이 **아예 없었습니다** — 카드
       세 꼭지는 door-tarot 안에만 있습니다. 덮여서 사라진 것이
       아니라 처음부터 없었던 것입니다. 그래서 새로 만듭니다.

       ★ 카드 표를 다시 적지 않습니다. 책이 window.StellaTarot 로
         일흔여덟 장을 이미 내놓고 있습니다 (메이저 스물둘 + 마이너
         쉰여섯). 카드마다 now · over · then 세 가지 풀이가 다 있습니다.
       ★ 자리마다 읽는 법이 다릅니다 (책 주석 그대로) —
           I 지금 서 있는 자리 · II 넘어야 할 것 · III 그 너머
       ★ 카드를 안 뽑으셨으면 이 장을 아예 안 만듭니다. */
    function cardChapter(){
      var T=window.StellaTarot;
      if(!T){ return ''; }
      var pick=read('stella_cards');
      if(!(pick instanceof Array)){ return ''; }
      if(pick.length<3){ return ''; }
      var SEAT=[['I','지금 서 있는 자리','now'],
                ['II','넘어야 할 것','over'],
                ['III','그 너머','then']];
      /* ★ 2026-09-14 · 소희 님 : 「카드 그림이 없어서 없는줄」
         글만 있으니 카드 장인 줄 모르셨습니다. 그림을 넣습니다.
         ★ 그림은 책이 이미 쓰고 있는 것을 그대로 씁니다 —
           door-tarot 의 「마지막에 놓는 세 장」이 st001.jpg ~ st078.jpg
           를 부릅니다. 새로 올리실 것이 없습니다.
         ★ 뒤집힘(역방향)도 같이 봅니다 — 2026-09-15 · 소희 님
           「역방향도 있어야지 크게 변화가 있을수 있는거잖아」
           판정하는 함수는 door-tarot 안에 있어 못 부릅니다. 그런데
           그것은 난수가 아니라 생년월일시와 오늘 날짜로 정해지는 셈이라,
           그 셈을 그대로 옮기면 카드 쪽과 또같은 모양이 나옵니다.
           역방향 글(StellaRev)은 window 에 나와 있어 그대로 씁니다 —
           메이저 스물두 장만 역방향 글이 있고, 마이너는 늘 정방향입니다. */
      var UP='https://stellasaju.com/wp-content/uploads/2026/08/';
      var REV=window.StellaRev ? window.StellaRev : {};
      function numOf(x){ if(typeof x==='number'){ return x; } return 0; }
      function seedOf(){
        var d=new Date();
        var v=numOf(pr.year)*10007 + numOf(pr.month)*331 + numOf(pr.day)*97
            + numOf(pr.hour)*13 + numOf(pr.minute)*7
            + d.getFullYear()*1103 + (d.getMonth()+1)*37 + d.getDate()*3 + 29;
        var s2=v % 2147483647;
        if(s2<=0){ s2+=2147483646; }
        return s2;
      }
      var SEED=seedOf();
      function flip(ci, nth){
        if(Number(ci)>21){ return false; }
        var v=(SEED + (Number(ci)+1)*911 + (nth+1)*577) % 100;
        if(v<32){ return true; }
        return false;
      }
      var RVS=[], z;
      for(z=0;z<3;z++){ RVS.push(flip(pick[z], z)); }
      function sayOf(c, rv, key){
        if(rv){
          var r=REV[c.n];
          if(r){ if(r[key]){ return r[key]; } }
        }
        return c[key];
      }
      var h='<p class="keepline">사주가 한 해의 결을 말한다면, 카드는 '+
            '지금 이 순간의 자리를 말합니다.</p>'+
            '<p>질문 화면에서 세 장을 뽑으셨습니다. 앞의 열 장을 뒤집는 것이 '+
            '아니라, 같은 해를 어떤 마음으로 지날지를 덧붙입니다.</p>';
      var i, c, seat, no;
      /* 세 장을 나란히 폅니다 */
      h+='<div style="display:flex;gap:12px;justify-content:center;'+
         'margin:24px 0 10px;flex-wrap:wrap">';
      for(i=0;i<3;i++){
        c=T[pick[i]];
        if(!c){ continue; }
        seat=SEAT[i];
        no=('00'+(Number(pick[i])+1));
        no=no.slice(no.length-3);
        h+='<figure style="flex:1 1 28%;max-width:190px;min-width:120px;'+
           'margin:0;text-align:center">'+
           '<img decoding="async" loading="lazy" alt="'+esc(c.ko)+'" '+
           'src="'+UP+'st'+no+'.jpg" '+
           'style="width:100%;display:block;border-radius:8px;'+
           'border:1px solid rgba(212,175,106,.35)'+
           (RVS[i] ? ';transform:rotate(180deg)' : '')+'">'+
           '<figcaption style="margin-top:9px;font-size:.78rem;line-height:1.6;'+
           'opacity:.72">'+seat[0]+' · '+seat[1]+
           '<br><b style="font-size:.92rem;opacity:1">'+esc(c.ko)+'</b>'+
           (RVS[i] ? '<br><span style="opacity:.8">뒤집혀 나왔습니다</span>' : '')+
           '</figcaption></figure>';
      }
      h+='</div>';
      for(i=0;i<3;i++){
        c=T[pick[i]];
        if(!c){ continue; }
        seat=SEAT[i];
        h+='<h3>'+seat[0]+' · '+seat[1]+' — 「'+esc(c.ko)+'」'+
           (RVS[i] ? ' <em>뒤집힘</em>' : '')+'</h3>';
        h+='<p>'+esc(sayOf(c, RVS[i], seat[2]))+'</p>';
      }
      /* ── 셋을 겹쳐 읽습니다 ────────────────────────────────
         2026-09-14 · 소희 님 : 「카드가 의미하는거 말고
                                 그 세개를 합께 말하는 거」
         한 장씩 읽는 것과 셋을 겹쳐 읽는 것은 다릅니다. 조합이 너무
         많아 하나하나 쓸 수 없으니, 책이 door-tarot 에서 쓰는 잣대를
         그대로 가져옵니다 (책 주석 : 「세 잣대로만 읽습니다 — 큰 카드가
         몇 장인가 · 숫자가 오르는가 내리는가 · 뒤집힌 것이 몇 장인가」).
         ★ 세 잣대를 다 씁니다 — 뒤집힘은 위에서 책과 같은 셈으로
           구해 두었습니다(RVS).
         ★ 값 매기기도 책과 같은 결 — 메이저는 번호, 마이너는 spd(1~21). */
      function valOf(ci){
        var k=Number(ci);
        if(k<=21){ return k; }
        var cc=T[k];
        if(cc){ if(cc.spd){ return Number(cc.spd); } }
        return 11;
      }
      var maj=0, vs=[], q;
      for(q=0;q<3;q++){
        if(Number(pick[q])<=21){ maj++; }
        vs.push(valOf(pick[q]));
      }
      h+='<h3>세 장을 겹쳐 놓으면</h3>';
      if(maj===0){
        h+='<p>세 장이 모두 <em>작은 카드</em>입니다. 큰 카드가 한 장도 없어요. '+
           '올해가 바깥에서 통째로 흔들리는 해는 아니라는 뜻입니다. '+
           '<strong>크게 터지는 일보다, 매일 하는 선택이 한 해를 만듭니다.</strong></p>';
      } else if(maj===1){
        h+='<p>큰 카드가 <em>한 장</em> 섞여 있습니다. '+
           '올해 가운데 한 번은 내 뜻과 상관없이 움직이는 일이 옵니다. '+
           '<strong>나머지는 {이름}님이 정하는 대로 갑니다.</strong></p>';
      } else {
        h+='<p>큰 카드가 <em>'+maj+' 장</em>이나 됩니다. '+
           '올해가 조용히 지나가지는 않습니다. 좋은 쪽이든 아닌 쪽이든 '+
           '<strong>지금과 같은 모양으로 끝나지는 않습니다.</strong> '+
           '계획을 너무 촘촘히 잡아두시면 오히려 어긋납니다.</p>';
      }
      var gap=vs[2]-vs[0];
      if(gap>=5){
        h+='<p>숫자가 <em>올라갑니다.</em> 지금이 가장 낮고 뒤로 갈수록 커지는 모양이에요. '+
           '<strong>지금 답답한 것이 올해의 바닥입니다.</strong> '+
           '다만 올라가는 속도가 느려 한동안은 티가 안 납니다.</p>';
      } else if(gap<=-5){
        h+='<p>숫자가 <em>내려갑니다.</em> 지금이 가장 크고 뒤로 갈수록 작아지는 모양이에요. '+
           '나빠진다는 뜻이 아닙니다. <strong>벌여둔 것을 정리하고 매듭짓는 해</strong>라는 '+
           '뜻이에요. 새로 크게 벌이시면 올해 안에는 결론이 안 납니다.</p>';
      } else {
        h+='<p>숫자가 <em>크게 오르지도 내리지도 않습니다.</em> 평평한 모양이에요. '+
           '답답하실 수 있는데 <strong>흔들리지 않는다는 뜻</strong>이기도 합니다. '+
           '이런 해에 정해둔 것이 제일 오래 갑니다.</p>';
      }
      /* 세째 잣대 — 뒤집힌 것이 몇 장인가 */
      var rvn=0, rvi=-1;
      for(q=0;q<3;q++){
        if(RVS[q]){ rvn++; if(rvi<0){ rvi=q; } }
      }
      if(rvn===0){
        h+='<p>세 장이 모두 <em>바로 놓였습니다.</em> 뒤집혀 나온 카드가 한 장도 '+
           '없어요. 카드가 말하는 것이 그대로 그 방향으로 흘러간다는 뜻입니다. '+
           '<strong>올해는 보이는 대로 가는 해입니다.</strong> 다만 뒤집힌 것이 없다는 말은 '+
           '뒤집히며 열리는 문도 없다는 뜻이라, 올해는 {이름}님이 밀어야 움직입니다.</p>';
      } else if(rvn===1){
        h+='<p><em>'+SEAT[rvi][1]+'</em> 한 장이 뒤집혀 나왔습니다. '+
           '세 자리 가운데 그곳에서만 방향이 한 번 바뀝니다. '+
           '<strong>그 자리는 처음 생각하신 대로 가지 않습니다.</strong> '+
           '막혔다는 뜻은 아닙니다 — 다른 모양으로 풀린다는 뜻입니다. '+
           '그 한 자리만 계획을 느슨하게 잡아두세요.</p>';
      } else {
        h+='<p>뒤집혀 나온 카드가 <em>'+rvn+' 장</em>입니다. '+
           '올해는 생각하신 순서대로 가는 해가 아닙니다. '+
           '<strong>한 해 가운데 한 번은 크게 바뀝니다.</strong> 나쁘다는 뜻이 아니라, '+
           '지금 세워둔 계획이 그대로 쓰이기 어렵다는 뜻이에요. '+
           '바뀌는 것을 받아낼 자리를 미리 비워두시는 편이 낫습니다.</p>';
      }
      h+='<blockquote class="nysay"><strong>카드는 올해를 정해주지 않습니다. '+
         '다만 지금 어디에 서 있는지를 소리 내어 말해 줍니다.</strong></blockquote>';
      h+='<p class="keepline">미르</p>';
      /* 카드 장은 fill() 을 안 거치므로 {이름} 을 여기서 채웁니다 */
      return h.split('{이름}').join(nm ? nm : '당신');
    }

    var NOS=['01','02','03','04','05','06','07','08','09','10'];
    var MARK=['제 1 장','제 2 장','제 3 장','제 4 장','제 5 장',
              '제 6 장','제 7 장','제 8 장','제 9 장','제 10 장','제 11 장'];
    /* 카드 장은 ⑨ 뒤 · ⑩(건네는 말) 앞에 놓습니다 — 배웅이 마지막이라야
       책이 제대로 닫힙니다. 그래서 ⑩ 은 「제 11 장」이 됩니다. */
    CARDHTML=cardChapter();
    var cardAt=CARDHTML ? 9 : -1;
    var mark=0;
    var i, j, blocks, b, html, tt;

    for(i=0;i<NOS.length;i++){
      if(i===cardAt){
        pages.push(sheet(MARK[mark], '카드가 말하는 것', 'two'));
        mark++;
        page(CARDHTML, 'two');
      }
      blocks=NY[NOS[i]];
      if(!blocks){ continue; }
      /* 장 표지 한 쪽을 먼저 놓습니다 */
      var ct='';
      for(j=0;j<blocks.length;j++){
        if(blocks[j].kind==='title'){ ct=bare(blocks[j].t); break; }
      }
      var hadSheet=false;
      if(ct){ pages.push(sheet(MARK[mark], fill(ct, nm), (i<4?'one':'two'))); mark++; hadSheet=true; }
      html='';
      for(j=0;j<blocks.length;j++){
        b=blocks[j];
        if(b.kind==='title'){
          /* 원고에 붙은 ①②③ 은 제가 쓰기 좋으라고 단 번호입니다.
             책에는 「제 1 장」 딱지가 따로 있으니 뗍니다. */
          tt=String(b.t);
          while(tt.length){
            var c0=tt.charCodeAt(0);
            if(c0>=9312){ if(c0<=9331){ tt=tt.slice(1); continue; } }
            if(c0===32){ tt=tt.slice(1); continue; }
            break;
          }
          /* 장 속표지를 바로 앞에 놓았으면 같은 제목을 또 쓰지 않습니다.
             2026-09-14 · ?leadwhy=1 차례에 제목이 두 번씩 찍혀 드러났습니다
             (1. 올해나는어떤해를보내는가 / 2. 올해나는어떤해를보내는가).
             속표지에 큰 글씨로 이미 있으니 본문은 머리글부터 시작합니다. */
          if(hadSheet){ html+=fill(b.h, nm); continue; }
          html+='<h2>'+fill(tt, nm)+'</h2>'+fill(b.h, nm);
          continue;
        }
        if(b.kind==='always'){
          tt=b.t?('<h3>'+fill(b.t, nm)+'</h3>'):'';
          html+=tt+fill(b.h, nm);
          continue;
        }
        if(b.kind==='group'){
          if(b.key!==SP){ continue; }
          tt=b.t?('<h3>'+fill(b.t, nm)+'</h3>'):'';
          html+=tt+fill(b.h, nm);
          continue;
        }
        if(b.kind==='dae'){
          /* 대운 갈래 — 지금 지나는 십 년 것만 냅니다 */
          if(b.key!==DAE){ continue; }
          tt=b.t?('<h3>'+fill(b.t, nm)+'</h3>'):'';
          html+=tt+fill(b.h, nm);
          continue;
        }
        if(b.kind==='branch'){
          if(b.group!==SP){ continue; }
          if(b.key!==DAE){ continue; }
          tt=b.t?('<h3>'+fill(b.t, nm)+'</h3>'):'';
          html+=tt+fill(b.h, nm);
          continue;
        }
        if(b.kind==='pick'){
          if(WANT[b.axis]!==b.key){ continue; }
          tt=b.t?('<h3>'+fill(b.t, nm)+'</h3>'):'';
          html+=tt+fill(b.h, nm);
          continue;
        }
      }
      page(html, (i<4?'one':'two'));
    }

    if(n===0){ return null; }
    return { html:pages.join(''), n:n,
             title:(nm?nm+'님의 ':'당신의 ')+YEAR+'년 운세',
             sp:SP, dae:DAE };
  }



  /* ── 장 속표지 사진이 안 뜨면 한 번 더 ───────────────
     2026-09-15 · 소희 님 「중간표지에도 그림 안들어감」

     동그라미 안에 사진 대신 흐린 로고만 보였습니다. 크기는 우리가
     박았으니 자리는 있는데 **그림이 안 받아졌다**는 뜻입니다.
     사이트 주소와 젯팩 주소(i0.wp.com) 가운데 어느 쪽이 살아 있는지
     제가 여기서 확인할 수 없으므로, 안 뜨면 다른 쪽으로 한 번 더
     시도하게 둡니다. 어느 쪽이 살아 있든 사진이 나옵니다. */
  function altURL(src){
    var s=String(src===null?'':src), k=s.indexOf('://');
    if(k<0){ return ''; }
    var rest=s.slice(k+3);
    if(rest.indexOf('i0.wp.com/')===0){ return ''; }
    return 'https://i0.wp.com/'+rest;
  }
  function retryImg(im){
    if(!im){ return; }
    /* ★ 미루지 말고 바로 받게 합니다 — 2026-09-16
       innerHTML 로 끼운 lazy 그림은 브라우저가 화면에 들어온 줄
       모르고 끝까지 안 받는 일이 있습니다. 옛 판으로 그려진
       그림에도 걸리도록 여기서 한 번 더 벗겨 줍니다. */
    try{
      if(im.getAttribute('loading')){
        im.removeAttribute('loading');
        var cur0=im.getAttribute('src');
        if(cur0){ im.setAttribute('src', cur0); }
      }
    }catch(e0){}
    if(im.getAttribute('data-retry')==='1'){ return; }
    var go=function(){
      if(im.getAttribute('data-retry')==='1'){ return; }
      im.setAttribute('data-retry','1');
      var u=altURL(im.getAttribute('src'));
      if(u){ im.setAttribute('src', u); }
    };
    im.addEventListener('error', go);
    if(im.complete){ if(!im.naturalWidth){ go(); } }
  }
  /* ── 겉표지 아치 ────────────────────────────
     2026-09-16 · 소희 님 사진에 아치가 **둘** 나왔습니다.

     원본 표지의 아치는 <img> 태그가 아니라 **배경 그림**으로
     그려집니다. 태그만 찾으면 「없다」고 보고 하나 더 만듭니다.
     그래서 책이 화면에 붙은 **뒤에** 배경까지 읽어 판단합니다.

     아치가 이미 있으면(태그로든 배경으로든) 아무것도 안 합니다.
     아예 없을 때만 만듭니다 — 신년운세 표지가 그렇습니다. */
  function fixCoverArch(root){
    try{
      var cov = root.querySelector('.page.cover');
      if(!cov){ cov = root.querySelector('.page[data-part="cover"]'); }
      if(!cov){ return; }
      if(cov.getAttribute('data-archdone') === '1'){ return; }
      cov.setAttribute('data-archdone', '1');

      /* ① 그림 태그가 있으면 이미 아치가 있는 것입니다 */
      if(cov.querySelector('img')){ return; }

      /* ② 배경 그림으로 그려진 것도 찾습니다 */
      var kids = cov.querySelectorAll('*'), i, st, bg;
      for(i = 0; i < kids.length; i++){
        try{
          st = window.getComputedStyle(kids[i]);
          if(!st){ continue; }
          bg = String(st.backgroundImage === undefined ? '' : st.backgroundImage);
          if(bg){ if(bg !== 'none'){ if(bg.indexOf('url') >= 0){ return; } } }
        }catch(e1){}
      }

      /* ③ 아무것도 없을 때만 만듭니다 */
      if(!COVPIC){ return; }
      var fa = document.createElement('div');
      fa.className = 'dvmark dvface';
      fa.setAttribute('data-ourarch', '1');
      var im = document.createElement('img');
      im.setAttribute('decoding', 'async');
      im.setAttribute('src', COVPIC);
      im.setAttribute('alt', COVALT ? COVALT : '');
      fa.appendChild(im);

      var mk = cov.querySelector('.mark'), h0 = cov.querySelector('h1');
      if(mk){
        if(mk.nextSibling){ cov.insertBefore(fa, mk.nextSibling); }
        else { cov.appendChild(fa); }
      }
      else if(h0){ cov.insertBefore(fa, h0); }
      else { cov.insertBefore(fa, cov.firstChild); }
      retryImg(im);
    }catch(e){}
  }

  function fixFaces(root){
    try{
      var ims=root.querySelectorAll('.dvmark.dvface img'), i;
      for(i=0;i<ims.length;i++){ retryImg(ims[i]); }
    }catch(e){}
  }
  /* ── 사진이 왜 안 뜨는지 찍어 줍니다 ──────────────────
     2026-09-15 · 소희 님 「장표지에 그림이 ...」
     표지 아치에는 사진이 들어가는데 장 속표지 동그라미만 비어
     있습니다. 더 짐작하지 않고 **실제 주소와 받아졌는지**를
     관리자 띠에 찍습니다. 한 번만 보시면 까닭이 바로 나옵니다.
     ★ 손님에게는 안 보입니다 (관리자 띠 안에서만 부릅니다). */
  function picReport(root){
    try{
      var ims=root.querySelectorAll('.dvmark.dvface img');
      if(!ims.length){ return '사진 — ★ 그림칸이 하나도 없습니다'; }
      var i, im, got=0, bad=0, wait=0, cov=0, dv=0, first='', badone='', size='';
      for(i=0;i<ims.length;i++){
        im=ims[i];
        var onCover=0;
        try{ if(im.closest){ if(im.closest('.page.cover')){ onCover=1; } } }catch(e2){}
        if(onCover){ cov++; } else { dv++; }
        if(!im.complete){ wait++; }
        else if(im.naturalWidth){
          got++;
          if(!first){ first=String(im.getAttribute('src'));
                      size=im.naturalWidth+'x'+im.naturalHeight; }
        }
        else { bad++; if(!badone){ badone=String(im.getAttribute('src')); } }
      }
      var nl=String.fromCharCode(10);
      var s='사진 — 표지 '+cov+'칸 · 장 속표지 '+dv+'칸';
      s+=nl+'  받음 '+got+' · ★ 못 받음 '+bad+' · 받는 중 '+wait;
      if(first){ s+=nl+'  받은 것 '+size+' · '+first; }
      if(badone){ s+=nl+'  ★ 못 받은 주소 '+badone; }
      return s;
    }catch(e){ return '사진 — ★ '+e; }
  }

  /* ★ 표지에 쓸 사진 — 책을 지을 때 담아 둡니다.
     사진 주소(DOORIMG)는 book()/build() **안**에 있어서 fixCover 에서는
     안 보입니다. 보이는 자리에 옮겨 담습니다 (2026-09-15).
     이 한 줄이 없어 가족운·삼재 표지에 아치가 안 만들어졌습니다. */
  var COVPIC, COVALT;   /* ★ 여기서 ='' 로 두면 안 됩니다 — 신년운세는
     사진 주소를 이 줄보다 **위**에서 담는데, 그 값을 빈 글자로
     덮어써서 표지에 사진이 안 들어갔습니다 (2026-09-15 에 그랬습니다). */

  /* ── 겉표지 손보기 ──────────────────────────
     2026-09-15 · 소희 님 「아치문이 없어」

     ① 아치문(표지의 금빛 테두리)은 patch160_cover 가 쪽에 심어둔
        CSS 가 그립니다. 그 CSS 는 `.page[data-part="cover"]` 에
        걸려 있습니다. 살려온 표지에 그 **속성**이 없으면 테두리가
        한 줄도 안 그려집니다 — 클래스(.cover)만으로는 안 걸립니다.
        그래서 옮길 때 속성을 반드시 붙여 줍니다.

     ② 부제(.sub)와 제목(h1)은 원본 책이 정합니다. 원본은 우리
        주제를 모르므로 엉뚱한 기본값을 찍습니다 (소희 님이 보신
        「THE ARCHITECT」 — 그것은 직업운 부제입니다).
        글자만 갈아 끼웁니다. 테두리와 자리는 그대로입니다. */
  var COVSUB='THE YEAR AHEAD';
  function fixCover(el, ttl){
    try{
      var e=el.cloneNode(true);
      e.setAttribute('data-part','cover');
      var cls=String(e.className===undefined?'':e.className);
      if(cls.indexOf('page')<0){ cls=cls+' page'; }
      if(cls.indexOf('cover')<0){ cls=cls+' cover'; }
      e.className=cls;
      var s=e.querySelector('.sub');
      if(s){ if(COVSUB){ s.textContent=COVSUB; } }
      /* ★ 표지 아치는 여기서 만들지 않습니다 — 2026-09-16
         소희 님 사진에 아치가 또 둘 나왔습니다.
         까닭 : 원본 표지의 아치는 <img> 태그가 아니라 **배경 그림**
         으로 그려집니다. querySelector('img') 로는 못 찾습니다.
         그리고 여기서는 쪽이 아직 화면에 붙기 전이라 배경을 읽을
         수도 없습니다. 그래서 책을 다 그린 뒤에 fixCoverArch() 가
         배경까지 보고 판단합니다. 여기서는 글자만 고칩니다. */
      var h=e.querySelector('h1');
      if(h){ if(ttl){
        var t=String(ttl), i=t.indexOf('님의 ');
        h.textContent='';
        if(i<0){ h.appendChild(document.createTextNode(t)); }
        else{
          h.appendChild(document.createTextNode(t.slice(0, i+2)));
          h.appendChild(document.createElement('br'));
          h.appendChild(document.createTextNode(t.slice(i+3)));
        }
      } }
      return e.outerHTML;
    }catch(err){ return el.outerHTML; }
  }

  window.StellaNY={ build:build, has:isMine, year:YEAR };

  /* ── 관리자에게 보이는 진단 띠 ────────────────────────────
     2026-09-14 · 소희 님 : 「표지도 없고 내용도 없어」
     책이 하얗게 나오면 자바스크립트가 멈춘 것입니다. 그런데 지금까지는
     catch(e){} 가 까닭을 통째로 삼켜서 아무 말도 안 나왔습니다.

     ★ CLAUDE.md 의 GWHY 교훈대로 **띠를 먼저 그려 놓고** 읽습니다.
       띠를 그리는 일 자체가 죽지 않도록 통째로 try 로 감쌉니다.
     ★ 관리자에게만 보입니다. 손님 화면에는 안 나갑니다. */
  var LOG = [];
  function paint(){
    if(!ADMIN){ return; }
    try{
      var d=document.getElementById('ny-admin-'+YEAR);
      if(!d){
        d=document.createElement('div');
        d.id='ny-admin-'+YEAR;
        d.setAttribute('style','margin:12px;padding:10px 14px;'+
          'border:2px solid #2F7D4A;background:#F3F8F4;border-radius:8px;'+
          'font:13px/1.8 system-ui;color:#1d3a27;white-space:pre-wrap;');
        var ssb=document.getElementById('ssb');
        if(ssb){ if(ssb.parentNode){ ssb.parentNode.insertBefore(d, ssb); } }
        else { if(document.body){ document.body.appendChild(d); } }
      }
      d.textContent='관리자에게만 보입니다 · NY'+YEAR+' 판 '+STAMP+
        String.fromCharCode(10)+LOG.join(String.fromCharCode(10));
    }catch(e){}
  }
  function say(x){ LOG.push(x); paint(); }

  var tries=0;
  function go(){
    tries++;
    try{
      var bk=document.getElementById('bkBook');
      if(!bk){
        if(tries===1){ say('책 그릇(#bkBook)을 아직 못 찾음 — 기다립니다'); }
        if(tries>40){ say('★ 끝까지 책 그릇을 못 찾았습니다'); return; }
        setTimeout(go, 300); return;
      }
      if(bk.getAttribute('data-ny'+YEAR)==='1'){ return; }

      var o=read('stella_demo');
      if(!o){
        if(tries===1){ say('주문(stella_demo)이 아직 없음 — 기다립니다'); }
        if(tries>40){ say('★ 끝까지 주문을 못 찾았습니다'); return; }
        setTimeout(go, 300); return;
      }
      var tp=String(o.topic===undefined?'':o.topic);
      if(!isMine(tp)){
        say('주제가 「'+tp+'」 — 이 조각 것이 아닙니다 (물러납니다)');
        return;
      }
      if(String(bk.innerHTML).length<=200){
        if(tries>40){ say('★ 원본 책이 끝까지 안 그려졌습니다'); return; }
        setTimeout(go, 300); return;
      }

      var keep=cardPages(bk);
      var r=build();
      if(!r){
        say('★ 책을 못 지었습니다 — 사주 계산기(StellaSaju/StellaRead)나 '+
            '생년월일을 못 읽었습니다');
        return;
      }
      /* ★ 원본 책의 겉표지를 살려 맨 앞에 붙입니다 — 2026-09-15
         소희 님 「제일 겉표지 안붙었어」
         겉표지(.page.cover)는 원본 책이 짓습니다. innerHTML 로 통째로
         갈아끼우면 같이 날아갑니다. 카드 쪽을 살리듯 표지도 살립니다. */
      var cov=[];
      try{
        var cs=bk.querySelectorAll('.page.cover, .page[data-part="cover"]'), ci;
        /* ★ 겉표지는 **한 장만** 살립니다 — 2026-09-15
           소희 님 「건강운 표지가 2번들어감 목차 뒤에 또 표지가있음」
           원본 책이 겉표지 꼴의 쪽을 둘 짓습니다 (겉표지 + 속표지).
           둘 다 옮기면 목차 뒤에 또 표지가 나옵니다. 맨 앞 하나만. */
        if(cs.length){ cov.push(fixCover(cs[0], r.title)); }
      /* ★ 원본 책의 차례 쪽도 살립니다 — 2026-09-15
         소희 님 「목차가 없어졌어」
         차례(.tocpage)는 원본 책이 짓고, 우리 책의 장 제목을 읽어
         제 결로 채웁니다. innerHTML 로 덮으면 그 **그릇**까지
         사라져서 다시 채울 데가 없어집니다. 겉표지처럼 살립니다. */
      var toc=[];
      try{
        var ts=bk.querySelectorAll('.tocpage'), ti;
        for(ti=0; ti<ts.length; ti++){ toc.push(ts[ti].outerHTML); }
      }catch(e){}
      }catch(e){}
      bk.innerHTML=cov.join('')+toc.join('')+r.html+keep.join('');
      fixFaces(bk);   /* 사진이 안 뜨면 다른 주소로 한 번 더 */
      fixCoverArch(bk);   /* 표지 아치가 아예 없을 때만 만듭니다 */
      bk.setAttribute('data-ny'+YEAR,'1');
      bk.setAttribute('data-nycard', String(keep.length));
      var nAll=refolio(bk);
      var t=document.getElementById('bkTitle');
      if(t){ t.textContent=r.title; }
      var c=document.getElementById('bkN');
      if(c){ c.textContent=nAll+'쪽'; }
      /* ★ 2026-09-14 · 띠 문구를 바로잡습니다.
         「우리 열 장 22쪽」이라고 찍혀 헷갈렸습니다 — 그 22쪽 안에
         카드 장이 이미 들어 있습니다. 무엇이 몇 쪽인지 나눠 찍습니다.
         원본 카드 쪽 살리기는 살릴 것이 0쪽이라 (신년운세에는 원래
         없습니다) 실제로 살렸을 때만 적습니다. */
      var lab='';
      if(keep.length){ lab=' + 원본에서 살린 쪽 '+keep.length+'쪽 ['+
                            CARDNAMES.join(' / ')+']'; }
      var cardMsg = CARDHTML ? '카드 장 있음' : '카드 장 없음 (카드를 안 뽑으셨습니다)';
      say('그렸습니다 · 갈래 '+r.sp+' × 십 년 '+r.dae+
          ' · '+cardMsg+' · 우리 책 '+r.n+'쪽'+lab+' = 모두 '+nAll+'쪽');
      /* 사진이 다 받아질 틈을 두고 찍습니다 (2026-09-15) */
      setTimeout(function(){ say(picReport(bk)); }, 1400);
      return;
    }catch(e){
      say('★ 멈췄습니다 — '+(e ? String(e.message||e) : '까닭 모름'));
      return;
    }
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', go);
  } else {
    go();
  }

})();
</script>
	<?php
}, 3 );
'''

_YN, _LN, _TN = year_luck_names(json.loads(NY))
print('  올해이름 %d · 대운이름 %d 개를 원고에서 뽑았습니다' % (len(_YN), len(_LN)))


def _jstable(d):
    """홑따옴표 JS 표 — 쌍따옴표를 안 써서 역빗금이 안 생깁니다."""
    return '{' + ', '.join("'%s':'%s'" % (k, v) for k, v in sorted(d.items())) + '}'


head = HEAD % {'Y': YEAR, 'YE': YEAR_EL, 'YG': YEAR_GAN,
               'YN': _jstable(_YN), 'LN': _jstable(_LN), 'TN': _jstable(_TN),
               'STAMP': STAMP}
out = head + NY + TAIL
path = os.path.join(HERE, '..', 'php', 'patch160_ny%s.WPCODE.txt' % YEAR)
io.open(path, 'w', encoding='utf-8').write(out)
print('썼습니다 %s' % os.path.normpath(path))
print('  바이트 %d · 글자 %d' % (len(out.encode('utf-8')), len(out)))
print('  앰퍼샌드 %d (0 이어야 합니다)' % out.count('&'))
