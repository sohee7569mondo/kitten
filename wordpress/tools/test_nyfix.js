const {JSDOM}=require('jsdom'); const fs=require('fs');
const YEAR=process.argv[2]||'2026';
const JS=fs.readFileSync('ny'+YEAR+'.js','utf8');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function run(name){
  const dom=new JSDOM(`<!doctype html><body><div id="ssb"><div class="book" id="bkBook">${'x'.repeat(300)}</div></div><div id="bkTitle"></div><div id="bkN"></div></body>`,
    {url:'https://s.com/', runScripts:'dangerously', pretendToBeVisual:true});
  const w=dom.window;
  w.localStorage.setItem('stella_demo', JSON.stringify({topic:YEAR+'년 운세',
    profile:{name, year:1990,month:5,day:5,hour:9,minute:0,sex:'M',city:'서울',country:'KR'}}));
  w.StellaSaju={locate:()=>({lon:127,lat:37.5,tz:9}),
    compute:()=>({pillars:{day:{han:'丙子'}}, luck:{list:[{fromYear:1995,gan:2}]},
      five:[{element:'화',count:2},{element:'목',count:2},{element:'토',count:2},{element:'금',count:1},{element:'수',count:1}]})};
  w.StellaRead={interpret:()=>({groups:{}})};
  const sc=w.document.createElement('script'); sc.textContent=JS; w.document.body.appendChild(sc);
  await sleep(60);
  const d=w.document;
  const h2=[...d.querySelectorAll('#bkBook h2')].map(e=>e.textContent);
  return {title:d.getElementById('bkTitle').textContent, h2,
          flag:d.getElementById('bkBook').getAttribute('data-ny'+YEAR)};
}
(async()=>{
  console.log('=== 이름 자르기');
  for(const n of ['이소희','소희','남궁민수','김솔','정환','Sohee']){
    const r=await run(n);
    console.log('   %s→ %s', n.padEnd(8), r.title);
  }
  const r=await run('이소희');
  console.log('\n=== 장 제목 (①②③ 떼졌나)');
  r.h2.forEach(t=>console.log('   ', t));
  console.log('\n   동그라미 숫자 남은 자리', r.h2.filter(t=>/[①-⑳]/.test(t)).length);
})();
