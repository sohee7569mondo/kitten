const {JSDOM}=require('jsdom'); const fs=require('fs');
const JS=fs.readFileSync('coupon.js','utf8');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const LOGIN=`<div class="wrap"><h1>다시 오셨네요</h1>
 <p class="first">처음이신가요? <a href="/door-career/">무료로 시작하기</a></p></div>`;
const MY=`<div class="wrap">
 <section><h2>구슬</h2><div><span id="oNum">938</span></div></section></div>`;
// ★ 코드를 먼저 적어두고 나서 조각을 올려야 실제와 같습니다
function make(url, body, fetchFn, seed){
  const dom=new JSDOM(`<!doctype html><body>${body}</body>`,
    {url, runScripts:'dangerously', pretendToBeVisual:true});
  if(fetchFn) dom.window.fetch=fetchFn;
  if(seed) dom.window.localStorage.setItem('stella_coupon_pending', seed);
  const s=dom.window.document.createElement('script'); s.textContent=JS;
  dom.window.document.body.appendChild(s);
  return dom.window;
}
(async()=>{
  console.log('=== ① 로그인 쪽에서 코드 적어두기');
  let w=make('https://stellasaju.com/login/', LOGIN, ()=>Promise.resolve({ok:false,json:()=>Promise.resolve({})}));
  await sleep(150);
  let d=w.document;
  console.log('   쿠폰 칸 : ' + (d.getElementById('cpnKeep')?'붙음 ○':'★없음'));
  d.getElementById('cpnKeepIn').value='friend1974';
  d.getElementById('cpnKeepGo').click();
  await sleep(60);
  console.log('   알림    : ' + d.getElementById('cpnKeepSay').textContent);
  const saved=w.localStorage.getItem('stella_coupon_pending');
  console.log('   적어둔 것: ' + saved);
  w.close();

  console.log('\n=== ② 안 들어온 채로 열면 — 코드를 지우지 않아야 합니다');
  let sent=0;
  w=make('https://stellasaju.com/mypage/', MY, function(){ sent++;
    return Promise.resolve({ok:false, json:()=>Promise.resolve({message:'먼저 들어와 주세요.',data:{status:401}})}); },
    'friend1974');
  await sleep(200);
  console.log('   보낸 횟수 : ' + sent);
  console.log('   코드 남았나: ' + (w.localStorage.getItem('stella_coupon_pending')||'★지워짐'));
  w.close();

  console.log('\n=== ③ 들어온 뒤 — 저절로 들어가야 합니다');
  w=make('https://stellasaju.com/mypage/', MY, function(){
    return Promise.resolve({ok:true, json:()=>Promise.resolve({ok:true,orbs:30,balance:968})}); },
    'friend1974');
  await sleep(250);
  console.log('   잔액      : ' + w.document.getElementById('oNum').textContent);
  console.log('   코드 지워졌나: ' + (w.localStorage.getItem('stella_coupon_pending')?'★남음':'지워짐 ok'));
  w.close(); process.exit(0);
})();
