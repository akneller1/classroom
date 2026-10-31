(function(root){'use strict';
const doc=root.document, bank=root.MK_QUESTION_BANKS, catalog=root.MK_COURSE_CATALOG;
const $=id=>doc.getElementById(id), params=new URLSearchParams(root.location.search);
const course=root.LIBRARY.courses.find(c=>c.id==='algebra2');
const units=course.units, unitSelect=$('unit'), status=$('status');
function option(parent,val,label){const o=doc.createElement('option');o.value=val;o.textContent=label;parent.appendChild(o)}
function elt(tag,parent,value){const e=doc.createElement(tag);if(value!==undefined)e.textContent=String(value);parent.appendChild(e);return e}
function skills(){const list=$('skills');list.replaceChildren();catalog.getSkillRecords('algebra2',unitSelect.value).forEach(s=>{const label=elt('label',list);label.className='skill';const input=elt('input',label);input.type='checkbox';input.value=s.id;input.checked=true;elt('span',label,s.name)})}
function shuffle(arr){const copy=arr.slice();for(let i=copy.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[copy[i],copy[j]]=[copy[j],copy[i]]}return copy}
function renderQuestion(q,host,n,answerSide){
 const article=elt('article',host);article.className='item';
 elt('strong',article,n+'. '+q.prompt);
 if(q.diagram&&q.diagram.type==='image'){
  const src=q.diagram.spec&&q.diagram.spec.src;
  if(typeof src==='string'&&/^question-banks\/assets\/[a-zA-Z0-9_/-]+\.(png|jpg|jpeg|webp)$/.test(src)&&!src.includes('..')){
   const img=elt('img',article);img.src='../'+src;img.alt=q.diagram.spec.alt||'Mathematical diagram';
   img.onerror=function(){img.replaceWith(doc.createTextNode('[Diagram unavailable — check question asset]'))}
  }
 }
 if(!answerSide){
  if(q.options&&q.options.length){
   const options=elt('div',article);options.className='choices';
   q.options.forEach((o,i)=>elt('div',options,(q.format==='select-all'?'☐ ':'○ ')+String.fromCharCode(65+i)+'. '+o.text));
  }
  if(Array.isArray(q.parts)) {const ol=elt('ol',article);ol.className='parts';q.parts.forEach(p=>elt('li',ol,typeof p==='string'?p:JSON.stringify(p)))}
  if(q.format==='short-answer'||q.format==='open-response') {const w=elt('div',article);w.className='workspace'}
 }else{
  elt('p',article,'Answer: '+(Array.isArray(q.answer)?q.answer.join(', '):typeof q.answer==='object'?JSON.stringify(q.answer):q.answer));
  if(q.options&&q.options.length)elt('p',article,'Correct choices: '+q.options.map((o,i)=>o.correct?String.fromCharCode(65+i):null).filter(Boolean).join(', '));
  if(q.solutionSteps&&q.solutionSteps.length){const ol=elt('ol',article);q.solutionSteps.forEach(step=>elt('li',ol,step))}
 }
}
let versions=[],activeVersion=0, pool=[],wantedCount=12;
function sample(count){return shuffle(pool).slice(0,count).map(q=>({source:q,question:JSON.parse(JSON.stringify(q))}))}
function currentItems(){return versions[activeVersion]||[]}
function build(){
 const unitId=unitSelect.value, level=$('level').value, fmt=$('format').value;
 const skillIds=Array.from(doc.querySelectorAll('#skills input:checked')).map(x=>x.value);
 if(!skillIds.length){status.textContent='Choose at least one skill.';return}
 pool=bank.select({courseId:'algebra2',unitId,level,skillIds,formats:fmt==='all'?undefined:[fmt]}).filter(q=>!q.diagram||q.diagram.type==='image');
 wantedCount=Math.max(1,Math.min(60,Number($('count').value)||12));
 if(!pool.length){versions=[];$('output').replaceChildren();$('editor').hidden=true;$('print').disabled=true;status.textContent='No matching questions for these settings.';return}
 const total=Math.max(1,Math.min(4,Number($('versions').value)||1));
 versions=Array.from({length:total},()=>sample(wantedCount));activeVersion=0;
 const chooser=$('currentVersion');chooser.replaceChildren();
 versions.forEach((_,i)=>option(chooser,String(i),'Version '+String.fromCharCode(65+i)));
 chooser.value='0';$('editor').hidden=false;$('print').disabled=false;
 renderEditor();renderAll();
}
function renderEditor(){
 const host=$('editItems');host.replaceChildren();
 currentItems().forEach((item,index)=>{
  const card=elt('section',host);card.className='edit-card';
  elt('strong',card,'Question '+(index+1)+' · '+item.question.format);
  const area=elt('textarea',card);area.value=item.question.prompt;area.setAttribute('aria-label','Question '+(index+1)+' wording');
  area.addEventListener('input',()=>{item.question.prompt=area.value;renderAll()});
  const controls=elt('div',card);controls.className='controls';
  function addButton(label,fn){const b=elt('button',controls,label);b.type='button';b.addEventListener('click',fn);return b}
  const up=addButton('Move up',()=>move(index,-1));up.disabled=index===0;
  const down=addButton('Move down',()=>move(index,1));down.disabled=index===currentItems().length-1;
  addButton('Replace',()=>{
   const used=new Set(currentItems().filter((_,i)=>i!==index).map(x=>x.question.id));
   const alternate=shuffle(pool.filter(q=>q.id!==item.question.id&&!used.has(q.id)))[0];
   if(!alternate){status.textContent='No unused replacement questions match the selected settings.';return}
   currentItems()[index]={source:alternate,question:JSON.parse(JSON.stringify(alternate))};renderEditor();renderAll();
  });
  addButton('Remove',()=>{currentItems().splice(index,1);renderEditor();renderAll()});
 });
}
function move(index,direction){
 const arr=currentItems(),to=index+direction;if(to<0||to>=arr.length)return;
 [arr[index],arr[to]]=[arr[to],arr[index]];renderEditor();renderAll();
}
function renderAll(){
 const out=$('output');out.replaceChildren();
 const unit=units.find(u=>u.id===unitSelect.value),mode=$('mode').value;
 versions.forEach((items,vi)=>{
  const paper=elt('section',out);paper.className='sheet';
  elt('h2',paper,($('customTitle').value.trim()||unit.name+' — '+(mode==='worksheet'?'Practice Worksheet':'Assessment'))+(versions.length>1?' · Version '+String.fromCharCode(65+vi):''));
  elt('p',paper,'Name: __________________________  Date: ______________');
  items.forEach((item,i)=>renderQuestion(item.question,paper,i+1,false));
  if($('key').checked){
   const key=elt('section',out);key.className='sheet key';
   elt('h2',key,'Teacher Answer Key — '+unit.name+(versions.length>1?' · Version '+String.fromCharCode(65+vi):''));
   items.forEach((item,i)=>renderQuestion(item.question,key,i+1,true));
  }
 });
 const sizes=versions.map(v=>v.length);
 status.textContent='Preview ready: '+versions.length+' version(s), '+sizes.join('/')+' questions. Review mathematical answers before printing.';
 $('print').disabled=versions.every(v=>!v.length);
}
$('currentVersion').addEventListener('change',()=>{activeVersion=Number($('currentVersion').value);renderEditor()});
$('refreshVersion').addEventListener('click',()=>{versions[activeVersion]=sample(wantedCount);renderEditor();renderAll()});
$('resetEdits').addEventListener('click',()=>{versions[activeVersion]=currentItems().map(x=>({source:x.source,question:JSON.parse(JSON.stringify(x.source))}));renderEditor();renderAll()});
$('key').addEventListener('change',()=>{if(versions.length)renderAll()});
$('customTitle').addEventListener('input',()=>{if(versions.length)renderAll()});
units.forEach((u,i)=>option(unitSelect,u.id,'Unit '+(i+1)+' · '+u.name));
const requested=params.get('unit');if(units.some(u=>u.id===requested))unitSelect.value=requested;
if(params.get('mode')==='assessment')$('mode').value='assessment';
unitSelect.addEventListener('change',()=>{skills();versions=[];$('output').replaceChildren();$('editor').hidden=true;$('print').disabled=true;status.textContent=bank.available('algebra2',unitSelect.value)?'Ready to generate.':'No question bank available for this unit yet.'});
$('all').addEventListener('click',()=>doc.querySelectorAll('#skills input').forEach(x=>x.checked=true));
$('none').addEventListener('click',()=>doc.querySelectorAll('#skills input').forEach(x=>x.checked=false));
$('build').addEventListener('click',build);$('print').addEventListener('click',()=>root.print());
skills();
root.MK_BANK_LOADER.loadFromSite(undefined,'../').then(()=>{
 status.textContent=bank.available('algebra2',unitSelect.value)?'Ready to generate.':'No question bank available for this unit yet.';
}).catch(e=>{status.textContent='Could not load question banks: '+e.message;$('build').disabled=true});
})(window);