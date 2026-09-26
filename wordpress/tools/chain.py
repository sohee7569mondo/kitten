# -*- coding: utf-8 -*-
"""사이트 상태 위에 네 패치를 차례로 먹여 봅니다. 실제로 손님이 넣을 순서 그대로."""
import io, subprocess, shutil, sys
S='/tmp/claude-0/-home-user-kitten/c2a43b1d-0c4f-566e-ae2a-79f351d35055/scratchpad/'
PH='/home/user/kitten/wordpress/php/'
ORDER=['patch160_paper','patch160_byline','patch160_taste','patch160_evidence']
cur=S+'chain_cur.html'
shutil.copy(S+'live_recon.html', cur)
allok=True
for nm in ORDER:
    p=io.open(PH+nm+'.WPCODE.txt',encoding='utf-8').read()
    i=p.index("\t$jobs[] = array("); j=p.index("\n\n\t$apply")
    io.open(S+'_c.php','w',encoding='utf-8').write(
      "<?php\n$c = file_get_contents('"+cur+"');\n$jobs = array();\n"+p[i:j]+"""
$new=$c; $ok=true;
foreach ( $jobs as $j ) {
  $n = preg_match_all( $j['find'], $c );
  if (1 !== $n) { echo "   X ".$j['name']." => ".$n."\\n"; $ok=false; }
  $new = preg_replace( $j['find'], str_replace('\\\\','\\\\\\\\',$j['to']), $new, 1 );
  if (null === $new) { echo "   STOP\\n"; exit(2); }
}
if (!$ok) { exit(2); }
file_put_contents('"""+cur+"""', $new);
echo strlen($c)." -> ".strlen($new)."\\n";
""")
    r=subprocess.run(['php',S+'_c.php'],capture_output=True,text=True)
    out=(r.stdout+r.stderr).strip()
    mark='OK ' if r.returncode==0 else '★  '
    print('%s%-20s %s' % (mark, nm, out))
    if r.returncode: allok=False; break
if allok:
    shutil.move(cur, S+'chain_final.html')
    print('\n네 개가 이 순서로 전부 걸립니다.')
