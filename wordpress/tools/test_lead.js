/* patch160_lead 검사 — jsdom
   실제 책(reading-book)의 쪽 제목을 그대로 쓴 가짜 책으로 돌려봅니다.
   실행 : node wordpress/tools/test_lead.js                               */
var fs = require('fs'), path = require('path');
var { JSDOM } = require('jsdom');

var HERE = path.join(__dirname, '..');
var php  = fs.readFileSync(path.join(HERE, 'php/patch160_lead.php'), 'utf8');
var out  = php.split('?>')[1]; out = out.slice(0, out.lastIndexOf('<?php'));
var JS   = out.match(/<script>([\s\S]*?)<\/script>/)[1];

/* 살아 있는 책의 차례 그대로 (삼재 · door-fortune) */
var BOOK = [
  ['cover',  '',        ''],
  ['',       '',        ''],                       /* 가디언 한마디 — 제목 없음 */
  ['',       '시각을 먼저 바로잡습니다', ''],
  ['',       '여덟 글자', ''],
  ['',       '기운의 저울', ''],
  ['',       '십 년마다 바뀌는 판', ''],
  ['',       '태어나던 밤의 하늘', ''],
  ['',       '여덟 글자가 서로 부딪히는 자리', ''],
  ['',       '당신이 아무 말도 하기 전에', ''],
  ['turn',   '사주를 삼재로 풀어보면', '1부 · 묻기 전에 읽은 것'],
  ['',       '당신이 답해주신 것', ''],
  ['',       '적어주신 말', ''],
  ['',       '타고난 성향과 적어주신 현재의 생활이 맞지 않은 부분을 정리해보았습니다', ''],
  ['',       '타고난 성향과 실제 생활이 다른 부분 — 남은 셋', ''],
  ['',       '앞으로 십 년의 대운', '삼재'],        /* ← 여기부터 본론 */
  ['',       '지금 판과 다음 판', '삼재'],
  ['',       '올해의 달별 흐름', '삼재'],
  ['',       '인생의 큰 전환점', '삼재'],
  ['',       '소희님, 세 가지만 기억하세요', '맺음말'],
  ['close',  '소희님께', '맺음말'],
  ['',       '', '']                               /* 배웅 */
];

function make(rows, url){
  var h = '<div id="ssb"><div class="book" id="bkBook">';
  rows.forEach(function(r, i){
    h += '<div class="page' + (r[0] ? ' ' + r[0] : '') + '">'
      + (r[2] ? '<p class="eyebrow">' + r[2] + '</p>' : '')
      + (r[1] ? '<h2>' + r[1] + '</h2>' : '')
      + (r[0] === 'cover' ? '' : '<div class="folio">' + (i < 9 ? '0' : '') + (i + 1) + '</div>')
      + '</div>';
  });
  h += '</div></div>';
  var dom = new JSDOM('<!doctype html><html><body>' + h + '</body></html>',
    { runScripts: 'outside-only', url: url || 'https://stellasaju.com/reading-book/' });
  dom.window.eval(JS);
  /* jsdom 은 DOMContentLoaded 를 다음 틱에 쏩니다. 조각이 그것을 기다리고
     있을 수 있으므로 여기서 한 번 흉내 내 줍니다 — 안 그러면 검사가
     「아무 일도 안 일어났다」고 잘못 말합니다 (2026-09-14 에 걸렸습니다). */
  var ev = dom.window.document.createEvent('Event');
  ev.initEvent('DOMContentLoaded', true, true);
  dom.window.document.dispatchEvent(ev);
  return dom.window;
}

function order(w){
  var bk = w.document.getElementById('bkBook');
  var o = [], i, k = bk.children;
  for(i = 0; i < k.length; i++){
    if(k[i].className.indexOf('page') < 0){ continue; }
    var h = k[i].querySelector('h2');
    var e = k[i].querySelector('.eyebrow');
    var f = k[i].querySelector('.folio');
    o.push((f ? f.textContent : '--') + ' ' + (h ? h.textContent : (e ? '(' + e.textContent + ')' : '(제목 없음)')));
  }
  return o;
}

console.log('=== ① 삼재 책 — 옮긴 뒤 차례');
var w1 = make(BOOK);
order(w1).forEach(function(l){ console.log('   ' + l); });
var o1 = order(w1);
var bodyAt = o1.findIndex(function(l){ return l.indexOf('앞으로 십 년의 대운') > -1; });
console.log('   본론까지 : ' + bodyAt + '쪽  (옮기기 전 14쪽)');
console.log('   깃발      : ' + w1.document.getElementById('bkBook').getAttribute('data-lead'));

console.log('');
console.log('=== ② 자료 제목이 하나도 없는 책 — 손대지 않아야 합니다');
var NONE = [['cover','',''],['','우리 주제 하나',''],['','둘',''],['','셋',''],
             ['','넷',''],['','다섯',''],['close','소희님께','맺음말']];
var w2 = make(NONE);
console.log('   차례 : ' + order(w2).join(' | '));
console.log('   깃발 : ' + w2.document.getElementById('bkBook').getAttribute('data-lead'));

console.log('');
console.log('=== ③ 맺음말이 없는 책 — 맨 뒤에 붙어야 합니다');
var NOEND = [['cover','',''],['','여덟 글자',''],['','기운의 저울',''],
              ['','본론이에요',''],['','본론 둘',''],['','본론 셋',''],['','본론 넷','']];
var w3 = make(NOEND);
console.log('   차례 : ' + order(w3).join(' | '));

console.log('');
console.log('=== ④ 두 번 돌려도 한 번만');
var w4 = make(BOOK);
var a = order(w4).join('|');
w4.eval(JS.replace('window.StellaLead', 'window.StellaLeadX'));
var b = order(w4).join('|');
console.log('   같은가 : ' + (a === b ? '예 ok' : '★ 달라졌습니다'));

console.log('');
console.log('=== ⑤ 쪽번호가 1부터 빠짐없이 다시 매겨졌나');
var nums = order(w1).map(function(l){ return l.split(' ')[0]; }).filter(function(x){ return x !== '--'; });
var good = nums.every(function(v, i){ return parseInt(v, 10) === i + 2; });
console.log('   ' + nums.join(' ') + '  → ' + (good ? '차례대로 ok' : '★ 어긋납니다'));

console.log('');
console.log('=== ⑥ ?leadwhy=1 — 차례를 찍어주는가');
var w6 = make(BOOK, 'https://stellasaju.com/reading-book/?leadwhy=1');
var box = w6.document.getElementById('stellaLeadWhy');
console.log(box ? '   ' + box.textContent.split('\n').slice(0, 3).join(' / ') : '   ★ 안 나옴');

setTimeout(function(){ process.exit(0); }, 50);
