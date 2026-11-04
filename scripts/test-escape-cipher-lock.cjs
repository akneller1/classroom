/* Shared and standalone Escape Room numeric-cipher progression regression.
 * Every cipher stays hidden until a correct numerical answer is locked.
 * Incorrect answers cost exactly 30 seconds. A correct answer reveals +1,
 * but the student must shift forward manually to decode the next-room clue. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');

class FakeNode{
  constructor(){this.value='';this.hidden=true;this._text='';this.html='';this.children=[];
    this.style={};this.offsetWidth=1;this.disabled=false;
    this.classList={add(){},remove(){},toggle(){}};}
  set textContent(x){this._text=String(x);this.children=[];}
  get textContent(){return this._text+this.children.map(n=>n.textContent).join('');}
  set innerHTML(x){this.html=String(x);}
  get innerHTML(){return this.html;}
  appendChild(n){this.children.push(n);return n;}
  closest(){return this;}
}
function run(source,filename,shared){
 function sandbox(){
  const nodes=new Map();
  const get=sel=>{if(!nodes.has(sel))nodes.set(sel,new FakeNode());return nodes.get(sel);};
  const document={querySelector:get,createElement:()=>new FakeNode(),
    createTextNode:t=>{const n=new FakeNode();n.textContent=t;return n;}};
  const env={document,location:{search:'',hash:''},URLSearchParams,
    setInterval:()=>1,clearInterval(){},console,Math,Date};env.window=env;
  vm.createContext(env);
  return {env,get};
 }
 if(shared){
  for(const shift of [1,5,13,25]){
   const {env,get}=sandbox();
   const stage={type:'cipher',name:'Cipher',shift,plain:'THE KEY IS STAR',
    answer:'STAR',prompt:'Solve x + 2 = '+(shift+2),
    scene:{kind:'emoji',items:[]},hints:[],stamp:1,letter:'A'};
   env.MK_ACTIVE_ESCAPE_ROOM={title:'Test',intro:'Test',endEmoji:'*',
    stages:[stage],word:'A',finalAsk:'Code',finalStory:'Done'};
   vm.runInContext(source,env,{filename,timeout:2000});
   check(env,get,stage,filename+' shift '+shift);
  }
 }else{
  const {env,get}=sandbox();
  assert.match(source,/cipher\(s\)/,filename+': cipher renderer');
  const scripts=[...source.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)];
  scripts.forEach(m=>new vm.Script(m[1],{filename}));
  let code=scripts.map(m=>m[1]).find(x=>x.includes('const ROOM='));
  assert.ok(code,filename+': ROOM declaration');
  code=code.replace('const TOTAL=',"ROOM.stages=ROOM.stages.filter(s=>s.type==='cipher'); const TOTAL=");
  vm.runInContext(code,env,{filename,timeout:2000});
  const stages=vm.runInContext('STAGES',env);
  assert.equal(stages.length,1,filename+': expected one cipher stage');
  check(env,get,stages[0],filename);
 }
}
function check(env,get,stage,label){
 const time=()=>typeof env.MK_ESCAPE_STATE==='function'?env.MK_ESCAPE_STATE().t:vm.runInContext('t',env);
 const roomIndex=()=>typeof env.MK_ESCAPE_STATE==='function'?env.MK_ESCAPE_STATE().stage:vm.runInContext('stage',env);
 const cipherSteps=()=>typeof env.MK_ESCAPE_STATE==='function'?env.MK_ESCAPE_STATE().st.k:vm.runInContext('st.k',env);
 env.start();
 const html=get('#app').innerHTML;
 assert.match(html,/Lock in this answer/,label+': numerical answer lock');
 assert.match(html,/id="cipherReveal"[^>]*hidden/,label+': +1 control initially hidden');
 assert.match(html,/onclick="sh\(1\)"/,label+': only +1 key');
 assert.doesNotMatch(html,/decodedShift|Shift the cipher BACKWARD/,label+': no automatic shift answer');
 const wrong=stage.shift===1?2:stage.shift-1;
 env.sh(1);
 assert.equal(cipherSteps(),0,label+': cannot shift before correct math');
 get('#shiftGuess').value=String(wrong);
 env.lockShift();
 assert.equal(time(),570,label+': incorrect lock costs 30 seconds');
 assert.notEqual(get('#cipherReveal').hidden,false,label+': wrong answer cannot access cipher');
 get('#shiftGuess').value=String(stage.shift);
 env.lockShift();
 assert.equal(time(),570,label+': no penalty for correct lock');
 assert.equal(get('#cipherReveal').hidden,false,label+': +1 key is unlocked');
 assert.equal(cipherSteps(),0,label+': no automatic cipher shift');
 assert.notEqual(get('#dec').textContent,stage.plain,label+': clue remains encoded');
 assert.notEqual(get('#cipherWordRow').hidden,false,label+': word input hidden before manual shifting');
 env.chkCipher();
 assert.equal(roomIndex(),0,label+': cannot bypass shifting');
 for(let n=1;n<stage.shift;n++){
  env.sh(1);
  assert.equal(cipherSteps(),n,label+': exactly one forward shift per click');
  assert.notEqual(get('#dec').textContent,stage.plain,label+': intermediate text remains encoded');
  assert.notEqual(get('#cipherWordRow').hidden,false,label+': word input remains hidden');
 }
 env.sh(1);
 assert.equal(cipherSteps(),stage.shift,label+': total shifts equals answer');
 assert.equal(get('#dec').textContent,stage.plain,label+': readable clue after manual shifts');
 assert.equal(get('#cipherWordRow').hidden,false,label+': word input now shown');
 get('#w').value=stage.answer;
 env.chkCipher();
 assert.equal(roomIndex(),1,label+': correct clue unlocks next room');
}
const shared='worksheet-generator/games/escape-runtime.js';
run(fs.readFileSync(path.join(root,shared),'utf8'),shared,true);
const artifacts=fs.readdirSync(path.join(root,'artifacts'))
  .filter(d=>d.includes('escape-room')&&fs.existsSync(path.join(root,'artifacts',d,'index.html')));
for(const dir of artifacts){
 const file='artifacts/'+dir+'/index.html';
 run(fs.readFileSync(path.join(root,file),'utf8'),file,false);
}
console.log('PASS: shared cipher and '+artifacts.length+' standalone rooms unlock the +1 key after numeric answers and require manual forward decoding.');
