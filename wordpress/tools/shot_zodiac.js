/* 띠별운세 카드를 실제로 그려서 사진으로 뽑습니다
   살아 있는 쪽과 같게 하려면 ① 쪽 CSS ② 2026-09-08 흰 바탕 덮어쓰기
   ③ 제 조각을 차례로 얹어야 합니다.
   실행 : node wordpress/tools/shot_zodiac.js                          */
var fs = require('fs'), path = require('path'), os = require('os');
var { chromium } = require('playwright');

var HERE = path.join(__dirname, '..');
var page92 = fs.readFileSync(path.join(HERE, 'pages/zodiac-year-92.html'), 'utf8');
var php    = fs.readFileSync(path.join(HERE, 'php/patch92_look.php'), 'utf8');
var out    = php.split('?>')[1]; out = out.slice(0, out.lastIndexOf('<?php'));
var MYCSS  = out.match(/<style[^>]*>([\s\S]*?)<\/style>/)[1];
var MYJS   = out.match(/<script>([\s\S]*?)<\/script>/)[1];

/* ① 쪽 CSS */
var css92 = (page92.match(/<style[^>]*>[\s\S]*?<\/style>/g) || []).join('\n');

/* ② 2026-09-08 흰 바탕 덮어쓰기 — /price/ 쪽(같은 #ssp)에서 그대로 */
var WHITE = '<style>#ssp{'
  + '--void:#F1EDE3; --void-deep:#FBF8F2; --nebula:#FFFFFF; --nebula-soft:#F7F3EA;'
  + '--purple-glow:rgba(107,79,176,.16); --lilac:#6B4FB0;'
  + '--gold:#A9791F; --gold-soft:#B98A47; --gold-lite:#8A6520;'
  + '--star:#221C33; --ink-soft:#4E4763; --ink-dim:#8B849C; --line:#E2DACB;'
  + 'background:#F1EDE3 !important; color:var(--star);}'
  + '#ssp .card,#ssp .acard{background:#FFFFFF !important;border:1px solid #E2DACB !important;'
  + 'color:var(--star) !important;}'
  + '</style>';

var ANIMAL = ['쥐','소','범','토끼','용','뱀','말','양','원숭이','닭','개','돼지'];
var JI_H   = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
var EMOJI = ['🐭','🐮','🐯','🐰','🐲','🐍','🐴','🐐','🐵','🐓','🐶','🐷'];
var YEARS = ['1948 · 1960 · 1972 · 1984 · 1996 · 2008 · 2020',
             '1949 · 1961 · 1973 · 1985 · 1997 · 2009',
             '1950 · 1962 · 1974 · 1986 · 1998 · 2010',
             '1951 · 1963 · 1975 · 1987 · 1999 · 2011',
             '1952 · 1964 · 1976 · 1988 · 2000 · 2012',
             '1953 · 1965 · 1977 · 1989 · 2001 · 2013',
             '1954 · 1966 · 1978 · 1990 · 2002 · 2014',
             '1955 · 1967 · 1979 · 1991 · 2003 · 2015',
             '1956 · 1968 · 1980 · 1992 · 2004 · 2016',
             '1957 · 1969 · 1981 · 1993 · 2005 · 2017',
             '1958 · 1970 · 1982 · 1994 · 2006 · 2018',
             '1959 · 1971 · 1983 · 1995 · 2007 · 2019'];

/* 이번주가 토끼(卯)일 때의 진짜 관계 */
var K = {};
K[3]  = 'same';   K[11] = 'samhap'; K[7] = 'samhap';
K[10] = 'yukhap'; K[9]  = 'chung';  K[4] = 'hae';
var REL = { same:'비화 · 같은 기운', samhap:'삼합 · 손이 맞는 주',
  yukhap:'육합 · 붙잡아 주는 주', chung:'충 · 흔들리는 주',
  hae:'해 · 어긋나는 주', plain:'무관 · 잔잔한 주' };
var T1 = {
  same:'이번주 하늘의 기운이 이 띠와 같은 결로 들어옵니다. 힘이 두 배로 실리는 대신, 같은 성질끼리 겹쳐서 고집도 같이 세집니다.',
  samhap:'이번주 기운과 삼합(三合)으로 묶입니다. 혼자 하던 일에 사람이 붙고, 막혀 있던 연락이 먼저 옵니다.',
  yukhap:'이번주 기운과 육합(六合)으로 만납니다. 크게 뻗기보다 안으로 단단해지는 흐름이에요.',
  chung:'이번주 기운과 정면으로 부딪힙니다. 충(沖)은 나쁜 게 아니라 흔드는 것이라, 붙어 있던 게 떨어지고 미뤄둔 게 터져 나옵니다.',
  hae:'이번주 기운과 살짝 어긋납니다. 크게 무너지지는 않는데, 말이 한 번씩 헛돌고 일정이 자꾸 밀립니다.',
  plain:'이번주 기운과 특별히 얽히지 않습니다. 크게 밀어주지도, 막아서지도 않는 잔잔한 한 주예요.' };
var T2 = {
  same:'밀어붙일 일이 있다면 이번주가 그 주입니다. 다만 사람과 부딪히는 자리는 한 박자만 늦추세요.',
  samhap:'부탁할 일이 있다면 이번주에 꺼내세요. 거절당할 확률이 가장 낮은 자리입니다.',
  yukhap:'새로 벌이는 것보다, 이미 있는 관계와 이미 시작한 일을 손보기에 좋습니다.',
  chung:'큰돈이 오가는 결정과 감정이 실린 대화는 다음주로 미루세요. 대신 버릴 것을 버리기에는 가장 좋은 주입니다.',
  hae:'약속은 한 번 더 확인하고, 중요한 말은 글로 남겨두세요.',
  plain:'이런 주에는 흐름을 기다리기보다 내가 정한 속도로 가는 편이 낫습니다.' };
var COLOR = ['#6B4FB0','#C4453A','#2F7D4A','#A9791F','#2E6FA8','#8A6520',
             '#C4453A','#A9791F','#2F7D4A','#6B4FB0','#2E6FA8','#8A6520'];
var CNAME = ['보라','붉은색','초록','금빛','푸른색','흙빛',
             '붉은색','금빛','초록','보라','푸른색','흙빛'];

var cards = '';
for(var z = 0; z < 12; z++){
  var k = K[z] || 'plain';
  cards += '<div class="acard' + (z === 2 ? ' mine' : '') + '" data-z="' + z + '" id="zc' + z + '">'
    + '<div class="ahead"><div class="asym">' + EMOJI[z] + '</div>'
    + '<div><div class="aname">' + ANIMAL[z] + '띠 <span style="color:#A79FB8;font-size:.8rem">' + JI_H[z] + '</span>'
    + ({3:1,7:1,11:1}[z] ? '<span class="sj-tag">눌삼재</span>' : '') + '</div>'
    + '<div class="ayears">' + YEARS[z] + '</div></div></div>'
    + '<div class="arel">' + REL[k] + '</div>'
    + '<p class="atext">' + T1[k] + '</p>'
    + '<p class="atext">' + T2[k] + '</p>'
    + '<dl class="arows">'
    + '<div class="arow"><dt>잘 맞는 띠</dt><dd>' + ANIMAL[(z + 4) % 12] + '띠</dd></div>'
    + '<div class="arow"><dt>조심할 띠</dt><dd>' + ANIMAL[(z + 6) % 12] + '띠 <span style="color:#9A92AC">· 부딪히면 크게 부딪힙니다</span></dd></div>'
    + '<div class="arow"><dt>행운의 색</dt><dd><span class="swatch" style="background:' + COLOR[z] + '"></span>' + CNAME[z] + '</dd></div>'
    + '<div class="arow"><dt>행운의 물건</dt><dd>나무로 만든 것</dd></div>'
    + '</dl>'
    + ({3:1,7:1,11:1}[z] ? '<div class="sj-line"><p>올해 삼재입니다. 삼재 세 해 가운데 한가운데입니다. 가장 무겁게 느껴지는 해예요. 큰 결정은 한 해만 미루시면 한결 수월합니다.</p><a href="#">' + ANIMAL[z] + '띠의 삼재 풀이 보기 →</a></div>' : '')
    + (z === 2 ? '<p class="amine">1975년 1월 23일생이시라면 범띠입니다. 그 해 입춘 전에 태어나셔서, 사주로는 1974년에 들어갑니다.</p>' : '')
    + '</div>';
}

var HTML = '<!doctype html><meta charset="utf-8">'
  + '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@700&display=swap" rel="stylesheet">'
  + css92 + WHITE
  + '<style>' + MYCSS + '</style>'
  + '<style>#ssp .acard .sj-tag{margin-left:7px;font-size:.78rem;font-weight:400;opacity:.6;}</style>'
  + '<div id="ssp"><div class="wrap" style="max-width:1180px;margin:0 auto;padding:30px 22px 60px">'
  + '<div class="weekbox"><div class="wk" id="zWeek">9월 14일 ~ 9월 20일</div>'
  + '<div class="gz" id="zGz">辛卯</div>'
  + '<div class="gzk" id="zGzk">신묘 · 토끼의 자리 · 목(木)의 주</div>'
  + '<p class="say" id="zSay">이번주는 묘(卯)의 기운이 판을 잡습니다. 목(木)은 자라려는 기운이라, 새로 시작한 일에 힘이 붙습니다.</p></div>'
  + '<input id="zYear" value="1975"><input id="zMon" value="1"><input id="zDay" value="23">'
  + '<button type="button" id="zFind">내 띠 찾기</button>'
  + '<div class="agrid" id="zGrid">' + cards + '</div></div></div>'
  + '<script>' + MYJS + '</' + 'script>';

var tmp = path.join(os.tmpdir(), 'zodiac-shot.html');
fs.writeFileSync(tmp, HTML);

(async function(){
  var browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  var p = await browser.newPage({ viewport: { width: 1180, height: 1400 },
    deviceScaleFactor: 2 });
  await p.goto('file://' + tmp);
  await p.waitForTimeout(2200);
  var dst = path.join(__dirname, 'zodiac-cards.png');
  await p.screenshot({ path: dst, clip: { x: 0, y: 0, width: 1180, height: 1150 } });
  console.log('찍었습니다 : ' + dst);

  /* 눈으로 보기 전에 숫자로도 재둡니다 */
  var m = await p.evaluate(function(){
    var c = document.querySelector('.acard');
    var r = c.getBoundingClientRect();
    var head = c.querySelector('.ahead');
    var sym = c.querySelector('.asym');
    var rel = c.querySelector('.arel');
    return {
      카드폭: Math.round(r.width),
      머리높이: Math.round(head.getBoundingClientRect().height),
      그림: Math.round(sym.getBoundingClientRect().width),
      딱지가머리안에: head.contains(rel),
      색띠: getComputedStyle(c, ':before').backgroundColor,
      갈래: c.getAttribute('data-rel')
    };
  });
  console.log(JSON.stringify(m, null, 1));
  await browser.close();
  process.exit(0);
})();
