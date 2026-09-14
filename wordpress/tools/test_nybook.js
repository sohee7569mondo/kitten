const {JSDOM}=require('jsdom'); const fs=require('fs');
const YEAR=process.argv[2]||'2026';
const JS=fs.readFileSync('ny'+YEAR+'.js','utf8');
const FIVE=['비겁','식상','재성','관성','인성'];
// 일간 한자 → 그 일간이 화(병정)를 만나 되는 무리
const DAY={'비겁':'丙','식상':'甲','재성':'壬','관성':'庚','인성':'戊'};
// 대운 천간 인덱스: 갑0 을1 병2 정3 무4 기5 경6 신7 임8 계9
const GAN={'비겁':null,'식상':null,'재성':null,'관성':null,'인성':null};
const EL_OF_IDX=['목','목','화','화','토','토','금','금','수','수'];
const SAENG={'목':'화','화':'토','토':'금','금':'수','수':'목'};
const GEUK={'목':'토','토':'수','수':'화','화':'금','금':'목'};
const GAN_EL={'甲':'목','乙':'목','丙':'화','丁':'화','戊':'토','己':'토','庚':'금','辛':'금','壬':'수','癸':'수'};
function groupOf(my,el){ if(el===my)return'비겁'; if(SAENG[my]===el)return'식상';
  if(GEUK[my]===el)return'재성'; if(GEUK[el]===my)return'관성'; if(SAENG[el]===my)return'인성'; return''; }
function ganIdxFor(myEl, wantGroup){
  for(let i=0;i<10;i++){ if(groupOf(myEl, EL_OF_IDX[i])===wantGroup) return i; }
  return -1;
}
let bad=0, sizes=[];
const rows=[];
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
for(const sp of FIVE){
  for(const dae of FIVE){
    const dayHan=DAY[sp], myEl=GAN_EL[dayHan];
    const gi=ganIdxFor(myEl, dae);
    const dom=new JSDOM(`<!doctype html><body><div id="ssb"><div class="book" id="bkBook">${'x'.repeat(300)}</div></div><div id="bkTitle"></div><div id="bkN"></div></body>`,
      {url:'https://s.com/reading-book/', runScripts:'dangerously', pretendToBeVisual:true});
    const w=dom.window;
    w.localStorage.setItem('stella_demo', JSON.stringify({topic:YEAR+'년 운세',
      profile:{name:'정환', year:1990, month:5, day:5, hour:9, minute:0, sex:'M', city:'서울', country:'KR'}}));
    w.StellaSaju={ locate:()=>({lon:127,lat:37.5,tz:9}),
      compute:()=>({ pillars:{day:{han:dayHan+'子'}},
        luck:{list:[{fromYear:1995,gan:gi,ji:0,han:'x',kor:'x'}]},
        five:[{element:'목',count:2},{element:'화',count:2},{element:'토',count:2},
              {element:'금',count:1},{element:'수',count:1}] }) };
    w.StellaRead={ interpret:()=>({groups:{}}) };
    const sc=w.document.createElement('script'); sc.textContent=JS; w.document.body.appendChild(sc);
    await sleep(60);            /* go() 가 setTimeout 으로 도니 기다립니다 */
    const bk=w.document.getElementById('bkBook');
    const html=bk.innerHTML, pages=(html.match(/class="page"/g)||[]).length;
    const flag=bk.getAttribute('data-ny'+YEAR);
    sizes.push(html.length);
    const ok = flag==='1' && pages===10 && html.length>10000;
    if(!ok){ bad++; rows.push(['★',sp,dae,pages,html.length,flag]); }
    else rows.push(['ok',sp,dae,pages,html.length,w.document.getElementById('bkTitle').textContent]);
  }
}
rows.slice(0,3).concat(rows.slice(-2)).forEach(r=>console.log(r.join('  ')));
console.log('\n'+YEAR+' · 스물다섯 갈래 · 어긋난 자리 '+bad);
console.log('  쪽 10 · html '+Math.min(...sizes)+' ~ '+Math.max(...sizes)+'자');
})();
