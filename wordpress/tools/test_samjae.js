/* patch92_samjae 검사
   ① 삼재 셈이 맞는가 — 알려진 해와 대봅니다
   ② 띠별운세 쪽 뼈대에 실제로 붙는가 (jsdom)
   실행 : node wordpress/tools/test_samjae.js                        */
var fs = require('fs'), path = require('path');
var { JSDOM } = require('jsdom');

var HERE = path.join(__dirname, '..');
var php  = fs.readFileSync(path.join(HERE, 'php/patch92_samjae.php'), 'utf8');
var out  = php.split('?>')[1]; out = out.slice(0, out.lastIndexOf('<?php'));
var JS   = out.match(/<script>([\s\S]*?)<\/script>/)[1];

var ANIMAL = ['쥐','소','범','토끼','용','뱀','말','양','원숭이','닭','개','돼지'];
var START = [2, 11, 8, 5];
var NAME = ['들삼재', '눌삼재', '날삼재'];

function jiOf(y){ return ((y + 8) % 12 + 12) % 12; }
function stageOf(z, ji){
  var s = START[((z % 4) + 4) % 4];
  var k = ((ji - s) % 12 + 12) % 12;
  return k > 2 ? -1 : k;
}
function samjaeOf(y){
  var ji = jiOf(y), out = [], z;
  for(z = 0; z < 12; z++){
    var s = stageOf(z, ji);
    if(s >= 0){ out.push({ z: z, stage: s }); }
  }
  return out;
}

console.log('=== ① 해마다 어느 띠가 삼재인가');
var JIK = ['자','축','인','묘','진','사','오','미','신','유','술','해'];
for(var y = 2022; y <= 2033; y++){
  var r = samjaeOf(y);
  console.log('  ' + y + ' (' + JIK[jiOf(y)] + '년)  '
    + r.map(function(x){ return ANIMAL[x.z] + '띠'; }).join(' · ')
    + '   ' + (r.length ? NAME[r[0].stage] : ''));
}

/* 알려진 답과 대봅니다 */
var WANT = {
  2022: ['원숭이','쥐','용',   '들삼재'],
  2023: ['원숭이','쥐','용',   '눌삼재'],
  2024: ['원숭이','쥐','용',   '날삼재'],
  2025: ['토끼','양','돼지',   '들삼재'],
  2026: ['토끼','양','돼지',   '눌삼재'],
  2027: ['토끼','양','돼지',   '날삼재'],
  2028: ['범','말','개',       '들삼재'],
  2031: ['소','뱀','닭',       '들삼재']
};
var bad = 0;
Object.keys(WANT).forEach(function(y){
  var r = samjaeOf(parseInt(y, 10));
  var got = r.map(function(x){ return ANIMAL[x.z]; }).sort().join(',');
  var want = WANT[y].slice(0, 3).sort().join(',');
  var gs = NAME[r[0].stage], ws = WANT[y][3];
  if(got !== want || gs !== ws){
    bad++;
    console.log('  ★ ' + y + ' — 나온 것 ' + got + '(' + gs + ') / 맞는 것 ' + want + '(' + ws + ')');
  }
});
console.log(bad === 0 ? '  여덟 해 다 맞습니다 ok' : '  ★ 어긋난 해 ' + bad);

console.log('');
console.log('=== ② 쪽에 실제로 붙는가');
var cards = '';
for(var z = 0; z < 12; z++){
  cards += '<div class="acard" data-z="' + z + '" id="zc' + z + '">'
    + '<div class="ahead"><div><div class="aname">' + ANIMAL[z] + '띠</div></div></div>'
    + '<p class="atext">이번주 이야기</p>'
    + '<p class="amine" style="display:none">지금 보고 계신 띠예요.</p></div>';
}
var PAGE = '<div id="ssp"><div class="wrap"><div class="agrid" id="zGrid">' + cards + '</div></div></div>';

var dom = new JSDOM('<!doctype html><html><body>' + PAGE + '</body></html>',
  { runScripts: 'outside-only', url: 'https://stellasaju.com/zodiac-year/' });
var w = dom.window;
w.eval(JS);
var ev = w.document.createEvent('Event');
ev.initEvent('DOMContentLoaded', true, true);
w.document.dispatchEvent(ev);

var box = w.document.getElementById('sjBox');
console.log('  안내 상자 : ' + (box ? box.querySelector('h3').textContent : '★ 안 나옴'));
if(box){
  console.log('  단추      : ' + box.querySelector('.sj-go').textContent.trim());
  console.log('  단추 주소 : ' + box.querySelector('.sj-go').getAttribute('href'));
  console.log('  자리      : ' + (box.nextElementSibling === w.document.getElementById('zGrid')
    ? '열두 칸 바로 위 ok' : '★ 엉뚱한 자리'));
}
var marked = w.document.querySelectorAll('.acard[data-samjae]');
console.log('  딱지 붙은 칸 : ' + marked.length + '개 (셋이어야 합니다)');
for(var i = 0; i < marked.length; i++){
  var nm = marked[i].querySelector('.aname').textContent.trim();
  var ln = marked[i].querySelector('.sj-line p').textContent.trim();
  console.log('    ' + nm + '  |  ' + ln.slice(0, 46) + ' …');
}
var clean = w.document.querySelectorAll('.acard:not([data-samjae])');
var dirty = 0;
for(i = 0; i < clean.length; i++){ if(clean[i].querySelector('.sj-line')){ dirty++; } }
console.log('  나머지 아홉 칸 : ' + (dirty === 0 ? '한 자도 안 건드림 ok' : '★ ' + dirty + '칸이 더러워짐'));

/* 두 번 돌려도 한 번만 */
var before = w.document.querySelectorAll('.sj-tag').length;
w.eval(JS.replace('window.StellaSamjae', 'window.StellaSamjaeX'));
var after = w.document.querySelectorAll('.sj-tag').length;
console.log('  두 번 돌려도 : ' + (before === after ? '딱지 ' + after + '개 그대로 ok' : '★ ' + before + ' → ' + after));

setTimeout(function(){ process.exit(0); }, 60);
