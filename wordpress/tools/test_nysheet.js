/* 신년운세 책 — 장 속표지 다음에 같은 제목이 또 나오지 않는지
   실행 : node wordpress/tools/test_nysheet.js [2026|2027]                */
var fs = require('fs'), path = require('path');
var { JSDOM } = require('jsdom');
var Y = process.argv[2] || '2026';
var HERE = path.join(__dirname, '..');
var snip = fs.readFileSync(path.join(HERE, 'php/patch160_ny' + Y + '.WPCODE.txt'), 'utf8');
var JS = snip.match(/<script>([\s\S]*?)<\/script>/)[1];

var dom = new JSDOM('<!doctype html><html><body><div id="ssb"><div class="book" id="bkBook"></div></div></body></html>',
  { runScripts: 'outside-only', url: 'https://stellasaju.com/reading-book/' });
var w = dom.window;

/* 셈에 쓰는 것만 흉내 냅니다 — build() 는 인자를 안 받고
   localStorage 의 stella_demo 와 두 엔진을 스스로 읽습니다. */
var chart = {
  five: { 목:2, 화:1, 토:2, 금:2, 수:1 },
  luck: [ { age:5, han:'壬子', kor:'임자', gan:'壬' }, { age:15, han:'癸丑', kor:'계축', gan:'癸' },
          { age:25, han:'甲寅', kor:'갑인', gan:'甲' }, { age:35, han:'乙卯', kor:'을묘', gan:'乙' },
          { age:45, han:'丙辰', kor:'병진', gan:'丙' }, { age:55, han:'丁巳', kor:'정사', gan:'丁' } ],
  pillars: { year:{han:'辛亥',kor:'신해',gan:'辛',ji:'亥'},
             month:{han:'丁酉',kor:'정유',gan:'丁',ji:'酉'},
             day:{han:'乙巳',kor:'을사',gan:'乙',ji:'巳'},
             hour:{han:'丙戌',kor:'병술',gan:'丙',ji:'戌'} }
};
var profile = { name:'이소희', firstName:'소희', year:1971, month:9, day:17,
                hour:8, minute:20, sex:'여', city:'서울', country:'KR' };

w.localStorage.setItem('stella_demo', JSON.stringify({ profile: profile }));
w.StellaSaju = {
  locate: function(){ return { lon:126.98, lat:37.57, tz:9 }; },
  compute: function(){ return chart; }
};
w.StellaRead = { interpret: function(){ return {}; } };

w.eval(JS);

if(!w.StellaNY){ console.log('★ window.StellaNY 가 없습니다'); process.exit(1); }

var pages = w.StellaNY.build();
if(!pages){ console.log('★ build() 가 아무것도 안 돌려줬습니다'); process.exit(1); }
console.log('쪽 수(build) : ' + pages.n);

var box = w.document.getElementById('bkBook');
box.innerHTML = pages.html;
var kids = box.children, i, rows = [];
for(i = 0; i < kids.length; i++){
  var el = kids[i];
  var h = el.querySelector('h2');
  var no = el.querySelector('.dvno');
  rows.push({
    divider: el.className.indexOf('divider') > -1,
    no: no ? no.textContent.trim() : '',
    title: h ? h.textContent.trim() : '(제목 없음)'
  });
}

console.log('쪽 ' + rows.length + '장');
rows.forEach(function(r, i){
  console.log('  ' + (i + 1) + '. ' + (r.divider ? '［속표지 ' + r.no + '］ ' : '') + r.title);
});

/* 속표지 바로 다음 쪽이 같은 제목이면 안 됩니다 */
var bad = 0;
for(i = 0; i + 1 < rows.length; i++){
  if(!rows[i].divider){ continue; }
  if(rows[i].title === rows[i + 1].title){
    bad++;
    console.log('  ★ ' + (i + 1) + '·' + (i + 2) + ' 쪽 제목이 겹칩니다 — ' + rows[i].title);
  }
}
console.log(bad === 0 ? '겹치는 제목 없음 ok' : '★ 겹치는 자리 ' + bad + '군데');

/* 본문 쪽이 비어 있지 않은지 — 제목만 떼고 머리글이 남아야 합니다 */
var thin = 0;
for(i = 0; i < kids.length; i++){
  if(kids[i].className.indexOf('divider') > -1){ continue; }
  var txt = kids[i].textContent.replace(/\s+/g, ' ').trim();
  if(txt.length < 40){ thin++; console.log('  ★ ' + (i + 1) + '쪽이 너무 짧습니다 (' + txt.length + '자)'); }
}
console.log(thin === 0 ? '본문 쪽 모두 살아 있음 ok' : '★ 빈 쪽 ' + thin + '장');
console.log('');
console.log('제1장 본문 첫머리 —');
console.log('  ' + kids[1].textContent.replace(/\s+/g, ' ').trim().slice(0, 150) + ' …');
setTimeout(function(){ w.close(); process.exit(0); }, 30);
