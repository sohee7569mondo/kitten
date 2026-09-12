const fs=require('fs'), vm=require('vm');
const N=fs.readdirSync('blocks').filter(f=>f.endsWith('.js')).length;
function el(id){ return { id, style:{}, _t:'', _h:'',
  get textContent(){return this._t;}, set textContent(v){this._t=v;},
  get innerHTML(){return this._h;}, set innerHTML(v){this._h=v;},
  setAttribute(){}, getAttribute(){return null;}, addEventListener(){},
  appendChild(){}, insertBefore(){}, getElementsByTagName(){return [];},
  querySelector(){return null;}, querySelectorAll(){return [];},
  classList:{add(){},remove(){},contains(){return false;}}, children:[], firstChild:null }; }
function run(slug, topic){
  const store={}, els={};
  const get=id=>{ if(!els[id]) els[id]=el(id); return els[id]; };
  const doc={ getElementById:get, querySelector:()=>null, querySelectorAll:()=>[],
    createElement:()=>el('x'), addEventListener(){}, body:el('body'), readyState:'complete', documentElement:el('html') };
  const win={ localStorage:{ getItem:k=>(k in store?store[k]:null), setItem:(k,v)=>{store[k]=String(v)}, removeItem:k=>{delete store[k]} },
    document:doc, location:{search:'',href:'x'}, addEventListener(){}, print(){}, Date, Math, JSON, console };
  win.window=win;
  const ctx=vm.createContext(win);
  ctx.localStorage=win.localStorage; ctx.document=doc; ctx.location=win.location;
  ctx.setTimeout=f=>{try{f()}catch(e){}}; ctx.console={log(){},warn(){},error(){}};
  const order={ guardian_slug:slug, topic, profile:{ name:'덕선', year:1971,month:9,day:17,hour:8,minute:20,sex:'F',city:'서울',country:'KR' } };
  store['stella_demo']=JSON.stringify(order);
  store['stella_answers']=JSON.stringify({});
  for(let i=0;i<N;i++){
    try{ vm.runInContext(fs.readFileSync('blocks/b'+String(i).padStart(2,'0')+'.js','utf8'), ctx, {filename:'b'+i}); }catch(e){}
  }
  return els['bkBook']?els['bkBook']._h:'';
}
function grab(html, head){
  const i=html.indexOf(head); if(i<0) return '(그 장을 못 찾음)';
  const j=html.indexOf('</section>', i); 
  return html.slice(i, j<0? i+2600 : Math.min(j, i+2600)).replace(/<[^>]+>/g,'').replace(/\s+/g,' ').trim();
}
const TOPICS=['직장운','취업운','이직운','퇴사운','사업운','재물운'];
const out={};
for(const t of TOPICS) out[t]=run('door-career', t);
for(const head of ['풀어보면','올해의 시기 흐름','나에게 맞는 일의 결']){
  console.log('\n════════ ' + head + ' ════════');
  const seen={};
  for(const t of TOPICS){
    const txt=grab(out[t], head).slice(0,160);
    const key=grab(out[t], head);
    seen[key]=(seen[key]||[]).concat(t);
    console.log(('  '+t).padEnd(10)+' │ '+txt);
  }
  const groups=Object.values(seen);
  const dup=groups.filter(g=>g.length>1);
  console.log('  → 서로 다른 글: '+groups.length+'가지 / 6주제'+(dup.length?('   같은 것끼리: '+dup.map(g=>g.join('=')).join(', ')):'   전부 다름'));
}
