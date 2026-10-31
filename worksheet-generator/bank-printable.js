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
function build(){
 const unitId=unitSelect.value, level=$('level').value, fmt=$('format').value;
 const skillIds=Array.from(doc.querySelectorAll('#skills input:checked')).map(x=>x.value);
 if(!skillIds.length){status.textContent='Choose at least one skill.';return}
 const formats=fmt==='all'?undefined:[fmt];
 const candidates=bank.select({courseId:'algebra2',unitId,level,skillIds,formats}).filter(q=>!q.diagram||q.diagram.type==='image');
 const wanted=Math.max(1,Math.min(60,Number($('count').value)||12));
 const selected=shuffle(candidates).slice(0,wanted);
 const out=$('output');out.replaceChildren();
 if(!selected.length){status.textContent='No questions match these settings. Change the unit, level, skills, or format.';$('print').disabled=true;return}
 const unit=units.find(u=>u.id===unitId),mode=$('mode').value;
 const paper=elt('section',out);paper.className='sheet';
 elt('h2',paper,unit.name+' — '+(mode==='worksheet'?'Practice Worksheet':'Assessment'));
 elt('p',paper,'Name: __________________________  Date: ______________');
 selected.forEach((q,i)=>renderQuestion(q,paper,i+1,false));
 if($('key').checked){const key=elt('section',out);key.className='sheet key';elt('h2',key,'Teacher Answer Key — '+unit.name);selected.forEach((q,i)=>renderQuestion(q,key,i+1,true))}
 status.textContent='Prepared '+selected.length+' questions'+(selected.length<wanted?' (only '+selected.length+' match these settings)':'')+'. Review before printing.';
 $('print').disabled=false;
}
units.forEach((u,i)=>option(unitSelect,u.id,'Unit '+(i+1)+' · '+u.name));
const requested=params.get('unit');if(units.some(u=>u.id===requested))unitSelect.value=requested;
if(params.get('mode')==='assessment')$('mode').value='assessment';
unitSelect.addEventListener('change',()=>{skills();$('output').replaceChildren();$('print').disabled=true;status.textContent=bank.available('algebra2',unitSelect.value)?'Ready to generate.':'No question bank available for this unit yet.'});
$('all').addEventListener('click',()=>doc.querySelectorAll('#skills input').forEach(x=>x.checked=true));
$('none').addEventListener('click',()=>doc.querySelectorAll('#skills input').forEach(x=>x.checked=false));
$('build').addEventListener('click',build);$('print').addEventListener('click',()=>root.print());
skills();
root.MK_BANK_LOADER.loadFromSite(undefined,'../').then(()=>{
 status.textContent=bank.available('algebra2',unitSelect.value)?'Ready to generate.':'No question bank available for this unit yet.';
}).catch(e=>{status.textContent='Could not load question banks: '+e.message;$('build').disabled=true});
})(window);