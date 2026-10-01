const {JSDOM}=require('jsdom'); const fs=require('fs');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const CASES=[
  ['가족운', 'patch160_family.js',   'data-family'],
  ['건강운', 'patch160_health4.js',  'data-health4'],
];
(async()=>{
 for(const [topic, file, flag] of CASES){
  const JS=fs.readFileSync(file,'utf8');
  const dom=new JSDOM(`<!doctype html><body><div id="ssb"><div class="book" id="bkBook">${'x'.repeat(400)}</div></div><div id="bkTitle"></div><div id="bkN"></div></body>`,
    {url:'https://s.com/', runScripts:'dangerously', pretendToBeVisual:true});
  const w=dom.window;
  w.localStorage.setItem('stella_demo', JSON.stringify({topic,
    profile:{firstName:'소희', year:1990,month:5,day:5,hour:9,minute:0,sex:'F',city:'서울',country:'KR'}}));
  w.StellaSaju={locate:()=>({lon:127,lat:37.5,tz:9}),
    compute:()=>({pillars:{day:{han:'丙子'},year:{han:'庚午'},month:{han:'辛巳'},hour:{han:'癸巳'}},
      luck:{list:[{fromYear:1995,gan:8}]},
      five:[{element:'화',count:2},{element:'목',count:2},{element:'토',count:2},{element:'금',count:1},{element:'수',count:1}]})};
  w.StellaRead={interpret:()=>({groups:{}})};
  const sc=w.document.createElement('script'); sc.textContent=JS; w.document.body.appendChild(sc);
  await sleep(200);
  const bk=w.document.getElementById('bkBook');
  const h=bk.innerHTML;
  const dv=(h.match(/class="page divider"/g)||[]).length;
  const pg=(h.match(/class="page/g)||[]).length;
  const nos=[...h.matchAll(/dvno dvch">([^<]*)/g)].map(m=>m[1]);
  const img=(h.match(/dvmark"><img[^>]*src="([^"]*)"/)||[])[1];
  console.log('%s  깃발 %s · 전체 쪽 %d · 장 표지 %d', topic, bk.getAttribute(flag)||'-', pg, dv);
  console.log('   %s', nos.join(' '));
  console.log('   얼굴 %s', img?img.split('/').pop():'★없음');
  console.log('   src 에 앰퍼샌드 %d\n', (h.match(/src="[^"]*&/g)||[]).length);
 }
})();
