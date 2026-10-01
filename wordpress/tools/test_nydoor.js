const {JSDOM}=require('jsdom'); const fs=require('fs');
const JS=fs.readFileSync('nydoor.js','utf8');
function topics(vals){return vals.map(v=>`<label class="topic"><input type="radio" name="ssg-topic" value="${v}"${v===vals[0]?' checked':''}><span>${v}</span></label>`).join('');}
function run(url, vals){
  const dom=new JSDOM(`<!doctype html><body><div class="topics">${topics(vals)}</div></body>`,
    {url, runScripts:'dangerously', pretendToBeVisual:true});
  dom.window.HTMLElement.prototype.scrollIntoView=function(){};
  const s=dom.window.document.createElement('script'); s.textContent=JS;
  dom.window.document.body.appendChild(s);
  const d=dom.window.document;
  const got=[...d.querySelectorAll('input[name="ssg-topic"]')].map(i=>i.value);
  const on=[...d.querySelectorAll('input[name="ssg-topic"]')].filter(i=>i.checked).map(i=>i.value);
  return {got, on};
}
const FORT=['신년운세','대운','올해 총운','전환기','삼재','평생운'];
const LOVE=['결혼운','연애운','재회운','이별운','짝사랑','궁합'];
let bad=0;
function t(name, url, vals, wantList, wantOn){
  const r=run(url, vals);
  const okL = wantList===null || JSON.stringify(r.got)===JSON.stringify(wantList);
  const okO = r.on.length===1 && r.on[0]===wantOn;
  if(!okL||!okO){ bad++; console.log('★',name,'\n   단추',r.got,'\n   골라짐',r.on); }
  else console.log('ok  '+name+'  → 골라짐 「'+r.on[0]+'」');
}
t('운세문 · 그냥 열기','https://s.com/door-fortune/',FORT,
  ['2026년 운세','2027년 운세','대운','올해 총운','전환기','삼재','평생운'],'2026년 운세');
t('운세문 · ?topic=2027년 운세','https://s.com/door-fortune/?topic='+encodeURIComponent('2027년 운세'),FORT,
  ['2026년 운세','2027년 운세','대운','올해 총운','전환기','삼재','평생운'],'2027년 운세');
t('연애문 · ?topic=결혼운','https://s.com/door-love/?topic='+encodeURIComponent('결혼운'),LOVE,LOVE,'결혼운');
t('연애문 · ?topic=궁합','https://s.com/door-love/?topic='+encodeURIComponent('궁합'),LOVE,LOVE,'궁합');
t('연애문 · 주제 없이','https://s.com/door-love/',LOVE,LOVE,'결혼운');
t('연애문 · 없는 주제','https://s.com/door-love/?topic='+encodeURIComponent('없는것'),LOVE,LOVE,'결혼운');
console.log('\n어긋난 자리', bad);
