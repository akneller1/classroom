'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const files=['worksheet-generator/games/escape-runtime.js',...fs.readdirSync(path.join(root,'artifacts')).map(d=>'artifacts/'+d+'/index.html').filter(p=>fs.existsSync(path.join(root,p))&&fs.readFileSync(path.join(root,p),'utf8').includes('function sh(d)'))];
class Node {
 constructor(tag='#text',text=''){this.tagName=tag;this.children=[];this.style={};this._text=text;}
 set textContent(v){this._text=String(v);this.children=[];}
 get textContent(){return this._text+this.children.map(n=>n.textContent).join('');}
 appendChild(n){this.children.push(n);return n;}
}
function check(source,s){
 const nodes=new Map(['#dec','#kk','#wheel'].map(id=>[id,new Node('div')]));
 const c={STAGES:[s],stage:0,st:{k:s.shift,shiftLocked:false},$:id=>nodes.get(id),document:{createElement:tag=>new Node(tag),createTextNode:t=>new Node('#text',t)}};
 vm.createContext(c);
 vm.runInContext(source.match(/const ALPHA=.*;/)[0]+'\n'+source.match(/const caesar=.*;/)[0]+'\n'+source.slice(source.indexOf('function renderDecodedCipher('),source.indexOf('function chkCipher(')),c);
 c.sh(0);assert.equal(nodes.get('#dec').textContent,'','locked cipher must stay unrevealed');
 c.st.shiftLocked=true;c.sh(0);
 const box=nodes.get('#dec'),marks=()=>box.children.filter(n=>n.className==='cipher-clue-word');
 assert.equal(box.textContent,s.plain,'decoded sentence stays intact');
 assert.ok(marks().length,'answer word is highlighted');
 for(const mark of marks()){assert.equal(mark.textContent.toUpperCase(),s.answer.toUpperCase());assert.match(mark.style.cssText,/color:var\(--gold/);assert.match(mark.style.cssText,/underline/);}
 c.sh(1);assert.equal(marks().length,0,'wrong shifts must clear highlighting');
 c.sh(-1);assert.ok(marks().length,'correct shift restores highlighting');
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
const shared=fs.readFileSync(path.join(root,files[0]),'utf8');
for(const s of [{plain:'STAR STARS STAR.',shift:0,answer:'STAR'},{plain:'THE CLUE IS A+B.',shift:3,answer:'A+B'},{plain:'LOOK IN THE BLUE ROOM',shift:25,answer:'BLUE ROOM'},{plain:'OPEN <DOOR> NOW',shift:2,answer:'DOOR'}])check(shared,s);
console.log('PASS '+files.length+' escape-room renderers: locked/incorrect shifts, clue color and underline, intact text, punctuation, repeated words and safe text nodes');
