# -*- coding: utf-8 -*-
"""사이트에 이미 들어간 패치 다섯을 사본에 차례로 먹여 live 상태를 되살립니다."""
import io, re, sys, subprocess, os
S='/tmp/claude-0/-home-user-kitten/c2a43b1d-0c4f-566e-ae2a-79f351d35055/scratchpad/'
PH='/home/user/kitten/wordpress/php/'
# ══ 2026-09-08 · 이 되살리기는 이제 믿으면 안 됩니다 ══════════════
# 사이트에서 「어느 쪽에 무엇이 들어갔나」(?stella_state=1)를 읽어보니
# 160 번 쪽에 자국이 서른한 개 있습니다 —
#   amp ask body box break byline dbg div ev fortune fortune2 gap2
#   head health lens lock love money name paper rope sip span3 split
#   sum tail taste tiny topics2 twice voice
# 아래 ORDER 에는 열일곱 개만 있습니다. 빠진 것 열넷 —
#   body(patch160_body20) break(sentence_break) fortune fortune2
#   health(health_topics) lens(lens_career) lock love(love_topics)
#   money(money_topics) rope(rope4) span3(life_span3)
#   topics2(career_rest2) tiny dbg(파일 없음)
# 그래서 되살린 크기 1,193,838 과 사이트의 1,211,058 이 17,220 만큼
# 다릅니다. 넣은 차례도 모릅니다.
#
# ★ 앞으로 160 번 쪽에 패치를 만들 때는 이걸로 자리를 잡지 마세요.
#   사이트에서 곧장 읽는 ?stella_look= 로 진짜 글을 보고 잡으세요.
#   (wordpress/php/patch_find.WPCODE.txt)
# ═══════════════════════════════════════════════════════════════

ORDER=['patch160_tail','patch160_split','patch160_amp','patch160_divider','patch160_name','patch160_paper','patch160_say',
       'patch160_byline','patch160_taste','patch160_evidence',
       'patch160_box','patch160_voice','patch160_ask',
       'patch160_head','patch160_sip','patch160_sum','patch160_gap2']
# 2026-09-08 · 소희 님이 넣으신 순서 그대로입니다.
#   box → voice → ask → (gap 은 ⑪ 때문에 막힘) → head → sip → sum → gap2
#   gap2 는 gap 에서 ⑪ 을 뺀 판입니다. 마지막에 들어갔는데 자리가 다 걸렸습니다.
# 2026-09-08 · byline · taste · evidence 를 더했습니다.
#   소희 님이 ?stella_today=1 을 열었더니 17 자리 가운데 셋만 걸렸는데,
#   그 셋이 전부 「제 패치를 먹고도 다시 걸리는」 자리였습니다.
#   여기에 셋을 먹이고 today 를 재보니 사이트와 똑같이 3 걸림 · 14 못찾음.
#   즉 patch160_today 는 이 셋을 묶은 것이고, 사이트에는 이미 들어가 있습니다.

src=S+'recon_in.html'
import shutil
shutil.copy('/home/user/kitten/wordpress/pages/reading-book.html', src)

for nm in ORDER:
    p=io.open(PH+nm+'.WPCODE.txt',encoding='utf-8').read()
    i=p.index("\t$jobs[] = array(")
    j=p.index("\n\n\t$apply")
    php=("<?php\n$c = file_get_contents('"+src+"');\n$jobs = array();\n"+p[i:j]+"""
$new = $c; $ok = true;
foreach ( $jobs as $j ) {
  $n = preg_match_all( $j['find'], $c );
  if ( $n > 1 ) { echo "  X " . $j['name'] . " => " . $n . "\\n"; $ok = false; }
  if ( 0 === $n ) { echo "  - 이미 들어감: " . $j['name'] . "\\n"; continue; }
  $new = preg_replace( $j['find'], str_replace( '\\\\', '\\\\\\\\', $j['to'] ), $new, 1 );
  if ( null === $new ) { echo "  STOP\\n"; exit(1); }
}
if ( ! $ok ) { exit(2); }
file_put_contents('"""+src+"""', $new);
echo strlen($c) . " -> " . strlen($new) . "\\n";
""")
    io.open(S+'_r.php','w',encoding='utf-8').write(php)
    r=subprocess.run(['php',S+'_r.php'],capture_output=True,text=True)
    print('%-20s %s' % (nm, r.stdout.strip() or r.stderr.strip()))
    if r.returncode: sys.exit(1)

shutil.move(src, S+'live_recon.html')
n=os.path.getsize(S+'live_recon.html')
print()
print('되살린 크기 :', format(n,','), '바이트')
print('바탕 : 소희 님이 넣으신 것 전부 (2026-09-08)')
print('되살린 값을 앞으로의 바탕으로 씁니다')
