<?php
/* ── 워드프레스·④번 시늉 ───────────────────────────── */
function wp_upload_dir(){ return array('basedir'=>'/tmp/ud','baseurl'=>'https://stellasaju.com/wp-content/uploads'); }
function home_url($p=''){ return 'https://stellasaju.com'.$p; }
function get_option($k,$d=''){ return $d; }
function wp_json_encode($x){ return json_encode($x); }
function wp_remote_get($u,$a=array()){ return new WP_Error(); }
function is_wp_error($x){ return $x instanceof WP_Error; }
function wp_remote_retrieve_body($r){ return ''; }
function wp_mkdir_p($d){ return @mkdir($d,0777,true); }
function add_action(){} function add_filter(){}
class WP_Error {}
$F='/tmp/fonts/';
function stella_um_font($w='jua',&$log=null){
  $m=array('num'=>'num.ttf','gothic'=>'gothic.ttf','gothicb'=>'gothicb.ttf','dodum'=>'dodum.ttf');
  $p='/tmp/fonts/'.(isset($m[$w])?$m[$w]:'gothicb.ttf');
  return file_exists($p)?$p:'';
}
function stella_um_tier($n){ return $n>=70?'좋은 궁합':'무난한 사이'; }
function stella_um_nick($n,$rel){
  return array('나무와 그늘 같은 사이','🫶','곁에 있는 것만으로 편해집니다.',
               '애쓰지 않아도 오래 갑니다.','','오래 갈 사이','🫶');
}
function stella_um_card_name($s,$r,$a,$b,$c,$n=''){ return "$s-$r-$a-$b-$c-vtest.png"; }

/* ── 가짜 세로 카드 1080x1920 (소희 님 카드 흉내) ── */
@mkdir('/tmp/ud/uandme/card',0777,true);
$tallf='/tmp/ud/uandme/card/79-lover-30-12-21-vtest.png';
if(!file_exists($tallf)){
  $t=imagecreatetruecolor(1080,1920);
  imagefilledrectangle($t,0,0,1080,1920,imagecolorallocate($t,255,255,255));
  // 연보라 원 장식
  imagefilledellipse($t,980,180,420,420,imagecolorallocatealpha($t,200,180,240,70));
  $g=stella_um_font('gothicb'); $k=stella_um_font('gothic'); $d=stella_um_font('dodum');
  $ink=imagecolorallocate($t,63,58,82); $pu=imagecolorallocate($t,107,91,168);
  if($g){
    imagefilledrectangle($t,90,120,430,185,imagecolorallocate($t,240,232,252));
    imagettftext($t,30,0,110,166,$pu,$g,'연인 궁합 · 79점');
    imagettftext($t,34,0,90,300,$pu,$g,'오래 갈 사이');
    imagettftext($t,62,0,90,390,$ink,$k,'나무와 그늘 같은 사이');
    imagettftext($t,30,0,90,490,$pu,$d,'곁에 있는 것만으로 편해집니다.');
    imagettftext($t,30,0,90,545,$pu,$d,'애쓰지 않아도 오래 갑니다.');
    // 동물 자리
    imagefilledellipse($t,380,1000,300,300,imagecolorallocate($t,222,190,160));
    imagefilledellipse($t,700,1000,300,300,imagecolorallocate($t,190,190,190));
    // 발치 알약 (맨 아래)
    imagefilledrectangle($t,230,1700,850,1790,imagecolorallocate($t,63,58,82));
    imagettftext($t,30,0,268,1758,imagecolorallocate($t,255,255,255),$g,'나도 해보기 · stellasaju.com/uandme');
  }
  imagepng($t,$tallf); imagedestroy($t);
}

/* ── 조각에서 그리는 함수만 떼어옵니다 ── */
$src=file_get_contents('/home/user/kitten/wordpress/php/patch_umog.WPCODE.txt');
foreach(array('stella_umw_name','stella_umw_wrap','stella_umw_text','stella_umw_tall','stella_umw_draw','stella_umw_sq') as $fn){
  $a=strpos($src,"if ( ! function_exists( '$fn' ) ) {");
  if($a===false){ echo "못 찾음 $fn\n"; continue; }
  $b=strpos($src,"\n}\n",$a); // 바깥 닫는 괄호 (줄머리)
  $chunk=substr($src,$a,$b-$a+3);
  eval($chunk);
}
function stella_umog_shape(){ return 'wide'; }

$p=array('sc'=>79,'rel'=>'lover','a'=>30,'b'=>12,'c'=>21);
$t0=microtime(true);
$w=stella_umw_draw($p); imagejpeg($w,'/tmp/out_wide.jpg',86); imagedestroy($w);
$t1=microtime(true);
$s=stella_umw_sq($p);  imagejpeg($s,'/tmp/out_sq.jpg',88);  imagedestroy($s);
$t2=microtime(true);
printf("가로 %s바이트 · %.0fms\n", number_format(filesize('/tmp/out_wide.jpg')), ($t1-$t0)*1000);
printf("정사각 %s바이트 · %.0fms\n", number_format(filesize('/tmp/out_sq.jpg')), ($t2-$t1)*1000);
$a=getimagesize('/tmp/out_wide.jpg'); $b=getimagesize('/tmp/out_sq.jpg');
echo "가로 {$a[0]}x{$a[1]} · 정사각 {$b[0]}x{$b[1]}\n";
