/* ═══════════════════════════════════════════════════════════════
   STELLA SAJU — 브라우저에서 도는 사주 계산기
   ───────────────────────────────────────────────────────────────
   생년월일시와 태어난 곳을 넣으면 아래를 돌려줍니다.
     · 진태양시 (경도 보정 + 균시차)
     · 절기 (태양 황경 기준)
     · 사주 원국 네 기둥
     · 오행 비율
     · 대운 (양남음녀 순행 / 음남양녀 역행)
     · 태양 별자리 · 상승궁 · 천정
   서버 없이 도는 순수 계산이라 회원가입 전에도 쓸 수 있습니다.
   ═══════════════════════════════════════════════════════════════ */
(function(root){
  'use strict';

  var GAN_H=['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'];
  var GAN_L=['갑','을','병','정','무','기','경','신','임','계'];
  var JI_H =['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
  var JI_L =['자','축','인','묘','진','사','오','미','신','유','술','해'];
  var GAN_EL=['목','목','화','화','토','토','금','금','수','수'];
  var JI_EL =['수','토','목','목','토','화','화','토','금','금','토','수'];
  var JI_ANIMAL=['쥐','소','호랑이','토끼','용','뱀','말','양','원숭이','닭','개','돼지'];
  var ELEMENTS=['목','화','토','금','수'];

  /* 12절(節). 월지가 바뀌는 지점입니다. 중기(中氣)는 월주를 가르지 않아 뺐습니다.
     month 는 그 절기가 실제로 떨어지는 양력 달입니다 (모두 4~9일 사이). */
  var TERMS=[
    {deg:285, name:'소한', ji:1,  month:1},
    {deg:315, name:'입춘', ji:2,  month:2},
    {deg:345, name:'경칩', ji:3,  month:3},
    {deg:15,  name:'청명', ji:4,  month:4},
    {deg:45,  name:'입하', ji:5,  month:5},
    {deg:75,  name:'망종', ji:6,  month:6},
    {deg:105, name:'소서', ji:7,  month:7},
    {deg:135, name:'입추', ji:8,  month:8},
    {deg:165, name:'백로', ji:9,  month:9},
    {deg:195, name:'한로', ji:10, month:10},
    {deg:225, name:'입동', ji:11, month:11},
    {deg:255, name:'대설', ji:0,  month:12}
  ];

  var SIGNS=['양자리','황소자리','쌍둥이자리','게자리','사자자리','처녀자리',
             '천칭자리','전갈자리','사수자리','염소자리','물병자리','물고기자리'];


  /* 태어난 곳 → 경도 · 위도 · 표준시 · 서머타임.
     진태양시는 경도로 갈립니다. 서울과 부산도 8분쯤 차이가 나서
     시 경계에 걸린 분은 시주가 바뀔 수 있습니다.
     해외에서 태어나신 분은 그 나라 표준시와 서머타임까지 봐야 맞습니다. */
  var CITIES={
    '서울':[126.978,37.567], '인천':[126.705,37.456], '수원':[127.029,37.264],
    '성남':[127.127,37.420], '고양':[126.832,37.658], '용인':[127.178,37.241],
    '부천':[126.766,37.504], '안산':[126.831,37.322], '안양':[126.957,37.394],
    '남양주':[127.216,37.636], '화성':[126.832,37.199], '평택':[127.113,36.992],
    '의정부':[127.034,37.738], '파주':[126.780,37.760], '김포':[126.716,37.615],
    '광명':[126.865,37.479], '이천':[127.435,37.272], '양주':[127.046,37.785],
    '춘천':[127.730,37.881], '원주':[127.920,37.342], '강릉':[128.896,37.752],
    '속초':[128.591,38.207], '동해':[129.114,37.525],
    '대전':[127.385,36.350], '세종':[127.289,36.480], '천안':[127.115,36.815],
    '청주':[127.489,36.642], '충주':[127.930,36.991], '아산':[126.980,36.790],
    '공주':[127.119,36.447], '서산':[126.450,36.785], '제천':[128.191,37.133],
    '대구':[128.601,35.872], '포항':[129.365,36.019], '경주':[129.225,35.856],
    '구미':[128.344,36.120], '안동':[128.729,36.568], '김천':[128.114,36.140],
    '경산':[128.741,35.825], '영주':[128.624,36.806],
    '부산':[129.075,35.180], '울산':[129.311,35.539], '창원':[128.682,35.228],
    '진주':[128.108,35.180], '김해':[128.882,35.229], '통영':[128.433,34.854],
    '거제':[128.621,34.880], '양산':[129.037,35.335], '사천':[128.064,35.004],
    '광주':[126.852,35.160], '전주':[127.148,35.824], '목포':[126.392,34.812],
    '여수':[127.662,34.760], '순천':[127.487,34.951], '군산':[126.737,35.968],
    '익산':[126.958,35.948], '나주':[126.711,35.016], '정읍':[126.856,35.570],
    '제주':[126.532,33.499], '서귀포':[126.566,33.254],
    '평양':[125.738,39.039], '개성':[126.556,37.971], '함흥':[127.536,39.918]
  };

  /* 해외 — [경도, 위도, 표준시, 서머타임 규칙]
     규칙 : 'na' 북미 · 'eu' 유럽 · 'au' 호주 남동부 · '' 없음 */
  var WORLD={
    /* 캐나다 */
    '밴쿠버':[-123.121,49.283,-8,'na'], '빅토리아':[-123.365,48.428,-8,'na'],
    '캘거리':[-114.071,51.045,-7,'na'], '에드먼턴':[-113.491,53.546,-7,'na'],
    '위니펙':[-97.138,49.895,-6,'na'],  '토론토':[-79.383,43.653,-5,'na'],
    '오타와':[-75.697,45.421,-5,'na'],  '몬트리올':[-73.568,45.502,-5,'na'],
    /* 미국 서부 */
    '로스앤젤레스':[-118.243,34.052,-8,'na'], 'LA':[-118.243,34.052,-8,'na'],
    '샌프란시스코':[-122.419,37.775,-8,'na'], '샌디에이고':[-117.161,32.716,-8,'na'],
    '새너제이':[-121.887,37.339,-8,'na'],     '시애틀':[-122.332,47.606,-8,'na'],
    '포틀랜드':[-122.676,45.512,-8,'na'],     '라스베이거스':[-115.139,36.170,-8,'na'],
    '피닉스':[-112.074,33.448,-7,''],         '덴버':[-104.991,39.739,-7,'na'],
    '솔트레이크시티':[-111.891,40.761,-7,'na'],
    /* 미국 중부·동부 */
    '시카고':[-87.630,41.878,-6,'na'],  '댈러스':[-96.797,32.777,-6,'na'],
    '휴스턴':[-95.370,29.760,-6,'na'],  '오스틴':[-97.743,30.267,-6,'na'],
    '애틀랜타':[-84.388,33.749,-5,'na'],'뉴욕':[-74.006,40.713,-5,'na'],
    '뉴저지':[-74.406,40.058,-5,'na'],  '필라델피아':[-75.165,39.953,-5,'na'],
    '보스턴':[-71.059,42.360,-5,'na'],  '워싱턴':[-77.037,38.907,-5,'na'],
    '마이애미':[-80.192,25.762,-5,'na'],'올랜도':[-81.379,28.538,-5,'na'],
    '호놀룰루':[-157.858,21.307,-10,''], '하와이':[-157.858,21.307,-10,''],
    '앵커리지':[-149.900,61.218,-9,'na'],
    /* 아시아 */
    '도쿄':[139.692,35.690,9,''],   '요코하마':[139.638,35.444,9,''],
    '오사카':[135.502,34.694,9,''], '교토':[135.768,35.012,9,''],
    '나고야':[136.907,35.181,9,''], '후쿠오카':[130.402,33.590,9,''],
    '삿포로':[141.355,43.062,9,''], '오키나와':[127.681,26.212,9,''],
    '베이징':[116.407,39.904,8,''], '상하이':[121.474,31.230,8,''],
    '칭다오':[120.383,36.067,8,''], '선양':[123.432,41.805,8,''],
    '옌볜':[129.514,42.905,8,''],   '광저우':[113.264,23.129,8,''],
    '홍콩':[114.169,22.319,8,''],   '타이베이':[121.566,25.033,8,''],
    '싱가포르':[103.820,1.352,8,''],'방콕':[100.501,13.756,7,''],
    '하노이':[105.834,21.028,7,''], '호치민':[106.660,10.823,7,''],
    '마닐라':[120.984,14.599,8,''], '자카르타':[106.845,-6.208,7,''],
    '델리':[77.209,28.614,5.5,''],  '두바이':[55.271,25.205,4,''],
    /* 오세아니아 */
    '시드니':[151.209,-33.868,10,'au'],  '멜버른':[144.946,-37.840,10,'au'],
    '브리즈번':[153.026,-27.470,10,''],  '퍼스':[115.861,-31.950,8,''],
    '오클랜드':[174.763,-36.848,12,'au'],
    /* 유럽 */
    '런던':[-0.128,51.507,0,'eu'],      '더블린':[-6.260,53.350,0,'eu'],
    '파리':[2.352,48.857,1,'eu'],       '베를린':[13.405,52.520,1,'eu'],
    '프랑크푸르트':[8.682,50.111,1,'eu'],'뮌헨':[11.582,48.135,1,'eu'],
    '암스테르담':[4.904,52.367,1,'eu'], '브뤼셀':[4.352,50.847,1,'eu'],
    '취리히':[8.542,47.377,1,'eu'],     '빈':[16.373,48.208,1,'eu'],
    '로마':[12.496,41.903,1,'eu'],      '밀라노':[9.190,45.464,1,'eu'],
    '마드리드':[-3.704,40.417,1,'eu'],  '바르셀로나':[2.173,41.385,1,'eu'],
    '프라하':[14.438,50.076,1,'eu'],    '스톡홀름':[18.069,59.329,1,'eu'],
    '모스크바':[37.618,55.756,3,''],
    /* 남미·아프리카 */
    '상파울루':[-46.633,-23.551,-3,''], '부에노스아이레스':[-58.382,-34.604,-3,''],
    '멕시코시티':[-99.133,19.433,-6,''],'카이로':[31.236,30.044,2,''],
    '요하네스버그':[28.034,-26.205,2,'']
  };

  /* 도시를 못 찾았을 때 쓰는 나라 대표 도시 */
  var COUNTRY_CITY={
    '대한민국':'서울', '미국':'로스앤젤레스', '캐나다':'토론토', '일본':'도쿄',
    '중국':'베이징', '호주':'시드니', '영국':'런던', '뉴질랜드':'오클랜드',
    '독일':'베를린', '프랑스':'파리', '싱가포르':'싱가포르', '필리핀':'마닐라',
    '베트남':'호치민', '태국':'방콕', '기타':'서울'
  };

  /* ── 서머타임과 옛 표준시 ─────────────────────────────── */
  function ymd(y,m,d){ return y*10000+m*100+d; }

  /* 그 달 n번째 일요일 */
  function nthSun(y,m,n){
    var first=new Date(Date.UTC(y,m-1,1)).getUTCDay();      // 0=일
    var day=1+((7-first)%7)+(n-1)*7;
    return day;
  }
  /* 그 달 마지막 일요일 */
  function lastSun(y,m){
    var last=new Date(Date.UTC(y,m,0)).getUTCDate();
    var dow=new Date(Date.UTC(y,m-1,last)).getUTCDay();
    return last-dow;
  }

  /* 한국이 서머타임을 쓴 해와 기간 (표준시 자료 기준) */
  var KR_DST=[
    [19480601,19480913],[19490403,19490911],[19500401,19500910],[19510506,19510909],
    [19550505,19550909],[19560520,19560930],[19570505,19570922],[19580504,19580921],
    [19590504,19590920],[19600501,19600918],
    [19870510,19871011],[19880508,19881009]
  ];

  /* 한국 표준시는 두 번 바뀌었습니다 (동경 135도 ↔ 127.5도) */
  function koreaTz(y,mo,d){
    var t=ymd(y,mo,d);
    if(t < 19120101){ return 8.5; }
    if(t < 19540321){ return 9; }
    if(t < 19610810){ return 8.5; }
    return 9;
  }

  /* 서머타임이면 60(분), 아니면 0 */
  function dstMinutes(zone, y, mo, d){
    var t=ymd(y,mo,d);
    var i;

    if(zone==='kr'){
      for(i=0;i<KR_DST.length;i++){
        if(t>=KR_DST[i][0]){ if(t<KR_DST[i][1]){ return 60; } }
      }
      return 0;
    }

    if(zone==='na'){                                  /* 미국 · 캐나다 */
      if(y>=2007){
        if(t>=ymd(y,3,nthSun(y,3,2))){ if(t<ymd(y,11,nthSun(y,11,1))){ return 60; } }
        return 0;
      }
      if(y>=1987){
        if(t>=ymd(y,4,nthSun(y,4,1))){ if(t<ymd(y,10,lastSun(y,10))){ return 60; } }
        return 0;
      }
      if(y>=1976){
        if(t>=ymd(y,4,lastSun(y,4))){ if(t<ymd(y,10,lastSun(y,10))){ return 60; } }
        return 0;
      }
      return 0;
    }

    if(zone==='eu'){                                  /* 유럽 */
      if(y>=1996){
        if(t>=ymd(y,3,lastSun(y,3))){ if(t<ymd(y,10,lastSun(y,10))){ return 60; } }
        return 0;
      }
      if(y>=1981){
        if(t>=ymd(y,3,lastSun(y,3))){ if(t<ymd(y,9,lastSun(y,9))){ return 60; } }
        return 0;
      }
      return 0;
    }

    if(zone==='au'){                                  /* 호주 남동부 · 뉴질랜드 (남반구) */
      if(y>=2008){
        if(t>=ymd(y,10,nthSun(y,10,1))){ return 60; }
        if(t<ymd(y,4,nthSun(y,4,1))){ return 60; }
        return 0;
      }
      if(y>=1972){
        if(t>=ymd(y,10,lastSun(y,10))){ return 60; }
        if(t<ymd(y,3,lastSun(y,3))){ return 60; }
        return 0;
      }
      return 0;
    }

    return 0;
  }

  /* 옛 방식으로 부르는 화면을 위해 — 경도만 보고 어느 곳이었는지 되찾습니다.
     locate() 가 이 표에서 꺼낸 값이라 소수점까지 그대로 맞습니다. */
  function zoneOfLon(lon, tz){
    var keys=Object.keys(WORLD), i, w;
    for(i=0;i<keys.length;i++){
      w=WORLD[keys[i]];
      if(w[0]===lon){ if(w[2]===tz){ return w[3]; } }
    }
    keys=Object.keys(CITIES);
    for(i=0;i<keys.length;i++){
      if(CITIES[keys[i]][0]===lon){ return 'kr'; }
    }
    return '';
  }

  /* 도시 이름을 받아 좌표를 찾습니다. 못 찾으면 나라 대표 도시로.
     태어난 날짜를 같이 주시면 그날의 서머타임까지 셈해 돌려줍니다. */
  function locate(city, country, y, mo, d){
    var name=(city||'').replace(/\s/g,'').toUpperCase();
    var raw =(city||'').replace(/\s/g,'');
    var keys, i;

    /* 1) 해외 도시를 먼저 봅니다 (이름이 길어 더 정확합니다) */
    keys=Object.keys(WORLD);
    for(i=0;i<keys.length;i++){
      if(raw.indexOf(keys[i])>=0 || name.indexOf(keys[i].toUpperCase())>=0){
        var w=WORLD[keys[i]];
        return { lon:w[0], lat:w[1], tz:w[2], zone:w[3],
                 dst:dstMinutes(w[3],y,mo,d), matched:keys[i], exact:true, korea:false };
      }
    }

    /* 2) 국내 도시 */
    keys=Object.keys(CITIES);
    for(i=0;i<keys.length;i++){
      if(raw.indexOf(keys[i])>=0){
        return { lon:CITIES[keys[i]][0], lat:CITIES[keys[i]][1],
                 tz:koreaTz(y,mo,d), zone:'kr', dst:dstMinutes('kr',y,mo,d),
                 matched:keys[i], exact:true, korea:true };
      }
    }

    /* 3) 못 찾으면 나라 대표 도시 */
    var cc = COUNTRY_CITY[country] || '서울';
    if(CITIES[cc]){
      return { lon:CITIES[cc][0], lat:CITIES[cc][1],
               tz:koreaTz(y,mo,d), zone:'kr', dst:dstMinutes('kr',y,mo,d),
               matched:cc, exact:false, korea:true };
    }
    var g=WORLD[cc];
    return { lon:g[0], lat:g[1], tz:g[2], zone:g[3],
             dst:dstMinutes(g[3],y,mo,d), matched:cc, exact:false, korea:false };
  }

  /* ── 기본 도구 ───────────────────────────────────────────── */
  function jd(y,m,d,h,mi){
    h=h||0; mi=mi||0;
    if(m<=2){ y-=1; m+=12; }
    var A=Math.floor(y/100), B=2-A+Math.floor(A/4);
    return Math.floor(365.25*(y+4716))+Math.floor(30.6001*(m+1))
           +d+B-1524.5+(h+mi/60)/24;
  }

  function sunLon(j){          // 겉보기 황경(도)
    var T=(j-2451545.0)/36525.0;
    var L0=(280.46646+36000.76983*T+0.0003032*T*T)%360;
    var M =(357.52911+35999.05029*T-0.0001537*T*T)%360;
    var Mr=M*Math.PI/180;
    var C =(1.914602-0.004817*T-0.000014*T*T)*Math.sin(Mr)
          +(0.019993-0.000101*T)*Math.sin(2*Mr)+0.000289*Math.sin(3*Mr);
    var om=125.04-1934.136*T;
    return (L0+C-0.00569-0.00478*Math.sin(om*Math.PI/180)+720)%360;
  }

  /* 태양 황경이 deg 가 되는 순간(UT 기준 JD).
     절기는 늘 그 달 4~9일 사이에 떨어지므로 창을 좁게 잡습니다. */
  function findTerm(deg, year, month){
    var lo=jd(year,month,1)-5, hi=jd(year,month,1)+15;
    function f(t){ var d=(sunLon(t)-deg+360)%360; return d>180 ? d-360 : d; }
    for(var i=0;i<60;i++){
      var mid=(lo+hi)/2;
      if(f(lo)*f(mid)<=0){ hi=mid; } else { lo=mid; }
    }
    return (lo+hi)/2;
  }

  /* 한 해의 열두 절기를 시각 순으로 */
  var termCache={};
  function termsOfYear(y){
    if(termCache[y]) return termCache[y];
    var list=TERMS.map(function(t){
      return { jd:findTerm(t.deg, y, t.month), name:t.name, ji:t.ji, deg:t.deg };
    }).sort(function(a,b){ return a.jd-b.jd; });
    termCache[y]=list;
    return list;
  }
  /* 앞뒤 해까지 이어 붙인 절기 목록 */
  function termsAround(y){
    return termsOfYear(y-1).concat(termsOfYear(y), termsOfYear(y+1));
  }

  /* 균시차(분) */
  function eqOfTime(j){
    var T=(j-2451545.0)/36525.0;
    var L0=(280.46646+36000.76983*T)%360;
    var M =(357.52911+35999.05029*T)%360;
    var e =0.016708634-0.000042037*T;
    var eps=23.439291-0.0130042*T;
    var y=Math.pow(Math.tan(eps/2*Math.PI/180),2);
    var Mr=M*Math.PI/180, L0r=L0*Math.PI/180;
    var E=y*Math.sin(2*L0r)-2*e*Math.sin(Mr)+4*e*y*Math.sin(Mr)*Math.cos(2*L0r)
         -0.5*y*y*Math.sin(4*L0r)-1.25*e*e*Math.sin(2*Mr);
    return E*180/Math.PI*4;
  }

  function pad(n){ return (n<10?'0':'')+n; }

  /* ── 본체 ────────────────────────────────────────────────── */
  /* opts = {year, month, day, hour, minute, sex:'M'|'F',
             lon, lat, tz}  (tz 는 표준시 오프셋, 한국은 9) */
  function compute(opts){
    var y=opts.year, mo=opts.month, d=opts.day;
    /* 워드프레스가 script 안의 논리연산자 두 개짜리 기호를 망가뜨려서, if 를 겹쳐 씁니다 */
    var hourKnown = true;
    if(opts.hour===null){ hourKnown=false; }
    if(opts.hour===undefined){ hourKnown=false; }
    var h = hourKnown ? opts.hour : 12;
    var mi= opts.minute || 0;
    var lon=126.978; if(opts.lon!==undefined){ if(opts.lon!==null){ lon=opts.lon; } }
    var lat=37.5665; if(opts.lat!==undefined){ if(opts.lat!==null){ lat=opts.lat; } }
    var tz=9; if(opts.tz!==undefined){ if(opts.tz!==null){ tz=opts.tz; } }

    /* 어느 시간대 규칙을 쓰는 곳인지 — 안 알려주면 경도로 되찾습니다 */
    var zone=''; if(opts.zone){ zone=opts.zone; }
    if(zone===''){ zone=zoneOfLon(lon, tz); }

    /* 우리나라 표준시는 1954~1961 사이에 동경 127.5도였습니다 */
    if(zone==='kr'){ tz=koreaTz(y,mo,d); }

    /* 서머타임을 쓰던 날이면 시계가 한 시간 앞서 있었습니다 */
    var dstMin=0;
    if(opts.dst!==undefined){ if(opts.dst!==null){ dstMin=opts.dst; } }
    else { dstMin=dstMinutes(zone, y, mo, d); }

    var clockMin=h*60+mi;
    var stdMin=clockMin-dstMin;        // 시계에서 서머타임을 벗긴 표준시

    var jdUT = jd(y,mo,d) + stdMin/1440 - tz/24;

    /* 1) 진태양시 */
    var lonCorr=(lon-tz*15)*4;          // 표준자오선과의 경도차 (분)
    var eot=eqOfTime(jdUT);
    var trueMin=stdMin+lonCorr+eot;
    var dayShift=0;
    while(trueMin<0){ trueMin+=1440; dayShift-=1; }
    while(trueMin>=1440){ trueMin-=1440; dayShift+=1; }
    /* 보여줄 때 쓸 분 단위. 먼저 반올림해야 02:60 같은 표기가 안 나옵니다. */
    var showMin=Math.round(trueMin);
    if(showMin>=1440){ showMin-=1440; }

    /* 2) 절기 — 태어난 순간이 어느 절 안에 있는지 */
    var jdLocal=jdUT;
    var around=termsAround(y);
    var found=null;
    for(var i=0;i<around.length;i++){
      if(around[i].jd<=jdLocal){ found=around[i]; } else { break; }
    }
    var monthJi = found ? found.ji : 2;
    var termName= found ? found.name : '입춘';

    /* 3) 연주 — 입춘을 새해로 봅니다 */
    var ipchun=findTerm(315, y, 2);
    var sajuYear = (jdLocal < ipchun) ? y-1 : y;
    var yg=((sajuYear-4)%10+10)%10;
    var yz=((sajuYear-4)%12+12)%12;

    /* 4) 월주 — 오호둔(五虎遁): 연간에 따라 인월의 천간이 정해집니다 */
    var startGan=[2,4,6,8,0][yg%5];      // 갑기→丙, 을경→戊, 병신→庚, 정임→壬, 무계→甲
    var fromTiger=((monthJi-2)%12+12)%12;      // 인월(寅)에서 몇 달째인지
    var mg=((startGan+fromTiger)%10+10)%10;
    var mz=monthJi;

    /* 5) 일주 — 1900-01-01(KST) 을 갑술일로 잡습니다.
          자시(23시)부터 다음 날로 넘기는 만세력 방식을 씁니다. */
    var dayNo=Math.round(jd(y,mo,d)-jd(1900,1,1))+dayShift;
    if(trueMin>=23*60){ dayNo+=1; }
    var dg=((dayNo)%10+10)%10;
    var dz=((dayNo+10)%12+12)%12;

    /* 6) 시주 — 오자둔(五子遁) */
    var hz=null, hg=null;
    if(hourKnown){
      hz=Math.floor(((trueMin+60)%1440)/120);   // 23~01 이 자시
      hg=((dg%5)*2+hz)%10;
    }

    /* 7) 오행 — 최대잔여법으로 반올림해 합이 100 이 되게 맞춥니다 */
    var gans=[yg,mg,dg], jis=[yz,mz,dz];
    if(hourKnown){ gans.push(hg); jis.push(hz); }
    var cnt={}; ELEMENTS.forEach(function(e){ cnt[e]=0; });
    gans.forEach(function(g){ cnt[GAN_EL[g]]++; });
    jis.forEach(function(z){ cnt[JI_EL[z]]++; });
    var totalChars=gans.length+jis.length;
    var raw=ELEMENTS.map(function(e){ return {el:e, n:cnt[e], exact:cnt[e]/totalChars*100}; });
    var floors=raw.map(function(r){ return Math.floor(r.exact); });
    var rest=100-floors.reduce(function(a,b){return a+b;},0);
    var order=raw.map(function(r,i){ return {i:i, frac:r.exact-Math.floor(r.exact)}; })
                 .sort(function(a,b){ return b.frac-a.frac; });
    for(var k=0;k<rest;k++){ floors[order[k%5].i]+=1; }
    var five=raw.map(function(r,i){ return {element:r.el, count:r.n, percent:floors[i]}; });

    /* 8) 대운 — 양남음녀는 순행, 음남양녀는 역행 */
    var yangYear=(yg%2===0);
    var male=(opts.sex==='M');
    var forward = (yangYear===male);
    var luckJd, luckDays;
    if(forward){
      luckJd=nextTermJd(jdLocal, y);  luckDays=luckJd-jdLocal;
    } else {
      luckJd=prevTermJd(jdLocal, y);  luckDays=jdLocal-luckJd;
    }
    var startAge=luckDays/3;
    var luck=[];
    for(var n=1;n<=8;n++){
      var lg=((mg+(forward?n:-n))%10+10)%10;
      var lz=((mz+(forward?n:-n))%12+12)%12;
      var a0=startAge+(n-1)*10;
      luck.push({ from:Math.round(a0*10)/10, to:Math.round((a0+10)*10)/10,
                  fromYear:y+Math.floor(a0), toYear:y+Math.floor(a0)+10,
                  gan:lg, ji:lz, han:GAN_H[lg]+JI_H[lz], kor:GAN_L[lg]+JI_L[lz] });
    }

    /* 9) 별 — 태양 · 상승궁 · 천정 */
    var sun=sunLon(jdUT);
    var T=(jdUT-2451545.0)/36525.0;
    var eps=(23.439291-0.0130042*T)*Math.PI/180;
    var d0=jdUT-2451545.0;
    var gmst=((280.46061837+360.98564736629*d0)%360+360)%360;
    var lst=((gmst+lon)%360+360)%360;
    var ramc=lst*Math.PI/180, phir=lat*Math.PI/180;
    var mc=(Math.atan2(Math.sin(ramc), Math.cos(ramc)*Math.cos(eps))*180/Math.PI+360)%360;
    var asc=(Math.atan2(Math.cos(ramc),
             -(Math.sin(eps)*Math.tan(phir)+Math.cos(eps)*Math.sin(ramc)))*180/Math.PI+360)%360;

    /* 경계에 걸린 분께는 알려드려야 합니다 */
    var warnings=[];
    if(found){
      var minsFromTerm=(jdLocal-found.jd)*1440;
      if(minsFromTerm<180){
        warnings.push('태어나신 시각이 ' + found.name + ' 로 넘어온 지 ' +
          Math.round(minsFromTerm) + '분밖에 안 됩니다. 절기 계산에 몇 분의 오차가 있을 수 있어 ' +
          '월주가 앞 달로 바뀔 가능성이 있습니다.');
      }
      var nextJd=nextTermJd(jdLocal, y);
      if(nextJd!==null){
        var minsToTerm=(nextJd-jdLocal)*1440;
        if(minsToTerm<180){
          warnings.push('태어나신 시각이 다음 절기까지 ' + Math.round(minsToTerm) +
            '분 남은 자리입니다. 월주가 다음 달로 바뀔 가능성이 있습니다.');
        }
      }
    }
    if(hourKnown){
      var intoHour=((trueMin+60)%1440)%120;
      if(intoHour<10 || intoHour>110){
        warnings.push('진태양시가 시주 경계에 붙어 있습니다. 태어난 시각이 10분만 달라도 시주가 바뀝니다.');
      }
    }
    if(dstMin>0){
      warnings.push('태어나신 날은 서머타임(일광절약시간)을 쓰던 기간입니다. ' +
        '그때 시계는 실제 해보다 한 시간 앞서 있었기 때문에, 한 시간을 빼고 세웠습니다.');
    }
    if(tz===8.5){
      warnings.push('1954년 3월부터 1961년 8월까지 우리나라 표준시는 동경 127.5도 기준이었습니다. ' +
        '지금 기준과 30분이 다르므로 그때 기준으로 세웠습니다.');
    }
    if(!hourKnown){
      warnings.push('태어난 시간을 모르셔서 시주는 세우지 않았습니다. ' +
        '시주가 빠지면 하루의 결이 흐려지고, 특히 자식·말년 자리를 읽기 어렵습니다.');
    }

    var out = {
      warnings: warnings,
      trueSolar:{
        clock: pad(h)+':'+pad(mi),
        tz: tz,
        zone: zone,
        dst: dstMin,
        lonCorrection: Math.round(lonCorr*10)/10,
        equationOfTime: Math.round(eot*10)/10,
        time: pad(Math.floor(showMin/60))+':'+pad(showMin%60),
        dayShift: dayShift
      },
      term:{ name:termName, monthJi:monthJi },
      sajuYear: sajuYear,
      pillars:{
        year:{ gan:yg, ji:yz, han:GAN_H[yg]+JI_H[yz], kor:GAN_L[yg]+JI_L[yz] },
        month:{ gan:mg, ji:mz, han:GAN_H[mg]+JI_H[mz], kor:GAN_L[mg]+JI_L[mz] },
        day:{ gan:dg, ji:dz, han:GAN_H[dg]+JI_H[dz], kor:GAN_L[dg]+JI_L[dz] },
        hour: hourKnown ? { gan:hg, ji:hz, han:GAN_H[hg]+JI_H[hz], kor:GAN_L[hg]+JI_L[hz] } : null
      },
      dayMaster:{ gan:dg, han:GAN_H[dg], kor:GAN_L[dg], element:GAN_EL[dg],
                  yin: (dg%2===1) },
      animal: JI_ANIMAL[yz],
      five: five,
      luck:{ forward:forward, startAge:Math.round(startAge*10)/10, list:luck },
      stars:{
        sun: signOf(sun), sunDeg: Math.round(sun*10)/10,
        ascendant: signOf(asc), ascDeg: Math.round(asc*10)/10,
        midheaven: signOf(mc), mcDeg: Math.round(mc*10)/10
      }
    };
    LAST = out;
    return out;
  }

  /* 마지막으로 세운 사주 — 화면이 문구를 고를 때 씁니다 */
  var LAST = null;
  function lastChart(){ return LAST; }

  function signOf(x){
    return { name:SIGNS[Math.floor(x/30)], degree:Math.round((x%30)*10)/10 };
  }

  /* 출생 시각 바로 다음 절기 */
  function nextTermJd(jdLocal, y){
    var list=termsAround(y);
    for(var i=0;i<list.length;i++){ if(list[i].jd>jdLocal) return list[i].jd; }
    return null;
  }
  /* 출생 시각 바로 앞 절기 */
  function prevTermJd(jdLocal, y){
    var list=termsAround(y), best=null;
    for(var i=0;i<list.length;i++){ if(list[i].jd<=jdLocal){ best=list[i].jd; } else { break; } }
    return best;
  }

  root.StellaSaju={ compute:compute, locate:locate, lastChart:lastChart,
                    CITIES:CITIES, WORLD:WORLD,
                    koreaTz:koreaTz, dstMinutes:dstMinutes, GAN_H:GAN_H, JI_H:JI_H,
                    GAN_L:GAN_L, JI_L:JI_L, ELEMENTS:ELEMENTS,
                    terms:termsOfYear, sunLon:sunLon, jd:jd };
})(typeof window!=='undefined' ? window : globalThis);

if(typeof module!=='undefined'){ module.exports=globalThis.StellaSaju; }
