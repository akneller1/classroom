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
let versionSections=[];
let spiralPool=[];
const DEFAULT_SECTIONS=[
 ['Do Now',2],['Mixed Review',0],['Notes',0],['Examples',3],['Practice',5],['Challenge Problems',0],['Summary',0],['Exit Ticket',2]
];
let sections=[],sectionCounter=0;
function newSection(type,count){return {id:'s'+(++sectionCounter),type,title:type,count:count===undefined?2:count,note:'',enabled:true,skillIds:[]}}
function resetSections(){sections=DEFAULT_SECTIONS.map(x=>newSection(x[0],x[1]));renderSections()}
function sectionSkills(){return Array.from(doc.querySelectorAll('#skills input:checked')).map(x=>x.value)}
function renderSections(){
 const host=$('sectionList');host.replaceChildren();
 sections.forEach((sec,i)=>{
  const card=elt('div',host);card.className='section-config';
  const row=elt('div',card);row.className='controls';
  const enabled=elt('input',row);enabled.type='checkbox';enabled.checked=sec.enabled;enabled.setAttribute('aria-label','Include '+sec.title);enabled.addEventListener('change',()=>{sec.enabled=enabled.checked});
  const heading=elt('input',row);heading.value=sec.title;heading.setAttribute('aria-label','Section '+(i+1)+' heading');heading.addEventListener('input',()=>{sec.title=heading.value});
  const countLabel=elt('label',row,'Problems');const count=elt('input',countLabel);count.type='number';count.min='0';count.max='60';count.value=sec.count;count.addEventListener('change',()=>{sec.count=Math.max(0,Math.min(60,Number(count.value)||0))});
  function btn(label,fn,disabled){const b=elt('button',row,label);b.type='button';b.disabled=!!disabled;b.addEventListener('click',fn)}
  btn('↑',()=>shiftSection(i,-1),i===0);btn('↓',()=>shiftSection(i,1),i===sections.length-1);
  btn('Duplicate',()=>{sections.splice(i+1,0,{...sec,id:'s'+(++sectionCounter),skillIds:sec.skillIds.slice()});renderSections()});
  btn('Remove',()=>{sections.splice(i,1);renderSections()});
  const note=elt('textarea',card);note.value=sec.note;note.placeholder='Optional teacher notes, instructions or summary text';note.setAttribute('aria-label',sec.title+' notes');note.addEventListener('input',()=>{sec.note=note.value});
  const group=elt('div',card);group.className='section-skills';
  elt('strong',group,'Skills for this section (none selected = use overall selection)');
  catalog.getSkillRecords('algebra2',unitSelect.value).forEach(record=>{
   const label=elt('label',group);label.className='skill';
   const cb=elt('input',label);cb.type='checkbox';cb.value=record.id;cb.checked=sec.skillIds.includes(record.id);
   cb.addEventListener('change',()=>{sec.skillIds=Array.from(group.querySelectorAll('input:checked')).map(x=>x.value)});
   elt('span',label,record.name);
  });
 });
}
function shiftSection(i,by){const j=i+by;if(j<0||j>=sections.length)return;[sections[i],sections[j]]=[sections[j],sections[i]];renderSections()}
function spiralSelections(){return Array.from(doc.querySelectorAll('#spiralUnits input:checked')).map(x=>x.value)}
function renderSpiralUnits(){const host=$('spiralUnits');host.replaceChildren();const index=units.findIndex(u=>u.id===unitSelect.value);units.slice(0,index).forEach(u=>{const label=elt('label',host);label.className='skill';const cb=elt('input',label);cb.type='checkbox';cb.value=u.id;cb.checked=bank.available('algebra2',u.id);cb.disabled=!bank.available('algebra2',u.id);elt('span',label,u.name+(cb.disabled?' (no bank)':''))})}
function sectionsSnapshot(){return sections.filter(x=>x.enabled).map(x=>({...x,skillIds:x.skillIds.slice()}))}
function sectionQuestions(layout,used){
 const selections=[];
 layout.forEach(sec=>{
  const count=Math.max(0,Math.min(60,Number(sec.count)||0));
  if(!count)return;
  const source=sec.type==='Mixed Review'&&$('spiralEnabled').checked?pool.concat(spiralPool):pool;
  const eligible=source.filter(q=>{const crossUnit=q._spiral===true;const permitted=crossUnit ? sec.type==='Mixed Review'&&$('spiralEnabled').checked : (!sec.skillIds.length||sec.skillIds.includes(q.skillId));return permitted&&!used.has((q._origin||unitSelect.value)+'/'+q.id)});
  // Mixed Review deliberately samples across distinct skills instead of allowing
  // the largest question category to dominate the section.
  const chosen=[];
  if(sec.type==='Mixed Review'){
   const grouped=new Map();
   shuffle(eligible).forEach(q=>{if(!grouped.has(q.skillId))grouped.set(q.skillId,[]);grouped.get(q.skillId).push(q)});
   const groups=shuffle(Array.from(grouped.values()));
   while(chosen.length<count&&groups.some(g=>g.length)){
    for(const group of groups){if(group.length&&chosen.length<count)chosen.push(group.pop())}
   }
  }else chosen.push(...shuffle(eligible).slice(0,count));
  chosen.forEach(q=>{used.add((q._origin||unitSelect.value)+'/'+q.id);selections.push({source:q,question:JSON.parse(JSON.stringify(q)),sectionId:sec.id})});
 });
 return selections;
}
$('addSection').addEventListener('click',()=>{sections.push(newSection($('sectionType').value));renderSections()});
$('resetSections').addEventListener('click',resetSections);

const LAYOUT_KEY='mk-algebra2-section-layout-v1';
function snapshotLayout(){
 return {schema:1,unitId:unitSelect.value,sections:sections.map(x=>({...x,skillIds:x.skillIds.slice()})),
 level:$('level').value,format:$('format').value,count:$('count').value,versions:$('versions').value,
 heading:$('customTitle').value,selectedSkills:sectionSkills(),spiralEnabled:$('spiralEnabled').checked,spiralUnits:spiralSelections()};
}
function applyLayout(saved){
 if(!saved||saved.schema!==1||!Array.isArray(saved.sections)||saved.sections.length>40||
    !units.some(u=>u.id===saved.unitId))throw Error('Invalid Algebra 2 layout');
 const records=catalog.getSkillRecords('algebra2',saved.unitId),valid=new Set(records.map(x=>x.id));
 const clean=saved.sections.map(x=>{
  if(!x||typeof x.title!=='string'||x.title.length>120||typeof x.note!=='string'||x.note.length>5000||
     !Number.isFinite(Number(x.count)))throw Error('Invalid section configuration');
  return {id:'s'+(++sectionCounter),type:String(x.type||x.title).slice(0,120),title:x.title,
   count:Math.max(0,Math.min(60,Number(x.count))),enabled:x.enabled!==false,note:x.note,
   skillIds:Array.isArray(x.skillIds)?x.skillIds.filter(id=>valid.has(id)):[ ]};
 });
 if(!clean.length)throw Error('Layout has no sections');
 unitSelect.value=saved.unitId;skills();
 const chosen=new Set(Array.isArray(saved.selectedSkills)?saved.selectedSkills:records.map(x=>x.id));
 doc.querySelectorAll('#skills input').forEach(x=>x.checked=chosen.has(x.value));
 sections=clean;
 renderSpiralUnits();$('spiralEnabled').checked=!!saved.spiralEnabled;
 const spiralSet=new Set(Array.isArray(saved.spiralUnits)?saved.spiralUnits:[]);
 doc.querySelectorAll('#spiralUnits input').forEach(x=>x.checked=!x.disabled&&spiralSet.has(x.value));
 $('level').value=['cp2','cp1','honors'].includes(saved.level)?saved.level:'cp1';
 $('format').value=['all','short-answer','multiple-choice','select-all','open-response'].includes(saved.format)?saved.format:'all';
 $('count').value=Math.max(1,Math.min(60,Number(saved.count)||12));
 $('versions').value=Math.max(1,Math.min(4,Number(saved.versions)||1));
 $('customTitle').value=String(saved.heading||'').slice(0,150);
 versions=[];$('output').replaceChildren();$('editor').hidden=true;$('print').disabled=true;
 renderSections();status.textContent='Configuration loaded. Generate a fresh preview.';
}
$('exportLayout').addEventListener('click',()=>{
 const blob=new Blob([JSON.stringify(snapshotLayout(),null,2)],{type:'application/json'});
 const url=URL.createObjectURL(blob),a=doc.createElement('a');
 a.href=url;a.download='algebra2-'+unitSelect.value+'-layout.json';a.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
});
$('importLayout').addEventListener('click',()=>$('importFile').click());
$('importFile').addEventListener('change',async()=>{
 const file=$('importFile').files[0];if(!file)return;
 try{if(file.size>100000)throw Error('Configuration exceeds 100 KB');
  applyLayout(JSON.parse(await file.text()));
 }catch(e){status.textContent='Could not import configuration: '+e.message}
 $('importFile').value='';
});
$('saveLayout').addEventListener('click',()=>{
 const config={schema:1,unitId:unitSelect.value,sections:sections.map(x=>({...x,skillIds:x.skillIds.slice()})),
  level:$('level').value,format:$('format').value,count:$('count').value,versions:$('versions').value,heading:$('customTitle').value,
  selectedSkills:sectionSkills()};
 try{root.localStorage.setItem(LAYOUT_KEY,JSON.stringify(config));status.textContent='Section configuration saved in this browser.'}
 catch(e){status.textContent='Unable to save configuration in this browser.'}
});
$('loadLayout').addEventListener('click',()=>{
 let saved;try{saved=JSON.parse(root.localStorage.getItem(LAYOUT_KEY)||'null')}catch(e){}
 if(!saved||saved.schema!==1||!Array.isArray(saved.sections)||!units.some(u=>u.id===saved.unitId)){
  status.textContent='No valid saved configuration found.';return;
 }
 unitSelect.value=saved.unitId;skills();
 const selected=new Set(saved.selectedSkills||[]);
 doc.querySelectorAll('#skills input').forEach(x=>x.checked=selected.has(x.value));
 sections=saved.sections.filter(x=>x&&typeof x.title==='string'&&Number.isFinite(Number(x.count))).map(x=>({
  id:'s'+(++sectionCounter),type:String(x.type||x.title),title:x.title,count:Math.max(0,Math.min(60,Number(x.count))),
  enabled:x.enabled!==false,note:String(x.note||''),skillIds:Array.isArray(x.skillIds)?x.skillIds.filter(id=>catalog.getSkillRecords('algebra2',saved.unitId).some(k=>k.id===id)):[]
 }));
 if(!sections.length){status.textContent='Saved configuration had no usable sections.';resetSections();return}
 $('level').value=['cp2','cp1','honors'].includes(saved.level)?saved.level:'cp1';
 $('format').value=['all','short-answer','multiple-choice','select-all','open-response'].includes(saved.format)?saved.format:'all';
 $('count').value=Math.max(1,Math.min(60,Number(saved.count)||12));
 $('versions').value=Math.max(1,Math.min(4,Number(saved.versions)||1));
 $('customTitle').value=String(saved.heading||'');
 versions=[];$('output').replaceChildren();$('editor').hidden=true;$('print').disabled=true;
 renderSections();status.textContent='Configuration loaded. Generate a fresh preview.';
});
resetSections();

function sample(count){return shuffle(pool).slice(0,count).map(q=>({source:q,question:JSON.parse(JSON.stringify(q))}))}
function currentItems(){return versions[activeVersion]||[]}
function build(){
 const unitId=unitSelect.value, level=$('level').value, fmt=$('format').value;
 const skillIds=Array.from(doc.querySelectorAll('#skills input:checked')).map(x=>x.value);
 if(!skillIds.length){status.textContent='Choose at least one skill.';return}
 pool=bank.select({courseId:'algebra2',unitId,level,skillIds,formats:fmt==='all'?undefined:[fmt]}).filter(q=>!q.diagram||q.diagram.type==='image');
 spiralPool=[];
 if($('spiralEnabled').checked){const fmtList=fmt==='all'?undefined:[fmt];spiralSelections().forEach(id=>{bank.select({courseId:'algebra2',unitId:id,level,formats:fmtList}).forEach(q=>{if(!q.diagram||q.diagram.type==='image')spiralPool.push({...q,_spiral:true,_origin:id})})})}
 wantedCount=Math.max(1,Math.min(60,Number($('count').value)||12));
 const requestedTotal=sections.filter(x=>x.enabled).reduce((sum,x)=>sum+Math.max(0,Number(x.count)||0),0);
 if(requestedTotal>wantedCount){status.textContent='Section counts exceed the total question limit. Increase the question limit or reduce section counts.';return;}
 if(!pool.length){versions=[];$('output').replaceChildren();$('editor').hidden=true;$('print').disabled=true;status.textContent='No matching questions for these settings.';return}
 const total=Math.max(1,Math.min(4,Number($('versions').value)||1));
 if(!sections.some(x=>x.enabled)){status.textContent='Include at least one section before generating.';return;}
 versionSections=Array.from({length:total},sectionsSnapshot);
 versions=versionSections.map(layout=>sectionQuestions(layout,new Set()));activeVersion=0;
 if(versions.every(v=>v.length===0)&&!versionSections[0].some(sec=>sec.note.trim())){status.textContent='Add questions or notes to at least one included section.';$('print').disabled=true;return;}
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
   const used=new Set(currentItems().filter((_,i)=>i!==index).map(x=>(x.question._origin||unitSelect.value)+'/'+x.question.id));
   const layout=versionSections[activeVersion].find(sec=>sec.id===item.sectionId);
   const choices=layout?.type==='Mixed Review'&&$('spiralEnabled').checked?pool.concat(spiralPool):pool;
   const alternate=shuffle(choices.filter(q=>((q._origin||unitSelect.value)+'/'+q.id)!==(item.question._origin||unitSelect.value)+'/'+item.question.id)&&!used.has((q._origin||unitSelect.value)+'/'+q.id)&&(q._spiral===true?layout?.type==='Mixed Review':!layout?.skillIds.length||layout.skillIds.includes(q.skillId))))[0];
   if(!alternate){status.textContent='No unused replacement questions match the selected settings.';return}
   currentItems()[index]={source:alternate,question:JSON.parse(JSON.stringify(alternate)),sectionId:item.sectionId};renderEditor();renderAll();
  });
  addButton('Remove',()=>{currentItems().splice(index,1);renderEditor();renderAll()});
 });
}
function move(index,direction){
 const arr=currentItems(),to=index+direction;if(to<0||to>=arr.length)return;
 if(arr[index].sectionId!==arr[to].sectionId){status.textContent='Use the section controls to reorder sections; questions can be moved within their own section.';return;}
 [arr[index],arr[to]]=[arr[to],arr[index]];renderEditor();renderAll();
}
function renderAll(){
 const out=$('output');out.replaceChildren();
 const unit=units.find(u=>u.id===unitSelect.value),mode=$('mode').value;
 versions.forEach((items,vi)=>{
  const paper=elt('section',out);paper.className='sheet';
  elt('h2',paper,($('customTitle').value.trim()||unit.name+' — '+(mode==='worksheet'?'Practice Worksheet':'Assessment'))+(versions.length>1?' · Version '+String.fromCharCode(65+vi):''));
  elt('p',paper,'Name: __________________________  Date: ______________');
  versionSections[vi].forEach(sec=>{
   const block=elt('section',paper);block.className='section-print';
   elt('h3',block,sec.title);
   if(sec.note) {const p=elt('p',block,sec.note);p.className='section-notes'}
   items.filter(item=>item.sectionId===sec.id).forEach((item,i)=>renderQuestion(item.question,block,i+1,false));
  });
  if($('key').checked){
   const key=elt('section',out);key.className='sheet key';
   elt('h2',key,'Teacher Answer Key — '+unit.name+(versions.length>1?' · Version '+String.fromCharCode(65+vi):''));
   versionSections[vi].forEach(sec=>{
    const sectionItems=items.filter(item=>item.sectionId===sec.id);
    if(!sectionItems.length)return;
    const block=elt('section',key);block.className='section-print';
    elt('h3',block,sec.title);
    sectionItems.forEach((item,i)=>renderQuestion(item.question,block,i+1,true));
   });
  }
 });
 const sizes=versions.map(v=>v.length);
 status.textContent='Preview ready: '+versions.length+' version(s), '+sizes.join('/')+' questions. Review mathematical answers before printing.';
 $('print').disabled=versions.every(v=>!v.length);
}
$('currentVersion').addEventListener('change',()=>{activeVersion=Number($('currentVersion').value);renderEditor()});
$('refreshVersion').addEventListener('click',()=>{versions[activeVersion]=sectionQuestions(versionSections[activeVersion],new Set());renderEditor();renderAll()});
$('resetEdits').addEventListener('click',()=>{versions[activeVersion]=currentItems().map(x=>({source:x.source,question:JSON.parse(JSON.stringify(x.source)),sectionId:x.sectionId}));renderEditor();renderAll()});
$('key').addEventListener('change',()=>{if(versions.length)renderAll()});
$('customTitle').addEventListener('input',()=>{if(versions.length)renderAll()});
units.forEach((u,i)=>option(unitSelect,u.id,'Unit '+(i+1)+' · '+u.name));
const requested=params.get('unit');if(units.some(u=>u.id===requested))unitSelect.value=requested;
if(params.get('mode')==='assessment')$('mode').value='assessment';
unitSelect.addEventListener('change',()=>{skills();renderSpiralUnits();renderSections();versions=[];$('output').replaceChildren();$('editor').hidden=true;$('print').disabled=true;status.textContent=bank.available('algebra2',unitSelect.value)?'Ready to generate.':'No question bank available for this unit yet.'});
$('all').addEventListener('click',()=>doc.querySelectorAll('#skills input').forEach(x=>x.checked=true));
$('none').addEventListener('click',()=>doc.querySelectorAll('#skills input').forEach(x=>x.checked=false));
$('build').addEventListener('click',build);$('print').addEventListener('click',()=>root.print());
skills();renderSpiralUnits();
root.MK_BANK_LOADER.loadFromSite(undefined,'../').then(()=>{
 renderSpiralUnits();status.textContent=bank.available('algebra2',unitSelect.value)?'Ready to generate.':'No question bank available for this unit yet.';
}).catch(e=>{status.textContent='Could not load question banks: '+e.message;$('build').disabled=true});
})(window);