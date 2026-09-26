const {JSDOM}=require('jsdom'); const fs=require('fs');
const JS=fs.readFileSync('join.js','utf8');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
// 살아 있는 /login/ 의 그 줄들
const BODY=`<div class="wrap">
 <h1>다시 오셨네요</h1>
 <p>비밀번호는 묻지 않습니다. 가입하실 때도 만들지 않으셨으니까요.</p>
 <button>로그인 링크 받기</button>
 <p class="first">처음이신가요? <a href="/door-career/">무료로 시작하기 →</a></p>
</div>`;
(async()=>{
  for(const url of ['https://stellasaju.com/login/','https://stellasaju.com/mypage/']){
    const dom=new JSDOM(`<!doctype html><body>${BODY}</body>`,
      {url, runScripts:'dangerously', pretendToBeVisual:true});
    const w=dom.window;
    const s=w.document.createElement('script'); s.textContent=JS; w.document.body.appendChild(s);
    await sleep(150);
    const n=w.document.getElementById('joinNote');
    console.log('%s → 안내 %s', url.replace('https://stellasaju.com',''), n?'붙음 ○':'안 붙음');
    if(n){
      console.log('   ' + n.textContent.replace(/\s+/g,' ').trim());
      console.log('   자리: 「처음이신가요」 바로 뒤인가 → ' +
        (w.document.querySelector('.first').nextSibling===n?'맞음 ok':'★아님'));
      // 두 번 돌려도 하나
      const s2=w.document.createElement('script'); s2.textContent=JS; w.document.body.appendChild(s2);
      await sleep(120);
      console.log('   안내 개수 ' + w.document.querySelectorAll('#joinNote').length + ' (1 이어야 합니다)');
    }
    w.close();
  }
  process.exit(0);
})();
