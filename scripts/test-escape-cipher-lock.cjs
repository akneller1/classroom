/* Shared and standalone Escape Room numeric-cipher progression regression.
 * Every cipher stays hidden until a correct numerical answer is locked.
 * An incorrect lock costs exactly 30 seconds and a correct one exposes
 * the actual shift and decoded next-room clue. */
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
  const nodes=new Map();
  const get=sel=>{if(!nodes.has(sel))nodes.set(sel,new FakeNode());return nodes.get(sel);};
  const document={querySelector:get,createElement:()=>new FakeNode(),
    createTextNode:t=>{const n=new FakeNode();n.textContent=t;return n;}};
  const env={document,location:{search:'',hash:''},URLSearchParams,
    setInterval:()=>1,clearInterval(){},console,Math,Date};
  env.window=env;
  if(shared){
    for(const shift of [1,5,13,25]){
      const stage={type:'cipher',name:'Cipher',shift,plain:'THE KEY IS STAR',
        answer:'STAR',prompt:'Solve x + 2 = '+(shift+2),
        scene:{kind:'emoji',items:[]},hints:[],stamp:1,letter:'A'};
      env.MK_ACTIVE_ESCAPE_ROOM={title:'Test',intro:'Test',endEmoji:'*',
        stages:[stage],word:'A',finalAsk:'Code',finalStory:'Done'};
      vm.createContext(env);
      vm.runInContext(source,env,{filename,timeout:2000});
      check(env,get,stage,filename+' shift '+shift);
      nodes.clear();
    }
  } else {
    assert.match(source,/cipher\(s\)/,filename+': cipher renderer');
    const scripts=[...source.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)];
    scripts.forEach(m=>new vm.Script(m[1],{filename}));
    let code=scripts.map(m=>m[1]).find(x=>x.includes('const ROOM='));
    assert.ok(code,filename+': ROOM declaration');
    code=code.replace('const TOTAL=',"ROOM.stages=ROOM.stages.filter(s=>s.type==='cipher'); const TOTAL=");
    vm.createContext(env);
    vm.runInContext(code,env,{filename,timeout:2000});
    const stages=vm.runInContext('STAGES',env);
    assert.equal(stages.length,1,filename+': expected one cipher stage');
    check(env,get,stages[0],filename);
  }
}
function check(env,get,stage,label){
  env.start();
  const html=get('#app').innerHTML;
  assert.match(html,/Lock in this answer/,label+': numerical answer lock control');
  assert.match(html,/id="cipherReveal"[^>]*hidden/,label+': next-room clue starts hidden');
  assert.doesNotMatch(html,/Lock shift \(wrong/,label+': old shift picker absent');
  const wrong=stage.shift===1?2:stage.shift-1;
  get('#shiftGuess').value=String(wrong);
  env.lockShift();
  assert.equal(vm.runInContext('t',env),570,label+': wrong lock takes exactly 30 seconds');
  assert.notEqual(get('#cipherReveal').hidden,false,label+': wrong answer does not reveal clue');
  get('#shiftGuess').value=String(stage.shift);
  env.lockShift();
  assert.equal(vm.runInContext('t',env),570,label+': correct answer has no penalty');
  assert.equal(get('#cipherReveal').hidden,false,label+': correct lock reveals clue');
  assert.equal(get('#decodedShift').textContent,String(stage.shift),label+': displayed shift matches numerical answer');
  assert.equal(get('#dec').textContent,stage.plain,label+': clue is decoded correctly');
  assert.equal(get('#shiftGuess').disabled,true,label+': locked numeric answer is immutable');
  get('#w').value=stage.answer;
  env.chkCipher();
  assert.equal(vm.runInContext('stage',env),1,label+': correct clue unlocks next room');
}
const shared='worksheet-generator/games/escape-runtime.js';
run(fs.readFileSync(path.join(root,shared),'utf8'),shared,true);
const artifacts=fs.readdirSync(path.join(root,'artifacts'))
  .filter(d=>d.includes('escape-room')&&fs.existsSync(path.join(root,'artifacts',d,'index.html')));
for(const dir of artifacts){
 const file='artifacts/'+dir+'/index.html';
 run(fs.readFileSync(path.join(root,file),'utf8'),file,false);
}
console.log('PASS: shared cipher and '+artifacts.length+' standalone rooms lock numerics before revealing decoded clues.');
