const {JSDOM}=require('jsdom'); const fs=require('fs');
const JS=fs.readFileSync('join.js','utf8');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const LOGIN=`<div class="wrap">
 <h1>다시 오셨네요</h1>
 <p>비밀번호는 묻지 않습니다.</p>
 <input type="email" id="e"><button type="button" id="go">로그인 링크 받기</button>
 <p class="first">처음이신가요? <a href="/door-career/">무료로 시작하기</a></p></div>`;
(async()=>{
  const dom=new JSDOM(`<!doctype html><body>${LOGIN}</body>`,
    {url:'https://stellasaju.com/login/', runScripts:'dangerously', pretendToBeVisual:true});
  const w=dom.window;
  const s=w.document.createElement('script'); s.textContent=JS; w.document.body.appendChild(s);
  await sleep(150);
  const d=w.document;
  console.log('제목            : ' + d.querySelector('h1').textContent);
  const btn=d.querySelector('#joinNote a');
  console.log('가입 단추       : ' + (btn?btn.textContent+' → '+btn.getAttribute('href'):'★없음'));
  console.log('「링크 받기」 누르기 전 안내 : ' + (d.getElementById('lateNote')?'★벌써 떴음':'아직 없음 ok'));
  d.getElementById('go').click();
  await sleep(300);
  console.log('누른 직후                   : ' + (d.getElementById('lateNote')?'★너무 빨리 뜸':'아직 없음 ok'));
  await sleep(8200);
  const late=d.getElementById('lateNote');
  console.log('여덟 걸음 뒤                : ' + (late?'떴음 ok':'★안 뜸'));
  if(late){
    console.log('   ' + late.textContent.replace(/\s+/g,' ').trim().slice(0,90) + '…');
    console.log('   단추 : ' + late.querySelector('a').textContent);
  }
  w.close(); process.exit(0);
})();
