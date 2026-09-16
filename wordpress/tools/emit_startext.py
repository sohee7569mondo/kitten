# -*- coding: utf-8 -*-
"""스타 사주 글(판2)을 WPCode 조각으로 뽑습니다.

왜 DOM 을 고치나 —
  살아 있는 star-saju 쪽은 제 사본(pages/celeb.html)과 다릅니다.
  사본에는 「일간은 <em>癸</em>입니다」 인데 화면에는 「일간 癸 —
  이슬과 실개천」 이 나옵니다. 그래서 **앵커를 안 잡습니다.**
  그려진 뒤에 제목을 보고 그 바로 아래 문단만 갈아끼웁니다.

무엇을 건드리나 —
  제목 바로 뒤에 **잇달아 오는 <p> 만** 바꿉니다. <p> 가 아닌 것을
  만나면 멈춥니다. 오행 막대 같은 것을 지우지 않으려고요.
"""
import io, os, sys, datetime
from build_startext import read, GAN, OH, SIP

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, '..', 'php', 'patch_startext.WPCODE.txt')


def js_list(ps):
    return '[' + ','.join("'" + p + "'" for p in ps) + ']'


def js_map(d, keys):
    rows = []
    for k in keys:
        rows.append("  '%s':%s" % (k, js_list(d[k])))
    return '{\n' + ',\n'.join(rows) + '\n}'


def main():
    day, much, none, sip, probs = read()
    if probs:
        for p in probs:
            print('★ ' + p)
        sys.exit(1)

    stamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    n_par = sum(len(v) for d in (day, much, none, sip) for v in d.values())
    n_chr = sum(len(p) for d in (day, much, none, sip)
                for v in d.values() for p in v)

    head = HEAD % {'S': stamp, 'P': n_par, 'C': n_chr}
    data = ('var D_DAY  = %s;\n\nvar D_MUCH = %s;\n\nvar D_NONE = %s;\n\nvar D_SIP  = %s;\n'
            % (js_map(day, GAN), js_map(much, OH),
               js_map(none, OH), js_map(sip, SIP)))
    out = head + data + BODY   # BODY 는 치환하지 않습니다 (i % 2 가 있어 % 가 깨집니다)

    io.open(OUT, 'w', encoding='utf-8').write(out)
    print('썼습니다 : %s' % os.path.normpath(OUT))
    print('문단 %d개 · %d자 · 파일 %d바이트' % (n_par, n_chr, len(out.encode('utf-8'))))


HEAD = '''/* ════════════════════════════════════════════════════════════
   스타 사주 글 · 판 2 — 팬이 읽는 결로
   ★ 판 %(S)s   (도구가 뽑았습니다. 손으로 고치지 마세요)

   소희 님 : 「스타 사주의 내용이 너무 어렵다. 잘된 애들인데
              이래서 잘된, 이래서 인기가 좋은, 이래서 매력이
              있는 듯한 느낌이 없어」
              「인기를 얻기까지 오래 걸릴수 있지만 한번 인기를
              얻으면 오래 갑니다. 라는 식의 내용을 넣으면」

   ── 무엇이 바뀌나 ───────────────────────────────────
   일간 열 · 가장 강한 오행 다섯 · 없는 오행 다섯 · 십성 열.
   모두 서른 자리, 문단 %(P)d개 %(C)d자를 새 글로 갈아끼웁니다.

   전 : 버티는 힘이 넘칩니다. 좀처럼 안 움직여서 안전하지만,
        기회가 지나간 뒤에 결심하는 일이 잦습니다.
   후 : 인기를 얻기까지는 오래 걸렸을 수 있습니다. 대신 한번
        자리를 잡으면 잘 안 내려옵니다. 유행이 바뀌어도
        {이름}의 자리는 그대로 남습니다.
        ─ 처음부터 결승선이 다른 종목이었던 사람.

   ── 어떻게 바꾸나 (앵커를 안 잡습니다) ───────────────
   살아 있는 쪽은 제 사본과 다릅니다. 그래서 쪽 글을 찾아
   바꾸지 않고, **그려진 뒤에** 제목을 보고 그 바로 아래
   문단만 갈아끼웁니다.

       제목 바로 뒤에 **잇달아 오는 <p> 만** 바꿉니다.
       <p> 가 아닌 것을 만나면 멈춥니다.
       (오행 막대처럼 문단이 아닌 것을 안 지우려고요)

   이름은 생년월일 줄 바로 위의 제목에서 가져옵니다.

   ── 켜졌는지 보기 ───────────────────────────────────
   관리자로 보시면 결과 발치에 초록 한 줄이 뜹니다 —
   서른 자리 가운데 몇 자리를 갈았는지 세어 줍니다.
   손님에게는 안 보입니다.

   붙여넣기 : WPCode → 새 스니펫 → PHP Snippet → 저장 → Active
   ★ 위치(Location)를 반드시 「어디서나 실행 / Run Everywhere」로.
   ★ 크롬 번역을 끄고 붙여넣으세요.
   ════════════════════════════════════════════════════════════ */

add_action( 'wp_head', function () {

	if ( ! is_page( 'star-saju' ) ) { return; }
	$admin = current_user_can( 'manage_options' ) ? 1 : 0;
	?>
<!-- stella 스타 사주 글 · 판 %(S)s -->
<style id="stella-startext">
#ssx-band{
  margin:14px 0 0; padding:8px 12px; font-size:.82rem; line-height:1.6;
  border-left:3px solid #2F7D4A; background:rgba(47,125,74,.07); color:#1d3a27;
}
.ss-stkey{ font-size:1.02em; }
.ss-stkey strong{ color:#5B4A96; }
</style>
<script>
(function(){
  if(window.StellaStarText){ return; }
  window.StellaStarText = 1;

  var ADMIN = <?php echo (int) $admin; ?>;
  var STAMP = '%(S)s';

  var GAN = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'];
  var OH  = ['목','화','토','금','수'];
  var SP  = ['비견','겁재','식신','상관','편재','정재','편관','정관','편인','정인'];

'''

BODY = '''
  /* ═══ 잔심부름 ═══════════════════════════════════════ */
  function tidy(v){
    var s = String(v === null ? '' : v), out = '', i, ch;
    var SPC = ' ' + String.fromCharCode(9) + String.fromCharCode(10) + String.fromCharCode(13);
    for(i = 0; i < s.length; i++){
      ch = s.charAt(i);
      if(SPC.indexOf(ch) >= 0){ ch = ' '; }
      out += ch;
    }
    while(out.indexOf('  ') >= 0){ out = out.split('  ').join(' '); }
    return out.trim();
  }

  /* ═══ 이름 — 생년월일 줄 바로 위의 제목 ══════════════
     셀럽고와 같은 방법입니다. 쪽 구조가 바뀌어도
     「네 자리 숫자 + 년」 은 안 바뀝니다. */
  function isDateLine(t){
    if(t.length < 8){ return 0; }
    if(t.length > 44){ return 0; }
    var i, d = '0123456789';
    for(i = 0; i < 4; i++){ if(d.indexOf(t.charAt(i)) < 0){ return 0; } }
    if(t.charAt(4) !== '년'){ return 0; }
    return 1;
  }
  var NOTNAME = ['일간','가장 강','없습니다','한 글자','십성','오행',
                 '나와 이 사람','궁합','사주','생년월일'];
  function looksName(t){
    if(!t){ return 0; }
    if(t.length > 18){ return 0; }
    var i;
    for(i = 0; i < NOTNAME.length; i++){
      if(t.indexOf(NOTNAME[i]) >= 0){ return 0; }
    }
    return 1;
  }
  function isHead(el){
    var g = String(el.tagName === undefined ? '' : el.tagName).toLowerCase();
    if(g === 'h1'){ return 1; }
    if(g === 'h2'){ return 1; }
    if(g === 'h3'){ return 1; }
    if(g === 'h4'){ return 1; }
    if(g === 'h5'){ return 1; }
    return 0;
  }
  function findName(){
    try{
      var all = document.querySelectorAll('p, div, span, small, time, li'), i, el, t, n, p, tt;
      for(i = 0; i < all.length; i++){
        el = all[i];
        if(el.children.length > 0){ continue; }
        t = tidy(el.textContent);
        if(!isDateLine(t)){ continue; }
        n = el;
        var lv = 0;
        while(n){
          p = n.previousElementSibling;
          while(p){
            if(isHead(p)){
              tt = tidy(p.textContent);
              if(looksName(tt)){ return tt; }
            }
            p = p.previousElementSibling;
          }
          n = n.parentElement;
          lv++;
          if(lv > 6){ break; }
          if(!n){ break; }
          if(n === document.body){ break; }
        }
      }
    }catch(e){}
    return '';
  }

  /* ═══ 제목이 어느 자리인가 ═══════════════════════════ */
  function classify(t){
    var i;
    if(t.indexOf('일간') >= 0){
      for(i = 0; i < GAN.length; i++){
        if(t.indexOf(GAN[i]) >= 0){ return ['day', GAN[i]]; }
      }
    }
    if(t.indexOf('가장 강') >= 0){
      for(i = 0; i < OH.length; i++){
        if(t.indexOf(OH[i]) === 0){ return ['much', OH[i]]; }
      }
    }
    if(t.indexOf('없습니다') >= 0){
      for(i = 0; i < OH.length; i++){
        if(t.indexOf(OH[i]) === 0){ return ['none', OH[i]]; }
      }
    }
    for(i = 0; i < SP.length; i++){
      if(t.indexOf(SP[i]) === 0){ return ['sip', SP[i]]; }
    }
    return null;
  }

  /* ═══ 문단 하나 만들기 ═══════════════════════════════
     ** 로 싸인 데만 굵게. innerHTML 을 안 씁니다 —
     글에 홑따옴표도 앰퍼샌드도 없게 도구가 검사합니다. */
  function para(txt, nm){
    var p = document.createElement('p');
    var parts = txt.split('**'), i, s, b, bold = 0, plain = 0;
    for(i = 0; i < parts.length; i++){
      s = parts[i].split('{이름}').join(nm);
      if(!s){ continue; }
      if(i % 2){
        b = document.createElement('strong');
        b.appendChild(document.createTextNode(s));
        p.appendChild(b);
        bold++;
      } else {
        p.appendChild(document.createTextNode(s));
        plain++;
      }
    }
    /* 통째로 굵은 한 줄이면 맺음말입니다 */
    if(bold === 1){ if(plain === 0){ p.className = 'ss-stkey'; } }
    return p;
  }

  /* ═══ 갈아끼우기 ═════════════════════════════════════ */
  function swap(h, list, nm){
    if(h.getAttribute('data-sstext') === '1'){ return 0; }
    var olds = [], n = h.nextElementSibling, i;
    while(n){
      if(String(n.tagName).toLowerCase() !== 'p'){ break; }
      olds.push(n);
      n = n.nextElementSibling;
    }
    if(!olds.length){ return 0; }          /* 문단이 없으면 안 건드립니다 */
    h.setAttribute('data-sstext', '1');
    var at = olds[0];
    if(!at.parentNode){ return 0; }
    for(i = 0; i < list.length; i++){
      at.parentNode.insertBefore(para(list[i], nm), at);
    }
    for(i = 0; i < olds.length; i++){
      if(olds[i].parentNode){ olds[i].parentNode.removeChild(olds[i]); }
    }
    return 1;
  }

  var done = 0, seen = 0, lastName = '';

  function run(){
    try{
      var nm = findName();
      if(!nm){ return; }
      lastName = nm;
      var hs = document.querySelectorAll('h1, h2, h3, h4, h5'), i, h, t, k, tbl, list;
      for(i = 0; i < hs.length; i++){
        h = hs[i];
        if(h.getAttribute('data-sstext') === '1'){ continue; }
        t = tidy(h.textContent);
        k = classify(t);
        if(!k){ continue; }
        seen++;
        tbl = null;
        if(k[0] === 'day'){  tbl = D_DAY;  }
        if(k[0] === 'much'){ tbl = D_MUCH; }
        if(k[0] === 'none'){ tbl = D_NONE; }
        if(k[0] === 'sip'){  tbl = D_SIP;  }
        if(!tbl){ continue; }
        list = tbl[k[1]];
        if(!list){ continue; }
        done += swap(h, list, nm);
      }
      band();
    }catch(e){ band(String(e)); }
  }

  /* ═══ 관리자 띠 — 먼저 그려 놓고 채웁니다 ════════════ */
  function band(err){
    if(!ADMIN){ return; }
    try{
      var b = document.getElementById('ssx-band');
      if(!b){
        var hs = document.querySelectorAll('h1, h2, h3, h4, h5');
        if(!hs.length){ return; }
        var last = hs[hs.length - 1];
        b = document.createElement('p');
        b.id = 'ssx-band';
        if(last.parentNode){ last.parentNode.appendChild(b); }
      }
      var msg = '관리자에게만 보입니다 · 스타 사주 글 판 ' + STAMP
              + ' · 갈아끼운 자리 ' + done + '개 (찾은 제목 ' + seen + '개)'
              + ' · 이름 ' + (lastName ? lastName : '못 찾음');
      if(err){ msg += ' · 멈춘 까닭 ' + err; }
      b.textContent = msg;
    }catch(e){}
  }

  function start(){
    run();
    var k = 0;
    var t = setInterval(function(){
      k++;
      run();
      if(k > 240){ clearInterval(t); }
    }, 500);
  }
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', start);
  } else { start(); }
})();
</script>
	<?php
} );
'''

if __name__ == '__main__':
    main()
