/* Dependency-free protocol/DOM tests using the actual game-bank catalogues. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../../..'),source=p=>fs.readFileSync(path.join(root,p),'utf8');
class Node {
 constructor(tag='div'){this.tagName=tag.toUpperCase();this.children=[];this.parentNode=null;this.events={};this.style={};this.attrs={};this.isConnected=true;this.classList={add(){}};}
 set innerHTML(s){this._text=String(s).replace(/<[^>]*>/g,'').replace(/&nbsp;/g,' ').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>');}
 get textContent(){return (this._text||'')+this.children.map(c=>c.textContent).join('');}
 set textContent(s){this._text=String(s);this.children=[];}
 appendChild(n){n.parentNode=this;this.children.push(n);return n;}
 replaceChildren(...n){this.children=[];n.forEach(x=>this.appendChild(x));}
 remove(){if(this.parentNode)this.parentNode.children=this.parentNode.children.filter(x=>x!==this);this.isConnected=false;}
 setAttribute(k,v){this.attrs[k]=v;} getAttribute(k){return this.attrs[k]??null;}
 addEventListener(k,f){(this.events[k]??=[]).push(f);} removeEventListener(k,f){this.events[k]=(this.events[k]||[]).filter(x=>x!==f);}
 dispatch(k,e={}){for(const f of this.events[k]||[])f(e);} click(){if(!this.disabled){if(this.onclick)this.onclick();this.dispatch('click');}}
 showModal(){this.open=true;} close(){this.open=false;this.dispatch('close');} focus(){} select(){}
}
const walk=n=>[n,...n.children.flatMap(walk)];
function environment(url){
 const body=new Node('body'),doc={body,title:'Test game',addEventListener(){},createElement:tag=>{const n=new Node(tag);if(tag==='iframe')n.contentWindow={};return n;},createTextNode:s=>{const n=new Node('#text');n.textContent=s;return n;},getElementById:id=>walk(body).find(n=>n.id===id)||null};
 const listeners={};
 const win={document:doc,location:new URL(url),URL,URLSearchParams,Set,Array,navigator:{},setTimeout,addEventListener:(k,f)=>(listeners[k]??=[]).push(f),removeEventListener:(k,f)=>listeners[k]=(listeners[k]||[]).filter(x=>x!==f)};
 win.window=win;win.parent=win;win.receive=e=>{for(const f of listeners.message||[])f(e);};
 return {win,doc,run:p=>vm.runInNewContext(source(p),win,{filename:p})};
}
function find(doc,text){return walk(doc.body).find(n=>n.tagName==='BUTTON'&&n.textContent===text);}
const data={window:{}};vm.runInNewContext(source('data.js'),data);
const entries=[];
for(const c of data.window.LIBRARY.courses)for(const u of c.units)for(const a of u.artifacts){
 const types=Array.isArray(a.type)?a.type:[a.type];
 if(a.path.endsWith('/index.html')&&!/escape-room|jeopardy|showdown|connect-four|inequality-four|tic-tac-toe/.test(a.path)&&(types.includes('Game')||/flashcards/.test(a.path))&&!entries.some(e=>e.path===a.path))entries.push(a);
}
const load=require('../../menu/tests/load.cjs');const env=load(['games/bank.js']);
function catalogue(entry){
 const html=source(entry.path);
 assert(html.includes('games/skill-setup.js'),entry.path+' integrates shared setup');
 if(html.includes('games/games.js')){
  const unit=/data-unit="([^"]+)"/.exec(html)[1],only=(/data-skills="([^"]+)"/.exec(html)||[])[1];
  return {skills:env.MKMENU.skillSets[unit].skills.filter(s=>(!only||only.split(',').includes(s.id))&&env.MKGAMES.hasGameItems(unit,s.id)).map(s=>({id:s.id,name:s.name}))};
 }
 for(const name of ['Q','CARDS','CASE']){
  const m=new RegExp('const '+name+'\\s*=\\s*(.*);').exec(html);
  if(m){const value=JSON.parse(m[1]);return {items:name==='CASE'?value.questions:value,label:q=>q.skill&&!/^clue\s*\d+$/i.test(q.skill)?q.skill:q.instr};}
 }
 if(entry.path.includes('slope-links'))return {items:[{name:'Slope'}],label:q=>q.name};
 const name=entry.path.includes('basketball')?'levels':'LEVELS',m=new RegExp('const '+name+' = (\\[[\\s\\S]*?\\n\\]);').exec(html);
 const items=vm.runInNewContext('('+m[1]+')');return {items,label:q=>q.challenge||q.tip};
}
let checked=0;
for(const entry of entries){
 // Both public entry points must route to configuration rather than copying.
 const cardHost=environment('https://classroom.test/index.html');cardHost.win.LIBRARY=data.window.LIBRARY;
 let opened=null;cardHost.win.TeacherGameShare={supports:()=>true,open:p=>opened=p};cardHost.win.MutationObserver=class{observe(){}};
 const main=new Node();main.id='main';cardHost.doc.body.appendChild(main);
 const card=new Node(),actions=new Node(),heading=new Node('h3');heading.textContent=entry.title;card.setAttribute('data-path',entry.path);
 card.querySelector=selector=>selector==='.actions'?actions:selector==='h3'?heading:null;cardHost.doc.querySelectorAll=()=>[card];
 cardHost.run('student-share-cards.js');assert(actions.children.length);actions.children[0].click();assert.equal(opened,entry.path,'card opens setup');
 const teacherViewer=environment('https://classroom.test/activity.html?path='+encodeURIComponent(entry.path));teacherViewer.win.LIBRARY=data.window.LIBRARY;
 for(const id of ['activity-title','activity-message','original-link','activity-content','resource-details','report-problem','share-student']){const n=new Node();n.id=id;teacherViewer.doc.body.appendChild(n);}
 opened=null;teacherViewer.win.TeacherGameShare={supports:()=>true,open:p=>opened=p};teacherViewer.run('activity.js');teacherViewer.doc.getElementById('share-student').click();assert.equal(opened,entry.path,'activity viewer opens setup');
 const cat=catalogue(entry),host=environment('https://classroom.test/index.html');host.run('student-game-share.js');
 host.win.TeacherGameShare.open(entry.path);const frame=walk(host.doc.body).find(n=>n.tagName==='IFRAME');
 const teacher=environment(frame.src);frame.contentWindow=teacher.win;
 teacher.win.parent={postMessage:data=>host.win.receive({data,origin:'https://classroom.test',source:teacher.win})};
 teacher.run('worksheet-generator/games/skill-setup.js');let started=false;
 if(cat.skills)teacher.win.TeacherSkills.choose(cat.skills,()=>{started=true;});else teacher.win.TeacherSkills.bank(cat.items,cat.label,()=>{started=true;});
 host.win.receive({origin:'https://unrelated.test',source:teacher.win,data:{type:'teacher-skills-selected',skills:['0']}});
 host.win.receive({origin:'https://classroom.test',source:{},data:{type:'teacher-skills-selected',skills:['0']}});
 assert(!host.doc.getElementById('game-student-link'),'no link before choosing skills');
 find(teacher.doc,'Clear All').click();assert(find(teacher.doc,'Generate student link').disabled);
 find(teacher.doc,'Select All').click();assert(!find(teacher.doc,'Generate student link').disabled);
 find(teacher.doc,'Clear All').click();const inputs=walk(teacher.doc.body).filter(n=>n.type==='checkbox'),last=inputs.at(-1);assert(last);
 last.checked=true;last.onchange();find(teacher.doc,'Generate student link').click();assert(!started,'share mode must not launch game');
 const link=host.doc.getElementById('game-student-link').value,url=new URL(link);assert.equal(url.searchParams.get('path'),entry.path);assert.deepEqual(JSON.parse(url.searchParams.get('skills')),[last.value]);
 // Exercise actual activity viewer forwarding, including the student flag.
 const viewer=environment(link);viewer.win.LIBRARY=data.window.LIBRARY;
 for(const id of ['activity-title','activity-message','original-link','activity-content','resource-details','report-problem','share-student']){const n=new Node();n.id=id;viewer.doc.body.appendChild(n);}
 viewer.run('activity.js');const studentFrame=walk(viewer.doc.body).find(n=>n.tagName==='IFRAME');assert(studentFrame);
 assert.equal(new URL(studentFrame.src).searchParams.get('skills'),JSON.stringify([last.value]));assert.equal(new URL(studentFrame.src).searchParams.get('student'),'1');
 for(let reload=0;reload<2;reload++){
  const student=environment(studentFrame.src);student.run('worksheet-generator/games/skill-setup.js');let selected;
  if(cat.skills)student.win.TeacherSkills.choose(cat.skills,s=>selected=s);else student.win.TeacherSkills.bank(cat.items,cat.label,s=>selected=s);
  assert(selected&&selected.length,entry.path+' starts with selected questions');
  if(cat.skills)assert.deepEqual(Array.from(selected),[last.value]);
  else {
   const normalize=q=>{const e=student.doc.createElement('div');e.innerHTML=String(cat.label(q)||'');return e.textContent.replace(/\s+/g,' ').trim();};
   assert(selected.every(q=>normalize(q)===last.parentNode.textContent.replace(/\s+/g,' ').trim()),entry.path+' filters actual bank');
  }
  assert(!walk(student.doc.body).some(n=>n.tagName==='DIALOG'),'students do not see teacher setup');
 }
 const all=environment('https://classroom.test/game.html?student=1&skills='+encodeURIComponent(JSON.stringify(inputs.map(n=>n.value))));all.run('worksheet-generator/games/skill-setup.js');let allSelected;
 if(cat.skills)all.win.TeacherSkills.choose(cat.skills,s=>allSelected=s);else all.win.TeacherSkills.bank(cat.items,cat.label,s=>allSelected=s);
 assert.equal(allSelected.length,cat.skills?cat.skills.length:cat.items.length,'all-skills links preserve full bank');
 checked++;console.log('PASS '+entry.path);
}
for(const skills of ['[]','["no-such-skill"]','null','malformed']){
 const s=environment('https://classroom.test/game.html?student=1&skills='+encodeURIComponent(skills));s.run('worksheet-generator/games/skill-setup.js');let started=false;
 s.win.TeacherSkills.choose([{id:'valid',name:'Valid skill'}],()=>started=true);assert(!started);assert(s.doc.body.textContent.includes('Ask your teacher'));
}
const legacy=environment('https://classroom.test/game.html?student=1');legacy.run('worksheet-generator/games/skill-setup.js');let ids;legacy.win.TeacherSkills.choose([{id:'valid',name:'Valid'}],s=>ids=s);assert.deepEqual(Array.from(ids),['valid']);
console.log(`PASS ${checked} game catalogues: picker, bulk controls, selection-only links, viewer forwarding, student filtering and reload. Invalid and legacy links also passed.`);
