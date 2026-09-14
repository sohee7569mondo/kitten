/* patch92_look 검사 — 띠별운세 쪽 뼈대로 돌립니다
   실행 : node wordpress/tools/test_look.js                            */
var fs = require('fs'), path = require('path');
var { JSDOM } = require('jsdom');

var HERE = path.join(__dirname, '..');
var php  = fs.readFileSync(path.join(HERE, 'php/patch92_look.php'), 'utf8');
var out  = php.split('?>')[1]; out = out.slice(0, out.lastIndexOf('<?php'));
var JS   = out.match(/<script>([\s\S]*?)<\/script>/)[1];

var ANIMAL = ['쥐','소','범','토끼','용','뱀','말','양','원숭이','닭','개','돼지'];
var EMOJI  = ['🐭','🐮','🐯','🐰','🐲','🐍','🐴','🐐','🐵','🐓','🐶','🐷'];
/* 이번주가 신묘(卯)일 때 쪽이 붙이는 딱지 — 살아 있는 화면에서 본 그대로 */
var REL = ['무관 · 잔잔한 주','무관 · 잔잔한 주','무관 · 잔잔한 주',
           '삼합 · 한 무리인 주','무관 · 잔잔한 주','무관 · 잔잔한 주',
           '무관 · 잔잔한 주','삼합 · 한 무리인 주','무관 · 잔잔한 주',
           '충 · 부딪히는 주','육합 · 짝이 되는 주','삼합 · 한 무리인 주'];

var cards = '';
for(var z = 0; z < 12; z++){
  cards += '<div class="acard" data-z="' + z + '" id="zc' + z + '">'
    + '<div class="ahead"><div class="asym">' + EMOJI[z] + '</div>'
    + '<div><div class="aname">' + ANIMAL[z] + '띠</div></div></div>'
    + '<div class="arel r' + z + '">' + REL[z] + '</div>'
    + '<p class="atext">이번주 이야기</p>'
    + '<p class="amine" style="display:none">지금 보고 계신 띠예요.</p></div>';
}
var PAGE = '<div id="ssp"><div class="wrap">'
  + '<input id="zYear" value=""><input id="zMon" value=""><input id="zDay" value="">'
  + '<button type="button" id="zFind">내 띠 찾기</button>'
  + '<div class="agrid" id="zGrid">' + cards + '</div></div></div>';

function make(user){
  var dom = new JSDOM('<!doctype html><html><body>' + PAGE + '</body></html>',
    { runScripts: 'outside-only', url: 'https://stellasaju.com/zodiac-year/' });
  var w = dom.window;
  /* 쪽의 「내 띠 찾기」를 흉내 냅니다 — 입춘(2월 4일) 앞이면 앞 해 */
  w.document.getElementById('zFind').addEventListener('click', function(){
    var y = parseInt(w.document.getElementById('zYear').value, 10);
    var m = parseInt(w.document.getElementById('zMon').value, 10) || 0;
    var d = parseInt(w.document.getElementById('zDay').value, 10) || 0;
    if(!y){ return; }
    var sy = y;
    if(m < 2){ sy = y - 1; }
    else if(m === 2 && d < 4){ sy = y - 1; }
    var z = ((sy - 4) % 12 + 12) % 12;
    var c = w.document.getElementById('zc' + z);
    if(c){ c.classList.add('mine'); }
  });
  if(user){ w.STELLA_USER = user; }
  w.eval(JS);
  var ev = w.document.createEvent('Event');
  ev.initEvent('DOMContentLoaded', true, true);
  w.document.dispatchEvent(ev);
  return w;
}

console.log('=== ① 띠 그림이 들어갔나');
var w = make({ profile: { year: 1975, month: 1, day: 23 } });
var imgs = w.document.querySelectorAll('#ssp .asym img');
console.log('  그림 : ' + imgs.length + '장 (열두 장이어야 합니다)');
console.log('  범띠 : ' + w.document.querySelector('#zc2 .asym img').getAttribute('src'));
console.log('  alt  : ' + w.document.querySelector('#zc2 .asym img').getAttribute('alt'));
console.log('  앰퍼샌드 : ' + (w.document.body.innerHTML.indexOf(String.fromCharCode(38) + 'resize') > -1 ? '★ 있음' : '없음 ok'));

console.log('');
console.log('=== ② 내 띠 강조 — 1975년 1월 23일 (입춘 앞 → 범띠)');
var mine = w.document.querySelector('.acard.mine');
console.log('  강조된 칸 : ' + (mine ? mine.querySelector('.aname').textContent : '★ 없음'));
console.log('  칸에 채워진 값 : ' + w.document.getElementById('zYear').value
  + ' / ' + w.document.getElementById('zMon').value
  + ' / ' + w.document.getElementById('zDay').value);

console.log('');
console.log('=== ③ 딱지의 한자말이 쉬운 말로');
var rs = w.document.querySelectorAll('#ssp .arel');
var seen = {};
for(var i = 0; i < rs.length; i++){
  var t = rs[i].textContent.trim();
  var k = rs[i].getAttribute('data-rel');
  if(seen[t]){ continue; }
  seen[t] = 1;
  console.log('  ' + ANIMAL[i] + '띠  「' + t + '」  갈래=' + k);
}
var han = ['삼합','육합','무관','충'].filter(function(x){
  return w.document.querySelector('#ssp .agrid').textContent.indexOf(x) > -1; });
console.log('  남은 한자말 : ' + (han.length ? '★ ' + han.join(' ') : '없음 ok'));

console.log('');
console.log('=== ④ 안 들어오신 분 — 그림만 바뀌고 강조는 없어야 합니다');
var w2 = make(null);
console.log('  그림 : ' + w2.document.querySelectorAll('#ssp .asym img').length + '장');
console.log('  강조 : ' + (w2.document.querySelector('.acard.mine') ? '★ 붙음' : '안 붙음 ok'));

console.log('');
console.log('=== ⑤ 두 번 돌려도 한 번만');
var before = w.document.querySelectorAll('#ssp .asym img').length;
w.eval(JS.replace('window.StellaLook', 'window.StellaLookX'));
var after = w.document.querySelectorAll('#ssp .asym img').length;
console.log('  그림 ' + before + ' → ' + after + (before === after ? '  ok' : '  ★ 늘었습니다'));

setTimeout(function(){ process.exit(0); }, 60);
