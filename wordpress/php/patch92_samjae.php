<?php
/* ═══════════════════════════════════════════════════════
   띠별운세에 삼재 표시   patch92_samjae
   2026-09-14

   ★ 크롬 번역을 끄고 붙여넣으세요.
   ★ WPCode 위치(Location) = 「어디서나 실행 / Run Everywhere」

   소희 님 : 「지금 삼재가 있는데 내가 삼재인지 아닌지가 안 나와있어.
              신년운이나 다른데서 삼재라는 말이 나와야 삼재를 사볼거
              같아」 · 「무료 이번 주 띠별운세에 표시하면 되지 않을까?」

   맞습니다. 손님은 **자기가 삼재인 줄 몰라서** 안 삽니다.
   삼재는 띠로 정해지는데 그걸 알려주는 자리가 없었습니다.
   띠별운세 쪽은 열두 띠가 이미 다 나와 있어 딱 맞습니다.

   삼재를 어떻게 세나
     삼합 무리마다 삼재 드는 해가 다릅니다. 지지 번호를 4로 나눈
     나머지가 곧 무리입니다 — 이것만 알면 표가 필요 없습니다.

       신자진 (8,0,4)  %4=0  →  인묘진 (2,3,4)
       사유축 (5,9,1)  %4=1  →  해자축 (11,0,1)
       인오술 (2,6,10) %4=2  →  신유술 (8,9,10)
       해묘미 (11,3,7) %4=3  →  사오미 (5,6,7)

     2026년은 병오년, 지지가 오(6)입니다. 6은 사오미 한가운데라
     **돼지 · 토끼 · 양띠가 눌삼재**(가운데 해)입니다.
     2025 을사년에 들어왔고 2027 정미년에 나갑니다.

     ★ 열두 지지가 네 무리에 빠짐없이 덮이므로 **어느 해든 반드시
       세 띠가 삼재**입니다. 「올해는 삼재가 없다」는 해는 없습니다.

   입춘
     사주에서 한 해는 입춘에 바뀝니다. 2월 4일 앞이면 앞 해로 봅니다.
     쪽 안에 정확한 입춘 셈(ipchunJd)이 있지만 그 덩어리 안에만
     있어서 밖에서 못 부릅니다. 하루 차이가 날 수 있는데, 삼재는
     해 단위라 2월 3~5일에만 문제가 되고 그때는 어차피 경계입니다.

   어디에 붙나
     · 열두 칸 위에 안내 상자 하나
     · 삼재인 띠 세 칸에만 붉은 딱지와 한 줄, 그리고 삼재 풀이로 가는 길
     · 나머지 아홉 칸은 한 자도 안 건드립니다

   ★ 어두운 쪽에서도 흰 쪽에서도 읽히게 색을 직접 씁니다.
     이 쪽의 색표(var(--gold) 같은 것)를 빌리지 않습니다 —
     2026-09-08 에 여러 쪽을 흰 바탕으로 덮었는데 이 쪽이
     포함됐는지 제 사본으로는 알 수 없기 때문입니다.
   ═══════════════════════════════════════════════════════ */

add_action( 'wp_footer', function () {

	if ( ! is_page( 'zodiac-year' ) ) { return; }
	?>
<style id="stella-samjae-css">
#sjBox{ margin:36px auto 0; padding:22px 24px; border-radius:13px;
  background:#C4453A; color:#FFFDF9; text-align:left;
  box-shadow:0 18px 40px -20px rgba(196,69,58,.75); }
#sjBox .sj-kick{ font-size:.74rem; letter-spacing:.26em; opacity:.85;
  margin-bottom:10px; }
#sjBox h3{ margin:0 0 10px; font-size:1.28rem; font-weight:800;
  line-height:1.5; }
#sjBox p{ margin:0 0 8px; font-size:.96rem; line-height:1.85;
  color:#FFF3F1; }
#sjBox .sj-go{ display:inline-block; margin-top:12px; padding:13px 22px;
  border-radius:8px; background:#FFFDF9; color:#C4453A;
  font-weight:800; font-size:.95rem; text-decoration:none; }
#ssp .acard[data-samjae] .sj-tag{ display:inline-block; margin-left:8px;
  padding:3px 10px; border-radius:20px; background:#C4453A; color:#FFFDF9;
  font-size:.7rem; font-weight:800; vertical-align:middle; }
#ssp .acard[data-samjae] .sj-line{ margin-top:14px; padding:13px 15px;
  border-radius:9px; background:rgba(196,69,58,.14);
  border:1px solid rgba(196,69,58,.42); }
#ssp .acard[data-samjae] .sj-line b{ color:#C4453A; }
#ssp .acard[data-samjae] .sj-line p{ margin:0; font-size:.9rem;
  line-height:1.8; }
#ssp .acard[data-samjae] .sj-line a{ display:inline-block; margin-top:7px;
  color:#C4453A; font-weight:800; font-size:.9rem; text-decoration:underline; }
</style>
<script>
(function(){
  if(window.StellaSamjae){ return; }
  window.StellaSamjae = 1;

  var ANIMAL = ['쥐','소','범','토끼','용','뱀','말','양','원숭이','닭','개','돼지'];
  var GO = String.fromCharCode(8594);   /* → — 앰퍼샌드를 안 씁니다 */
  var LINK = '/door-fortune/?topic=' + encodeURIComponent('삼재');

  /* 삼합 무리(지지 번호 나머지 4)마다 삼재가 드는 첫 해 */
  var START = [2, 11, 8, 5];

  /* 올해 지지 — 입춘 앞이면 앞 해로 */
  function yearJi(){
    var d = new Date();
    var y = d.getFullYear();
    var m = d.getMonth() + 1;
    var day = d.getDate();
    if(m < 2){ y = y - 1; }
    if(m === 2){ if(day < 4){ y = y - 1; } }
    return { y: y, ji: ((y + 8) % 12 + 12) % 12 };
  }

  /* 이 띠가 올해 삼재인가 — 0 들 · 1 눌 · 2 날 · -1 아님 */
  function stageOf(z, ji){
    var s = START[ ((z % 4) + 4) % 4 ];
    var k = ((ji - s) % 12 + 12) % 12;
    if(k > 2){ return -1; }
    return k;
  }

  var NAME = ['들삼재', '눌삼재', '날삼재'];
  var HEAD = ['삼재 들어오는 해', '삼재 가운데 해', '삼재 나가는 해'];
  var LINE = [
    '올해부터 삼재가 시작됩니다. 새로 벌이는 일보다 있는 것을 지키는 데 마음을 쓰세요.',
    '삼재 세 해 가운데 한가운데입니다. 가장 무겁게 느껴지는 해예요. 큰 결정은 한 해만 미루시면 한결 수월합니다.',
    '올해로 삼재가 끝납니다. 오래 끌던 것을 매듭짓기에 좋은 해예요.'
  ];

  function box(grid, y, list, stage){
    if(document.getElementById('sjBox')){ return; }
    var names = [];
    var i;
    for(i = 0; i < list.length; i++){ names.push(ANIMAL[list[i]] + '띠'); }

    var d = document.createElement('div');
    d.id = 'sjBox';
    d.innerHTML =
      '<div class="sj-kick">SAMJAE</div>'
      + '<h3>' + y + '년 삼재는 ' + names.join(' · ') + '입니다</h3>'
      + '<p>이 세 띠는 지금 <b>' + NAME[stage] + '</b>'
      + '(' + HEAD[stage] + ')를 지나고 있습니다. '
      + '삼재는 세 해 동안 이어집니다.</p>'
      + '<p>같은 삼재라도 여덟 글자에 따라 무엇이 흔들리는지가 다릅니다. '
      + '사람 때문에 오는 분이 있고, 몸으로 오는 분이 있어요.</p>'
      + '<a class="sj-go" href="' + LINK + '">내 삼재는 어떻게 오는지 보기 ' + GO + '</a>';

    grid.parentNode.insertBefore(d, grid);
  }

  function mark(card, z, stage){
    if(card.getAttribute('data-samjae')){ return; }
    card.setAttribute('data-samjae', NAME[stage]);

    var nm = card.querySelector('.aname');
    if(nm){
      var t = document.createElement('span');
      t.className = 'sj-tag';
      t.textContent = NAME[stage];
      nm.appendChild(t);
    }

    var w = document.createElement('div');
    w.className = 'sj-line';
    w.innerHTML =
      '<p><b>올해 삼재입니다.</b> ' + LINE[stage] + '</p>'
      + '<a href="' + LINK + '">' + ANIMAL[z] + '띠의 삼재 풀이 보기 ' + GO + '</a>';
    card.appendChild(w);
  }

  function run(){
    var grid = document.getElementById('zGrid');
    if(!grid){ return 0; }
    var cards = grid.querySelectorAll('.acard[data-z]');
    if(cards.length < 12){ return 0; }

    var Y = yearJi();
    var list = [], stage = -1, i, z, s;

    for(i = 0; i < cards.length; i++){
      z = parseInt(cards[i].getAttribute('data-z'), 10);
      s = stageOf(z, Y.ji);
      if(s < 0){ continue; }
      list.push(z);
      stage = s;
      mark(cards[i], z, s);
    }
    if(list.length === 0){ return 1; }
    box(grid, Y.y, list, stage);
    return 1;
  }

  function watch(){
    if(run()){ return; }
    var n = 0;
    var t = setInterval(function(){
      n++;
      if(run()){ clearInterval(t); return; }
      if(n > 80){ clearInterval(t); }
    }, 300);
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', watch);
  } else {
    watch();
  }
})();
</script>
	<?php
} );
