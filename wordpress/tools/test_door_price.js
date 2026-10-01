const {JSDOM}=require('jsdom'); const fs=require('fs');
const JS=fs.readFileSync('listprice.js','utf8');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const BOX=`<section class="bill">
<div class="bline"><b>기본 풀이</b><span id="pBase">3구슬 · 3,000원</span></div>
<div class="btotal"><div class="btotal-k">합계</div>
  <div class="btotal-v"><span id="total">3</span><small>구슬</small></div></div>
<div class="balance only-member">내 잔액 <span id="balance">938</span>구슬</div>
<button type="button" class="go" id="goBtn">벼리에게 물어보기</button>
<div class="pay-note">구슬 1개는 <b>1,000원</b>이에요. 이 풀이 한 편은 <b>3구슬 · 3,000원</b>입니다. <b>여는 기념 값</b>이고, 여는 기간이 끝나면 9구슬 · 9,000원이 됩니다.<br>결제가 끝나면 <b>바로 이 화면에서 펼쳐지고</b>, 「내 자리」에 남습니다.</div>
</section>`;
(async()=>{
  const dom=new JSDOM(`<!doctype html><body>${BOX}</body>`,
    {url:'https://stellasaju.com/door-love/', runScripts:'dangerously', pretendToBeVisual:true});
  const w=dom.window;
  const s=w.document.createElement('script'); s.textContent=JS; w.document.body.appendChild(s);
  await sleep(200);
  const d=w.document;
  const line=e=>e?e.textContent.replace(/\s+/g,' ').trim():'★없음';
  console.log('기본 풀이      : ' + line(d.querySelector('#pBase')));
  console.log('여는 기념 할인 : ' + line(d.querySelector('.lp-off-line')));
  console.log('합계           : ' + line(d.querySelector('.btotal-v')));
  console.log('안내 줄        : ' + line(d.querySelector('.pay-note')));
  console.log('');
  const note=line(d.querySelector('.pay-note'));
  console.log('  「구슬 1개는 1,000원」 : ' + (note.indexOf('1개는')>=0?'★남음':'없음 ok'));
  console.log('  「N구슬 · 」 남았나    : ' + (/\d구슬 · /.test(note)?'★남음':'없음 ok'));
  console.log('  기간 표시              : ' + (line(d.querySelector('.lp-off-line')).indexOf('10월 31일')>=0?'있음 ok':'★없음'));
  d.getElementById('total').textContent='25';
  await sleep(400);
  console.log('  합계를 25 로 바꾸면    : ' + line(d.querySelector('.btotal-v')));
  w.close(); process.exit(0);
})();
