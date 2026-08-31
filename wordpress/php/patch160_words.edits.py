# -*- coding: utf-8 -*-
"""페이지 160 을 고치는 자리 목록. 각 항목: (이름, 찾는 정규식, 바꿀 글, 몇 번 나와야 하는지)"""

SIDE_TABLE = r"""
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

  """

EL_HELPER = r"""<script>
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
"""

EDITS = [
  # ── 1. 오행 풀어쓰기 도우미를 섹션 10 맨 앞(함수 바깥)에 둡니다 ──
  ('오행 도우미 심기',
   r"<script>\n\(function\(\)\{\n  var root=document\.getElementById\('ssb'\); if\(!root\) return;",
   EL_HELPER + "(function(){\n  var root=document.getElementById('ssb'); if(!root) return;",
   1),

  # ── 2. 저울 양쪽 이름표를 gapBlock 앞에 심습니다 ──
  ('저울 이름표 심기',
   r"  function gapBlock\(key, title\)\{",
   SIDE_TABLE + r"function gapBlock(key, title){",
   1),

  # ── 3~6. 본문에 나오는 기운 쪽 이름을 소제목과 같은 말로 ──
  ('사주는 ○○ 쪽으로 (손님 말 글이 있을 때)',
   r"'<p>사주는 <em>'\+A\.name\+'</em> 쪽으로 '\+tiltWord\(d\)",
   r"'<p>사주는 <em>'+sideWord(key,A.name)+'</em> 쪽으로 '+tiltWord(d)",
   1),
  ('사주가 ○○ 쪽으로 (옛 글일 때)',
   r"'<p>사주가 <em>'\+A\.name\+'</em> 쪽으로 '\+A\.a\+' 대 '",
   r"'<p>사주가 <em>'+sideWord(key,A.name)+'</em> 쪽으로 '+A.a+' 대 '",
   1),
  ('결국 ○○ 쪽을 가운데 두고',
   r"결국 <em>'\+A\.name\+'</em> 쪽을 가운데 두고",
   r"결국 <em>'+sideWord(key,A.name)+'</em> 쪽을 가운데 두고",
   1),
  ('타고난 결은 ○○ 쪽인데',
   r"'<p>타고난 결은 '\+A\.name\+' 쪽인데 지금은 '",
   r"'<p>타고난 결은 '+sideWord(key,A.name)+' 쪽인데 지금은 '",
   1),
  ('답해주신 쪽 이름 (otherName)',
   r"function otherName\(key, side\)\{\n    var A=R\.AXES\[key\];\n    return side==='A' \? A\.A : A\.B;\n  \}",
   ("function otherName(key, side){\n"
    "    var A=R.AXES[key];\n"
    "    /* 2026-08-31 · 답해주신 쪽 이름도 소제목과 같은 말로 */\n"
    "    return sideWord(key, side==='A' ? A.A : A.B);\n  }"),
   1),

  # ── 7. 저울 두 번째 장 머리말 ──
  ('저울 둘째 장 머리말',
   r"'<h2>남은 저울 셋</h2>'",
   r"'<h2>타고난 성향과 실제 생활이 다른 부분 — 남은 셋</h2>'",
   1),

  # ── 8~13. 오행을 보여주는 자리 ──
  ('기운으로는 · 인연의 별 목록',
   r"'기운으로는 <em>' \+ elList\.join\('·'\) \+ '</em>입니다\.</p>'",
   r"'기운으로는 <em>' + stellaEl(elList.join('·')) + '</em>입니다.</p>'",
   1),
  ('기운으로는 · 인연의 별 한 줄',
   r"'기운으로는 <em>' \+ elList\.join\('·'\) \+ '</em>' \+ iyeyo\(elList\[elList\.length - 1\]\)",
   r"'기운으로는 <em>' + stellaEl(elList.join('·')) + '</em>' + iyeyo(elList[elList.length - 1])",
   1),
  ('기운으로는 · 올해의 기운 (T.syEl)',
   r"기운으로는 '\+T\.syEl\+'입니다\. ",
   r"기운으로는 '+stellaEl(T.syEl)+'입니다. ",
   3),
  ('기운으로는 · 올해의 기운 (syEl)',
   r"기운으로는 '\+syEl\+'입니다\. ",
   r"기운으로는 '+stellaEl(syEl)+'입니다. ",
   1),
  ('기운으로는 · 일간과 몸',
   r"기운으로는 '\+dayEl\+'입니다\. ",
   r"기운으로는 '+stellaEl(dayEl)+'입니다. ",
   1),
  ('기운으로는 · 일지와 배우자',
   r"기운으로는 '\+R\.josa\(iljiEl,'이에요','예요'\)\+'\.</p>'",
   r"기운으로는 '+stellaEl(iljiEl)+(R.hasBatchim(iljiEl)?'이에요':'예요')+'.</p>'",
   1),
  ('기운으로는 · 달자리',
   r"기운으로는 <em>'\+dayEl\+'</em>'\+\n      \(batchim\(dayEl\)\?'이었습니다':'였습니다'\)",
   "기운으로는 <em>'+stellaEl(dayEl)+'</em>'+\n      (batchim(dayEl)?'이었습니다':'였습니다')",
   1),

  # ── 14. 인연의 흐름 · 달 이름 풀이를 표 밑에 붙입니다 ──
  ('달 이름 풀이 붙이기',
   r"(push :\{ tag:'흔들리는 달' \}.*?)('<p class=\"mini\">절기 기준입니다)",
   "\\1'<h3>달 이름이 뜻하는 것</h3>'+\n      '<p><em>말이 나가는 달</em> — 내가 먼저 마음을 내보내는 달입니다. 연락도, 미뤄둔 말도 이때 잘 나갑니다.</p>'+\n      '<p><em>견주는 달</em> — 남의 관계와 내 관계를 자꾸 견주게 되는 달입니다. 비교가 마음을 갉습니다.</p>'+\n      '<p><em>끌리는 달</em> — 사람이 눈에 들어오는 달입니다. 만남이 늘고 마음이 먼저 갑니다.</p>'+\n      '<p><em>흔들리는 달</em> — 밖에서 오는 일이 마음을 흔드는 달입니다. 급하게 답하지 않는 것이 유일한 방패예요.</p>'+\n      '<p><em>기대고 싶은 달</em> — 마음이 안으로 들어가는 달입니다. 새로 벌이기보다 쉬고 정리하기 좋습니다.</p>'+\n      \\2",
   1),

  # ── 15. 연성의 신 닫는 말을 쉽고 충분하게 ──
  ('연성의 신 닫는 말',
   "last:'붙잡을지 놓을지 모르겠다면, 그 사람과 있을 때의 당신이 마음에 드는지를 보세요\\. 답은 상대가 아니라 거기에 있습니다\\.'",
   "last:'붙잡을지 놓을지 아직 모르겠다면, 그 사람이 어떤 사람인지를 따지는 대신 이렇게 해보세요. 그 사람과 함께 있을 때의 내 모습을 떠올려 보는 겁니다. 그때의 내가 마음에 드는지, 아니면 자꾸 작아지고 눈치를 보고 있는지. 상대가 좋은 사람인가를 재는 것보다 그 답이 훨씬 정확합니다. 답은 그 사람에게 있는 것이 아니라, 처음부터 거기에 있었습니다.'",
   1),

  # ── 16. 한 장 안에서 접는 상자 모양 ──
  ('접는 상자 CSS',
   r"#ssb \.foldbtn:hover\{ background:var\(--gold\); color:#0B0817; \}",
   "#ssb .foldbtn:hover{ background:var(--gold); color:#0B0817; }\n/* 2026-08-31 · 한 장 안에서 접는 상자. 누구에게나 같은 안내글을 기본으로 접어둡니다.\n   자바스크립트 없이 브라우저가 스스로 여닫습니다. 인쇄할 때는 펼쳐서 나갑니다. */\n#ssb details.readfold{\n  border:1px solid var(--rule); border-radius:14px;\n  background:rgba(28,21,51,.5); padding:0 24px; margin:26px 0 0;\n}\n#ssb details.readfold>summary{\n  list-style:none; cursor:pointer; padding:18px 0;\n  font-family:var(--serif); font-size:1.02rem; color:var(--gold-lite);\n}\n#ssb details.readfold>summary::-webkit-details-marker{ display:none; }\n#ssb details.readfold>summary::after{ content:'  펼쳐 보기 ↓'; color:var(--dim); font-size:.9rem; }\n#ssb details.readfold[open]>summary::after{ content:'  접어 두기 ↑'; }\n#ssb details.readfold[open]{ padding-bottom:16px; }\n#ssb details.readfold>summary:focus-visible{ outline:2px solid var(--gold); outline-offset:3px; }\n@media print{ #ssb details.readfold>summary{ display:none; } }",
   1),

  # ── 17. 「다섯 저울을 읽는 법」은 누구에게나 같은 글 — 접어둡니다 ──
  ('다섯 저울을 읽는 법 접기',
   r"('<h3>다섯 저울을 읽는 법</h3>'\+)(.*?)(, null, 'two'\);)",
   '\'<details class=\\"readfold\\"><summary>다섯 저울을 읽는 법</summary>\'+\\2+\'</details>\'\\3',
   1),

  # ── 18. 「고르지 않기로 하는 일」을 쉬운 말로 (조사 버그도 같이) ──
  ('배우자 고르는 대목',
   "'<p>마음을\\ 여러\\ 곳에\\ 두지\\ 마세요\\.\\ <em>고르는\\ 일보다\\ 고르지\\ 않기로\\ 하는\\ 일</em>이\\ '\\\n\\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\+\\ esc\\(mate\\)\\ \\+\\ '을\\ 고르는\\ 데는\\ 더\\ 중요합니다\\.</p>';",
   "'<p>마음을 여러 곳에 나누어 두기보다, 결혼을 결정한 뒤에는 한 사람에게 마음의 방향을 모으는 것이 중요합니다. '\n          /* 2026-08-31 · mate 는 「남편」 또는 「아내」 — 조사를 받침에 맞춰 고릅니다 */\n          + esc(mate) + ((mate.charCodeAt(mate.length-1)-0xAC00)%28 ? '을' : '를')\n          + ' 고르는 일에서는 누구를 선택하느냐만큼, 선택한 사람에게 집중하기로 하는 것도 중요합니다.</p>';",
   1),

  # ── 19. 달 표가 올해 이야기로 오해되지 않게 ──
  ('달 표는 해마다 되풀이됨을 밝힘',
   "var\\ out\\ =\\ '<p>'\\ \\+\\ w\\.lead\\ \\+\\ '</p>';",
   "var out = '<p>' + w.lead + '</p>'\n      /* 2026-08-31 · 「올해 8월인가?」 하고 읽으신 분이 계셔서 못 박아 둡니다.\n         monthGrade 는 태어난 날의 글자(일지) 하나만 봅니다. 그 해의 글자는\n         전혀 안 들어가므로, 이 표는 해마다 똑같이 되풀이됩니다. */\n      + '<p>여기 적힌 달은 <em>올해만의 이야기가 아닙니다.</em> 태어난 날의 글자와 그 달의 글자가 만나는 방식으로 갈리는 것이라, 내년에도 그 다음 해에도 같은 달이 같은 자리에 옵니다. 절기 기준이라 달력의 1일이 아니라 절기가 드는 날에 바뀝니다.</p>';",
   1),

  # ── 20. 맺음말 · 결은 ○○ 쪽입니다 ──
  ('맺음말 · 결은 ○○ 쪽입니다',
   'class="kt">결은\\ \'\\+\\(leaned\\ \\?\\ leanAxis\\.name\\+\'\\ 쪽입니다\'',
   'class="kt">결은 \'+(leaned ? sideWord(leanKey, leanAxis.name)+\' 쪽입니다\'',
   1),

  # ── 21. 맺음말 · 가장 크게 기운 저울 ──
  ('맺음말 · 가장 크게 기운 저울',
   "'여덟\\ 글자에서\\ 가장\\ 크게\\ 기운\\ 저울은\\ <em>'\\+AXNAME\\[leanKey\\]\\+'</em>였습니다\\.\\ '\\+\\\n\\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ '당신은\\ 아무런\\ 기준\\ 없이\\ 처음부터\\ 새로운\\ 답을\\ 만들어가기보다,\\ '\\+leanAxis\\.say\\+'\\ 쪽으로\\ 나올\\ 때\\ 마음이\\ 더\\ 편한\\ 사람이에요\\.</p>'\\+",
   "'여덟 글자에서 가장 크게 기운 저울은 <em>'+axTitle(leanKey, AXNAME[leanKey])+'</em>였습니다. '+\n            /* 2026-08-31 · saySide 값이 모두 「…쪽」으로 끝나 옛 문장에 넣으면 「쪽 쪽으로」가 됩니다 */\n            '당신은 <em>'+saySide(leanKey)+'</em>'+(R.hasBatchim(saySide(leanKey))?'이에요':'예요')+'.</p>'+",
   1),

  # ── 22. 맺음말 · 어긋난 자리 목록 ──
  ('맺음말 · 어긋난 자리 목록',
   'gapKeys\\.map\\(function\\(k\\)\\{\\ return\\ AXNAME\\[k\\];\\ \\}\\)',
   'gapKeys.map(function(k){ return axTitle(k, AXNAME[k]); })',
   1),
]
