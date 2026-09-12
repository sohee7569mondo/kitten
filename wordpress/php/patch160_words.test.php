<?php
function add_action($h, $f, $p = 10, $a = 1) { /* CLI 흉내 */ }
require '/home/user/kitten/wordpress/php/patch160_words.php';

$content = file_get_contents('live160.txt');
$want    = file_get_contents('live160_patched.txt');

/* 스니펫과 똑같이 줄바꿈을 되돌립니다 */
$fixnl = function ($t) { return str_replace(array("\r\n", "\r"), "\n", $t); };

$bad = false;
foreach ($STELLA_W_EDITS as $e) {
    $n = preg_match_all($fixnl($e['re']), $content);
    if ($n !== $e['n']) { printf("⚠ %-32s %s / %d\n", $e['name'], var_export($n, true), $e['n']); $bad = true; }
}
if ($bad) { exit("앵커 불일치\n"); }
echo "앵커 전부 예상대로\n";

$out = $content;
foreach ($STELLA_W_EDITS as $e) {
    $rep = $fixnl($e['rep']);
    $out = preg_replace_callback($fixnl($e['re']), function ($m) use ($rep) {
        $o = $rep;
        for ($i = count($m) - 1; $i >= 1; $i--) { $o = str_replace('\\' . $i, $m[$i], $o); }
        return $o;
    }, $out);
    if ($out === null) { exit("치환 실패: {$e['name']}\n"); }
}

printf("늘어난 바이트 : %d  (스니펫이 기대하는 값 %d)\n", strlen($out) - strlen($content), STELLA_W_GROW);
printf("본문 지문     : %s\n", substr(sha1($out), 0, 12));
printf("스니펫 기대값 : %s\n", substr(STELLA_W_SHA, 0, 12));
echo (sha1($out) === STELLA_W_SHA) ? "→ 스니펫 기대값과 일치\n" : "→ ⚠ 스니펫 기대값과 다름\n";
echo ($out === $want) ? "→ 제가 검증한 결과와 바이트 단위로 동일\n" : "→ ⚠ 검증본과 다름\n";
file_put_contents('php_out.txt', $out);
