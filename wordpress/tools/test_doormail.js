const {JSDOM}=require('jsdom'); const fs=require('fs');
const JS=fs.readFileSync('mailcheck.js','utf8');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const DOOR=`<div id="ssg"><div class="f">
 <label for="gEmail">이메일 · 필수 (결제창을 열려면 꼭 필요해요)</label>
 <input type="email" id="gEmail" maxlength="60" placeholder="you@example.com">
</div>
<button type="button" class="go" id="goBtn">벼리에게 물어보기</button></div>`;
(async()=>{
  const dom=new JSDOM(`<!doctype html><body>${DOOR}</body>`,
    {url:'https://stellasaju.com/door-love/', runScripts:'dangerously', pretendToBeVisual:true});
  const w=dom.window;
  let went=0;
  w.document.getElementById('goBtn').addEventListener('click', function(){ went++; });
  w.HTMLElement.prototype.scrollIntoView=function(){};
  const s=w.document.createElement('script'); s.textContent=JS; w.document.body.appendChild(s);
  await sleep(120);
  const d=w.document, f=d.getElementById('gEmail'), b=d.getElementById('goBtn');
  const say=()=> (d.getElementById('mkDoorSay')||{textContent:''}).textContent;

  const cases=[['', '빈칸'],['abc','골뱅이 없음'],['abc@','뒤가 없음'],
               ['abc@gmail','점 없음'],['abc@gmail.','점 뒤가 없음'],
               [' abc@gmail.com ','앞뒤 빈칸 (넘어가야 함)'],['a@b.co','짧은 것 (넘어가야 함)']];
  for(const [v,label] of cases){
    f.value=v; went=0; b.click(); await sleep(30);
    console.log('   %-22s → %s  %s', label, went?'넘어감':'막음  ', went?'':('· '+say().slice(0,24)+'…'));
  }
  console.log('\n   앞뒤 빈칸을 다듬었나 : ' + JSON.stringify(f.value));
  w.close(); process.exit(0);
})();
