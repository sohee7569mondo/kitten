/* patch160_pricetext 검사 — 살아 있는 /price/ 글 토막을 그대로 붙여 돌립니다
   실행 : node wordpress/tools/test_pricetext.js                            */
var fs = require('fs'), path = require('path');
var { JSDOM } = require('jsdom');
var HERE = path.join(__dirname, '..');
var php = fs.readFileSync(path.join(HERE, 'php/patch160_pricetext.php'), 'utf8');
var out = php.split('?>')[1]; out = out.slice(0, out.lastIndexOf('<?php'));
var JS = out.match(/<script>([\s\S]*?)<\/script>/)[1];

/* 2026-09-14 에 워드프레스에서 그대로 떠온 토막입니다 */
var PAGE = [
'<div id="ssp"><div class="wrap">',
'<h1>가격 안내</h1>',
'<p class="dek">미리 충전해 두는 것이 없습니다.<br>',
'  풀이를 열 때, 그 한 편의 값만 치르시면 됩니다.</p>',
'<section><h2>가입하시면 드리는 것</h2>',
'<p class="sub">값을 치르지 않고도 두 편을 보실 수 있습니다.</p>',
'<div class="free"><p><b>가입하시면 구슬 3개를 드립니다.</b> 가입 축하 2개 + 여는 기념 1개예요.<br>',
'  풀이 한 편이 3구슬이니, <b>첫 한 편은 값을 치르지 않으셔도 됩니다.</b></p></div></section>',
'<section><h2>구슬이 뭐예요</h2>',
'<p class="sub">값을 세는 단위입니다. 따로 사실 수는 없습니다.</p>',
'<p>구슬은 풀이의 값을 세는 단위입니다. <b>구슬 한 개가 1,000원</b>이에요.',
'  <b>구슬만 따로 구매하실 수는 없습니다.</b>',
'  풀이를 여실 때 모자란 만큼만 그 자리에서 결제하시고, 그 즉시 쓰입니다.',
'  결제하신 뒤에 남는 구슬은 없습니다.</p></section>',
'</div></div>'
].join('\n');

function run(url){
  var dom = new JSDOM('<!doctype html><html><body>' + PAGE + '</body></html>',
    { runScripts: 'outside-only', url: url || 'https://stellasaju.com/price/' });
  dom.window.eval(JS);
  return dom.window;
}

function text(w, sel){
  var el = w.document.querySelector(sel);
  return el ? el.textContent.replace(/\s+/g, ' ').trim() : '(없음)';
}

var w = run();
console.log('① 맨 위 한 줄');
console.log('   ' + text(w, '.dek'));
console.log('   「충전」 남았나 : ' + (text(w, '.dek').indexOf('충전') > -1 ? '★ 남음' : '없음 ok'));
console.log('');
console.log('② 가입하시면 드리는 것 — 작은 글');
console.log('   ' + text(w, 'section .sub'));
console.log('');
console.log('③ 구슬이 뭐예요 — 본문');
var ps = w.document.querySelectorAll('section p');
console.log('   ' + ps[ps.length - 1].textContent.replace(/\s+/g, ' ').trim());
console.log('   1,000원 남았나 : ' + (w.document.body.textContent.indexOf('1,000원') > -1 ? '★ 남음' : '없음 ok'));
console.log('');
console.log('④ 쪽 전체에 「충전」이 남아 있나 : '
  + (w.document.body.textContent.indexOf('충전') > -1 ? '★ 남음' : '없음 ok'));
console.log('');
console.log('⑤ ?pricewhy=1');
var w2 = run('https://stellasaju.com/price/?pricewhy=1');
var box = w2.document.getElementById('stellaPriceWhy');
console.log(box ? box.textContent.split('\n').filter(function(l){ return l.trim(); }).map(function(l){ return '   ' + l; }).join('\n') : '   ★ 안 나옴');
setTimeout(function(){ process.exit(0); }, 40);
