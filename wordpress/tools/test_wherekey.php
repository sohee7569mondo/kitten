<?php
/* patch160_wherekey 검사 — 워드프레스를 흉내 내 돌려봅니다
   실행 : php wordpress/tools/test_wherekey.php                       */
$GLOBALS['acts']=array();
function add_action($h,$f,$p=10,$a=1){ $GLOBALS['acts'][]=array($h,$f); }
function esc_html($s){ return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8'); }
function nocache_headers(){}
function is_user_logged_in(){ return true; }
function current_user_can($c){ return true; }
function wp_die($m){ echo $m; exit; }

define('ABSPATH', sys_get_temp_dir().'/wk-fake/');
@mkdir(ABSPATH, 0777, true);
file_put_contents(ABSPATH.'wp-config.php',
  "<?php\ndefine('DB_NAME','x');\n"
 ."define( 'STELLA_PORTONE_SECRET', 'FAKEfakeFAKEfakeFAKEfake1234' );\n"
 ."define('WP_DEBUG', false);\n");

define('STELLA_PORTONE_SECRET','FAKEfakeFAKEfakeFAKEfake1234');
define('STELLA_PORTONE_STORE','store-0000-1111-2222-3333');
define('STELLA_PORTONE_CHANNEL','');

/* WPCode 스니펫 흉내 */
function get_posts($a){
  $s1=new stdClass(); $s1->ID=265; $s1->post_title='STELLA - 포트원 백엔드';
  $s1->post_content="<?php\n/* 여기 적어두면 스니펫 보는 사람 누구나 봅니다\n"
    ."   define('STELLA_PORTONE_SECRET', '...');\n*/\n"
    ."function stella_pay_key(\$w){ return ''; }\n";
  $s2=new stdClass(); $s2->ID=301; $s2->post_title='STELLA - 열쇠';
  $s2->post_content="<?php\ndefine( 'STELLA_PORTONE_CHANNEL', 'channel-key-aaaa-bbbb-cccc' );\n";
  return array($s1,$s2);
}
function get_post_meta($id){ return array(); }

$_GET['stella_wherekey']='1';
require dirname(__DIR__).'/php/patch160_wherekey.php';
foreach($GLOBALS['acts'] as $a){ if($a[0]==='template_redirect'){ $a[1](); } }
