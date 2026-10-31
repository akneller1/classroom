/* Read-only selection of authored questions. Automatic grading is restricted
 * to source-marked choices; written responses use worked-solution self review. */
(function(G){'use strict';
const $=id=>document.getElementById(id),course=G.LIBRARY.courses.find(c=>c.id==='algebra2'),bank=G.MK_QUESTION_BANKS,catalog=G.MK_COURSE_CATALOG;
let results=[];
function el(tag,parent,text){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;parent.appendChild(n);return n}
course.units.forEach(u=>{const o=el('option',$('unit'),u.name);o.value=u.id});
const requested=new URLSearchParams(location.search).get('unit');if(course.units.some(u=>u.id===requested))$('unit').value=requested;
function skills(){ $('skills').replaceChildren();catalog.getSkillRecords('algebra2',$('unit').value).forEach(s=>{const l=el('label',$('skills')),i=el('input',l);i.type='checkbox';i.value=s.id;i.checked=true;el('span',l,s.name)});$('questions').replaceChildren();$('report').replaceChildren();$('reportHeading').hidden=true;results=[]; }
function report(){const host=$('report');host.replaceChildren();$('reportHeading').hidden=!results.length;catalog.getSkillRecords('algebra2',$('unit').value).forEach(s=>{const rows=results.filter(r=>r.skillId===s.id),done=rows.filter(r=>r.done);if(rows.length)el('p',host,s.name+': '+done.length+'/'+rows.length+' reviewed; '+done.filter(r=>r.correct).length+' correct or self-rated ready.')})}
function start(){
 results=[];$('questions').replaceChildren();const ids=Array.from(document.querySelectorAll('#skills input:checked')).map(i=>i.value);
 if(!ids.length){$('status').textContent='Select at least one skill.';return}
 const pools=ids.map(id=>bank.select({courseId:'algebra2',unitId:$('unit').value,skillIds:[id],level:$('level').value}).filter(q=>Number(q.id.match(/(\d+)$/)?.[1]||0)%2===0).sort(()=>Math.random()-.5));
 const count=Math.min(30,Math.max(1,Number($('count').value)||12)),list=[];
 while(list.length<count&&pools.some(p=>p.length)){for(const p of pools){if(p.length&&list.length<count)list.push(p.pop())}}
 for(const [n,q] of list.entries()){
  const r={skillId:q.skillId,done:false,correct:false};results.push(r);const article=el('article',$('questions'));article.className='item';article.dataset.sourceId=q.id;
  el('h2',article,'Question '+(n+1));el('p',article,q.prompt);
  if(q.diagram?.type==='image'){const img=el('img',article);img.src='../'+q.diagram.spec.src;img.alt=q.diagram.spec.alt}
  const inputs=[];if(q.options)q.options.forEach((o,i)=>{const l=el('label',article),input=el('input',l);input.type=q.format==='select-all'?'checkbox':'radio';input.name='q'+n;inputs.push(input);el('span',l,o.text)});
  (q.parts||[]).forEach(p=>{el('p',article,p.prompt);const a=el('textarea',article);a.setAttribute('aria-label',p.prompt)});
  if(q.format==='short-answer'){const a=el('textarea',article);a.setAttribute('aria-label','Your answer')}
  const check=el('button',article,inputs.length?'Check answer':'Review worked solution');const feedback=el('p',article);feedback.setAttribute('role','status');const solution=el('div',article);solution.className='solution';solution.hidden=true;
  el('p',solution,'Answer: '+(typeof q.answer==='object'?JSON.stringify(q.answer):q.answer));const steps=el('ol',solution);q.solutionSteps.forEach(s=>el('li',steps,s));
  (q.parts||[]).forEach(p=>{if(p.answer!==undefined)el('p',solution,p.prompt+' — '+p.answer)});
  check.onclick=()=>{
   if(inputs.length){if(!inputs.some(i=>i.checked)){feedback.textContent='Select an answer first.';return}r.correct=q.options.every((o,i)=>inputs[i].checked===(o.correct===true));r.done=true;feedback.textContent=r.correct?'Correct.':'Review the worked solution.';check.disabled=true;inputs.forEach(i=>i.disabled=true)}
   else {check.disabled=true;el('p',solution,'Compare your work, then rate your readiness.');for(const [label,correct] of [['I understand this',true],['I need more practice',false]]){const b=el('button',solution,label);b.onclick=()=>{r.correct=correct;r.done=true;solution.querySelectorAll('button').forEach(x=>x.disabled=true);report()}}}
   solution.hidden=false;report();
  };
 }
 $('status').textContent=list.length+' questions ready. Written responses use self review.';report();
}
$('all').onclick=()=>document.querySelectorAll('#skills input').forEach(i=>i.checked=true);$('none').onclick=()=>document.querySelectorAll('#skills input').forEach(i=>i.checked=false);$('start').onclick=start;$('unit').onchange=skills;skills();
G.MK_BANK_LOADER.loadFromSite(undefined,'../').then(()=>{$('status').textContent='Ready to practice.';$('start').disabled=false}).catch(e=>{$('status').textContent='Unable to load questions: '+e.message});
})(window);
