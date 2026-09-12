# -*- coding: utf-8 -*-
"""패치 3 — 「셋을 겹쳐 놓으면」이 주제를 안 보던 것."""
import re

TBL = open('combo.js', encoding='utf-8', newline='').read()

_A_OLD = "    var majorN = 0, revN = 0;"
_A_NEW = TBL + "    var majorN = 0, revN = 0;"

_B_OLD = ("    page(\n"
          "      '<p class=\"eyebrow\">마지막에 놓는 세 장</p>'\n"
          "      + '<h2>셋을 겹쳐 놓으면</h2>'")
_B_NEW = ("    /* 주제별 글이 있으면 위에서 고른 갈래를 그것으로 바꿉니다.\n"
          "       없으면 바로 위 원래 글이 그대로 나갑니다. */\n"
          "    var __ct;\n"
          "    __ct = comboSay(majorN === 0 ? 'm0' : (majorN === 1 ? 'm1' : 'm2'), majorN);\n"
          "    if(__ct){ mSay = __ct; }\n"
          "    __ct = comboSay(flow >= 4 ? 'up' : (flow <= -4 ? 'down' : 'flat'), 0);\n"
          "    if(__ct){ fSay = __ct; }\n"
          "    __ct = comboSay(revN === 0 ? 'r0' : (revN === 3 ? 'r3' : 'rs'), revN);\n"
          "    if(__ct){ rSay = __ct; }\n"
          "\n" + _B_OLD)

EDITS = [
  ('겹쳐 읽기 · 주제별 표 심기', re.escape(_A_OLD), _A_NEW, 1),
  ('겹쳐 읽기 · 세 잣대를 주제별로',  re.escape(_B_OLD), _B_NEW, 1),
]
