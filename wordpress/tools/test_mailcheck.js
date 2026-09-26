const {JSDOM}=require('jsdom'); const fs=require('fs');
const JS=fs.readFileSync('mailcheck.js','utf8');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const PAY=`<div id="sso"><div class="wrap">
 <button type="button" class="go" id="oGo">3,000원 결제하기</button>
 <div class="say" id="oSay"></div></div></div>`;
function run(email){
  const dom=new JSDOM(`<!doctype html><body>${PAY}</body>`,
    {url:'https://stellasaju.com/pay/', runScripts:'dangerously', pretendToBeVisual:true});
  const w=dom.window;
  let paid=0, posted=null;
  w.document.getElementById('oGo').addEventListener('click', function(){ paid++; });
  w.fetch=function(u,o){
    if(String(u).indexOf('myemail')>=0){
      return Promise.resolve({ok:true, json:()=>Promise.resolve({member:true,email:email})});
    }
    posted=JSON.parse(o.body);
    return Promise.resolve({ok:true, json:()=>Promise.resolve({ok:true,email:posted.email})});
  };
  w.HTMLElement.prototype.scrollIntoView=function(){};
  const s=w.document.createElement('script'); s.textContent=JS; w.document.body.appendChild(s);
  return {w, paid:()=>paid, posted:()=>posted};
}
(async()=>{
  console.log('=== ① 이메일이 있을 때');
  let t=run('abc@gmail.com'); let d=t.w.document;
  d.getElementById('oGo').click(); await sleep(120);
  console.log('   결제로 넘어갔나 : ' + (t.paid()===0?'안 넘어감 ok (막았습니다)':'★그냥 넘어감'));
  console.log('   확인 상자        : ' + (d.getElementById('mkBox').className==='on'?'떴음 ok':'★안 뜸'));
  console.log('   보여준 이메일    : ' + d.getElementById('mkMail').textContent);
  d.getElementById('mkYes').click(); await sleep(80);
  console.log('   「맞아요」 누른 뒤: 결제 ' + t.paid() + ' 번 (1 이어야 합니다)');
  t.w.close();

  console.log('\n=== ② 「고칠게요」 로 바꾸고 결제');
  t=run('wrong@x.com'); d=t.w.document;
  d.getElementById('oGo').click(); await sleep(120);
  d.getElementById('mkNo').click();
  d.getElementById('mkIn').value=' new@gmail.com ';
  d.getElementById('mkYes').click(); await sleep(120);
  console.log('   서버로 보낸 것   : ' + JSON.stringify(t.posted()));
  console.log('   결제             : ' + t.paid() + ' 번 (1 이어야 합니다)');
  t.w.close();

  console.log('\n=== ③ 이메일이 아예 없을 때');
  t=run(''); d=t.w.document;
  d.getElementById('oGo').click(); await sleep(120);
  console.log('   안내             : ' + d.getElementById('mkWhy').textContent.slice(0,40) + '…');
  console.log('   고치는 칸 열렸나 : ' + (d.getElementById('mkEdit').style.display==='block'?'열림 ok':'★안 열림'));
  d.getElementById('mkYes').click(); await sleep(80);
  console.log('   빈 채로 누르면   : 결제 ' + t.paid() + ' 번 (0 이어야 합니다) · ' + d.getElementById('mkSay').textContent);
  t.w.close(); process.exit(0);
})();
