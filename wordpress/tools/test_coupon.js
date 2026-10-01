const {JSDOM}=require('jsdom'); const fs=require('fs');
const JS=fs.readFileSync('coupon.js','utf8');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
// 마이페이지의 구슬 칸을 흉내냅니다
const BODY=`<div id="ssm"><div class="wrap">
 <section><h2>구슬</h2><p class="sub">풀이 한 번에 쓰는 값입니다.</p>
   <div class="orb"><span id="oNum">938</span></div></section>
 <section><h2>친구 추천</h2></section>
</div></div>`;
(async()=>{
  const dom=new JSDOM(`<!doctype html><body>${BODY}</body>`,
    {url:'https://stellasaju.com/mypage/', runScripts:'dangerously', pretendToBeVisual:true});
  const w=dom.window;
  let sent=null;
  w.fetch=function(u,o){ sent={u:u,body:JSON.parse(o.body)};
    return Promise.resolve({ok:true, json:()=>Promise.resolve({ok:true,orbs:30,balance:968,name:'친구 쿠폰'})}); };
  const s=w.document.createElement('script'); s.textContent=JS; w.document.body.appendChild(s);
  await sleep(150);
  const d=w.document;
  const box=d.getElementById('cpnBox');
  console.log('쿠폰 칸 붙었나 : ' + (box?'○':'★없음'));
  console.log('  자리          : 구슬 칸 바로 뒤인가 → ' +
    (d.querySelectorAll('section')[1].id==='cpnBox'?'맞음 ok':'★아님'));
  d.getElementById('cpnIn').value=' FRIEND1974 ';
  d.getElementById('cpnGo').click();
  await sleep(120);
  console.log('  서버로 보낸 것 : ' + sent.u + '  ' + JSON.stringify(sent.body));
  console.log('  알림           : ' + d.getElementById('cpnSay').textContent);
  console.log('  잔액 바뀌었나  : ' + d.getElementById('oNum').textContent);
  // 두 번 돌려도 칸이 하나
  const s2=d.createElement('script'); s2.textContent=JS; d.body.appendChild(s2);
  await sleep(120);
  console.log('  쿠폰 칸 개수   : ' + d.querySelectorAll('#cpnBox').length + ' (1 이어야 합니다)');
  w.close(); process.exit(0);
})();
