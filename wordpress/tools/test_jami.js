/* patch171_jami 검사 — 살아 있는 door-astro 쪽 글을 그대로 써서 돌립니다
   실행 : node wordpress/tools/test_jami.js                             */
var fs = require('fs'), path = require('path');
var { JSDOM } = require('jsdom');

var HERE = path.join(__dirname, '..');
var php  = fs.readFileSync(path.join(HERE, 'php/patch171_jami.php'), 'utf8');
var parts = php.split('?>').slice(1).map(function(s){
  var i = s.lastIndexOf('<?php');
  return i > -1 ? s.slice(0, i) : s;
});
var all = parts.join('');
var scripts = all.match(/<script>[\s\S]*?<\/script>/g).map(function(s){
  return s.replace(/^<script>/, '').replace(/<\/script>$/, '');
});
var JS_DOOR = scripts[0], JS_MENU = scripts[1];

/* 살아 있는 문 쪽의 뼈대 (door-astro.html 에서 추린 것) */
var DOOR = [
'<header><nav>',
'  <a href="/door-career/">마루 · 일과 돈</a>',
'  <a href="/door-astro/">아라 · 점성술</a>',
'  <a href="/door-tarot/">아르카나 · 타로</a>',
'</nav></header>',
'<div id="ssg" style="--g-accent:#86B4D8">',
'  <div class="g-head">',
'    <div class="g-name">아라</div>',
'    <div class="g-en">Western Astrology</div>',
'  </div>',
'  <p class="g-intro">아라는 당신이 태어난 순간의 하늘을 그대로 펼쳐…</p>',
'  <section class="step"><span class="step-no">STEP 1</span>',
'    <input type="text" id="gName"><select id="gSex"></select>',
'    <input type="number" id="gYear"></section>',
'  <section class="step"><span class="step-no">STEP 2</span>',
'    <input type="text" id="gJob"></section>',
'  <section class="step"><span class="step-no">STEP 3</span>',
'    <input type="text" id="gWant"></section>',
'  <div class="gowrap"><button type="button" class="go" id="goBtn">아라에게 물어보기 →</button></div>',
'</div>'
].join('\n');

function make(html, url){
  var dom = new JSDOM('<!doctype html><html><body>' + html + '</body></html>',
    { runScripts: 'outside-only', url: url });
  return dom.window;
}

console.log('=== ① 문 쪽 (door-astro)');
var w = make(DOOR, 'https://stellasaju.com/door-astro/');
w.eval(JS_DOOR);
w.eval(JS_MENU);
var ev = w.document.createEvent('Event');
ev.initEvent('DOMContentLoaded', true, true);
w.document.dispatchEvent(ev);

var box = w.document.getElementById('jamiBox');
console.log('  안내 상자 : ' + (box ? box.querySelector('h3').textContent.trim() : '★ 안 나옴'));
console.log('  영문 이름 : ' + w.document.querySelector('.g-en').textContent);
console.log('  가디언    : ' + w.document.querySelector('.g-name').textContent);
var steps = w.document.querySelectorAll('#ssg .step');
var hidden = 0, shown = 0, i;
for(i = 0; i < steps.length; i++){
  if(steps[i].className.indexOf('jm-hide') > -1){ hidden++; } else { shown++; }
}
console.log('  STEP 칸   : 감춤 ' + hidden + ' · 남음 ' + shown + (shown === 0 ? '  ok' : '  ★ 남아 있습니다'));
var btn = w.document.getElementById('goBtn');
var bw = btn.parentNode;
console.log('  물어보기 단추 : '
  + (bw.className.indexOf('jm-hide') > -1 ? '감춰짐' : '★ 보임')
  + ' · ' + (btn.disabled ? '눌러도 안 먹힘 ok' : '★ 살아 있음'));
console.log('  자리      : ' + (box.nextElementSibling === steps[0] ? 'STEP 앞 ok' : '★ 엉뚱한 자리'));
var doors = box.querySelectorAll('.jm-doors a');
console.log('  다른 문   : ' + doors.length + '개 — '
  + Array.prototype.map.call(doors, function(a){ return a.textContent.trim().split(' ')[0]; }).join(' '));
var ml = w.document.querySelector('a[href="/door-astro/"]');
console.log('  차림표    : ' + (ml.getAttribute('data-jami') === '1' ? '고리에 깃발 ok' : '★ 깃발 없음')
  + ' · 감춘 칸 = ' + (w.document.querySelectorAll('[data-jamihide="1"]').length) + '개');

console.log('');
console.log('=== ② 다른 쪽에서는 차림표만');
var OTHER = '<header><nav><ul>'
  + '<li class="mi"><a href="/door-astro/">아라 · 점성술</a></li>'
  + '<li class="mi"><a href="/door-love/">벼리 · 연애와 결혼</a></li>'
  + '</ul></nav></header>'
  + '<div class="cards"><div class="one"><a href="/door-astro/"><img src="x.jpg" alt="아라"></a></div></div>'
  + '<div id="main">홈입니다</div>';
var w2 = make(OTHER, 'https://stellasaju.com/');
w2.eval(JS_MENU);
var ev2 = w2.document.createEvent('Event');
ev2.initEvent('DOMContentLoaded', true, true);
w2.document.dispatchEvent(ev2);
var links = w2.document.querySelectorAll('a[href="/door-astro/"]');
var hid = w2.document.querySelectorAll('[data-jamihide="1"]');
console.log('  door-astro 고리 : ' + links.length + '개 · 감춰진 칸 ' + hid.length + '개'
  + (hid.length === links.length ? '  둘 다 감춤 ok' : '  ★ 안 맞습니다'));
console.log('  사진 고리도 : ' + (links[1].closest('[data-jamihide="1"]') ? '감춤 ok' : '★ 남아 있음'));
var lv = w2.document.querySelector('a[href="/door-love/"]');
console.log('  다른 문   : ' + lv.textContent + ' · 감춰졌나 = '
  + (lv.parentNode.getAttribute('data-jamihide') === '1' ? '★ 감춰짐' : '아니요 ok'));
console.log('  감춘 것   : ' + Array.prototype.map.call(hid, function(n){
  return n.tagName.toLowerCase() + (n.className ? '.' + n.className : ''); }).join(' · '));
console.log('  jamiBox   : ' + (w2.document.getElementById('jamiBox') ? '★ 딴 쪽에 붙음' : '안 붙음 ok'));

console.log('');
console.log('=== ③ STEP 을 못 찾으면 아무것도 안 해야 합니다');
var BARE = '<div id="ssg"><div class="g-name">아라</div><p>글만 있습니다</p></div>';
var w3 = make(BARE, 'https://stellasaju.com/door-astro/');
w3.eval(JS_DOOR);
var ev3 = w3.document.createEvent('Event');
ev3.initEvent('DOMContentLoaded', true, true);
w3.document.dispatchEvent(ev3);
console.log('  안내 상자 : ' + (w3.document.getElementById('jamiBox') ? '★ 붙었습니다' : '안 붙음 ok'));
console.log('  깃발      : ' + (w3.document.getElementById('ssg').getAttribute('data-jami') || '없음 ok'));

setTimeout(function(){ process.exit(0); }, 60);
