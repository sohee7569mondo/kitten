<?php
/**
 * STELLA SAJU — 페이지 160 · 말을 손님 말로 맞추기        PATCH: WORDS-1
 * ------------------------------------------------------------------
 * 한 번만 돌리는 스니펫입니다. 돌린 뒤에는 반드시 지우세요.
 *
 * [무엇을 고치나]  열일곱 자리를 고칩니다.
 *
 *   1) 저울 소제목과 본문의 낱말을 맞춥니다
 *      소제목은 「다투고 나서, 삭이는가 붙잡는가」로 갈렸는데 본문은
 *      「사주는 함께 쪽으로…」처럼 옛 낱말을 그대로 썼습니다.
 *      이제 본문도 「사주는 붙잡는 쪽으로…」로 나갑니다.
 *      연성의 신·직성의 신 두 문만 표에 있고, 나머지 네 문은 손대지 않습니다.
 *
 *   2) 오행을 화면에 보일 때만 풀어 씁니다 — 목 → 목(나무 목)
 *      값은 절대 안 바꿉니다. 엔진이 오행을 셀 때 쓰는 열쇠말이라
 *      바꾸면 계산이 통째로 깨집니다. 보여주는 자리 아홉 곳만 감쌉니다.
 *      뒤에 붙는 조사(이에요/예요)는 원래 글자로 고르므로 그대로 맞습니다.
 *
 *   3) 「남은 저울 셋」 → 「타고난 성향과 실제 생활이 다른 부분 — 남은 셋」
 *
 *   4) 「올해 인연의 흐름」 표 밑에 달 이름 다섯 개의 뜻을 붙입니다
 *      말이 나가는 달 · 견주는 달 · 끌리는 달 · 흔들리는 달 · 기대고 싶은 달
 *
 *   5) 연성의 신 닫는 말을 쉽고 충분하게 다시 씁니다
 *
 * [미리 알아두실 것]
 *   · 1)번과 2)번은 여섯 문 전부가 지나가는 자리를 건드립니다.
 *     표에 없는 문은 원래 낱말 그대로 나가도록 해두었지만,
 *     제가 실제로 그려본 것은 연성의 신뿐입니다.
 *   · 오행 풀어쓰기는 아홉 곳에 한꺼번에 들어갑니다. 사장님이 짚어주신
 *     「인연의 별」 자리 말고 나머지 여덟 곳은 문장 모양만 확인했습니다.
 *     한 권에서 여러 번 나오면 되풀이처럼 보일 수 있습니다.
 *   · 「남은 셋」은 사장님 말씀을 그대로 옮기지 않고 조금 고쳤습니다.
 *     앞 장 제목과 거의 같아져서 두 장이 같은 제목이 되기 때문입니다.
 *
 * 넣는 곳 : WPCode → + Add Snippet → Add Your Custom Code
 *           Code Type = PHP Snippet / Location = Run Everywhere / Active
 *           (맨 윗줄 <?php 은 빼고 붙여넣으세요)
 *
 * 돌리는 법 :
 *   미리보기 (아무것도 안 고침) : /wp-admin/?stella_patch=dry
 *   진짜로 고치기               : /wp-admin/?stella_patch=go
 *   되돌리기                    : /wp-admin/?stella_patch=undo
 * ------------------------------------------------------------------
 */

defined( 'STELLA_W_PAGE' ) || define( 'STELLA_W_PAGE', 160 );
defined( 'STELLA_W_KEY' )  || define( 'STELLA_W_KEY',  'words1' );

/* 다 고치고 나면 본문이 이 모양이어야 합니다 — 제가 미리 걸어보고 잰 값입니다 */
defined( 'STELLA_W_GROW' ) || define( 'STELLA_W_GROW', 16281 );
defined( 'STELLA_W_SHA' )  || define( 'STELLA_W_SHA',  '4ad7991d3ca66c473ad9d5c4e96099ed1ce06d93' );

$STELLA_W_EDITS = array(
	array(
		'name' => <<<'NAME0'
오행 도우미 심기
NAME0,
		're'   => <<<'RE0'
~<script>\n\(function\(\)\{\n  var root=document\.getElementById\('ssb'\); if\(!root\) return;~s
RE0,
		'rep'  => <<<'REP0'
<script>
/* ═══ 오행을 화면에 보일 때만 풀어 씁니다 ═══════════════════════
   2026-08-31 · 「기운으로는 목이에요」의 목이 나무라는 걸 아는 손님은 많지 않습니다.
   목 → 목(나무 목) 처럼 풀어 씁니다. 괄호 안 마지막 글자가 원래 글자와 같아서
   뒤에 붙는 조사(이에요/예요)가 그대로 맞습니다.
   값 자체는 절대 안 바꿉니다 — 엔진이 오행을 셀 때 쓰는 열쇠말이라
   바꾸면 계산이 통째로 깨집니다. 보여줄 때만 감싸 씁니다.
   오행 낱말만으로 된 글일 때만 손대고, 아니면 받은 그대로 돌려줍니다. */
window.stellaEl=(function(){
  var W={ '목':'나무 목', '화':'불 화', '토':'흙 토', '금':'쇠 금', '수':'물 수' };
  var ONLY=/^[목화토금수](·[목화토금수])*$/;
  return function(v){
    var s=(v==null)?'':String(v);
    if(!ONLY.test(s)){ return v; }
    return s.split('·').map(function(c){ return c+'('+W[c]+')'; }).join('·');
  };
})();
</script>
<script>
(function(){
  var root=document.getElementById('ssb'); if(!root) return;
REP0,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME1'
저울 이름표 심기
NAME1,
		're'   => <<<'RE1'
~  function gapBlock\(key, title\)\{~s
RE1,
		'rep'  => <<<'REP1'

/* ═══ 저울 양쪽의 이름도 그 문의 말로 ═══════════════════════════
   2026-08-31 · 소제목은 AXIS_TITLE 로 쉬운 말로 갈렸는데 본문은 원래 낱말
   (혼자·함께·실물·무형…)을 그대로 써서, 손님 눈에 소제목과 본문이 딴 소리로
   보였습니다. 아래 표로 본문에 나오는 이름도 소제목과 같은 말로 맞춥니다.
   없는 문·없는 축은 원래 이름을 그대로 씁니다. */
  var AXIS_SIDE={
    'door-career':{
      solo:{ '혼자':'혼자 파고드는 일', '함께':'사람과 굴리는 일' },
      form:{ '실물':'손에 잡히는 것을 만드는', '무형':'안 보이는 것을 다루는' },
      many:{ '하나':'하나를 깊게 파는', '여럿':'여러 개를 굴리는' },
      risk:{ '안정':'자리를 지키는', '변화':'판을 흔드는' },
      make:{ '정답':'정해진 답을 지키는', '창조':'없던 답을 만드는' }
    },
    'door-love':{
      solo:{ '혼자':'삭이는', '함께':'붙잡는' },
      form:{ '실물':'물질로 해주는', '무형':'말로 표현해 주는' },
      many:{ '하나':'한 사람만 보는', '여럿':'마음이 여러 갈래인' },
      risk:{ '안정':'편안한 사이', '변화':'긴장이 도는 사이' },
      make:{ '정답':'남들 하는 대로 가는', '창조':'나만의 방식을 찾는' }
    }
  };
  /* 같은 문 안에서도 주제마다 말이 달라야 하는 자리 — AXIS_TITLE_TOPIC 과 짝을 맞춥니다 */
  var AXIS_SIDE_TOPIC={
    '결혼운':{
      risk:{ '안정':'편안한 결혼', '변화':'긴장이 도는 결혼' },
      make:{ '정답':'남들처럼 사는', '창조':'남들과 다르게 사는' }
    },
    '취업운':{
      risk:{ '안정':'안정된 곳', '변화':'도전적인 곳' },
      make:{ '정답':'정해진 스펙대로 준비하는', '창조':'나만의 강점을 새로 만드는' }
    },
    '직장운':{
      risk:{ '안정':'지금 자리를 지키는', '변화':'안에서 판을 흔드는' },
      make:{ '정답':'정해진 역할을 지키는', '창조':'없던 역할을 만들어가는' }
    },
    '이직운':{
      risk:{ '안정':'검증된 곳으로 옮기는', '변화':'낯선 곳에 걸어보는' },
      make:{ '정답':'비슷한 일을 이어가는', '창조':'완전히 다른 일로 건너가는' }
    },
    '퇴사운':{
      risk:{ '안정':'자리를 비워두고 쉬는', '변화':'바로 다른 판을 벌이는' },
      make:{ '정답':'해오던 대로 정리하는', '창조':'새로운 판을 짜는' }
    },
    '사업운':{
      risk:{ '안정':'안정적으로 확장하는', '변화':'크게 승부를 보는' },
      make:{ '정답':'검증된 방식을 따르는', '창조':'없던 방식을 만드는' }
    },
    '재물운':{
      risk:{ '안정':'모아두는', '변화':'굴리는' },
      make:{ '정답':'정해진 곳에 넣는', '창조':'새로운 곳을 찾아 넣는' }
    }
  };
  function sideWord(key, name){
    var t=AXIS_SIDE_TOPIC[topic];
    if(t){ if(t[key]){ if(t[key][name]){ return t[key][name]; } } }
    var m=AXIS_SIDE[slug];
    if(!m){ return name; }
    if(!m[key]){ return name; }
    return m[key][name] || name;
  }

  function gapBlock(key, title){
REP1,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME2'
사주는 ○○ 쪽으로 (손님 말 글이 있을 때)
NAME2,
		're'   => <<<'RE2'
~'<p>사주는 <em>'\+A\.name\+'</em> 쪽으로 '\+tiltWord\(d\)~s
RE2,
		'rep'  => <<<'REP2'
'<p>사주는 <em>'+sideWord(key,A.name)+'</em> 쪽으로 '+tiltWord(d)
REP2,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME3'
사주가 ○○ 쪽으로 (옛 글일 때)
NAME3,
		're'   => <<<'RE3'
~'<p>사주가 <em>'\+A\.name\+'</em> 쪽으로 '\+A\.a\+' 대 '~s
RE3,
		'rep'  => <<<'REP3'
'<p>사주가 <em>'+sideWord(key,A.name)+'</em> 쪽으로 '+A.a+' 대 '
REP3,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME4'
결국 ○○ 쪽을 가운데 두고
NAME4,
		're'   => <<<'RE4'
~결국 <em>'\+A\.name\+'</em> 쪽을 가운데 두고~s
RE4,
		'rep'  => <<<'REP4'
결국 <em>'+sideWord(key,A.name)+'</em> 쪽을 가운데 두고
REP4,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME5'
타고난 결은 ○○ 쪽인데
NAME5,
		're'   => <<<'RE5'
~'<p>타고난 결은 '\+A\.name\+' 쪽인데 지금은 '~s
RE5,
		'rep'  => <<<'REP5'
'<p>타고난 결은 '+sideWord(key,A.name)+' 쪽인데 지금은 '
REP5,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME6'
답해주신 쪽 이름 (otherName)
NAME6,
		're'   => <<<'RE6'
~function otherName\(key, side\)\{\n    var A=R\.AXES\[key\];\n    return side==='A' \? A\.A : A\.B;\n  \}~s
RE6,
		'rep'  => <<<'REP6'
function otherName(key, side){
    var A=R.AXES[key];
    /* 2026-08-31 · 답해주신 쪽 이름도 소제목과 같은 말로 */
    return sideWord(key, side==='A' ? A.A : A.B);
  }
REP6,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME7'
저울 둘째 장 머리말
NAME7,
		're'   => <<<'RE7'
~'<h2>남은 저울 셋</h2>'~s
RE7,
		'rep'  => <<<'REP7'
'<h2>타고난 성향과 실제 생활이 다른 부분 — 남은 셋</h2>'
REP7,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME8'
기운으로는 · 인연의 별 목록
NAME8,
		're'   => <<<'RE8'
~'기운으로는 <em>' \+ elList\.join\('·'\) \+ '</em>입니다\.</p>'~s
RE8,
		'rep'  => <<<'REP8'
'기운으로는 <em>' + stellaEl(elList.join('·')) + '</em>입니다.</p>'
REP8,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME9'
기운으로는 · 인연의 별 한 줄
NAME9,
		're'   => <<<'RE9'
~'기운으로는 <em>' \+ elList\.join\('·'\) \+ '</em>' \+ iyeyo\(elList\[elList\.length - 1\]\)~s
RE9,
		'rep'  => <<<'REP9'
'기운으로는 <em>' + stellaEl(elList.join('·')) + '</em>' + iyeyo(elList[elList.length - 1])
REP9,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME10'
기운으로는 · 올해의 기운 (T.syEl)
NAME10,
		're'   => <<<'RE10'
~기운으로는 '\+T\.syEl\+'입니다\. ~s
RE10,
		'rep'  => <<<'REP10'
기운으로는 '+stellaEl(T.syEl)+'입니다. 
REP10,
		'n'    => 3,
	),
	array(
		'name' => <<<'NAME11'
기운으로는 · 올해의 기운 (syEl)
NAME11,
		're'   => <<<'RE11'
~기운으로는 '\+syEl\+'입니다\. ~s
RE11,
		'rep'  => <<<'REP11'
기운으로는 '+stellaEl(syEl)+'입니다. 
REP11,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME12'
기운으로는 · 일간과 몸
NAME12,
		're'   => <<<'RE12'
~기운으로는 '\+dayEl\+'입니다\. ~s
RE12,
		'rep'  => <<<'REP12'
기운으로는 '+stellaEl(dayEl)+'입니다. 
REP12,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME13'
기운으로는 · 일지와 배우자
NAME13,
		're'   => <<<'RE13'
~기운으로는 '\+R\.josa\(iljiEl,'이에요','예요'\)\+'\.</p>'~s
RE13,
		'rep'  => <<<'REP13'
기운으로는 '+stellaEl(iljiEl)+(R.hasBatchim(iljiEl)?'이에요':'예요')+'.</p>'
REP13,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME14'
기운으로는 · 달자리
NAME14,
		're'   => <<<'RE14'
~기운으로는 <em>'\+dayEl\+'</em>'\+\n      \(batchim\(dayEl\)\?'이었습니다':'였습니다'\)~s
RE14,
		'rep'  => <<<'REP14'
기운으로는 <em>'+stellaEl(dayEl)+'</em>'+
      (batchim(dayEl)?'이었습니다':'였습니다')
REP14,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME15'
달 이름 풀이 붙이기
NAME15,
		're'   => <<<'RE15'
~(push :\{ tag:'흔들리는 달' \}.*?)('<p class=\"mini\">절기 기준입니다)~s
RE15,
		'rep'  => <<<'REP15'
\1'<h3>달 이름이 뜻하는 것</h3>'+
      '<p><em>말이 나가는 달</em> — 내가 먼저 마음을 내보내는 달입니다. 연락도, 미뤄둔 말도 이때 잘 나갑니다.</p>'+
      '<p><em>견주는 달</em> — 남의 관계와 내 관계를 자꾸 견주게 되는 달입니다. 비교가 마음을 갉습니다.</p>'+
      '<p><em>끌리는 달</em> — 사람이 눈에 들어오는 달입니다. 만남이 늘고 마음이 먼저 갑니다.</p>'+
      '<p><em>흔들리는 달</em> — 밖에서 오는 일이 마음을 흔드는 달입니다. 급하게 답하지 않는 것이 유일한 방패예요.</p>'+
      '<p><em>기대고 싶은 달</em> — 마음이 안으로 들어가는 달입니다. 새로 벌이기보다 쉬고 정리하기 좋습니다.</p>'+
      \2
REP15,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME16'
연성의 신 닫는 말
NAME16,
		're'   => <<<'RE16'
~last:'붙잡을지 놓을지 모르겠다면, 그 사람과 있을 때의 당신이 마음에 드는지를 보세요\. 답은 상대가 아니라 거기에 있습니다\.'~s
RE16,
		'rep'  => <<<'REP16'
last:'붙잡을지 놓을지 아직 모르겠다면, 그 사람이 어떤 사람인지를 따지는 대신 이렇게 해보세요. 그 사람과 함께 있을 때의 내 모습을 떠올려 보는 겁니다. 그때의 내가 마음에 드는지, 아니면 자꾸 작아지고 눈치를 보고 있는지. 상대가 좋은 사람인가를 재는 것보다 그 답이 훨씬 정확합니다. 답은 그 사람에게 있는 것이 아니라, 처음부터 거기에 있었습니다.'
REP16,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME17'
접는 상자 CSS
NAME17,
		're'   => <<<'RE17'
~#ssb \.foldbtn:hover\{ background:var\(--gold\); color:#0B0817; \}~s
RE17,
		'rep'  => <<<'REP17'
#ssb .foldbtn:hover{ background:var(--gold); color:#0B0817; }
/* 2026-08-31 · 한 장 안에서 접는 상자. 누구에게나 같은 안내글을 기본으로 접어둡니다.
   자바스크립트 없이 브라우저가 스스로 여닫습니다. 인쇄할 때는 펼쳐서 나갑니다. */
#ssb details.readfold{
  border:1px solid var(--rule); border-radius:14px;
  background:rgba(28,21,51,.5); padding:0 24px; margin:26px 0 0;
}
#ssb details.readfold>summary{
  list-style:none; cursor:pointer; padding:18px 0;
  font-family:var(--serif); font-size:1.02rem; color:var(--gold-lite);
}
#ssb details.readfold>summary::-webkit-details-marker{ display:none; }
#ssb details.readfold>summary::after{ content:'  펼쳐 보기 ↓'; color:var(--dim); font-size:.9rem; }
#ssb details.readfold[open]>summary::after{ content:'  접어 두기 ↑'; }
#ssb details.readfold[open]{ padding-bottom:16px; }
#ssb details.readfold>summary:focus-visible{ outline:2px solid var(--gold); outline-offset:3px; }
@media print{ #ssb details.readfold>summary{ display:none; } }
REP17,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME18'
다섯 저울을 읽는 법 접기
NAME18,
		're'   => <<<'RE18'
~('<h3>다섯 저울을 읽는 법</h3>'\+)(.*?)(, null, 'two'\);)~s
RE18,
		'rep'  => <<<'REP18'
'<details class=\"readfold\"><summary>다섯 저울을 읽는 법</summary>'+\2+'</details>'\3
REP18,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME19'
배우자 고르는 대목
NAME19,
		're'   => <<<'RE19'
~'<p>마음을\ 여러\ 곳에\ 두지\ 마세요\.\ <em>고르는\ 일보다\ 고르지\ 않기로\ 하는\ 일</em>이\ '\
\ \ \ \ \ \ \ \ \ \ \+\ esc\(mate\)\ \+\ '을\ 고르는\ 데는\ 더\ 중요합니다\.</p>';~s
RE19,
		'rep'  => <<<'REP19'
'<p>마음을 여러 곳에 나누어 두기보다, 결혼을 결정한 뒤에는 한 사람에게 마음의 방향을 모으는 것이 중요합니다. '
          /* 2026-08-31 · mate 는 「남편」 또는 「아내」 — 조사를 받침에 맞춰 고릅니다 */
          + esc(mate) + ((mate.charCodeAt(mate.length-1)-0xAC00)%28 ? '을' : '를')
          + ' 고르는 일에서는 누구를 선택하느냐만큼, 선택한 사람에게 집중하기로 하는 것도 중요합니다.</p>';
REP19,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME20'
달 표는 해마다 되풀이됨을 밝힘
NAME20,
		're'   => <<<'RE20'
~var\ out\ =\ '<p>'\ \+\ w\.lead\ \+\ '</p>';~s
RE20,
		'rep'  => <<<'REP20'
var out = '<p>' + w.lead + '</p>'
      /* 2026-08-31 · 「올해 8월인가?」 하고 읽으신 분이 계셔서 못 박아 둡니다.
         monthGrade 는 태어난 날의 글자(일지) 하나만 봅니다. 그 해의 글자는
         전혀 안 들어가므로, 이 표는 해마다 똑같이 되풀이됩니다. */
      + '<p>여기 적힌 달은 <em>올해만의 이야기가 아닙니다.</em> 태어난 날의 글자와 그 달의 글자가 만나는 방식으로 갈리는 것이라, 내년에도 그 다음 해에도 같은 달이 같은 자리에 옵니다. 절기 기준이라 달력의 1일이 아니라 절기가 드는 날에 바뀝니다.</p>';
REP20,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME21'
맺음말 · 결은 ○○ 쪽입니다
NAME21,
		're'   => <<<'RE21'
~class="kt">결은\ '\+\(leaned\ \?\ leanAxis\.name\+'\ 쪽입니다'~s
RE21,
		'rep'  => <<<'REP21'
class="kt">결은 '+(leaned ? sideWord(leanKey, leanAxis.name)+' 쪽입니다'
REP21,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME22'
맺음말 · 가장 크게 기운 저울
NAME22,
		're'   => <<<'RE22'
~'여덟\ 글자에서\ 가장\ 크게\ 기운\ 저울은\ <em>'\+AXNAME\[leanKey\]\+'</em>였습니다\.\ '\+\
\ \ \ \ \ \ \ \ \ \ \ \ '당신은\ 아무런\ 기준\ 없이\ 처음부터\ 새로운\ 답을\ 만들어가기보다,\ '\+leanAxis\.say\+'\ 쪽으로\ 나올\ 때\ 마음이\ 더\ 편한\ 사람이에요\.</p>'\+~s
RE22,
		'rep'  => <<<'REP22'
'여덟 글자에서 가장 크게 기운 저울은 <em>'+axTitle(leanKey, AXNAME[leanKey])+'</em>였습니다. '+
            /* 2026-08-31 · saySide 값이 모두 「…쪽」으로 끝나 옛 문장에 넣으면 「쪽 쪽으로」가 됩니다 */
            '당신은 <em>'+saySide(leanKey)+'</em>'+(R.hasBatchim(saySide(leanKey))?'이에요':'예요')+'.</p>'+
REP22,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME23'
맺음말 · 어긋난 자리 목록
NAME23,
		're'   => <<<'RE23'
~gapKeys\.map\(function\(k\)\{\ return\ AXNAME\[k\];\ \}\)~s
RE23,
		'rep'  => <<<'REP23'
gapKeys.map(function(k){ return axTitle(k, AXNAME[k]); })
REP23,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME24'
맺음말 주제별 표 심기
NAME24,
		're'   => <<<'RE24'
~\ \ var\ closeHtml='';~s
RE24,
		'rep'  => <<<'REP24'
  /* ═══ 맺음말도 주제마다 ═══════════════════════════════════════
     2026-08-31 · 「○○님께」와 마지막 배웅 한 줄이 가디언 단위로만 있어서
     결혼운으로 물으나 연애운으로 물으나 똑같은 글이 나갔습니다.
     주제별 글이 있으면 그것을 쓰고, 없으면 가디언 글로 갑니다. */
  var CLOSE_TOPIC={
    '결혼운':[
      '결혼은 사람을 고르는 일 같지만, 실은 매일 다시 고르는 일에 가깝습니다. 한 번 정하고 끝나는 것이 아니라 아침마다 같은 사람을 다시 택하는 일이에요.',
      '여기까지 걸어오면서 당신이 어떤 자리에서 편안하고 어떤 자리에서 유난히 힘이 드는지를 봤습니다. 결혼생활은 그 두 가지가 매일 부딪히는 곳입니다.',
      '이 책을 읽었다고 결혼이 쉬워지지는 않습니다. 다만 힘든 날에 「내가 부족해서인가」 대신 「여기는 원래 나한테 두 배로 드는 자리지」 하고 넘어가실 수 있어요. 그거면 충분합니다.'
    ],
    '연애운':[
      '사랑은 마음의 문제 같지만 습관의 문제이기도 합니다. 어떤 사람에게 끌리는지, 다투면 어떻게 하는지는 대개 몸에 먼저 새겨져 있어요.',
      '여기까지 걸어오면서 당신이 사랑을 어떻게 하는 사람인지를 봤습니다. 어디서 마음이 편해지고 어디서 자꾸 걸리는지도요.',
      '결을 안다고 연애가 쉬워지지는 않습니다. 다만 같은 자리에서 또 걸렸을 때, 그것이 내가 못나서가 아니라는 것은 아시게 될 거예요.'
    ],
    '재회운':[
      '다시 만나는 일은 처음 만나는 일보다 어렵습니다. 두 사람 다 그때 왜 끝났는지를 알면서도 모르는 척해야 하니까요.',
      '여기까지 걸어오면서 당신이 그 관계에서 어디에 걸렸는지를 봤습니다. 다시 만난다면 걸릴 자리도 대개 같은 곳입니다.',
      '이 책이 다시 만날지 말지를 정해주지는 않습니다. 다만 다시 만난다면 무엇을 다르게 해야 하는지는 적어두었어요.'
    ],
    '이별운':[
      '이별은 사건이 아니라 기간입니다. 헤어진 날 하루로 끝나는 것이 아니라, 그 뒤로 한참을 두고 천천히 끝납니다.',
      '여기까지 걸어오면서 당신이 어떻게 마음을 정리하는 사람인지를 봤습니다. 회복이 빠른 사람도 느린 사람도 있고, 그것은 마음의 크기와 아무 상관이 없어요.',
      '이 책이 덜 아프게 해드리지는 못합니다. 다만 지금 아픈 것이 이상한 일이 아니라는 것, 그리고 이 기간에 끝이 있다는 것은 말씀드릴 수 있습니다.'
    ],
    '짝사랑':[
      '짝사랑이 힘든 것은 마음이 커서가 아니라 그 마음을 둘 자리가 없어서입니다. 주지도 못하고 거두지도 못한 채로 계속 들고 있어야 하니까요.',
      '여기까지 걸어오면서 당신이 어떤 사람에게 마음이 가는지, 그 마음을 어떻게 다루는 사람인지를 봤습니다.',
      '이 책이 그 사람의 마음을 알려주지는 못합니다. 그건 제가 알 수 없어요. 다만 당신의 마음이 지금 어디에 서 있는지는 적어두었습니다.'
    ]
  };
  var LAST_TOPIC={
    '결혼운':'결혼을 앞두고 망설여진다면, 그 사람이 좋은 사람인지를 따지기 전에 그 사람과 함께 있을 때의 내가 마음에 드는지를 먼저 보세요. 평생 같이 사는 것은 그 사람이 아니라, 그 사람 곁에 있는 나입니다.',
    '연애운':'이 사람이 맞는 사람인지 모르겠다면, 그 사람이 어떤 사람인지 재는 대신 그 사람과 있을 때의 내가 마음에 드는지를 보세요. 답은 그 사람에게 있는 것이 아니라 늘 거기에 있었습니다.',
    '재회운':'다시 만나고 싶은 것이 그 사람인지, 아니면 그 사람과 함께이던 시절의 나인지 한 번 나누어 생각해보세요. 둘은 자주 겹쳐 보이지만 같은 것이 아닙니다.',
    '이별운':'지금 잘 지내고 있는지 스스로에게 묻지 마세요. 오늘 하루를 지나오셨으면 그것으로 된 겁니다. 잘 지내는지는 다 지나고 나서 물어도 늦지 않습니다.',
    '짝사랑':'고백할지 말지를 정하기 전에, 답을 듣지 못한 채로 얼마나 더 있을 수 있는지를 먼저 헤아려 보세요. 고백은 그 사람의 답을 얻는 일이면서, 내 마음을 내려놓는 일이기도 합니다.'
  };
  function closeOf(){
    if(slug==='door-love'){ if(CLOSE_TOPIC[topic]){ return CLOSE_TOPIC[topic]; } }
    return g.close;
  }
  function lastOf(){
    if(slug==='door-love'){ if(LAST_TOPIC[topic]){ return LAST_TOPIC[topic]; } }
    return g.last;
  }

  var closeHtml='';
REP24,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME25'
맺음말 · 주제별 글 쓰기
NAME25,
		're'   => <<<'RE25'
~\ \ if\(typeof\ g\.close\ ===\ 'string'\)\{\ closeHtml='<p\ class="lead">'\+g\.close\+'</p>';\ \}\
\ \ else\ \{\ for\(var\ gci=0;\ gci<g\.close\.length;\ gci\+\+\)\{\ closeHtml\+='<p\ class="lead">'\+g\.close\[gci\]\+'</p>';\ \}\ \}~s
RE25,
		'rep'  => <<<'REP25'
  var __cl=closeOf();
  if(typeof __cl === 'string'){ closeHtml='<p class="lead">'+__cl+'</p>'; }
  else { for(var gci=0; gci<__cl.length; gci++){ closeHtml+='<p class="lead">'+__cl[gci]+'</p>'; } }
REP25,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME26'
배웅 · 주제별 마지막 한 줄
NAME26,
		're'   => <<<'RE26'
~'오르막을\ 가더라도,\ 오르막인\ 줄\ 알고\ 가면\ 덜\ 억울합니다\.</p>'\+\
\ \ \ \ \ \ '<div\ class="fw\-last">'\+g\.last\+'</div>'\+~s
RE26,
		'rep'  => <<<'REP26'
'오르막을 가더라도, 오르막인 줄 알고 가면 덜 억울합니다.</p>'+
      '<div class="fw-last">'+lastOf()+'</div>'+
REP26,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME27'
타로 잇는 문장 표 심기
NAME27,
		're'   => <<<'RE27'
~\ \ \ \ var\ talk\ =\ '';~s
RE27,
		'rep'  => <<<'REP27'
    /* ═══ 카드와 물으신 것을 잇는 한 줄 ═══════════════════════════
       2026-08-31 · 카드 글은 스물두 장이든 일흔여덟 장이든 「그 카드가 무슨 뜻인가」
       만 말합니다. 손님이 무엇을 물었는지는 모릅니다. 그래서 결혼운으로 물어도
       일반론처럼 읽혔어요. 카드 글은 그대로 두고, 그 자리에서 어떻게 읽으라는
       한 줄만 뒤에 붙입니다. 주제 다섯 × 자리 셋 = 열다섯 줄. */
    var CARD_BRIDGE={
      '결혼운':{
        now :'결혼운을 물으신 자리에서 이 카드는 <em>지금 두 분 사이가 어디쯤 와 있는지</em>를 말합니다. 좋고 나쁨이 아니라 놓인 자리예요.',
        over:'결혼으로 가는 길에서 <em>지금 걸려 있는 것</em>입니다. 상대가 문제일 때보다, 두 사람이 아직 꺼내지 않은 이야기일 때가 많습니다.',
        then:'그것을 넘고 나면 결혼 이야기가 어떤 모양이 되는지입니다. <em>하느냐 마느냐</em>가 아니라 <em>어떤 결혼이 되느냐</em>에 가깝습니다.'
      },
      '연애운':{
        now :'연애운을 물으신 자리에서 이 카드는 <em>지금 이 관계가 놓여 있는 자리</em>를 말합니다.',
        over:'지금 이 관계에서 <em>걸려 있는 것</em>입니다. 상대의 몫일 수도 있고, 내가 관계마다 되풀이하는 습관일 수도 있어요.',
        then:'그 걸림을 지나면 이 관계가 닿는 곳입니다. 정해진 결말이 아니라 <em>지금 방향의 끝</em>입니다.'
      },
      '재회운':{
        now :'재회운을 물으신 자리에서 이 카드는 <em>끝난 뒤 지금 두 사람이 서 있는 자리</em>를 말합니다.',
        over:'다시 만나려면 <em>넘어야 할 것</em>입니다. 헤어진 이유가 아직 그대로라면 대개 여기에 나옵니다.',
        then:'그것을 넘었을 때 이 관계가 닿는 곳입니다. 다시 만나는 것이 <em>곧 예전으로 돌아가는 것은 아닙니다.</em>'
      },
      '이별운':{
        now :'이별운을 물으신 자리에서 이 카드는 <em>지금 당신이 이별의 어느 지점에 있는지</em>를 말합니다.',
        over:'이 이별에서 <em>아직 넘지 못한 것</em>입니다. 그 사람이 아니라 내 안에 남아 있는 것일 때가 많습니다.',
        then:'그것을 넘고 나면 오는 자리입니다. <em>잊는 것</em>이 아니라, 들고 다녀도 무겁지 않아지는 자리에 가깝습니다.'
      },
      '짝사랑':{
        now :'짝사랑을 물으신 자리에서 이 카드는 <em>지금 이 마음이 놓여 있는 자리</em>를 말합니다.',
        over:'이 마음이 지금 <em>걸려 있는 곳</em>입니다. 그 사람의 마음보다 내 쪽에 있는 것일 때가 많아요.',
        then:'그것을 넘고 나면 이 마음이 닿는 곳입니다. <em>이루어지느냐 아니냐</em>보다 이 마음이 어디로 가느냐에 가깝습니다.'
      }
    };
    function bridgeOf(key){
      if(slug!=='door-love'){ return ''; }
      var m=CARD_BRIDGE[topic];
      if(!m){ return ''; }
      if(!m[key]){ return ''; }
      return '<p>'+m[key]+'</p>';
    }

    var talk = '';
REP27,
		'n'    => 1,
	),
	array(
		'name' => <<<'NAME28'
타로 · 카드마다 잇는 한 줄
NAME28,
		're'   => <<<'RE28'
~\ \ \ \ \ \ \ \ \+\ '\ —\ '\ \+\ sayOf\(mm,\ SLOT3\[q\]\.key\)\ \+\ '</p>';~s
RE28,
		'rep'  => <<<'REP28'
        + ' — ' + sayOf(mm, SLOT3[q].key) + '</p>'
        + bridgeOf(SLOT3[q].key);
REP28,
		'n'    => 1,
	),
);


/* ------------------------------------------------------------------
 * 아래는 손대지 않으셔도 됩니다.
 * ---------------------------------------------------------------- */

add_action( 'admin_init', function () use ( $STELLA_W_EDITS ) {

	if ( ! isset( $_GET['stella_patch'] ) || ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$mode     = sanitize_key( wp_unslash( $_GET['stella_patch'] ) );
	$page_id  = (int) STELLA_W_PAGE;
	$done_opt = 'stella_patch_' . STELLA_W_KEY . '_done';
	$back_opt = 'stella_patch_' . STELLA_W_KEY . '_backup';
	$log      = array();

	$say = function ( $lines, $ok = true ) {
		add_action( 'admin_notices', function () use ( $lines, $ok ) {
			printf(
				'<div class="notice notice-%s"><p><strong>스텔라 패치 · 말 맞추기</strong></p><pre style="white-space:pre-wrap;margin:0">%s</pre></div>',
				$ok ? 'success' : 'error',
				esc_html( implode( "\n", $lines ) )
			);
		} );
	};

	global $wpdb;
	$row = $wpdb->get_row( $wpdb->prepare(
		"SELECT ID, post_content FROM {$wpdb->posts} WHERE ID = %d", $page_id ) );
	if ( ! $row ) {
		$say( array( "페이지 {$page_id} 을(를) 찾지 못했습니다." ), false );
		return;
	}
	$content = $row->post_content;

	/* ---- 되돌리기 ---- */
	if ( 'undo' === $mode ) {
		$backup = get_option( $back_opt );
		if ( ! is_string( $backup ) || '' === $backup ) {
			$say( array( '되돌릴 내용이 없습니다.' ), false );
			return;
		}
		$wpdb->update( $wpdb->posts, array(
			'post_content'      => $backup,
			'post_modified'     => current_time( 'mysql' ),
			'post_modified_gmt' => current_time( 'mysql', 1 ),
		), array( 'ID' => $page_id ) );
		clean_post_cache( $page_id );
		delete_option( $done_opt );
		$say( array( '고치기 전 내용으로 되돌렸습니다.',
			'되돌린 크기 : ' . number_format( strlen( $backup ) ) . ' 바이트',
			'호스팅 → 성능 → 캐시 비우기 를 눌러주세요.' ) );
		return;
	}

	$dry = ( 'go' !== $mode );

	if ( get_option( $done_opt ) ) {
		$say( array( '이 패치는 이미 돌렸습니다 (' . get_option( $done_opt ) . ').',
			'다시 돌리려면 먼저 ?stella_patch=undo 로 되돌리세요.' ) );
		return;
	}

	/* ---- 고칠 자리가 하나씩 다 있는지 먼저 셉니다 ---- */
	$bad = false;
	foreach ( $STELLA_W_EDITS as $e ) {
		$found = preg_match_all( $e['re'], $content );
		if ( false === $found ) {
			$log[] = '⚠ ' . $e['name'] . ' — 찾다가 오류가 났습니다';
			$bad   = true;
			continue;
		}
		$log[] = ( $found === $e['n'] ? '   ' : '⚠ ' ) . $e['name'] . ' : ' . $found . ' / ' . $e['n'];
		if ( $found !== $e['n'] ) { $bad = true; }
	}
	if ( $bad ) {
		$say( array_merge( $log, array( '',
			'고칠 자리가 예상과 다릅니다. 엔진이 그 사이에 바뀐 것 같습니다.',
			'아무것도 고치지 않았습니다. 이 화면을 그대로 알려주세요.' ) ), false );
		return;
	}

	/* ---- 실제로 바꿔봅니다 ---- */
	$updated = $content;
	foreach ( $STELLA_W_EDITS as $e ) {
		$rep     = $e['rep'];
		$updated = preg_replace_callback( $e['re'], function ( $m ) use ( $rep ) {
			$out = $rep;
			for ( $i = count( $m ) - 1; $i >= 1; $i-- ) {
				$out = str_replace( '\\' . $i, $m[ $i ], $out );
			}
			return $out;
		}, $updated );
		if ( null === $updated ) {
			$say( array_merge( $log, array( '', $e['name'] . ' 에서 바꾸다가 실패했습니다.' ) ), false );
			return;
		}
	}

	$grew  = strlen( $updated ) - strlen( $content );
	$sha   = sha1( $updated );
	$log[] = '';
	$log[] = '늘어난 바이트 : ' . number_format( $grew ) . '  (예상 ' . number_format( STELLA_W_GROW ) . ')';
	$log[] = '바뀐 본문 지문 : ' . substr( $sha, 0, 12 ) . '  (예상 ' . substr( STELLA_W_SHA, 0, 12 ) . ')';

	if ( abs( $grew - STELLA_W_GROW ) > 64 ) {
		$say( array_merge( $log, array( '',
			'늘어난 크기가 예상과 다릅니다. 뭔가 잘못된 것 같아 멈췄습니다.' ) ), false );
		return;
	}
	if ( $sha === STELLA_W_SHA ) {
		$log[] = '→ 제가 미리 걸어보고 확인한 것과 한 글자도 다르지 않습니다.';
	} else {
		$log[] = '→ 지문이 다릅니다. 크기는 맞으니 대개 줄바꿈 차이지만, 확인이 필요합니다.';
	}

	if ( $dry ) {
		$say( array_merge( $log, array( '',
			'※ 미리보기였습니다. 아무것도 고치지 않았습니다.',
			'진짜로 고치려면 ?stella_patch=go 로 다시 여세요.' ) ) );
		return;
	}

	update_option( $back_opt, $content, false );
	$ok = $wpdb->update( $wpdb->posts, array(
		'post_content'      => $updated,
		'post_modified'     => current_time( 'mysql' ),
		'post_modified_gmt' => current_time( 'mysql', 1 ),
	), array( 'ID' => $page_id ) );
	if ( false === $ok ) {
		$say( array_merge( $log, array( '저장 실패 : ' . $wpdb->last_error ) ), false );
		return;
	}
	clean_post_cache( $page_id );
	update_option( $done_opt, current_time( 'mysql' ), false );

	$say( array_merge( $log, array( '',
		'다 됐습니다.',
		'1) WPCode 에서 이 스니펫을 지우세요. (꼭)',
		'2) 호스팅 → 성능 → 캐시 비우기',
		'3) 시크릿 창에서 연성의 신 책을 한 권 뽑아 확인',
		'',
		'되돌리려면 : /wp-admin/?stella_patch=undo' ) ) );
} );
