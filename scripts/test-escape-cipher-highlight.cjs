'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const files=['worksheet-generator/games/escape-runtime.js',...fs.readdirSync(path.join(root,'artifacts')).map(d=>'artifacts/'+d+'/index.html').filter(p=>fs.existsSync(path.join(root,p))&&fs.readFileSync(path.join(root,p),'utf8').includes('function sh(d)'))];
class Node {
 constructor(tag='#text',text=''){this.tagName=tag;this.children=[];this.style={};this._text=text;this.hidden=true;this.value='';}
 set textContent(v){this._text=String(v);this.children=[];}
 get textContent(){return this._text+this.children.map(n=>n.textContent).join('');}
 appendChild(n){this.children.push(n);return n;}
}
function check(source,s){
 const nodes=new Map(['#dec','#kk','#cipherWordRow','#w'].map(id=>[id,new Node('div')]));
 const c={STAGES:[s],stage:0,st:{k:0,shiftLocked:false},$:id=>nodes.get(id),
  say(){},document:{createElement:tag=>new Node(tag),createTextNode:t=>new Node('#text',t)}};
 vm.createContext(c);
 const start=source.indexOf('function renderDecodedCipher('),stop=source.indexOf('function chkCipher(',start);
 vm.runInContext(source.match(/const ALPHA=.*;/)[0]+'\n'+source.match(/const caesar=.*;/)[0]+'\n'+source.slice(start,stop),c);
 c.sh(1);assert.equal(c.st.k,0,'cipher shifts stay locked before math answer');
 c.st.shiftLocked=true;c.renderDecodedCipher(s);
 const box=nodes.get('#dec'),marks=()=>box.children.filter(n=>n.className==='cipher-clue-word');
 assert.notEqual(box.textContent,s.plain,'the cipher starts scrambled');
 for(let i=1;i<s.shift;i++){
  c.sh(1);
  assert.equal(c.st.k,i,'each +1 advances one letter');
  assert.notEqual(box.textContent,s.plain,'no early decode');
  assert.equal(marks().length,0,'no premature highlighting');
 }
 c.sh(1);
 assert.equal(box.textContent,s.plain,'message decodes after exact number of forward shifts');
 assert.ok(marks().length,'the clue word is highlighted');
 for(const mark of marks()){
  assert.equal(mark.textContent.toUpperCase(),s.answer.toUpperCase());
  assert.match(mark.style.cssText,/color:var\(--gold/);
  assert.match(mark.style.cssText,/underline/);
 }
 c.sh(1);
 assert.equal(marks().length,0,'overshifting clears highlighting');
}
for(const file of files){
 const source=fs.readFileSync(path.join(root,file),'utf8');
 if(file.endsWith('.html'))for(const m of source.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi))new vm.Script(m[1],{filename:file});
 else new vm.Script(source,{filename:file});
 const declaration=source.indexOf('const ROOM=');
 const room=declaration<0?null:vm.runInNewContext(source.slice(source.lastIndexOf('<script',declaration)).replace(/^<script[^>]*>/,'').split('const TOTAL=')[0]+';ROOM;',{URLSearchParams,location:{search:''}});
 const stages=room?room.stages.filter(s=>s.type==='cipher'):[{plain:'THE NEXT KEY IS BEHIND THE PLANETS',shift:7,answer:'PLANETS'}];
 assert.ok(stages.length);for(const s of stages)check(source,s);
}
console.log('PASS '+files.length+' escape-room renderers: manual +1 shifting, gated clue highlights and safe decoded text.');
