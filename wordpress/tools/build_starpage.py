# -*- coding: utf-8 -*-
"""스타 사주 쪽(406) **원본**을 고칩니다 — 조각으로 덮지 않습니다.

소희 님 2026-09-16 :
  「위 너비가 안바뀌는것도 그렇고 예전에 안보이게 햇던 연애인 리스트도
   떴다가 가려지는 형식이야 그럼 전체 코딩이 무거워지지 않아?」

맞는 말씀이었습니다. 브라우저는 CSS 를 **그리기 전에**, 자바스크립트를
**그린 뒤에** 읽습니다. 조각으로 덮으면 반드시 한 번은 옛 모습이 보입니다.

이제 워드프레스로 쪽 내용을 직접 읽을 수 있게 되어(pages.get), 밖에서
덮을 까닭이 없어졌습니다. 쪽 안의 표와 그리는 자리를 곧바로 고칩니다.

이 도구가 끝나면 조각 넷이 필요 없어집니다 —
    patch_startext (34KB) · patch_starfind (27KB)
    patch_starfix (13KB)  · patch_celebgo 의 스타 쪽 부분 (36KB)
"""
import io, os, re, sys, datetime
from build_startext import read as read_star, GAN, OH, SIP

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, '..', 'pages', 'star-saju.live.html')
NEW  = os.path.join(HERE, '..', 'pages', 'star-saju.new.html')
OUT  = os.path.join(HERE, '..', 'php', 'patch_starsrc.WPCODE.txt')

EDITS = []          # (이름, 찾을 것, 바꿀 것)


def E(name, a, b):
    EDITS.append((name, a, b))


def para(ps):
    """문단 여럿을 한 덩어리로. ** 는 굵게, {이름}은 그대로 둡니다."""
    out = []
    for p in ps:
        t = ''
        bold = 0
        for i, seg in enumerate(p.split('**')):
            if i % 2:
                t += '<b>' + seg + '</b>'
                bold += 1
            else:
                t += seg
        cls = ''
        if bold == 1:
            if p.startswith('**'):
                if p.rstrip().endswith('**'):
                    cls = ' class="sr-key"'
        out.append('<p' + cls + '>' + t + '</p>')
    # 바깥에서 <p> 로 한 번 더 싸므로 첫 여는 태그와 끝 닫는 태그를 뗍니다
    joined = ''.join(out)
    joined = re.sub(r'^<p[^>]*>', '', joined)
    joined = re.sub(r'</p>$', '', joined)
    return joined


def js_map(d, keys, kor=None):
    rows = []
    for k in keys:
        rows.append("    '%s':'%s'" % (k, para(d[k])))
    return '{\n' + ',\n'.join(rows) + '\n  }'


def build():
    day, much, none, sip, probs = read_star()
    if probs:
        for p in probs:
            print('★ ' + p)
        sys.exit(1)

    whole = io.open(SRC, encoding='utf-8').read()

    # ★★ 표가 **두 번** 선언돼 있습니다 (CLAUDE.md 의 되풀이 탈).
    #   앞엣것은 전자책과 함께 쓰는 **풀이 엔진**이고,
    #   뒤엣것이 **스타 사주 화면**입니다. 뒤엣것만 고칩니다.
    MARK = '<script>\n(function(){\n  var STARS='
    if whole.count(MARK) != 1:
        print('★ 스타 사주 덩어리를 못 찾았습니다 : %d군데' % whole.count(MARK))
        sys.exit(1)
    cut = whole.index(MARK)
    head, s = whole[:cut], whole[cut:]

    # ── ① 오행 막대 다섯 줄 → 한 줄, 사주표 바로 아래 ─────────
    E('오행 한 줄 만들기',
      """    }).join('');

    var sipTxt=p.sip.map(function(s){""",
      """    }).join('');

    /* 오행은 막대 다섯 줄 대신 한 줄로 (2026-09-16) */
    var barsOne=ELS.map(function(e){
      return e+' '+(p.el[e]?p.el[e]:0);
    }).join('   ·   ');

    /* 글 안의 {이름} 을 그 사람 이름으로 */
    function fill(t){ return String(t===undefined?'':t).split('{이름}').join(esc(p.n)); }

    var sipTxt=p.sip.map(function(s){""")

    E('십성 글에 이름 넣기',
      """      return '<h3>'+t.t+'</h3><p>'+t.d+'</p>';""",
      """      return '<h3>'+t.t+'</h3><p>'+fill(t.d)+'</p>';""")

    E('오행 글에 이름 넣기',
      """    if(p.hi){ elTxt+='<h3>'+ga(p.hi)+' 가장 강합니다</h3><p>'+EL_MUCH[p.hi]+'</p>'; }
    if(p.no.length){
      elTxt+='<h3>'+eun(p.no.join('·'))+' 한 글자도 없습니다</h3>'+
        p.no.map(function(e){ return '<p>'+EL_NONE[e]+'</p>'; }).join('');
    }""",
      """    if(p.hi){ elTxt+='<h3>'+ga(p.hi)+' 가장 강합니다</h3><p>'+fill(EL_MUCH[p.hi])+'</p>'; }
    if(p.no.length){
      elTxt+='<h3>'+eun(p.no.join('·'))+' 한 글자도 없습니다</h3>'+
        p.no.map(function(e){ return '<p>'+fill(EL_NONE[e])+'</p>'; }).join('');
    }""")

    E('막대를 한 줄로 바꿔 표 아래에',
      """      '</div>'+
      knownTxt+
      '<h3>일간 '+p.g+' — '+d.image+'</h3>'+
      '<p>'+d.what+'</p><p>'+d.good+'</p><p>'+d.care+'</p>'+
      '<div class="scale">'+bars+'</div>'+""",
      """      '</div>'+
      '<div class="el1">'+barsOne+'</div>'+
      knownTxt+
      '<h3>일간 '+p.g+' — '+d.image+'</h3>'+
      '<p>'+fill(d.what)+'</p>'+""")

    # ── ② 이름만 쉰 개 늘어놓던 명단 접기 ──────────────────────
    E('같은 일간 명단 접기',
      """    var sameTxt='';
    if(same.length){
      sameTxt='<h3>일간이 같은 사람 '+same.length+'명</h3>'+""",
      """    var sameTxt='';
    if(0){      /* 2026-09-16 · 소희 님 「관심없는 내용일듯」 */
      sameTxt='<h3>일간이 같은 사람 '+same.length+'명</h3>'+""")

    # ── ③ 통계 갈래 접기 ──────────────────────────────────────
    E('얼마나 드문가 접기',
      """    var r = $('svRare');
    if(r){ r.innerHTML = srRare(p); }""",
      """    var r = $('svRare');
    if(r){ r.innerHTML = ''; }   /* 2026-09-16 · 통계는 팬이 볼 것이 아닙니다 */""")

    # ── ④ 어려운 말 한 줄 빼기 ────────────────────────────────
    E('편재·기토 줄 빼기',
      """          '<h3>나와 이 사람</h3>' +
          '<p>당신은 <b>' + me.ko + '</b>입니다. ' +
          esc(p.n) + ' 님은 당신에게 <b>' + rel + '</b>입니다.</p>' +""",
      """          '<h3>나와 이 사람</h3>' +""")

    # ── ⑤ 「내 사주로」 → 「○○ 님과 나의 궁합 보기」 ──────────
    E('궁합 단추로 바꾸기',
      """      '<a class="go" href="/door-career/">내 사주로 같은 것을 보기 →</a>'+""",
      """      '<a class="go sr-um" href="/uandme/">'+esc(p.n)+
        ' 님과 나의 궁합 보기<span>내 생일만 넣으면 됩니다 · 무료</span></a>'+""")

    # ── ⑥ 덮개가 머리글에 안 가리게 + 이름 담기 ───────────────
    E('머리글에 안 가리게 · 이름 담기',
      """    $('svSheet').className='sheet open';
    document.body.style.overflow='hidden';""",
      """    $('svSheet').className='sheet open';
    document.body.style.overflow='hidden';

    /* 유앤미로 넘길 이름을 담아 둡니다 (2026-09-16) */
    try{ localStorage.setItem('stella_celeb_go', p.n); }catch(e){}

    /* 사이트 머리글이 붙박이라 덮개 위를 덮습니다. 머리글을 재서
       그만큼 내려 줍니다 — 짐작으로 고정값을 쓰면 화면 폭에 따라
       모자라거나 남습니다. */
    try{
      var hb=0, hx=document.elementsFromPoint
        ? document.elementsFromPoint(Math.round(window.innerWidth/2),6) : [];
      for(var hi2=0; hi2<hx.length; hi2++){
        var hs=window.getComputedStyle(hx[hi2]);
        if(!hs){ continue; }
        if(hs.position!=='fixed'){ if(hs.position!=='sticky'){ continue; } }
        var hr=hx[hi2].getBoundingClientRect();
        if(hr.top>4){ continue; }
        if(hr.height<20){ continue; }
        if(hr.height>220){ continue; }
        if(hr.bottom>hb){ hb=hr.bottom; }
      }
      var cd=$('svCard');
      if(cd){
        var cr=cd.getBoundingClientRect();
        if(cr.top < hb+12){ cd.style.paddingTop=Math.round(hb+20-cr.top)+'px'; }
      }
    }catch(e){}""")

    # ── ⑦ 판2 원고를 표에 박습니다 ────────────────────────────
    #     DAY 는 what 한 칸에 다 담고, 그리는 자리에서 한 번만 씁니다
    for g in GAN:
        m = re.search(r"'" + g + r"':\{ kor:'([^']*)', image:'([^']*)',\s*\n"
                      r"\s*what:'([^']*)',\s*\n"
                      r"\s*good:'([^']*)',\s*\n"
                      r"\s*care:'([^']*)' \}", s)
        if not m:
            print('★ 일간 %s 의 칸을 못 찾았습니다' % g)
            sys.exit(1)
        E('일간 ' + g + ' 글',
          m.group(0),
          "'%s':{ kor:'%s', image:'%s',\n      what:'%s',\n      good:'', care:'' }"
          % (g, m.group(1), m.group(2), para(day[g])))

    old_much = re.search(r'var EL_MUCH=\{[\s\S]*?\n  \};', s)
    if not old_much:
        print('★ EL_MUCH 를 못 찾았습니다'); sys.exit(1)
    E('가장 강한 오행 글', old_much.group(0), 'var EL_MUCH=' + js_map(much, OH) + ';')

    old_none = re.search(r'var EL_NONE=\{[\s\S]*?\n  \};', s)
    if not old_none:
        print('★ EL_NONE 을 못 찾았습니다'); sys.exit(1)
    E('없는 오행 글', old_none.group(0), 'var EL_NONE=' + js_map(none, OH) + ';')

    for k in SIP:
        m = re.search(r"'" + k + r"':\{ t:'([^']*)',\s*\n\s*d:'([^']*)' \}", s)
        if not m:
            print('★ 십성 %s 의 칸을 못 찾았습니다' % k); sys.exit(1)
        E('십성 ' + k + ' 글', m.group(0),
          "'%s':{ t:'%s',\n      d:'%s' }" % (k, m.group(1), para(sip[k])))

    # ── ⑧ 새로 쓰는 모양 (한 줄 오행 · 맺음말 · 궁합 단추) ─────
    E('새 모양 CSS',
      """<style>
/* 2026-09-09 · 글꼴을 고딕으로, 작은 글씨를 키웁니다""",
      """<style>
/* ── 2026-09-16 · 한 줄 오행 · 맺음말 · 궁합 단추 ── */
  #ssv .el1{ margin:10px 0 18px; padding:9px 14px; border-radius:10px;
    background:rgba(94,69,166,.06); color:#5E45A6; text-align:center;
    font-size:.92rem; font-weight:700; letter-spacing:.02em; }
  #ssv .sr-key{ color:#5E45A6; font-weight:700; }
  #ssv a.go.sr-um{ display:block; box-sizing:border-box; width:100%;
    margin:22px 0 4px; padding:16px 20px; border-radius:14px; text-align:center;
    background:linear-gradient(135deg,#6B5BA8,#8E7BD0); color:#fff;
    font-weight:700; text-decoration:none; }
  #ssv a.go.sr-um span{ display:block; margin-top:5px;
    font-size:.82rem; font-weight:400; opacity:.88; }
</style>
<style>
/* 2026-09-09 · 글꼴을 고딕으로, 작은 글씨를 키웁니다""")

    # ── 적용 ──────────────────────────────────────────────────
    bad = []
    for name, a, b in EDITS:
        n = s.count(a)
        if n != 1:
            bad.append('%s : %d군데' % (name, n))
        else:
            s = s.replace(a, b, 1)
    if bad:
        print('★ 한 군데가 아닌 자리 %d :' % len(bad))
        for x in bad:
            print('   ' + x)
        sys.exit(1)

    io.open(NEW, 'w', encoding='utf-8').write(head + s)
    print('고친 쪽 : %s · %d자 (%d자 늘어남)'
          % (os.path.basename(NEW), len(head + s), len(head + s) - len(whole)))
    print('고친 자리 %d군데' % len(EDITS))
    return s


if __name__ == '__main__':
    build()


# ══════════════════════════════════════════════════════════════
#  살아 있는 쪽에 넣는 한 번짜리 조각
# ══════════════════════════════════════════════════════════════

HEAD = '''/* ════════════════════════════════════════════════════════════
   스타 사주 · **쪽 원본을 고칩니다**          판 %(S)s
   (도구가 뽑았습니다 — build_starpage.py. 손으로 고치지 마세요)

   소희 님 : 「연애인 리스트도 떴다가 가려지는 형식이야
              그럼 전체 코딩이 무거워지지 않아?」

   맞는 말씀이었습니다. 브라우저는 CSS 를 **그리기 전에**,
   자바스크립트를 **그린 뒤에** 읽습니다. 조각으로 덮으면
   반드시 한 번은 옛 모습이 보입니다.

   이제 워드프레스로 쪽 내용을 직접 읽을 수 있게 되어, 밖에서
   덮을 까닭이 없어졌습니다. 쪽 안의 표와 그리는 자리를 곧바로
   고칩니다. 깜빡임이 원천적으로 없어집니다.

   ── 이 조각이 끝나면 꺼도 되는 것 ───────────────────
       patch_startext   (34KB)  글을 덮던 것
       patch_starfind   (27KB)  리스트를 감추던 것
       patch_starfix    (13KB)  화면을 손보던 것
       patch_celebgo    (36KB)  스타 쪽 부분. ★ 유앤미 쪽에서
                                이름을 골라주는 일은 남으므로
                                **끄지 마시고** 그대로 두세요.

   ── 무엇이 바뀌나 (%(N)d군데) ────────────────────────
       · 일간 열 · 오행 열 · 십성 열의 글을 판2 원고로
       · 오행 막대 다섯 줄 → 사주표 아래 한 줄
       · 「일간이 같은 사람 N명」 이름 명단 접기
       · 「이 사람은 얼마나 드문가」 통계 접기
       · 「당신은 기토입니다 … 편재입니다」 어려운 줄 빼기
       · 「내 사주로 같은 것을 보기」 → 「○○ 님과 나의 궁합 보기」
       · 결과가 사이트 머리글에 안 가리게 (머리글을 재서 내림)

   ── 쓰는 법 ─────────────────────────────────────────
   ① 미리보기  https://stellasaju.com/?stella_starsrc=1
              한 군데라도 못 찾으면 **아무것도 안 바꿉니다.**
   ② 넣기     미리보기 화면의 「이대로 넣기」
   ③ 되돌리기  https://stellasaju.com/?stella_starsrc=1&undo=1
              넣기 직전 쪽을 그대로 되살립니다.

   붙여넣기 : WPCode → 새 스니펫 → PHP Snippet → 저장 → Active
   ★ 위치(Location)를 「어디서나 실행 / Run Everywhere」로.
   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ 파일이 큽니다. 메모장에 먼저 붙였다가 Ctrl+A 로 통째로
     옮기시면 중간에 끊길 일이 없습니다.
   ════════════════════════════════════════════════════════════ */

add_action( 'init', function () {

	if ( ! isset( $_GET['stella_starsrc'] ) ) { return; }

	header( 'Content-Type: text/html; charset=utf-8' );
	echo '<meta charset="utf-8"><body style="font:15px/1.8 system-ui;'
		. 'background:#141018;color:#eee;padding:24px;max-width:900px">';

	if ( ! current_user_can( 'manage_options' ) ) {
		echo '<h1 style="color:#ff7b7b">관리자만 볼 수 있습니다.</h1>';
		exit;
	}

	$pid = 406;
	$bak = 'stella_bak_406_src';
	$page = get_post( $pid );
	if ( ! $page ) {
		echo '<h1 style="color:#ff7b7b">쪽 406 을 못 찾았습니다.</h1>';
		exit;
	}
	/* ★★ 2026-09-16 · 줄끝 표시를 가지런히 합니다
	   살아 있는 쪽은 줄끝이 \r\n (윈도 방식)입니다. 제 쪽 도구는
	   \n 으로 읽어서, 눈에 안 보이는 한 글자 차이로 찾을 것을
	   못 찾았습니다. 먼저 \n 으로 맞춘 뒤에 고칩니다.
	   보이는 글은 하나도 안 바뀝니다. */
	$body = str_replace( array( "\r\n", "\r" ), "\n", $page->post_content );

	/* ★★ 표가 **두 번** 선언돼 있습니다 — 앞엣것은 전자책과 함께 쓰는
	   풀이 엔진이고, 뒤엣것이 스타 사주 화면입니다. 뒤엣것만 고칩니다. */
	$MARK = "<script>\n(function(){\n  var STARS=";
	$cut  = strpos( $body, $MARK );
	if ( false === $cut ) {
		echo '<h1 style="color:#ff7b7b">스타 사주 덩어리를 못 찾았습니다.</h1>';
		echo '<p>쪽이 그 사이에 바뀐 것입니다. 저에게 알려주세요.</p>';
		exit;
	}
	$head = substr( $body, 0, $cut );
	$tail = substr( $body, $cut );

	/* ── 되돌리기 ─────────────────────────────────────── */
	if ( isset( $_GET['undo'] ) ) {
		$old = get_post_meta( $pid, $bak, true );
		if ( ! $old ) {
			echo '<h1 style="color:#ff7b7b">되돌릴 것이 없습니다.</h1>';
			exit;
		}
		echo '<h1 style="color:#ffd76a">되돌리기</h1>';
		printf( '<p>지금 %%s자 → 되돌리면 %%s자</p>',
			number_format( strlen( $body ) ), number_format( strlen( $old ) ) );
		if ( ! isset( $_GET['go'] ) ) {
			echo '<p style="font-size:18px"><a style="color:#ffd76a" '
				. 'href="?stella_starsrc=1&amp;undo=1&amp;go=1">→ 이대로 되돌리기</a></p>';
			exit;
		}
		wp_update_post( array( 'ID' => $pid, 'post_content' => $old ) );
		clean_post_cache( $pid );
		echo '<h2 style="color:#7bff9b">되돌렸습니다.</h2>';
		exit;
	}

'''

FOOT = '''
	/* ── 찾아보기 ─────────────────────────────────────── */
	$go   = isset( $_GET['go'] );
	$miss = array();
	$hit  = 0;
	foreach ( $EDITS as $e ) {
		$n = substr_count( $tail, $e[1] );
		if ( 1 === $n ) { $hit++; }
		else { $miss[] = array( $e[0], $n ); }
	}

	printf( '<h1 style="color:#ffd76a">스타 사주 쪽 고치기 — %%s</h1>',
		$go ? '넣기' : '<span style="color:#9fd">미리보기 · 아무것도 안 바뀝니다</span>' );
	printf( '<p>쪽 406 · 지금 <b>%%s자</b> · 고칠 자리 <b>%%d</b>군데 가운데 '
		. '<b style="color:%%s">%%d군데</b>를 찾았습니다.</p>',
		number_format( strlen( $body ) ), count( $EDITS ),
		count( $miss ) ? '#ff7b7b' : '#7bff9b', $hit );

	if ( count( $miss ) ) {
		echo '<h2 style="color:#ff7b7b">★ 못 찾은 자리가 있어 아무것도 안 바꿉니다</h2>';
		echo '<ul style="font-size:13px">';
		foreach ( $miss as $m ) {
			printf( '<li>%%s — %%d군데</li>', esc_html( $m[0] ), $m[1] );
		}
		echo '</ul>';
		echo '<p style="color:#888">쪽이 그 사이에 바뀐 것입니다. 저에게 알려주세요 — '
			. '지금 쪽을 다시 읽어 조각을 새로 뽑겠습니다.</p>';
		exit;
	}

	/* ── 미리보기 ─────────────────────────────────────── */
	$new = $tail;
	foreach ( $EDITS as $e ) {
		$new = str_replace( $e[1], $e[2], $new );
	}
	$new = $head . $new;

	printf( '<p>고친 뒤 <b>%%s자</b> (%%+d자)</p>',
		number_format( strlen( $new ) ), strlen( $new ) - strlen( $body ) );

	echo '<table cellpadding="6" style="border-collapse:collapse;font-size:13px">';
	foreach ( $EDITS as $e ) {
		printf( '<tr><td style="color:#9fd">%%s</td><td style="color:#888">%%d자 → %%d자</td></tr>',
			esc_html( $e[0] ), strlen( $e[1] ), strlen( $e[2] ) );
	}
	echo '</table>';

	if ( ! $go ) {
		echo '<h2 style="color:#ffd76a;margin-top:22px">여기까지가 미리보기입니다.</h2>';
		echo '<p style="font-size:18px"><a style="color:#ffd76a" '
			. 'href="?stella_starsrc=1&amp;go=1">→ 이대로 넣기</a></p>';
		echo '<p style="color:#888">넣기 직전 쪽을 통째로 백업합니다. '
			. '?stella_starsrc=1&amp;undo=1 로 언제든 되돌립니다.</p>';
		exit;
	}

	/* ── 넣기 ─────────────────────────────────────────── */
	update_post_meta( $pid, $bak, $body );   /* 지금 쪽을 백업 */
	wp_update_post( array( 'ID' => $pid, 'post_content' => $new ) );
	clean_post_cache( $pid );
	if ( function_exists( 'wp_cache_flush' ) ) { wp_cache_flush(); }

	echo '<h2 style="color:#7bff9b">넣었습니다.</h2>';
	printf( '<p>백업 %%s자 · 지금 %%s자</p>',
		number_format( strlen( $body ) ), number_format( strlen( $new ) ) );
	printf( '<p style="font-size:18px"><a style="color:#ffd76a" href="%%s">→ 스타 사주 열어보기</a></p>',
		esc_url( get_permalink( $pid ) ) );
	echo '<h3 style="color:#ffd76a;margin-top:24px">이제 조각 셋을 꺼주세요</h3>';
	echo '<p><b>patch_startext</b> · <b>patch_starfind</b> · <b>patch_starfix</b><br>'
		. '세 조각이 하던 일이 쪽 안으로 들어갔습니다. 켜 두면 같은 일을 두 번 합니다.</p>';
	echo '<p style="color:#888">★ <b>patch_celebgo</b> 는 그대로 두세요 — '
		. '유앤미 쪽에서 이름을 골라주는 일이 남아 있습니다.</p>';
	echo '<p style="color:#888">이 조각도 이제 꺼두셔도 됩니다.</p>';
	exit;
}, 1 );
'''


def emit():
    build()
    stamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')

    rows = []
    for name, a, b in EDITS:
        rows.append("\t\tarray( '%s',\n\t\t\t<<<'STELLA_A'\n%s\nSTELLA_A\n\t\t\t,\n\t\t\t<<<'STELLA_B'\n%s\nSTELLA_B\n\t\t),"
                    % (name.replace("'", ''), a, b))
    php = "\t$EDITS = array(\n" + '\n'.join(rows) + "\n\t);\n"

    out = (HEAD % {'S': stamp, 'N': len(EDITS)}) + php + FOOT
    io.open(OUT, 'w', encoding='utf-8').write(out)
    print('조각 : %s · %d바이트' % (os.path.basename(OUT), len(out.encode('utf-8'))))
