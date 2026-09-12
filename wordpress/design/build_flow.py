# -*- coding: utf-8 -*-
import io, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-kitten/c2a43b1d-0c4f-566e-ae2a-79f351d35055/scratchpad')
from chars import CHARS
OUT = '/home/user/kitten/wordpress/design/'

HEAD = u'''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;700&display=swap">
  <style>
    body {{ margin: 0; background: #F7F2FC; }}
    a {{ color: #6B5BA8; text-decoration: none; }}
    a:hover {{ color: #52447F; }}
    * {{ box-sizing: border-box; }}
    .peek {{ position: absolute; z-index: 0; filter: drop-shadow(0 5px 8px rgba(107,91,168,0.22)); }}
    .front {{ position: relative; z-index: 1; }}
    .lbl {{ font-size: 12.5px; font-weight: 700; color: #8C82A6; margin-bottom: 8px; }}
    .fld {{ height: 54px; background: #FFFFFF; border-radius: 18px; display: flex; align-items: center;
            padding: 0 16px; font-size: 15px; color: #3F3A52; }}
    .ph {{ color: #C3BAD6; }}
    .btnP {{ display: flex; align-items: center; justify-content: center; height: 56px; background: #B8A6E8;
             color: #FFFFFF; border-radius: 20px; font-family: 'Jua', sans-serif; font-size: 16.5px;
             box-shadow: 0 10px 20px -12px rgba(107,91,168,0.8); }}
    .btnG {{ display: flex; align-items: center; justify-content: center; height: 52px; background: #FFFFFF;
             color: #7C7392; border-radius: 20px; font-size: 14.5px; font-weight: 500; }}
    .top {{ display: flex; align-items: center; gap: 8px; padding: 16px 20px 0; }}
    .h1 {{ font-family: 'Jua', sans-serif; font-size: 30px; line-height: 1.28; letter-spacing: -0.02em; color: #3F3A52; }}
    .sub {{ font-size: 14px; line-height: 1.75; color: #7C7392; margin-top: 10px; }}
    .wrap {{ width: 390px; background: #F7F2FC; font-family: 'Noto Sans KR','Apple SD Gothic Neo',sans-serif;
             color: #4A4358; padding-bottom: 48px; overflow: hidden; }}
  </style>
</helmet>
'''
TAIL = u'''
</x-dc>
</body>
</html>
'''

def bar(step):
    dots = ''
    for i in (1, 2, 3):
        on = i <= step
        dots += (f'<div style="height:5px;flex:1;border-radius:99px;'
                 f'background:{"#B8A6E8" if on else "#E4DCF2"}"></div>')
    return f'<div style="display:flex;gap:5px;padding:14px 20px 0">{dots}</div>'

def head_bar(title='유앤미'):
    return ('<div class="top"><div style="width:30px;height:30px">' + CHARS['bunny_white'] + '</div>'
            f'<div style="font-family:\'Jua\',sans-serif;font-size:21px;color:#6B5BA8">{title}</div></div>')

# ── 공유 버튼 (아이콘은 각 서비스 로고가 아니라 일반 기호입니다) ──
def share_btn(name, bg, fg, icon, note=''):
    sub = f'<div style="font-size:10px;color:#A79BC4;margin-top:2px">{note}</div>' if note else ''
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:7px;flex:1">'
            f'<div style="width:56px;height:56px;border-radius:20px;background:{bg};display:flex;'
            f'align-items:center;justify-content:center">{icon}</div>'
            f'<div style="font-size:11.5px;font-weight:700;color:#57506E;text-align:center">{name}{sub}</div></div>')

I_TALK = ('<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#3F2A08" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-9 8.4a9.7 9.7 0 0 1-2.7-.4'
          'L3 21l1.6-4.1A8.2 8.2 0 0 1 3 11.5a8.4 8.4 0 0 1 9-8.4a8.4 8.4 0 0 1 9 8.4z"/></svg>')
I_AT = ('<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/>'
        '<path d="M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-4 8"/></svg>')
I_CAM = ('<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="5"/>'
         '<circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/></svg>')
I_LINK = ('<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#6B5BA8" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/>'
          '<path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg>')
I_SAVE = ('<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#4F937A" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
          '<polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>')

SHARE_ROW = ('<div style="display:flex;gap:8px">'
             + share_btn('카카오톡', '#FAE100', '#3F2A08', I_TALK)
             + share_btn('스레드', '#1A1A1A', '#FFFFFF', I_AT)
             + share_btn('인스타', '#D9578C', '#FFFFFF', I_CAM, '이미지로')
             + share_btn('링크 복사', '#E7DEFA', '#6B5BA8', I_LINK)
             + '</div>')

# ══════════ 1. 내 생일 입력 ══════════
f1 = HEAD.format() + f'''
<div class="wrap">
  {head_bar()}
  {bar(1)}
  <div style="padding:22px 20px 0;position:relative">
    <div class="peek" style="width:82px;height:82px;right:4px;top:-6px;transform:rotate(9deg)">{CHARS['bunny_pink']}</div>
    <div class="h1 front" style="max-width:240px">먼저<br>내 것부터</div>
    <div class="sub front" style="max-width:250px">상대 생일은 몰라도 됩니다. 링크를 보내면 그쪽이 직접 넣어요.</div>
  </div>

  <div style="padding:26px 20px 0">
    <div class="lbl">누구와 보나요</div>
    <div style="display:flex;flex-wrap:wrap;gap:7px">
      <div style="background:#B8A6E8;color:#FFF;border-radius:999px;padding:11px 17px;font-size:13.5px;font-weight:700">연인</div>
      <div style="background:#FFF;border-radius:999px;padding:11px 17px;font-size:13.5px">부부</div>
      <div style="background:#FFF;border-radius:999px;padding:11px 17px;font-size:13.5px">친구</div>
      <div style="background:#FFF;border-radius:999px;padding:11px 17px;font-size:13.5px">형제자매</div>
      <div style="background:#FFF;border-radius:999px;padding:11px 17px;font-size:13.5px">부모와 자녀</div>
      <div style="background:#FFF;border-radius:999px;padding:11px 17px;font-size:13.5px">상사와 부하</div>
      <div style="background:#FFF;border-radius:999px;padding:11px 17px;font-size:13.5px">동업자</div>
    </div>
  </div>

  <div style="padding:24px 20px 0">
    <div class="lbl">부를 이름 <span style="font-weight:400;color:#B3A9C9">(안 넣어도 돼요)</span></div>
    <div class="fld"><span class="ph">지은</span></div>
  </div>

  <div style="padding:18px 20px 0">
    <div class="lbl">생년월일</div>
    <div style="display:flex;gap:7px">
      <div class="fld" style="flex:1.2"><span class="ph">1994</span></div>
      <div class="fld" style="flex:1"><span class="ph">03</span></div>
      <div class="fld" style="flex:1"><span class="ph">21</span></div>
    </div>
    <div style="display:flex;gap:7px;margin-top:8px">
      <div style="flex:1;height:44px;background:#B8A6E8;color:#FFF;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:13.5px;font-weight:700">양력</div>
      <div style="flex:1;height:44px;background:#FFF;color:#7C7392;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:13.5px">음력</div>
    </div>
  </div>

  <div style="padding:18px 20px 0">
    <div class="lbl">태어난 시각</div>
    <div style="display:flex;gap:7px">
      <div class="fld" style="flex:1"><span class="ph">시각 고르기</span></div>
      <div style="flex:0 0 118px;height:54px;background:#E7DEFA;color:#6B5BA8;border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:13.5px;font-weight:700">모름</div>
    </div>
    <div style="font-size:11.5px;color:#A79BC4;margin-top:9px;line-height:1.7">모르셔도 됩니다. 시각 없이도 나오고, 있으면 조금 더 정확해집니다.</div>
  </div>

  <div style="padding:18px 20px 0">
    <div class="lbl">성별</div>
    <div style="display:flex;gap:7px">
      <div style="flex:1;height:50px;background:#FFF;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:14px">여성</div>
      <div style="flex:1;height:50px;background:#FFF;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:14px">남성</div>
    </div>
  </div>

  <div style="padding:26px 20px 0;display:flex;flex-direction:column;gap:9px">
    <div class="btnP">궁합 링크 만들기</div>
    <div class="btnG">상대 생일도 내가 알아요</div>
  </div>

  <div style="padding:20px 20px 0;font-size:11.5px;line-height:1.9;color:#B3A9C9">
    넣으신 것은 이 기기에만 남습니다. 서버로 보내지 않습니다.
  </div>
</div>
''' + TAIL
io.open(OUT + 'Flow1Input.dc.html', 'w', encoding='utf-8').write(f1)

# ══════════ 2. 링크 만들어짐 + 공유 ══════════
f2 = HEAD.format() + f'''
<div class="wrap">
  {head_bar()}
  {bar(2)}
  <div style="padding:22px 20px 0;position:relative">
    <div class="peek" style="width:88px;height:88px;right:2px;top:-10px;transform:rotate(-8deg)">{CHARS['bunny_peek']}</div>
    <div class="h1 front" style="max-width:245px">링크가<br>만들어졌어요</div>
    <div class="sub front" style="max-width:250px">보내기만 하면 됩니다. 그 사람이 생일을 넣으면 둘 다 결과를 봐요.</div>
  </div>

  <!-- 카톡에 이렇게 보입니다 -->
  <div style="padding:26px 20px 0">
    <div class="lbl">이렇게 보내집니다</div>
    <div style="background:#FFFFFF;border-radius:22px;padding:16px;box-shadow:0 14px 26px -20px rgba(107,91,168,.5)">
      <div style="height:132px;border-radius:16px;background:linear-gradient(135deg,#E7DEFA,#FCE8F1);display:flex;align-items:center;justify-content:center;gap:2px">
        <div style="width:74px;height:74px">{CHARS['bunny_pink']}</div>
        <div style="font-family:'Jua',sans-serif;font-size:26px;color:#6B5BA8">?</div>
        <div style="width:74px;height:74px">{CHARS['cat_cream']}</div>
      </div>
      <div style="font-family:'Jua',sans-serif;font-size:17px;color:#3F3A52;margin-top:13px">지은님이 궁합 보자고 해요</div>
      <div style="font-size:12.5px;color:#A79BC4;margin-top:5px;line-height:1.6">생일만 넣으면 우리 둘 점수가 바로 나와요 · 유앤미</div>
    </div>
  </div>

  <div style="padding:26px 20px 0">
    <div class="lbl">어디로 보낼까요</div>
    {SHARE_ROW}
  </div>

  <div style="padding:24px 20px 0">
    <div style="background:#FFFFFF;border-radius:20px;padding:14px 16px;display:flex;align-items:center;gap:11px">
      <div style="flex:1;font-size:12.5px;color:#8C82A6;overflow:hidden;white-space:nowrap;text-overflow:ellipsis">stellasaju.com/uandme/?i=b3F4N2s5</div>
      <div style="flex:0 0 auto;height:38px;padding:0 15px;background:#E7DEFA;color:#6B5BA8;border-radius:13px;display:flex;align-items:center;font-size:12.5px;font-weight:700">복사</div>
    </div>
  </div>

  <div style="margin:30px 20px 0;background:#E7DEFA;border-radius:24px;padding:22px 20px">
    <div style="font-family:'Jua',sans-serif;font-size:19px;color:#3F3A52">그다음은 이렇게 됩니다</div>
    <div style="font-size:13.5px;line-height:1.8;color:#57506E;margin-top:8px">
      그 사람이 생일을 넣으면 그쪽 화면에 점수가 뜹니다.
      거기서 <b>「결과 보내기」</b> 한 번만 누르면 카톡으로 돌아와요.
      그때 두 분이 같은 점수를 보게 됩니다.
    </div>
  </div>

  <div style="padding:22px 20px 0;font-size:11.5px;line-height:1.9;color:#B3A9C9">
    링크에는 당신의 생년월일이 담깁니다. 아무에게나 보내지 마세요.
  </div>
</div>
''' + TAIL
io.open(OUT + 'Flow2Invite.dc.html', 'w', encoding='utf-8').write(f2)

# ══════════ 3. 상대가 링크를 열었을 때 ══════════
f3 = HEAD.format() + f'''
<div class="wrap">
  {head_bar()}
  <div style="padding:30px 20px 0;position:relative;text-align:center">
    <div style="display:flex;align-items:flex-end;justify-content:center;gap:0">
      <div style="width:96px;height:96px;transform:rotate(-8deg)">{CHARS['bunny_pink']}</div>
      <div style="width:82px;height:82px;margin-left:-14px;transform:rotate(9deg);opacity:.45">{CHARS['bunny_white']}</div>
    </div>
    <div class="h1" style="margin-top:14px">지은님이<br>궁합 보자고 했어요</div>
    <div class="sub">생일만 넣으면 둘 다 점수를 봅니다. 가입도 앱도 없어요.</div>
  </div>

  <div style="margin:26px 20px 0;background:#FFFFFF;border-radius:24px;padding:18px 18px">
    <div style="display:flex;align-items:center;gap:12px">
      <div style="width:44px;height:44px;flex:0 0 44px">{CHARS['bunny_pink']}</div>
      <div>
        <div style="font-size:11.5px;color:#A79BC4;font-weight:700">지은 · 1994년생 여성</div>
        <div style="font-size:14px;color:#3F3A52;margin-top:3px;font-weight:500">연인 궁합으로 물어봤어요</div>
      </div>
    </div>
  </div>

  <div style="padding:26px 20px 0">
    <div class="lbl">그럼 이제 당신 차례</div>
    <div style="display:flex;gap:7px">
      <div class="fld" style="flex:1.2"><span class="ph">1992</span></div>
      <div class="fld" style="flex:1"><span class="ph">11</span></div>
      <div class="fld" style="flex:1"><span class="ph">07</span></div>
    </div>
    <div style="display:flex;gap:7px;margin-top:8px">
      <div class="fld" style="flex:1"><span class="ph">태어난 시각</span></div>
      <div style="flex:0 0 108px;height:54px;background:#E7DEFA;color:#6B5BA8;border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:13.5px;font-weight:700">모름</div>
    </div>
    <div style="display:flex;gap:7px;margin-top:8px">
      <div style="flex:1;height:50px;background:#FFF;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:14px">여성</div>
      <div style="flex:1;height:50px;background:#B8A6E8;color:#FFF;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700">남성</div>
    </div>
  </div>

  <div style="padding:26px 20px 0">
    <div class="btnP">우리 점수 보기</div>
  </div>

  <div style="padding:20px 20px 0;font-size:11.5px;line-height:1.9;color:#B3A9C9">
    넣으신 것은 이 기기에만 남습니다. 서버로 보내지 않습니다.
  </div>
</div>
''' + TAIL
io.open(OUT + 'Flow3Partner.dc.html', 'w', encoding='utf-8').write(f3)

print('1~3 완료')

# ══════════ 4. 결과 + 공유 ══════════
SCORE_RING = '''<div style="position:relative;width:168px;height:168px">
  <svg width="168" height="168" viewBox="0 0 168 168">
    <defs><linearGradient id="rp" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#C3B2F0"/><stop offset="50%" stop-color="#F4B9D4"/><stop offset="100%" stop-color="#FFCBA8"/>
    </linearGradient></defs>
    <circle cx="84" cy="84" r="70" fill="none" stroke="#F1EBFA" stroke-width="17"/>
    <circle cx="84" cy="84" r="70" fill="none" stroke="url(#rp)" stroke-width="17" stroke-linecap="round"
            stroke-dasharray="404 440" transform="rotate(-90 84 84)"/>
  </svg>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <div style="font-family:'Jua',sans-serif;font-size:58px;line-height:1;color:#6B5BA8">92</div>
    <div style="font-size:12px;color:#A79BC4;font-weight:500;margin-top:3px">점</div>
  </div></div>'''

f4 = HEAD.format() + f'''
<div class="wrap">
  {head_bar()}
  {bar(3)}

  <div style="padding:22px 20px 0;position:relative">
    <div class="peek" style="width:72px;height:72px;left:38px;top:12px;transform:rotate(-9deg)">{CHARS['bunny_pink']}</div>
    <div class="peek" style="width:72px;height:72px;right:38px;top:12px;transform:rotate(9deg)">{CHARS['cat_cream']}</div>

    <div class="front" style="background:#FFFFFF;border-radius:28px;padding:24px 22px;margin-top:44px;box-shadow:0 18px 34px -20px rgba(107,91,168,.4)">
      <div style="display:flex;align-items:center;justify-content:space-between">
        <div style="background:#FFE2D6;color:#C4674A;font-size:11.5px;font-weight:700;padding:6px 13px;border-radius:999px">연인 궁합</div>
        <div style="font-size:11.5px;color:#B3A9C9;font-weight:500">지은 × 도현</div>
      </div>
      <div style="display:flex;justify-content:center;margin-top:14px">{SCORE_RING}</div>
      <div style="font-family:'Jua',sans-serif;font-size:27px;text-align:center;margin-top:10px;color:#3F3A52">완전 찰떡궁합</div>
      <div style="font-size:13.5px;line-height:1.8;color:#7C7392;margin-top:9px;text-align:center;text-wrap:pretty">
        갑돌이가 갑순이 시집가도 여전히 못 잊었다는데, 두 분은 그럴 걱정 없을 궁합이에요. 상견례 날짜부터 캘린더에 박아두세요.
      </div>
      <div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin-top:20px">
        <div style="background:#F1EBFA;border-radius:18px;padding:12px 6px;text-align:center"><div style="font-size:10.5px;color:#A79BC4;font-weight:500">성격</div><div style="font-family:'Jua',sans-serif;font-size:21px;color:#6B5BA8;margin-top:2px">90</div></div>
        <div style="background:#FCE8F1;border-radius:18px;padding:12px 6px;text-align:center"><div style="font-size:10.5px;color:#C58AA8;font-weight:500">연애</div><div style="font-family:'Jua',sans-serif;font-size:21px;color:#C4658F;margin-top:2px">85</div></div>
        <div style="background:#FFEFE2;border-radius:18px;padding:12px 6px;text-align:center"><div style="font-size:10.5px;color:#C99578;font-weight:500">결혼</div><div style="font-family:'Jua',sans-serif;font-size:21px;color:#C4784A;margin-top:2px">70</div></div>
        <div style="background:#E2F5EE;border-radius:18px;padding:12px 6px;text-align:center"><div style="font-size:10.5px;color:#7FAE9C;font-weight:500">금전</div><div style="font-family:'Jua',sans-serif;font-size:21px;color:#4F937A;margin-top:2px">95</div></div>
      </div>
    </div>
  </div>

  <!-- 지은에게 결과 돌려보내기 -->
  <div style="padding:18px 20px 0">
    <div style="height:56px;background:#FAE100;border-radius:20px;display:flex;align-items:center;justify-content:center;gap:9px">
      {I_TALK}
      <div style="font-size:15.5px;font-weight:700;color:#3F2A08">지은님에게 결과 보내기</div>
    </div>
  </div>

  <div style="padding:26px 20px 0">
    <div class="lbl">자랑하기</div>
    <div style="display:flex;gap:8px">
      {share_btn('스레드', '#1A1A1A', '#FFFFFF', I_AT)}
      {share_btn('인스타 스토리', '#D9578C', '#FFFFFF', I_CAM)}
      {share_btn('이미지 저장', '#E2F5EE', '#4F937A', I_SAVE)}
      {share_btn('링크 복사', '#E7DEFA', '#6B5BA8', I_LINK)}
    </div>
    <div style="font-size:11.5px;color:#A79BC4;margin-top:14px;line-height:1.75">
      인스타와 스레드는 글자를 못 붙여서, 위 카드를 <b>그림 한 장으로 만들어</b> 올립니다.
    </div>
  </div>

  <!-- 유료 -->
  <div style="margin:34px 20px 0;position:relative">
    <div class="peek" style="width:80px;height:80px;right:26px;top:-40px;transform:rotate(10deg)">{CHARS['bunny_happy']}</div>
    <div class="front" style="background:#FFFFFF;border-radius:28px;padding:24px 22px">
      <div style="font-family:'Jua',sans-serif;font-size:22px;color:#3F3A52">왜 92점인지 궁금하면</div>
      <div style="font-size:13.5px;line-height:1.8;color:#7C7392;margin-top:9px">
        네 항목이 왜 그 점수인지, 두 사람이 어디서 부딪히고 어디서 맞는지를 풀어서 읽어드려요.
      </div>
      <div style="display:flex;align-items:center;justify-content:space-between;margin-top:18px">
        <div style="font-family:'Jua',sans-serif;font-size:30px;color:#6B5BA8">500<span style="font-family:'Noto Sans KR',sans-serif;font-size:14px;font-weight:500;color:#A79BC4">원</span></div>
        <div style="display:flex;align-items:center;height:46px;padding:0 22px;background:#FFC2A8;color:#8C4A2E;border-radius:16px;font-size:14.5px;font-weight:700">자세히 보기</div>
      </div>
    </div>
  </div>

  <div style="padding:30px 20px 0">
    <div class="btnG" style="background:#FFFFFF">다른 사람과도 보기</div>
  </div>
</div>
''' + TAIL
io.open(OUT + 'Flow4Result.dc.html', 'w', encoding='utf-8').write(f4)

# ══════════ 5. SNS 로 나가는 그림 카드 ══════════
card = HEAD.format() + f'''
<div style="width:390px;height:488px;background:#F7F2FC;font-family:'Noto Sans KR',sans-serif;
            display:flex;align-items:center;justify-content:center;padding:14px">
  <div style="width:100%;height:100%;border-radius:26px;background:linear-gradient(160deg,#FBF6FF 0%,#F3EAFC 55%,#FFEFE6 100%);
              padding:26px 24px;position:relative;overflow:hidden;display:flex;flex-direction:column">

    <div style="position:absolute;left:-24px;bottom:-30px;width:132px;height:132px;transform:rotate(-12deg);opacity:.95">{CHARS['bunny_pink']}</div>
    <div style="position:absolute;right:-20px;bottom:-24px;width:120px;height:120px;transform:rotate(11deg);opacity:.95">{CHARS['cat_cream']}</div>

    <div style="display:flex;align-items:center;justify-content:space-between">
      <div style="display:flex;align-items:center;gap:6px">
        <div style="width:26px;height:26px">{CHARS['bunny_white']}</div>
        <div style="font-family:'Jua',sans-serif;font-size:17px;color:#6B5BA8">유앤미</div>
      </div>
      <div style="background:#FFFFFF;color:#C4674A;font-size:11px;font-weight:700;padding:6px 12px;border-radius:999px">연인 궁합</div>
    </div>

    <div style="text-align:center;margin-top:22px">
      <div style="font-size:13px;color:#A79BC4;font-weight:500">지은 × 도현</div>
      <div style="display:flex;align-items:flex-end;justify-content:center;gap:4px;margin-top:2px">
        <div style="font-family:'Jua',sans-serif;font-size:104px;line-height:.94;color:#6B5BA8;letter-spacing:-.03em">92</div>
        <div style="font-size:20px;color:#A79BC4;font-weight:500;padding-bottom:14px">점</div>
      </div>
      <div style="font-family:'Jua',sans-serif;font-size:30px;color:#3F3A52;margin-top:6px;letter-spacing:-.02em">완전 찰떡궁합</div>
    </div>

    <div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin-top:20px">
      <div style="background:rgba(255,255,255,.8);border-radius:16px;padding:11px 4px;text-align:center"><div style="font-size:10px;color:#A79BC4;font-weight:500">성격</div><div style="font-family:'Jua',sans-serif;font-size:19px;color:#6B5BA8">90</div></div>
      <div style="background:rgba(255,255,255,.8);border-radius:16px;padding:11px 4px;text-align:center"><div style="font-size:10px;color:#C58AA8;font-weight:500">연애</div><div style="font-family:'Jua',sans-serif;font-size:19px;color:#C4658F">85</div></div>
      <div style="background:rgba(255,255,255,.8);border-radius:16px;padding:11px 4px;text-align:center"><div style="font-size:10px;color:#C99578;font-weight:500">결혼</div><div style="font-family:'Jua',sans-serif;font-size:19px;color:#C4784A">70</div></div>
      <div style="background:rgba(255,255,255,.8);border-radius:16px;padding:11px 4px;text-align:center"><div style="font-size:10px;color:#7FAE9C;font-weight:500">금전</div><div style="font-family:'Jua',sans-serif;font-size:19px;color:#4F937A">95</div></div>
    </div>

    <div style="flex:1"></div>
    <div style="text-align:center;font-size:12px;color:#A79BC4;font-weight:500;position:relative">
      너도 해볼래? · stellasaju.com/uandme
    </div>
  </div>
</div>
''' + TAIL
io.open(OUT + 'ShareCard.dc.html', 'w', encoding='utf-8').write(card)
print('4~5 완료')
