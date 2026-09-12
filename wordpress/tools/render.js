const fs=require('fs'), vm=require('vm'), path=require('path');
const DIR=process.argv[2], DEMO=process.argv[3]||'door-love-2';

function El(tag){
  return {
    tagName:(tag||'div').toUpperCase(), _html:'', _text:'', style:{}, dataset:{},
    classList:{add(){},remove(){},toggle(){},contains(){return false;}},
    children:[], attributes:{},
    get innerHTML(){return this._html;}, set innerHTML(v){this._html=v;},
    get textContent(){return this._text;}, set textContent(v){this._text=v;},
    get value(){return this._value||'';}, set value(v){this._value=v;},
    setAttribute(k,v){this.attributes[k]=v;}, getAttribute(k){return this.attributes[k];},
    removeAttribute(k){delete this.attributes[k];},
    appendChild(c){this.children.push(c); return c;}, removeChild(){}, remove(){},
    addEventListener(){}, removeEventListener(){}, insertAdjacentHTML(){},
    querySelector(){return null;}, querySelectorAll(){return [];}, getElementsByTagName(){return [];}, getElementsByClassName(){return [];},
    closest(){return null;}, focus(){}, click(){}, scrollIntoView(){},
    getBoundingClientRect(){return {top:0,left:0,width:0,height:0,bottom:0,right:0};}
  };
}
const els={};
function get(id){ if(!els[id]){ els[id]=El('div'); els[id].id=id; } return els[id]; }

const store={};
const doc={
  readyState:'complete',
  getElementById:get,
  querySelector(){return null;}, querySelectorAll(){return [];},
  createElement:El, createTextNode(t){const e=El('span'); e._text=t; return e;},
  addEventListener(t,f){ if(t==='DOMContentLoaded'){ try{f();}catch(e){} } },
  removeEventListener(){},
  body:El('body'), head:El('head'), documentElement:El('html'),
  cookie:'', title:''
};
doc.body.appendChild=function(c){return c;};

const ctx={
  console, setTimeout:(f)=>{try{f();}catch(e){}}, clearTimeout(){},
  setInterval(){return 0;}, clearInterval(){}, requestAnimationFrame:(f)=>{try{f();}catch(e){}},
  document:doc,
  location:{href:'https://stellasaju.com/reading-book/?demo='+DEMO, search:'?demo='+DEMO,
            pathname:'/reading-book/', origin:'https://stellasaju.com', hash:'', host:'stellasaju.com',
            protocol:'https:', replace(){}, assign(){}, reload(){}},
  localStorage:{getItem:k=>(k in store?store[k]:null), setItem:(k,v)=>{store[k]=String(v);},
                removeItem:k=>{delete store[k];}, clear(){}},
  sessionStorage:{getItem:()=>null, setItem(){}, removeItem(){}, clear(){}},
  navigator:{userAgent:'node', language:'ko-KR'},
  history:{replaceState(){},pushState(){}},
  fetch:()=>Promise.resolve({ok:false,json:()=>Promise.resolve({}),text:()=>Promise.resolve('')}),
  matchMedia:()=>({matches:false, addListener(){}, addEventListener(){}}),
  alert(){}, confirm(){return true;}, prompt(){return null;},
  addEventListener(){}, removeEventListener(){},
  screen:{width:1200,height:900}, innerWidth:1200, innerHeight:900,
  scrollTo(){}, print(){},
  URLSearchParams, encodeURIComponent, decodeURIComponent, Intl
};
ctx.window=ctx; ctx.self=ctx; ctx.globalThis=ctx;
vm.createContext(ctx);

const files=fs.readdirSync(DIR).filter(f=>/^b\d+\.js$/.test(f)).sort();
let errs=0;
for(const f of files){
  try{ vm.runInContext(fs.readFileSync(path.join(DIR,f),'utf8'), ctx, {filename:f}); }
  catch(e){ errs++; console.error('['+f+'] '+e.message); }
}
const html=get('bkBook').innerHTML||'';
console.log('오류 블록:', errs);
console.log('책 길이:', html.length);
fs.writeFileSync(DIR+'/../rendered.html', html);
