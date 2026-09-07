# -*- coding: utf-8 -*-
"""사이트에 이미 들어간 패치 다섯을 사본에 차례로 먹여 live 상태를 되살립니다."""
import io, re, sys, subprocess, os
S='/tmp/claude-0/-home-user-kitten/c2a43b1d-0c4f-566e-ae2a-79f351d35055/scratchpad/'
PH='/home/user/kitten/wordpress/php/'
ORDER=['patch160_tail','patch160_split','patch160_amp','patch160_divider','patch160_name','patch160_paper','patch160_say']

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
print('사이트 크기 : 1,132,716 바이트 (paper · say 까지 적용된 값)')
print('일치' if n==1132716 else '★ 다릅니다 — 차이 %d' % (n-1132716))
