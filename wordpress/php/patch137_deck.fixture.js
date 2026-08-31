  var DECKSEQ=[];
  try{ DECKSEQ=(function(){
    var P={};
    if(ORDER){ if(ORDER.profile){ P=ORDER.profile; } }
    var now=new Date();
    var seed = (P.year||0)*10007 + (P.month||0)*331 + (P.day||0)*97
             + (P.hour||0)*13 + (P.minute||0)*7
             + now.getFullYear()*1103 + (now.getMonth()+1)*37 + now.getDate()*3 + 11;
    var s = seed % 2147483647;
    if(s<=0){ s += 2147483646; }
    function rnd(){ s=(s*16807)%2147483647; return (s-1)/2147483646; }
    var pool=POOL[SLUG]; if(!pool){ pool=POOL['door-tarot']; }
    var a=pool.slice();
    for(var j=a.length-1;j>0;j--){
      var k=Math.floor(rnd()*(j+1));
      var tmp=a[j]; a[j]=a[k]; a[k]=tmp;
    }
    return a;
  }()); }catch(err){ DECKSEQ=[0,1,2,3,4,5,6,7,8,9,10,11]; }
