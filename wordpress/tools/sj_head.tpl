<?php
/* ════════════════════════════════════════════════════════════
   삼재 — 여섯 장짜리 별도 구조 책
   ★ 만든 판 %(STAMP)s · 그 해 %(Y)s (%(YG)s · %(YE)s)

   무엇을 하나 — door-fortune 에서 「삼재」를 고르면 우리 여섯 장이
   나옵니다. 책 그릇(#bkBook)의 내용을 통째로 갈아끼웁니다.

   ★ 삼재는 값을 안 받습니다. 검색으로 들어오는 분을 받아 신년운세로
     이어주는 자리입니다.

   어떻게 갈리나
     삼재 자리 — 태어난 해(띠)로 정해집니다. 십성이 아닙니다.
         申子辰 → 寅卯辰   巳酉丑 → 亥子丑
         寅午戌 → 申酉戌   亥卯未 → 巳午未
     올해 세운 — 일간이 %(Y)s 천간(%(YE)s)을 만나 무엇이 되나
     ④장 스무 칸 = 자리 넷 × 세운 다섯. 손님은 한 칸만 받습니다.

   붙여넣기 : WPCode -> 새 스니펫 -> PHP Snippet -> 저장 -> Active
   ★ 위치(Location)를 반드시 「어디서나 실행 / Run Everywhere」로.
   ★ 크롬 번역을 끄고 붙여넣으세요.
   ════════════════════════════════════════════════════════════ */

/* ── 서버가 찍는 한 줄 — 울타리 밖입니다 ─────────────────
   조각이 켜져 있기만 하면 무조건 보입니다. 자바스크립트가 아예
   안 돌아도 보이므로, 「아무것도 안 나와요」일 때 맨 먼저 봅니다. */
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
	   . '관리자에게만 보입니다 · 삼재 조각이 켜져 있습니다 · 판 %(STAMP)s'
	   . '<br>지금 쪽 「' . esc_html( $slug ) . '」 · 우리 쪽인가 : ' . $mine
	   . '</div>';
}, 99 );

add_action( 'wp_head', function () {
	/* ★ 울타리 — 전자책 쪽에서만 내보냅니다. 없으면 홈 · 무료 쪽 ·
	   문 쪽까지 이 조각을 다 받습니다. */
	if ( ! is_page( 'reading-book' ) ) { return; }
	$stella_admin = current_user_can( 'manage_options' ) ? '1' : '';
	?>
<!-- stella 삼재 · 판 %(STAMP)s -->
%(CSS)s
<script>
(function(){
  if(window.StellaSamjae){ return; }

  var ADMIN = '<?php echo esc_js( $stella_admin ); ?>';
  var YEAR   = %(Y)s;
  var YEAR_EL= '%(YE)s';
  var GANJI  = '%(YG)s';
  var STAMP  = '%(STAMP)s';
  var GUARDIAN = '미르';
  var TOPICS = ['삼재'];

  function read(k){
    try{ var v=localStorage.getItem(k); return v?JSON.parse(v):null; }catch(e){ return null; }
  }
  function esc(s){
    /* ★ 집 규칙 — 페이지 <script> 안에 앰퍼샌드를 안 씁니다.
       꺾쇠를 실체참조로 바꾸려면 앰퍼샌드가 필요하므로, 신년운세
       조각과 같이 그냥 떼어냅니다 (카드 이름에는 꺾쇠가 안 나옵니다). */
    return String(s===undefined?'':s).split('<').join('').split('>').join('');
  }
  function two(x){ return (x<10?'0':'')+x; }

  /* ── 손님을 무엇이라 부를까 (신년운세와 같은 셈) ───────── */
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
    if(v.length>=3){ return v.slice(1); }
    return v;
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
  function headWord(v){
    var a=String(v).split(' '), i;
    for(i=0;i<a.length;i++){ if(a[i]){ return a[i]; } }
    return '';
  }
  function callName(pr){
    var f=firstOf(pr);
    if(f){ return f; }
    var raw=String(pr.name===undefined?'':pr.name);
    var v=raw.split(' ').join('');
    if(!v){ return ''; }
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
  function groupOf(myEl, el){
    if(el===myEl){ return '비겁'; }
    if(SAENG[myEl]===el){ return '식상'; }
    if(GEUK[myEl]===el){ return '재성'; }
    if(GEUK[el]===myEl){ return '관성'; }
    if(SAENG[el]===myEl){ return '인성'; }
    return '';
  }

  /* ── 삼재 셈 ──────────────────────────────────────────
     삼재는 태어난 해의 지지(띠)가 속한 삼합 무리로 정해집니다.
       申子辰(원숭이·쥐·용)  → 寅卯辰(범·토끼·용) 해
       巳酉丑(뱀·닭·소)      → 亥子丑(돼지·쥐·소) 해
       寅午戌(범·말·개)      → 申酉戌(원숭이·닭·개) 해
       亥卯未(돼지·토끼·양)  → 巳午未(뱀·말·양) 해
     ★ 열두 해에 세 해입니다. 아홉 해는 삼재가 아닙니다. */
  function branchOf(y){ return ((y - 4) %% 12 + 12) %% 12; }
  /* 지지 자리 → 삼재 첫 해의 지지 자리 */
  var FIRSTJI = {};
  (function(){
    var sets=[[8,0,4,2],[5,9,1,11],[2,6,10,8],[11,3,7,5]], i, j;
    for(i=0;i<sets.length;i++){
      for(j=0;j<3;j++){ FIRSTJI[sets[i][j]] = sets[i][3]; }
    }
  })();
  function samjaeFirst(birthY, nowY){
    var want = FIRSTJI[branchOf(birthY)];
    if(want===undefined){ return 0; }
    var y = nowY - 12;
    while(branchOf(y) !== want){ y++; }
    var cand=[y, y+12, y+24], i, pick=cand[0];
    for(i=0;i<cand.length;i++){
      pick = cand[i];
      if(nowY <= cand[i] + 3){ break; }
    }
    return pick;
  }
  /* 지금 서 있는 자리 */
  function slotOf(first, nowY){
    if(nowY === first - 1){ return 'before'; }
    if(nowY === first    ){ return 'in'; }
    if(nowY === first + 1){ return 'stay'; }
    if(nowY === first + 2){ return 'out'; }
    if(nowY === first + 3){ return 'after'; }
    return 'far';
  }
  /* ④장과 카드 장은 넷으로만 갈립니다 — 앞뒤와 먼 때는 한 칸으로 */
  function cellSlot(sl){
    if(sl==='in'){ return 'in'; }
    if(sl==='stay'){ return 'stay'; }
    if(sl==='out'){ return 'out'; }
    return 'none';
  }

  var SJ = 