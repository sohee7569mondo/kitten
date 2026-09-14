/* tool_doorwide 검사 — 크로미움으로 실제로 그려서 재봅니다
   제 사본 두 쪽(door-love · door-career)을 틀에 넣고 도구를 돌립니다.
   실행 : node wordpress/tools/test_doorwide.js                        */
var fs = require('fs'), path = require('path'), os = require('os');
var { chromium } = require('playwright');

var HERE = path.join(__dirname, '..');
var php  = fs.readFileSync(path.join(HERE, 'php/tool_doorwide.php'), 'utf8');
var JS   = php.match(/<script>([\s\S]*?)<\/script>/)[1]
  .replace("'<?php echo esc_js( $a ); ?>'", "'door-love'")
  .replace("'<?php echo esc_js( $b ); ?>'", "'door-career'");

var A = path.join(HERE, 'pages/door-love.html');
var B = path.join(HERE, 'pages/door-career.html');

/* 도구가 띄우는 화면을 그대로 흉내 냅니다 (틀 주소만 로컬 파일로) */
var PAGE = '<!doctype html><meta charset="utf-8"><body>'
  + '<div id="say">재는 중…</div><div id="out"></div>'
  + '<div id="frames" style="position:absolute;left:-9999px;top:0">'
  + '<iframe id="fa" src="file://' + A + '" width="1280" height="1500"></iframe>'
  + '<iframe id="fb" src="file://' + B + '" width="1280" height="1500"></iframe>'
  + '</div><script>' + JS + '</' + 'script></body>';

var tmp = path.join(os.tmpdir(), 'doorwide-test.html');
fs.writeFileSync(tmp, PAGE);

(async function(){
  var browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--allow-file-access-from-files']
  });
  var page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  await page.goto('file://' + tmp);
  await page.waitForTimeout(3500);

  var say = await page.textContent('#say');
  console.log('상태 : ' + say);

  var rows = await page.$$eval('#out table tr', function(trs){
    return trs.map(function(tr){
      var t = tr.querySelectorAll('td, th');
      return {
        diff: tr.className.indexOf('diff') > -1,
        cells: Array.prototype.map.call(t, function(c){ return c.textContent.trim(); })
      };
    });
  });

  if(rows.length === 0){ console.log('★ 표가 안 나왔습니다'); await browser.close(); process.exit(1); }

  console.log('');
  rows.forEach(function(r){
    var mark = r.diff ? '★ ' : '   ';
    console.log(mark + r.cells[0].padEnd(26) + ' | ' + (r.cells[1] || '').slice(0, 44)
      + ' | ' + (r.cells[2] || '').slice(0, 44));
  });

  var big = await page.textContent('.big');
  console.log('');
  console.log('맺음 : ' + big.trim());

  await browser.close();
  process.exit(0);
})();
