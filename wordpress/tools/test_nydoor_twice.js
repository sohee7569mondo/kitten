const {JSDOM}=require('jsdom'); const fs=require('fs');
const JS=fs.readFileSync('nydoor.js','utf8');
const FORT=['신년운세','대운','올해 총운','전환기','삼재','평생운'];
const html=FORT.map((v,i)=>`<label class="topic"><input type="radio" name="ssg-topic" value="${v}"${i===0?' checked':''}><span>${v}</span></label>`).join('');
const dom=new JSDOM(`<!doctype html><body><div class="topics">${html}</div></body>`,
  {url:'https://s.com/door-fortune/', runScripts:'dangerously', pretendToBeVisual:true});
dom.window.HTMLElement.prototype.scrollIntoView=function(){};
const s=dom.window.document.createElement('script'); s.textContent=JS;
dom.window.document.body.appendChild(s);
const d=dom.window.document;
console.log('처음 한 번 :', [...d.querySelectorAll('input[name="ssg-topic"]')].map(i=>i.value).join(' · '));
setTimeout(()=>{
  const v=[...d.querySelectorAll('input[name="ssg-topic"]')].map(i=>i.value);
  const on=[...d.querySelectorAll('input[name="ssg-topic"]')].filter(i=>i.checked).map(i=>i.value);
  console.log('되풀이 뒤 :', v.join(' · '));
  console.log('2026 개수', v.filter(x=>x==='2026년 운세').length, '· 2027 개수', v.filter(x=>x==='2027년 운세').length);
  console.log('골라짐', on, '· 단추 수', v.length);
  console.log(v.length===7 && v.filter(x=>x==='2026년 운세').length===1 ? '\nok · 되풀이해 돌아도 단추가 안 늘어납니다' : '\n★ 단추가 늘어났습니다');
  process.exit(0);
}, 1200);
