const {JSDOM}=require('jsdom'); const fs=require('fs');
const YEAR=process.argv[2]||'2026';
const JS=fs.readFileSync('ny'+YEAR+'.js','utf8');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const GAN=['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'];
// 일간 오행별로 무리가 달라집니다 — 열 일간을 다 돌립니다
async function run(dayGan, luckGan){
  const dom=new JSDOM(`<!doctype html><body><div id="ssb"><div class="book" id="bkBook">${'x'.repeat(300)}</div></div><div id="bkTitle"></div><div id="bkN"></div></body>`,
    {url:'https://s.com/', runScripts:'dangerously', pretendToBeVisual:true});
  const w=dom.window;
  w.localStorage.setItem('stella_demo', JSON.stringify({topic:YEAR+'년 운세',
    profile:{firstName:'소희', year:1990,month:5,day:5,hour:9,minute:0,sex:'F',city:'서울',country:'KR'}}));
  w.StellaSaju={locate:()=>({lon:127,lat:37.5,tz:9}),
    compute:()=>({pillars:{day:{han:dayGan+'子'}}, luck:{list:[{fromYear:1995,gan:luckGan}]},
      five:[{element:'화',count:2},{element:'목',count:2},{element:'토',count:2},{element:'금',count:1},{element:'수',count:1}]})};
  w.StellaRead={interpret:()=>({groups:{}})};
  const sc=w.document.createElement('script'); sc.textContent=JS; w.document.body.appendChild(sc);
  await sleep(60);
  const t=w.document.getElementById('bkBook').textContent;
  const m=t.match(/소희님의 \d{4}년은 「([^」]*)」입니다/);
  const l=t.match(/지금 「([^」]*)」의 십 ?년/);
  return {year:m?m[1]:'★못찾음', luck:l?l[1]:'★못찾음',
    left:(t.match(/\{[^}]{1,10}\}/g)||[])};
}
(async()=>{
  let bad=0;
  for(let i=0;i<10;i++){
    for(const lk of [0,4]){
      const r=await run(GAN[i], lk);
      const ok = r.year.indexOf('{')<0 && r.luck.indexOf('{')<0 && r.left.length===0;
      if(!ok) bad++;
      if(lk===0) console.log('   %s 일간  올해「%s」  대운「%s」  남은 자리표 %s',
        GAN[i], r.year.padEnd(22), r.luck.padEnd(14),
        r.left.length?('★'+r.left.join(',')):'0');
    }
  }
  console.log('\n   %s · 스무 가지 다 봄 · 어긋남 %d', YEAR, bad);
  if(bad) process.exit(1);
})();
