# -*- coding: utf-8 -*-
"""SAMJAE.json -> WPCode 조각 (삼재 책)

    python3 emit_samjae.py 2026

★ 삼재는 값을 안 받습니다 (2026-09-15 · 소희 님 「삼재는 돈받지 않아야
  할거 같아 · 변별력도 없고」). 검색으로 들어온 손님을 받아 신년운세로
  이어주는 자리입니다.
★ 삼재 자리는 띠가 정합니다. 십성은 「그 해에 무엇이 흔들리나」를
  읽으려고 겹치는 것입니다 (전통 삼재론에 십성은 없습니다).
★ 틀(PHP·CSS·JS)은 sj_head.tpl · sj_tail.tpl 에 있습니다.
  파이썬 안에 삼중따옴표로 담았다가 따옴표가 겹쳐 꼬였습니다 —
  틀을 밖에 두면 그런 일이 없습니다.
"""
import io, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
YEAR = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
STAMP = time.strftime('%Y-%m-%d %H:%M')

GAN = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
JI = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
GAN_EL = ['목', '목', '화', '화', '토', '토', '금', '금', '수', '수']
gi = (YEAR - 4) % 10
ji = (YEAR - 4) % 12
YEAR_GAN = GAN[gi] + JI[ji]
YEAR_EL = GAN_EL[gi]


def rd(name):
    return io.open(os.path.join(HERE, name), encoding='utf-8').read()


head = rd('sj_head.tpl') % {'Y': YEAR, 'YE': YEAR_EL, 'YG': YEAR_GAN,
                            'STAMP': STAMP, 'CSS': rd('sj_css.tpl')}
tail = rd('sj_tail.tpl')
out = head + rd('SAMJAE.json') + tail

path = os.path.join(HERE, '..', 'php', 'patch160_samjae.WPCODE.txt')
io.open(path, 'w', encoding='utf-8').write(out)
print('썼습니다 %s' % os.path.normpath(path))
print('  바이트 %d · 글자 %d' % (len(out.encode('utf-8')), len(out)))
print('  앰퍼샌드 %d (0 이어야 합니다)' % out.count('&'))
print('  역빗금 %d (0 이어야 합니다)' % out.count(chr(92)))
