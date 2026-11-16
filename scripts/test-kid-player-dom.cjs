// Exercise the assembled question-card events without a browser dependency.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
class Node{
 constructor(tag){this.tagName=tag;this.children=[];this.attributes={};this.style={};this.dataset={};this.value='';this.className='';this.classList={add:(...v)=>{this.className+=' '+v.join(' ')},toggle:(v,on)=>{let s=new Set(this.className.split(' '));if(on===undefined)on=!s.has(v);on?s.add(v):s.delete(v);this.className=[...s].join(' ');return on},contains:v=>this.className.split(' ').includes(v)};}
 appendChild(n){n.parent=this;this.children.push(n);return n}setAttribute(k,v){this.attributes[k]=String(v)}getAttribute(k){return this.attributes[k]}set innerHTML(s){this.children=[];this.html=s}get innerHTML(){return this.html||''}get textContent(){return this.text||''}set textContent(s){this.text=String(s)}focus(){}dispatchEvent(){}remove(){if(this.parent)this.parent.children=this.parent.children.filter(n=>n!==this)}querySelectorAll(s){const match=n=>s.startsWith('.')?n.classList.contains(s.slice(1)):n.tagName===s;return this.children.flatMap(n=>[...(match(n)?[n]:[]),...n.querySelectorAll(s)])}querySelector(s){return this.querySelectorAll(s)[0]||null}
}
const site=path.resolve(process.argv[2]||'_site');
for(let grade=1;grade<=5;grade++){
 const body=new Node('body'),storage={},G={document:{body,head:new Node('head'),createElement:t=>new Node(t),documentElement:new Node('html')},URLSearchParams,location:{search:'',pathname:'/grade'+grade+'/worksheet-generator/grade'+grade+'-games.html'},setTimeout:f=>f(),console,Event:class{},localStorage:{getItem:k=>storage[k],setItem:(k,v)=>storage[k]=v},MK_ELEMENTARY:{course:'math'+grade},MK_KID_BASE:'kid-ui/'};G.window=G;vm.createContext(G);
 const dir=path.join(site,'grade'+grade,'worksheet-generator',grade===5?'grade5':'elementary');for(const f of ['kid-ui/read-aloud.js','kid-ui/kid-ui.js',grade===5?'g5-core.js':'el-core.js'])vm.runInContext(fs.readFileSync(path.join(dir,f),'utf8'),G);
 const K=G.MKEL||G.G5,prefix=grade===5?'g5':'el',host=new Node('main');let answered=null,next=0;
 K.card(host,{prompt:'What is 2 + 3?',answer:'5',kind:'sa',steps:['Add 2 and 3.','The sum is 5.'],meta:{}},{onAnswer:ok=>answered=ok,onNext:()=>next++});
 const input=host.querySelector('input'),read=host.querySelector('.el-read-aloud');assert(read&&read.disabled,'Speech control falls back when speech is unavailable');
 if(grade<=2){const pad=host.querySelector('.kid-pad');assert(pad);assert.equal(input.getAttribute('inputmode'),'none');const five=pad.children.find(b=>b.textContent==='5');five.onclick();assert.equal(input.value,'5');pad.children.find(b=>b.textContent==='✓').onclick();assert(pad.children.every(b=>b.disabled));five.onclick();assert.equal(input.value,'5','Finished answer cannot be edited through pad')}
 else{assert(!host.querySelector('.kid-pad'));input.value='5';host.querySelector('.'+prefix+'-typed').children.find(b=>b.tagName==='button').onclick()}
 assert.equal(answered,true);host.querySelector('.'+prefix+'-q-tools').children.find(b=>b.textContent==='Next →').onclick();assert.equal(next,1);
 // Correct answer after a retry and an exhausted incorrect answer both finish once.
 for(const values of [['4','5'],['4','4']]){let count=0,result;K.card(host,{prompt:'2 + 3 = ?',answer:'5',kind:'sa',steps:[],meta:{}},{onAnswer:ok=>{count++;result=ok}});const inp=host.querySelector('input'),go=host.querySelector('.'+prefix+'-typed').children.find(b=>b.tagName==='button');for(const value of values){inp.value=value;go.onclick()}assert.equal(count,1);assert.equal(result,values[1]==='5');go.onclick();assert.equal(count,1)}
 storage['mk-sticker-book']='null';G.MKKid.finish(host,{right:3,total:3,grade,unit:'test'});G.MKKid.finish(host,{right:3,total:3,grade,unit:'test'});assert.equal(host.querySelectorAll('.kid-sticker').at(-1).src,'kid-ui/stickers/trophy.svg');
 for(let i=0;i<20;i++)G.MKKid.finish(host,{right:1,total:3,grade,unit:'test'});assert.equal(JSON.parse(storage['mk-sticker-book']).test.length,12);
 G.localStorage.getItem=()=>{throw Error('blocked')};G.localStorage.setItem=()=>{throw Error('blocked')};assert.doesNotThrow(()=>G.MKKid.finish(host,{right:1,total:2,grade,unit:'test'}));
 console.log('PASS Grade '+grade+' answer events, retries, disabled keypad, next question, rewards and blocked/corrupt storage');
}
