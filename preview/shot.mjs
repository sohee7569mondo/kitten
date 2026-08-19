import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const b = await chromium.launch();
for (const [name, w, h] of [['desktop',1440,900],['mobile',390,844]]) {
  const p = await b.newPage({ viewport:{width:w,height:h}, deviceScaleFactor:1 });
  await p.goto('file://' + process.cwd() + '/index.html');
  await p.waitForTimeout(3500);
  // scroll through so all .reveal sections fire
  const H = await p.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < H; y += Math.floor(h*0.8)) { await p.evaluate(v=>scrollTo(0,v), y); await p.waitForTimeout(220); }
  await p.evaluate(()=>scrollTo(0,0)); await p.waitForTimeout(600);
  await p.screenshot({ path:`shot-${name}-full.png`, fullPage:true });
  await p.screenshot({ path:`shot-${name}-top.png` });
  console.log(name, 'pageHeight', H);
  // report any horizontal overflow
  const ov = await p.evaluate(()=>({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
  console.log('  scrollWidth', ov.sw, 'clientWidth', ov.cw, ov.sw > ov.cw+1 ? '<<< H-OVERFLOW' : 'no h-overflow');
  await p.close();
}
await b.close();
