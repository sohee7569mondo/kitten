const {JSDOM}=require('jsdom'); const fs=require('fs');
const YEAR=process.argv[2]||'2027';
const JS=fs.readFileSync('ny'+YEAR+'.js','utf8');
const EL=['목','목','화','화','토','토','금','금','수','수'];
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const out=[];
  for(const gi of [2,4,6,8,0]){          /* 대운 천간 다섯 */
    const dom=new JSDOM(`<!doctype html><body><div id="ssb"><div class="book" id="bkBook">${'x'.repeat(300)}</div></div><div id="bkTitle"></div><div id="bkN"></div></body>`,
      {url:'https://s.com/', runScripts:'dangerously', pretendToBeVisual:true});
    const w=dom.window;
    w.localStorage.setItem('stella_demo', JSON.stringify({topic:YEAR+'년 운세',
      profile:{name:'정환',year:1990,month:5,day:5,hour:9,minute:0,sex:'M',city:'서울',country:'KR'}}));
    w.StellaSaju={locate:()=>({lon:127,lat:37.5,tz:9}),
      compute:()=>({pillars:{day:{han:'丙子'}}, luck:{list:[{fromYear:1995,gan:gi}]},
        five:[{element:'화',count:2},{element:'목',count:2},{element:'토',count:2},{element:'금',count:1},{element:'수',count:1}]})};
    w.StellaRead={interpret:()=>({groups:{}})};
    const sc=w.document.createElement('script'); sc.textContent=JS; w.document.body.appendChild(sc);
    await sleep(60);
    const h=w.document.getElementById('bkBook').innerHTML;
    out.push({gi, el:EL[gi], len:h.length, hash:h.length+'|'+h.slice(4000,4200)});
  }
  const uniq=new Set(out.map(o=>o.hash));
  out.forEach(o=>console.log('  대운천간 '+o.gi+'('+o.el+')  html '+o.len+'자'));
  console.log('\n  서로 다른 책 '+uniq.size+' / 5  '+(uniq.size===5?'ok · 대운마다 다른 책이 나옵니다':'★ 같은 책이 섞였습니다'));
})();
