<?php
function add_action($h, $f, $p = 10, $a = 1) {}
require $argv[1];
$fixnl = function ($t) { return str_replace(array("\r\n", "\r"), "\n", $t); };
$re = $fixnl($STELLA_D_RE); $new = $fixnl($STELLA_D_NEW);
$src = file_get_contents('fixture137.js');
$n = preg_match_all($re, $src);
printf("씨앗 자리 찾은 횟수 : %d / 1\n", $n);
if ($n !== 1) { exit("앵커 불일치\n"); }
$old_len = 0;
$out = preg_replace_callback($re, function ($m) use ($new, &$old_len) { $old_len = strlen($m[0]); return $new; }, $src, 1);
printf("늘어난 바이트 : %d  (예상 %d)\n", strlen($out) - strlen($src), strlen($new) - $old_len);
if (strlen($out) - strlen($src) !== strlen($new) - $old_len) { exit("크기 불일치\n"); }
file_put_contents('fixture137_patched.js', $out);
echo "치환 OK\n";
