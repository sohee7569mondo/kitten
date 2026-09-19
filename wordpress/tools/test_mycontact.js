/* patch160_mycontact 검사 — jsdom
   ① 이메일·휴대폰 둘 다 있을 때
   ② 가짜 이메일 · 전화 없음 → 고쳐 넣기
   ③ 안 들어온 분 (member:false) → 칸이 안 붙되 제목은 바뀜
   실행 : node wordpress/tools/test_mycontact.js            */
var fs = require('fs');
var path = require('path');
var { JSDOM } = require('jsdom');

var HERE = path.join(__dirname, '..');
var php  = fs.readFileSync(path.join(HERE, 'php/patch160_mycontact.php'), 'utf8');
var out  = php.split('?>')[1];
out = out.slice(0, out.lastIndexOf('<?php'));
var JS = out.match(/<script>([\s\S]*?)<\/script>/)[1];

/* 살아 있는 마이페이지의 뼈대 — 구슬 칸이 든 section */
var PAGE = fs.readFileSync(path.join(HERE, 'pages/mypage.html'), 'utf8');

function run(name, contact, then){
  var dom = new JSDOM('<!doctype html><html><body>' + PAGE + '</body></html>',
                      { runScripts: 'outside-only', url: 'https://stellasaju.com/mypage/' });
  var w = dom.window;
  var sent = [];
  w.fetch = function(url, opt){
    if(url.indexOf('/contact') > -1){
      return Promise.resolve({ ok:true, json:function(){ return Promise.resolve(contact); } });
    }
    var body = JSON.parse(opt.body);
    sent.push(url + ' ' + opt.body);
    var j = { ok:true };
    if(url.indexOf('/email') > -1){ j.email = body.email; }
    if(url.indexOf('/myphone') > -1){
      j.phone = String(body.phone).replace(/[^0-9]/g,'')
                 .replace(/^(\d{3})(\d{4})(\d{4})$/, '$1-$2-$3');
    }
    return Promise.resolve({ ok:true, json:function(){ return Promise.resolve(j); } });
  };
  w.eval(JS);
  setTimeout(function(){
    console.log('=== ' + name);
    var h1 = w.document.querySelector('h1');
    console.log('   큰 제목 : ' + h1.textContent);
    var box = w.document.getElementById('ctBox');
    if(!box){ console.log('   연락처 칸 : 안 붙음'); w.close(); then && then(); return; }
    var num = w.document.getElementById('oNum');
    var sec = num; while(sec && sec.tagName !== 'SECTION'){ sec = sec.parentNode; }
    console.log('   자리    : ' + (sec.nextElementSibling === box ? '구슬 칸 바로 뒤 ok' : '★ 엉뚱한 자리'));
    console.log('   이메일  : ' + w.document.getElementById('ctMail').textContent
                + ' (' + w.document.getElementById('ctMail').className + ')');
    console.log('   휴대폰  : ' + w.document.getElementById('ctPhone').textContent
                + ' (' + w.document.getElementById('ctPhone').className + ')');
    if(then){ then(w, sent, function(){ w.close(); }); } else { w.close(); }
  }, 60);
}

run('① 둘 다 있을 때', { member:true, email:'abc@gmail.com', phone:'010-9999-8888' });

setTimeout(function(){
  run('② 가짜 이메일 · 전화 없음', { member:true, email:'', phone:'' }, function(w, sent, done){
    w.document.getElementById('ctMailEdit').click();
    w.document.getElementById('ctMailIn').value = 'me@naver.com';
    w.document.getElementById('ctMailGo').click();
    w.document.getElementById('ctPhoneEdit').click();
    w.document.getElementById('ctPhoneIn').value = '010 1234 5678';
    w.document.getElementById('ctPhoneGo').click();
    setTimeout(function(){
      sent.forEach(function(s){ console.log('   보냄    : ' + s); });
      console.log('   이메일  : ' + w.document.getElementById('ctMail').textContent);
      console.log('   휴대폰  : ' + w.document.getElementById('ctPhone').textContent);
      console.log('   말      : ' + w.document.getElementById('ctPhoneSay').textContent);
      done();
    }, 60);
  });
}, 400);

setTimeout(function(){
  run('③ 안 들어온 분', { member:false });
}, 900);

setTimeout(function(){ process.exit(0); }, 1600);
