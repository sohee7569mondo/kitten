<?php
$GLOBALS['acts']=array();
function add_action($h,$f,$p=10,$a=1){ $GLOBALS['acts'][]=array($h,$f); }
function esc_html($s){ return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8'); }
function nocache_headers(){}
function is_user_logged_in(){ return true; }
function get_current_user_id(){ return 7; }
function get_userdata($id){ $o=new stdClass(); $o->user_email='sohee7569@gmail.com'; return $o; }

define('STELLA_TRIAL', false);
define('STELLA_PORTONE_SECRET','FAKEfakeFAKEfakeFAKEfakeFAKE1234');
define('STELLA_PORTONE_CHANNEL','channel-key-0000-1111-2222');
define('STELLA_UM_KAKAO_REST','0123456789abcdef0123456789abcdef');
define('STELLA_PAY_SECRET','');
define('STELLA_WELCOME_ORBS', 2);
define('STELLA_EVENT_ORBS', 1);
define('STELLA_EVENT_UNTIL','2026-12-31');
define('STELLA_PRICE_BASE', 3);
define('STELLA_PRICE_ONELINE', 0);
define('STELLA_PRICE_DEEP', 0);
define('STELLA_PRICE_FULL', 50);
define('STELLA_MAX_DEEP', 2);
define('STELLA_REF_ORBS', 5);
define('STELLA_ORB_TTL_DAYS', 365);

function stella_clean_order($body){
  $deeps = isset($body['deeps'])?(array)$body['deeps']:array();
  $deeps = array_slice($deeps,0,STELLA_MAX_DEEP);
  return array('guardian'=>$body['guardian'],'slug'=>$body['guardian_slug'],
    'topic'=>$body['topic'],'oneline'=>$body['oneline'],'memo'=>'','deeps'=>$deeps);
}
function stella_price($o){
  if(STELLA_TRIAL){ return 0; }
  $sum=(int)STELLA_PRICE_BASE;
  if(trim($o['oneline'])!==''){ $sum+=(int)STELLA_PRICE_ONELINE; }
  $sum += count($o['deeps'])*(int)STELLA_PRICE_DEEP;
  return $sum;
}
function stella_orb_balance($u){ return 20; }
function stella_orb_add($u,$n,$w){ return true; }
function stella_orb_spend($u,$n,$w){ return true; }
function stella_place_order($u,$b){ return array(); }

$_GET['stella_money']='1';
require dirname(__DIR__).'/php/patch160_money.php';
foreach($GLOBALS['acts'] as $a){ if($a[0]==='template_redirect'){ $a[1](); } }
