const {JSDOM}=require('jsdom'); const fs=require('fs');
const JS=fs.readFileSync('listprice.js','utf8');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
// 살아 있는 /pay/ 의 paint() 가 만드는 줄을 그대로 흉내냅니다
function rows(q){
  let r='';
  r += '<div class="r"><span class="l">이 풀이의 값</span><span class="v">'+q.orbs+'구슬</span></div>';
  if(q.balance>0) r += '<div class="r"><span class="l">가지고 계신 구슬</span><span class="v">-'+Math.min(q.balance,q.orbs)+'구슬</span></div>';
  r += '<div class="r total"><span class="l">내실 값</span><span class="v">'+(q.free?'0원':q.price)+'</span></div>';
  return r;
}
async function run(q){
  const dom=new JSDOM(`<!doctype html><body><div id="sso"><div class="bill"><div class="rows" id="oRows">${rows(q)}</div></div></div></body>`,
    {url:'https://stellasaju.com/pay/', runScripts:'dangerously', pretendToBeVisual:true});
  const w=dom.window;
  const s=w.document.createElement('script'); s.textContent=JS; w.document.body.appendChild(s);
  await sleep(120);
  const box=w.document.getElementById('oRows');
  const out=[...box.querySelectorAll('.r')].map(e=>
    (e.querySelector('.l').textContent+' : '+e.querySelector('.v').textContent));
  const why=w.document.querySelector('.lp-why');
  return {rows:out, why:why?why.textContent:'', twice:box.getAttribute('data-lp'), w, box};
}
(async()=>{
  console.log('=== 3구슬 · 3,000원 내는 손님');
  let r=await run({orbs:3, balance:0, free:false, price:'3,000원'});
  r.rows.forEach(x=>console.log('   '+x));
  console.log('   밑에 한 줄: '+r.why);

  console.log('\n=== 구슬이 있어 0원인 손님');
  r=await run({orbs:3, balance:938, free:true, price:'0원'});
  r.rows.forEach(x=>console.log('   '+x));

  console.log('\n=== 25구슬 (정가를 모르는 것) — 아무것도 안 보태야 합니다');
  r=await run({orbs:25, balance:0, free:false, price:'25,000원'});
  r.rows.forEach(x=>console.log('   '+x));
  console.log('   보탠 줄 있나: '+(r.rows.some(x=>x.indexOf('정가')>=0)?'★있음':'없음 ok'));

  console.log('\n=== 두 번 돌려도');
  r=await run({orbs:3, balance:0, free:false, price:'3,000원'});
  const s2=r.w.document.createElement('script'); s2.textContent=JS; r.w.document.body.appendChild(s2);
  await sleep(120);
  console.log('   정가 줄 '+[...r.box.querySelectorAll('.lp-list')].length+' 개 (1 이어야 합니다)');
})();
