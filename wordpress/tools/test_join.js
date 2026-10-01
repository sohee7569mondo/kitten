const {JSDOM}=require('jsdom'); const fs=require('fs');
const JS=fs.readFileSync('join.js','utf8');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
// 살아 있는 머리글 · 마이페이지의 그 줄들을 그대로
const BODY=`
 <nav>
  <div class="ssnav-item" id="ssnav-auth"><a class="ssnav-top" href="/login/">로그인</a></div>
  <div class="ssnav-item" id="ssnav-join"><a class="ssnav-top" href="/door-career/">가입</a></div>
 </nav>
 <div id="my">
  <a href="/signin/?join=1">가입하기 →</a>
  <a class="alt" href="/signin/">이미 가입했어요</a>
 </div>
 <a href="/door-career/">마루 · 일과 돈</a>
 <a href="https://stellasaju.com/door-career/">가입</a>
`;
(async()=>{
  const dom=new JSDOM(`<!doctype html><body>${BODY}</body>`,
    {url:'https://stellasaju.com/mypage/', runScripts:'dangerously', pretendToBeVisual:true});
  const w=dom.window;
  const s=w.document.createElement('script'); s.textContent=JS; w.document.body.appendChild(s);
  await sleep(120);
  console.log('=== 고친 뒤');
  [...w.document.querySelectorAll('a')].forEach(a=>
    console.log('   %s  →  %s', (a.textContent.trim()||'-').padEnd(16), a.getAttribute('href')));
  // 링크만 셉니다 — 아래에 붙인 script 글까지 세면 안 됩니다
  const bad=[...w.document.querySelectorAll('a')]
    .filter(a=>String(a.getAttribute('href')).indexOf('/signin/')>=0);
  console.log('\n   /signin/ 으로 가는 링크 '+bad.length+' 개 (0 이어야 합니다)');
  console.log('   「가입」이라 적힌 단추 %d (0 이어야 합니다)',
    [...w.document.querySelectorAll('a')].filter(a=>a.textContent.trim()==='가입').length);
  console.log('   문으로 가는 보통 링크는 그대로: %s',
    [...w.document.querySelectorAll('a')].some(a=>a.textContent.indexOf('마루')>=0 && a.getAttribute('href')==='/door-career/')?'ok':'★건드림');
})();
