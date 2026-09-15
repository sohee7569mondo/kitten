const {JSDOM}=require('jsdom'); const fs=require('fs');
const JS=fs.readFileSync('orbword.js','utf8');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
// 살아 있는 door-love 에서 실제로 나온 문장 + 그 밖의 꼴
const BODY=`
 <p>결제하신 풀이는 「내 자리」에서 1년간 다시 보실 수 있습니다.<br>구슬은 충전일로부터 1년간 유효합니다.<br>본 콘텐츠는 참고용입니다.</p>
 <button>구슬로 먼저 충전하기</button>
 <h3>구슬 충전</h3>
 <div>충전 내역</div>
 <p>미리 충전해 두는 것이 없습니다.</p>
 <script>var x='충전일로부터';</script>
 <textarea>충전하기</textarea>
`;
(async(q)=>{
  const dom=new JSDOM(`<!doctype html><body>${BODY}</body>`,
    {url:'https://stellasaju.com/door-love/'+(q||''), runScripts:'dangerously', pretendToBeVisual:true});
  const w=dom.window;
  const s=w.document.createElement('script'); s.textContent=JS; w.document.body.appendChild(s);
  await sleep(120);
  // 눈에 보이는 글만 — script · textarea 는 뺍니다
  const vis=[...w.document.body.querySelectorAll('p,button,h3,div')]
    .map(e=>e.textContent).join(' ').replace(/\s+/g,' ');
  const t=vis;
  console.log('=== 바뀐 글');
  ['충전일로부터','구슬로 먼저 충전하기','구슬 충전','충전 내역','받으신 날로부터','결제 내역','결제하고 바로 보기']
    .forEach(k=>{const n=(t.match(new RegExp(k,'g'))||[]).length;
       console.log('   '+k.padEnd(20)+' '+n+' 번');});
  console.log('\n   script 안은 안 건드렸나: %s',
    w.document.querySelector('script').textContent.indexOf('충전일로부터')>=0?'그대로 ok':'★건드림');
  console.log('   textarea 안은 안 건드렸나: %s',
    w.document.querySelector('textarea').textContent.indexOf('충전하기')>=0?'그대로 ok':'★건드림');
  console.log('   「미리 충전해 두는 것이 없습니다」 남았나: %s',
    t.indexOf('미리 충전해 두는 것이 없습니다')>=0?'남음 ok (부정문이라 살려야 합니다)':'★사라짐');
})(process.argv[2]);
