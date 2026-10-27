/* Interactive Practice Test — shares the menu generator's independently checked questions. */
(function(G){
'use strict';
var N=G.MKMENU, W=G.MKWS, root=document.getElementById('practice'), STORE='mk-readiness-v2';
var state=null,config={unit:'algebra1-expressions-equations',level:'cp1',count:10,mode:'test',format:'mixed',minutes:0,skills:[]};
var esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
var fmt=s=>N.mathSafe(String(s||''));
var levels={cp2:2,cp1:4,honors:6};
function save(){try{localStorage.setItem(STORE,JSON.stringify({state:state,config:config}));}catch(e){}}
function read(){try{var d=JSON.parse(localStorage.getItem(STORE)||'null');if(d&&d.config){config=d.config;state=d.state||null;}}catch(e){}}
function units(){return N.CATALOG[0].units.filter(u=>N.skillSets[u[0]]);}
function chosen(){return N.skillSets[config.unit];}
function skills(){return chosen().skills.filter(s=>config.skills.indexOf(s.id)!==-1);}
function studentURL(){
 var base=G.location.href.split('#')[0];
 var skills= config.skills.length?config.skills:chosen().skills.map(x=>x.id);
 return base+'#unit='+encodeURIComponent(config.unit)+'&student=1&level='+encodeURIComponent(config.level)+'&count='+config.count+'&format='+encodeURIComponent(config.format)+'&minutes='+config.minutes+'&skills='+encodeURIComponent(skills.join(','));
}
function copyStudentLink(){
 var url=studentURL(),field=root.querySelector('#pt-student-link');
 if(field)field.value=url;
 if(G.navigator.clipboard&&G.navigator.clipboard.writeText)G.navigator.clipboard.writeText(url).then(()=>{var b=root.querySelector('#pt-share');if(b)b.textContent='Copied student link';}).catch(()=>{if(field){field.focus();field.select();}});
 else if(field){field.focus();field.select();}
}
function controls(){return '<section class="pt-card"><span class="pt-eyebrow">ASSESSMENT READINESS · VERSION 2</span><h1>Assessment Readiness Check</h1><p>Take a unit-style assessment, review your performance by skill, and generate a targeted reassessment.</p><div class="pt-fields"><label>Unit<select id="pt-unit">'+units().map(u=>'<option value="'+esc(u[0])+'" '+(config.unit===u[0]?'selected':'')+'>'+esc(u[1])+'</option>').join('')+'</select></label><label>Level<select id="pt-level">'+['cp2','cp1','honors'].map(l=>'<option value="'+l+'" '+(config.level===l?'selected':'')+'>'+l.toUpperCase()+'</option>').join('')+'</select></label><label>Questions<select id="pt-count">'+[5,10,15,20,25].map(n=>'<option '+(config.count===n?'selected':'')+'>'+n+'</option>').join('')+'</select></label><label>Time limit<select id="pt-minutes">'+[0,20,30,45].map(n=>'<option value="'+n+'" '+(config.minutes===n?'selected':'')+'>'+(n?n+' minutes':'Untimed')+'</option>').join('')+'</select></label><label>Format<select id="pt-format"><option value="mixed" '+(config.format==='mixed'?'selected':'')+'>Mixed</option><option value="mc" '+(config.format==='mc'?'selected':'')+'>Multiple choice</option><option value="self" '+(config.format==='self'?'selected':'')+'>Short answer / auto-check where supported</option></select></label></div><h2>Choose skills</h2><div class="pt-skills">'+chosen().skills.map(s=>'<label><input type="checkbox" data-skill="'+esc(s.id)+'" '+(config.skills.includes(s.id)?'checked':'')+'> '+esc(s.name)+'</label>').join('')+'</div><div class="pt-actions"><button id="pt-all" class="pt-secondary">Select all</button><button id="pt-build">Generate printable assessment</button><button id="pt-share" class="pt-secondary">Copy student link</button></div><label class="pt-share-label">Student link (opens this unit with your selected settings)<input id="pt-student-link" readonly value="'+esc(studentURL())+'"></label><p class="pt-muted">Results stay on this device. Numeric answers and supported inequalities are graded exactly; complex written responses use self-check.</p></section>';}
function setup(){config.mode='test';if(state&&!state.done){root.innerHTML='<section class="pt-card"><h1>Assessment saved</h1><p>Your unfinished assessment is saved in this browser.</p><div class="pt-actions"><button id="pt-resume">Resume assessment</button><button id="pt-discard" class="pt-secondary">Discard and create new</button></div></section>';root.querySelector('#pt-resume').onclick=show;root.querySelector('#pt-discard').onclick=()=>{if(confirm('Discard your saved assessment?')){state=null;save();setup();}};return;}if(!N.skillSets[config.unit])config.unit=units()[0][0];root.innerHTML=controls();root.querySelector('#pt-unit').onchange=e=>{config.unit=e.target.value;config.skills=chosen().skills.map(s=>s.id);save();setup();};['level','count','format','minutes'].forEach(f=>root.querySelector('#pt-'+f).onchange=e=>{config[f]=(f==='count'||f==='minutes')?+e.target.value:e.target.value;save();});root.querySelectorAll('[data-skill]').forEach(x=>x.onchange=()=>{config.skills=Array.from(root.querySelectorAll('[data-skill]:checked')).map(el=>el.dataset.skill);save();});root.querySelector('#pt-all').onclick=()=>{config.skills=chosen().skills.map(s=>s.id);save();setup();};root.querySelector('#pt-build').onclick=()=>build();root.querySelector('#pt-share').onclick=copyStudentLink;}
function makeQuestion(skill,seed,index,used){
 var policy={level:config.level,intOnly:config.level!=='honors'}, tier=levels[config.level]+(index%3===0?-1:index%3===2?1:0);
 var p=N.generateProblem(config.unit,skill.id,Math.max(1,Math.min(7,tier)),policy,seed,used);
 if(p.failed)return null;
 var mode=config.format==='mc'?'mc':config.format==='self'?'self':index%2===0?'mc':'self';
 var choices=null;
 if(mode==='mc'){
   var made=N.makeChoices(p);
   if(!made.fail){if(made.derived)p=made.derived;choices={opts:made.opts,key:made.key};}
   else if(config.format==='mc')return null;
   else mode='self';
 }
 if(mode==='self'&&G.MKPRACTICE&&G.MKPRACTICE.supports(p))mode='auto';
 return {id:config.unit+'-'+seed+'-'+index,skill:skill.id,skillName:skill.name,problem:p,kind:mode,choices:choices,response:null,checked:false,correct:null,review:false};
}
function build(overrides){
 config.mode='test';
 var chosenSkills=overrides&&overrides.length?chosen().skills.filter(x=>overrides.includes(x.id)):skills();
 if(!chosenSkills.length){alert('Select at least one skill.');return;}
 // This is the actual Assessment Generator's standard-test engine, not a duplicate question generator.
 var ac=N.defaultConfig(config.unit,'test');
 ac.level=config.level;ac.seed=Math.floor(Math.random()*1e9);ac.versions=1;ac.questionPool='practice';ac.skills={};
 chosenSkills.forEach(x=>ac.skills[x.id]=true);
 var mcCount=config.format==='self'?0:config.format==='mc'?config.count:Math.ceil(config.count/2);
 var writtenCount=config.count-mcCount;
 ac.sections=N.testSections('std');
 ac.sections[0].offered=ac.sections[0].required=mcCount;
 ac.sections[1].offered=ac.sections[1].required=writtenCount;
 ac.sections=ac.sections.filter(x=>x.offered>0);
 var generated=N.newAssessment(ac);
 var questions=[];
 generated.versions[0].sections.forEach(function(sec){
   sec.items.forEach(function(p){
      if(p.failed||!p.parts||!p.parts.length)return;
      var sk=chosen().byId[p.skill],choice=p.mc&&p.mc.opts&&p.mc.opts.length===4?{opts:p.mc.opts,key:p.mc.key}:null;
      var kind=choice?'mc':G.MKPRACTICE&&G.MKPRACTICE.supports(p)?'auto':'self';
      questions.push({id:p.uid,skill:p.skill,skillName:sk?sk.name:p.tag,problem:p,kind:kind,choices:choice,response:null,checked:false,correct:null,review:false});
   });
 });
 if(!questions.length){alert('The assessment generator could not create verified questions for this selection.');return;}
 var previous=state&&state.done?state.questions.filter(q=>q.correct===true).length+'/'+state.questions.length:null;
 state={questions:questions,index:0,done:false,started:Date.now(),deadline:config.minutes?Date.now()+config.minutes*60000:null,mode:'test',previousScore:overrides&&overrides.length?previous:null,source:'assessment-generator',paperView:true};
 save();show();
}
function problemHTML(q){var p=q.problem;return '<div class="pt-problem">'+fmt(p.prompt)+(p.fig&&N.figHtml?N.figHtml(p.fig):'')+(p.parts||[]).map((part,i)=>part.prompt?'<div class="pt-part">'+(part.label?esc(part.label)+' ':'')+fmt(part.prompt)+'</div>':'').join('')+'</div>';}
function solutionMath(value){var source=String(value==null?'':value).trim();if(!source)return '';if(source.indexOf('⟨')>=0)return fmt(source);try{return G.katex.renderToString(source.replace(/\\frac/g,'\\dfrac'),{throwOnError:false,output:'html',trust:false});}catch(e){return esc(source);}}
function feedback(q){var p=q.problem,part=p.parts[0];var lines=(p.steps||[]).map(x=>'<li>'+(x.t?fmt(x.t):'')+(x.m?'<div class="pt-step-math">'+solutionMath(x.m)+'</div>':'')+'</li>').join('');return '<div class="pt-explain"><strong>Answer:</strong> '+(p.parts||[]).map(x=>fmt(x.answer)).join(' · ')+(lines?'<h3>Worked solution</h3><ol>'+lines+'</ol>':'<p>Compare your process with the verified answer above.</p>')+(p.parts||[]).map(x=>x.answerFig&&N.figHtml?N.figHtml(x.answerFig):'').join('')+'</div>';}
function item(q,i){var answered=q.response!==null&&q.response!=='';var visible=state.done||state.mode==='practice'&&q.checked;return '<section class="pt-card"><div class="pt-top"><span class="pt-eyebrow">'+esc(q.skillName)+'</span><strong>Question '+(i+1)+' of '+state.questions.length+'</strong></div>'+problemHTML(q)+(q.kind==='mc'?'<div class="pt-options">'+q.choices.opts.map((v,j)=>'<label class="pt-option"><input type="radio" name="pt-answer-'+i+'" value="'+j+'" '+(+q.response===j&&answered?'checked':'')+' '+(visible?'disabled':'')+'> '+fmt(v)+'</label>').join('')+'</div>':'<label class="pt-response">Show your work and enter your response<textarea id="pt-written" rows="4" '+(visible?'disabled':'')+' placeholder="Explain your solution...">'+esc(q.response||'')+'</textarea></label>')+(visible?'<div class="pt-status '+(q.correct===true?'pt-good':q.correct===false?'pt-bad':'')+'">'+(q.correct===true?'Correct':q.correct===false?'Needs review':'Compare your work')+'</div>'+feedback(q)+(q.kind==='self'&&q.correct===null?'<div class="pt-actions"><button data-grade="yes">My work is correct</button><button data-grade="no" class="pt-secondary">I need more practice</button></div>':''):'')+'</section>';}
function paperHTML(){
 if(!state)return '';
 var ABC='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
 return '<div class="pt-paper-head"><span>MR. K’S CLASSROOM · ASSESSMENT READINESS</span><h2>'+esc(chosen().unitName||'Algebra 1')+'</h2><p>Name: ______________________________ Date: ______________</p><p><strong>Directions:</strong> Show all work on separate paper. Read the test below or print/save it as a PDF. Enter only your final answers into the numbered answer sheet on this page. Do not include your work in the answer boxes.</p></div>'+
 state.questions.map(function(q,i){return '<section class="pt-paper-question"><div class="pt-paper-number">'+(i+1)+'.</div><div class="pt-paper-content">'+problemHTML(q)+(q.kind==='mc'?'<div class="pt-paper-choices">'+q.choices.opts.map((v,j)=>'<div>'+ABC[j]+'. '+fmt(v)+'</div>').join('')+'</div>':'')+'</div></section>';}).join('');
}
function answerSheetHTML(){
 return '<section class="pt-card pt-answer-sheet" id="pt-answer-sheet"><h2>Student answer sheet</h2><p class="pt-muted">Work on paper. Enter the final response for each numbered question below. Multiple-choice: select A, B, C, or D.</p><div class="pt-answer-grid">'+state.questions.map(function(q,i){
  var value=q.response===null?'':q.kind==='mc'?'ABCD'[q.response]||'':q.response;
  return '<label class="pt-answer-row"><span>'+(i+1)+'.</span><input aria-label="Answer for question '+(i+1)+'" data-answer="'+i+'" autocomplete="off" placeholder="'+(q.kind==='mc'?'A–D':'Answer')+'" value="'+esc(value)+'"></label>';
 }).join('')+'</div></section>';
}
function printPaper(){
 var holder=G.document.createElement('div');holder.className='pt-print-standalone';holder.innerHTML=paperHTML();G.document.body.appendChild(holder);G.document.body.classList.add('pt-printing-paper');
 var clean=function(){G.document.body.classList.remove('pt-printing-paper');holder.remove();G.removeEventListener('afterprint',clean);};
 G.addEventListener('afterprint',clean);G.print();
}
function tickTimer(){
 if(!state||state.done||!state.deadline)return;
 var remain=Math.max(0,state.deadline-Date.now()),el=root.querySelector('#pt-timer');
 if(el)el.textContent='Time remaining: '+Math.floor(remain/60000)+':'+String(Math.floor(remain/1000)%60).padStart(2,'0');
 if(remain===0)submit(true);
}
var timerHandle=G.setInterval(tickTimer,1000);
function show(){
 if(!state){setup();return;}
 if(state.done){results();return;}
 if(state.deadline&&Date.now()>=state.deadline){submit(true);return;}
 state.mode='test';
 root.innerHTML='<header class="pt-header"><div><span class="pt-eyebrow">ASSESSMENT READINESS · PRINT & RESPOND</span><h1>'+esc(chosen().unitName||'Algebra 1')+' Unit Test</h1><p class="pt-muted" id="pt-timer">'+(state.deadline?'Timed assessment':'Untimed assessment')+'</p></div><button class="pt-secondary" id="pt-exit">Save & exit</button></header><div class="pt-actions"><button id="pt-print-paper">Print / Save Test as PDF</button><button class="pt-secondary" id="pt-jump-answers">Go to answer sheet</button></div><div class="pt-paper" id="pt-paper">'+paperHTML()+'</div>'+answerSheetHTML()+'<div class="pt-actions"><button id="pt-submit">Submit answers for grading</button></div>';
 root.querySelector('#pt-print-paper').onclick=printPaper;
 root.querySelector('#pt-jump-answers').onclick=()=>root.querySelector('#pt-answer-sheet').scrollIntoView({behavior:'smooth'});
 root.querySelector('#pt-exit').onclick=()=>{state.paused=true;save();setup();};
 root.querySelectorAll('[data-answer]').forEach(function(el){
  el.oninput=function(){
   var i=+el.dataset.answer,q=state.questions[i],v=el.value.trim();
   q.response=q.kind==='mc'?(v?(/^[ABCD]$/i.test(v)?'ABCD'.indexOf(v.toUpperCase()):v):null):(v||null);
   save();
  };
 });
 root.querySelector('#pt-submit').onclick=()=>submit();
 tickTimer();
}
function go(i){state.index=Math.max(0,Math.min(state.questions.length-1,i));save();show();}
function submit(forced){var missing=state.questions.filter(q=>q.response===null||q.response==='').length;if(!forced&&!confirm('Submit assessment now? '+missing+' question(s) are unanswered. '+state.questions.filter(q=>q.review).length+' marked for review.'))return;state.questions.forEach(q=>{if(q.kind==='mc')q.correct=typeof q.response==='number'&&q.response===q.choices.key;if(q.kind==='auto'){var g=G.MKPRACTICE.grade(q.problem,q.response);q.correct=g.status==='correct'?true:g.status==='incorrect'?false:null;if(g.status==='self')q.kind='self';q.invalidResponse=g.status==='invalid'?g.message:null;}if(q.kind==='self'&&(q.response===null||q.response===''))q.correct=false;q.checked=true;});state.done=true;state.finished=Date.now();save();results();}
function stats(){var buckets={};state.questions.forEach(q=>{var b=buckets[q.skill]||(buckets[q.skill]={name:q.skillName,correct:0,graded:0,missing:0});if(q.correct===null)b.missing++;else{b.graded++;if(q.correct)b.correct++;}});return Object.entries(buckets).map(([id,b])=>Object.assign({id:id},b));}
function recommendations(){
 var list=stats().filter(b=>b.graded>0).sort((a,b)=>a.correct/a.graded-b.correct/b.graded);
 if(!list.length)return 'Review your written responses to see which skills need more practice.';
 var weak=list.filter(b=>b.correct/b.graded<0.8).slice(0,3);
 if(!weak.length)return 'Strong results on the skills assessed. Try another version to confirm your understanding.';
 return 'Focus next on: '+weak.map(b=>b.name).join('; ')+'. Select Practice my weak skills for fresh questions.';
}
function results(){var qs=state.questions,graded=qs.filter(q=>q.correct!==null),good=graded.filter(q=>q.correct).length,remaining=qs.length-graded.length;root.innerHTML='<section class="pt-card"><span class="pt-eyebrow">ASSESSMENT REPORT</span><h1>Assessment Readiness Report</h1><p class="pt-score">'+(graded.length?Math.round(good/graded.length*100)+'%':'Self-review required')+'</p><p>'+good+' / '+graded.length+' graded correctly'+(remaining?' · '+remaining+' awaiting self-assessment':'')+'</p><h2>Your study plan</h2><p>'+esc(recommendations())+'</p><h2>Skills breakdown</h2>'+stats().map(b=>'<div class="pt-skillbar"><div><strong>'+esc(b.name)+'</strong><span>'+b.correct+'/'+b.graded+' graded'+(b.missing?' · '+b.missing+' unreviewed':'')+'</span></div><div class="pt-track"><div style="width:'+(b.graded?100*b.correct/b.graded:0)+'%"></div></div></div>').join('')+'<div class="pt-actions"><button id="pt-weak">Practice my weak skills</button><button id="pt-retry" class="pt-secondary">New version</button><button id="pt-print" class="pt-secondary">Print report</button><button id="pt-new" class="pt-secondary">New setup</button></div><h2>Review answers</h2>'+qs.map((q,i)=>'<details class="pt-review"><summary>Question '+(i+1)+' · '+esc(q.skillName)+' · '+(q.correct===null?'Self-check':q.correct?'Correct':'Incorrect')+'</summary>'+problemHTML(q)+'<p><strong>Your response: </strong>'+(q.kind==='mc'&&typeof q.response==='number'?fmt(q.choices.opts[q.response]):esc(q.response||'(blank)'))+'</p>'+feedback(q)+(q.invalidResponse?'<p class="pt-bad">'+esc(q.invalidResponse)+'</p>':'')+(q.kind==='self'?'<div class="pt-actions"><button data-self="'+i+'" data-val="yes">Correct</button><button data-self="'+i+'" data-val="no" class="pt-secondary">Needs practice</button></div>':'')+'</details>').join('')+'</section>';
 root.querySelector('#pt-weak').onclick=()=>{var weak=stats().filter(b=>(b.graded>0&&b.correct/b.graded<0.8)||b.missing>0).map(b=>b.id);if(!weak.length){alert('No weak skills identified. Try a new version!');return;}config.count=Math.min(10,Math.max(5,weak.length*3));config.minutes=0;config.mode='test';build(weak);};
 root.querySelector('#pt-retry').onclick=()=>build();root.querySelector('#pt-print').onclick=()=>{root.querySelectorAll('details.pt-review').forEach(d=>d.open=true);print();};root.querySelector('#pt-new').onclick=()=>{state=null;save();setup();};
 root.querySelectorAll('[data-self]').forEach(b=>b.onclick=()=>{qs[+b.dataset.self].correct=b.dataset.val==='yes';save();results();});
}
read();var params=new URLSearchParams((G.location.hash||'').replace(/^#/,''));var student=params.get('student')==='1';if(student&&N.skillSets[params.get('unit')]){config.unit=params.get('unit');config.level=['cp2','cp1','honors'].includes(params.get('level'))?params.get('level'):'cp1';config.count=[5,10,15,20,25].includes(+params.get('count'))?+params.get('count'):10;config.format=['mixed','mc','self'].includes(params.get('format'))?params.get('format'):'mixed';config.minutes=[0,20,30,45].includes(+params.get('minutes'))?+params.get('minutes'):0;config.skills=(params.get('skills')||'').split(',').filter(id=>N.skillSets[config.unit].byId[id]);if(!config.skills.length)config.skills=N.skillSets[config.unit].skills.map(x=>x.id);state=null;}config.mode='test';if(state&&!state.done){state.mode='test';save();}var requested=/unit=([a-z0-9-]+)/.exec(G.location.hash||'');if(requested&&N.skillSets[requested[1]]&&(!state||state.done)){config.unit=requested[1];config.skills=N.skillSets[config.unit].skills.map(s=>s.id);state=null;}
if(!N.skillSets[config.unit])config.unit=units()[0][0];
if(state&&!state.done){root.innerHTML='<section class="pt-card"><h1>Continue your practice test?</h1><p>Your previous assessment is saved in this browser.</p><div class="pt-actions"><button id="resume">Resume test</button><button id="fresh" class="pt-secondary">Start fresh</button></div></section>';root.querySelector('#resume').onclick=show;root.querySelector('#fresh').onclick=()=>{state=null;save();setup();};}
else if(state&&state.done)results();else setup();
})(window);