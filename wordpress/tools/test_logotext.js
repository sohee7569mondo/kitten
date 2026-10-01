/* patch_logotext 검사 — 테마마다 다른 로고 모양을 넣어 돌려봅니다
   실행 : node wordpress/tools/test_logotext.js                        */
var fs = require('fs'), path = require('path');
var { JSDOM } = require('jsdom');
var HERE = path.join(__dirname, '..');
var php = fs.readFileSync(path.join(HERE, 'php/patch_logotext.php'), 'utf8');
var out = php.split('?>')[1]; out = out.slice(0, out.lastIndexOf('<?php'));
var JS = out.match(/<script>([\s\S]*?)<\/script>/)[1];

function run(html, name){
  var dom = new JSDOM('<!doctype html><html><body>' + html + '</body></html>',
    { runScripts: 'outside-only', url: 'https://stellasaju.com/' });
  var w = dom.window;
  w.eval(JS);
  var ev = w.document.createEvent('Event');
  ev.initEvent('DOMContentLoaded', true, true);
  w.document.dispatchEvent(ev);

  var t = w.document.querySelector('.stella-logotext');
  var hid = w.document.querySelectorAll('.stella-logohide');
  var head = w.document.querySelector('header');
  console.log('  ' + name);
  console.log('     글씨    : ' + (t ? t.textContent : '★ 안 붙음'));
  console.log('     그림    : ' + (hid.length ? hid.length + '장 감춤 ok' : '★ 안 감춰짐'));
  if(t){
    var a = t.closest('a');
    console.log('     고리    : ' + (a ? a.getAttribute('href') : '(없음)'));
    console.log('     머리글 안 : ' + (head && head.contains(t) ? '예 ok' : '아니요'));
  }
  return w;
}

console.log('=== 테마마다 다른 로고 모양');
run('<header><a href="/" rel="home"><img class="custom-logo" src="logo.png" alt="스텔라사주"></a></header>',
    '① custom-logo');
run('<header><div class="wp-block-site-logo"><a href="/"><img src="logo.png"></a></div></header>',
    '② wp-block-site-logo');
run('<header><a href="/" rel="home"><img src="x.png" alt="로고"></a></header>',
    '③ header a[rel=home] img');

console.log('');
console.log('=== 바닥글 로고는 안 건드립니다 (FOOT=0)');
var w = run('<header><a href="/"><img class="custom-logo" src="l.png"></a></header>'
  + '<footer><a href="/"><img class="custom-logo" src="l.png"></a></footer>',
  '④ 머리글 + 바닥글');
console.log('     바닥글 글씨 : '
  + (w.document.querySelector('footer .stella-logotext') ? '★ 붙었습니다' : '안 붙음 ok'));

console.log('');
console.log('=== 두 번 돌려도 한 번만');
var w2 = run('<header><a href="/"><img class="custom-logo" src="l.png"></a></header>', '⑤ 첫 판');
var before = w2.document.querySelectorAll('.stella-logotext').length;
w2.eval(JS.replace('window.StellaLogoText', 'window.StellaLogoTextX'));
var after = w2.document.querySelectorAll('.stella-logotext').length;
console.log('     글씨 ' + before + ' → ' + after + (before === after ? '  ok' : '  ★ 늘었습니다'));

setTimeout(function(){ process.exit(0); }, 60);
