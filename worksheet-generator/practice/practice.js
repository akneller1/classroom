/* Interactive Practice Test — shares the menu generator's independently checked questions. */
(function(G){
'use strict';
var N=G.MKMENU, W=G.MKWS, root=document.getElementById('practice'), STORE='mk-readiness-auto-v3';
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
function controls(){return '<section class="pt-card"><span class="pt-eyebrow">ASSESSMENT READINESS · VERSION 2</span><h1>Assessment Readiness Check</h1><p>Take a unit-style assessment, review your performance by skill, and generate a targeted reassessment.</p><div class="pt-fields"><label>Unit<select id="pt-unit">'+units().map(u=>'<option value="'+esc(u[0])+'" '+(config.unit===u[0]?'selected':'')+'>'+esc(u[1])+'</option>').join('')+'</select></label><label>Level<select id="pt-level">'+['cp2','cp1','honors'].map(l=>'<option value="'+l+'" '+(config.level===l?'selected':'')+'>'+l.toUpperCase()+'</option>').join('')+'</select></label><label>Questions<select id="pt-count">'+[5,10,15,20,25].map(n=>'<option '+(config.count===n?'selected':'')+'>'+n+'</option>').join('')+'</select></label><label>Time limit<select id="pt-minutes">'+[0,20,30,45].map(n=>'<option value="'+n+'" '+(config.minutes===n?'selected':'')+'>'+(n?n+' minutes':'Untimed')+'</option>').join('')+'</select></label><label>Format<select id="pt-format"><option value="mixed" '+(config.format==='mixed'?'selected':'')+'>Mixed</option><option value="mc" '+(config.format==='mc'?'selected':'')+'>Multiple choice</option><option value="self" '+(config.format==='self'?'selected':'')+'>Automatically graded short answer</option></select></label></div><h2>Choose skills</h2><div class="pt-skills">'+chosen().skills.map(s=>'<label><input type="checkbox" data-skill="'+esc(s.id)+'" '+(config.skills.includes(s.id)?'checked':'')+'> '+esc(s.name)+'</label>').join('')+'</div><div class="pt-actions"><button id="pt-all" class="pt-secondary">Select all</button><button id="pt-build">Generate printable assessment</button><button id="pt-share" class="pt-secondary">Copy student link</button></div><label class="pt-share-label">Student link (opens this unit with your selected settings)<input id="pt-student-link" readonly value="'+esc(studentURL())+'"></label><p class="pt-muted">Results stay on this device. Every included question supports automatic grading; unsupported question formats are excluded.</p></section>';}
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
function autoKind(p,choice){
 if(!p||p.failed||!p.parts||p.parts.length!==1)return null;
 var graph={problem:p,kind:'auto'};
 if(G.MKEXPGRAPH&&G.MKEXPGRAPH.target(graph))return 'auto';
 if(G.MKSYSTEM&&G.MKSYSTEM.target(graph))return 'auto';
 if(G.MKLINE&&G.MKLINE.target(graph))return 'auto';
 if(G.MKPARABOLA&&G.MKPARABOLA.target(graph))return 'auto';
 if(G.MKGRAPH&&(G.MKGRAPH.supports(graph)||G.MKGRAPH.pointTarget(graph)))return 'auto';
 if(choice&&choice.opts&&choice.opts.length===4&&Number.isInteger(choice.key)&&choice.key>=0&&choice.key<4)return 'mc';
 if(G.MKPRACTICE&&G.MKPRACTICE.supports(p))return 'auto';
 return null;
}
function build(overrides){
 config.mode='test';
 var selected=overrides&&overrides.length?chosen().skills.filter(x=>overrides.includes(x.id)):skills();
 if(!selected.length){alert('Select at least one skill.');return;}
 var questions=[],seen=new Set(),skipped=0,requested=config.count;
 // Use the same verified teacher Assessment Generator, but accept ONLY fully gradeable questions.
 for(var attempt=0;attempt<7&&questions.length<requested;attempt++){
   var ac=N.defaultConfig(config.unit,'test');
   ac.level=config.level;ac.seed=Math.floor(Math.random()*1e9);ac.versions=1;ac.questionPool='practice';ac.skills={};
   selected.forEach(x=>ac.skills[x.id]=true);
   var remaining=requested-questions.length;
   var mcCount=config.format==='self'?0:config.format==='mc'?remaining*2:remaining;
   var openCount=config.format==='mc'?0:config.format==='self'?remaining*2:remaining;
   ac.sections=N.testSections('std');
   ac.sections[0].offered=ac.sections[0].required=mcCount;
   ac.sections[1].offered=ac.sections[1].required=openCount;
   ac.sections=ac.sections.filter(x=>x.offered>0);
   var generated=N.newAssessment(ac);
   generated.versions[0].sections.forEach(function(sec){
     sec.items.forEach(function(p){
       if(questions.length>=requested)return;
       var fingerprint=p.key||N.studentText(p).replace(/\s+/g,'');
       if(p.failed||seen.has(fingerprint)){skipped++;return;}
       var choice=p.mc&&p.mc.opts&&p.mc.opts.length===4?{opts:p.mc.opts,key:p.mc.key}:null;
       var graph={problem:p,kind:'auto'};
       if((G.MKEXPGRAPH&&G.MKEXPGRAPH.target(graph))||(G.MKSYSTEM&&G.MKSYSTEM.target(graph))||(G.MKLINE&&G.MKLINE.target(graph))||(G.MKPARABOLA&&G.MKPARABOLA.target(graph))||(G.MKGRAPH&&(G.MKGRAPH.supports(graph)||G.MKGRAPH.pointTarget(graph))))choice=null;
       var kind=autoKind(p,choice);
       if(!kind){skipped++;return;}
       var sk=chosen().byId[p.skill];
       seen.add(fingerprint);
       questions.push({id:p.uid,skill:p.skill,skillName:sk?sk.name:p.tag,problem:p,kind:kind,choices:kind==='mc'?choice:null,response:null,checked:false,correct:null,review:false});
     });
   });
 }
 if(!questions.length){alert('No fully auto-gradable questions could be generated. Try a different skill selection or choose Multiple Choice.');return;}
 if(questions.length<requested)alert('Only '+questions.length+' of '+requested+' requested questions could be generated with reliable automatic grading. Unsupported questions were excluded; no self-graded questions were included.');
 var previous=state&&state.done?state.questions.filter(q=>q.correct===true).length+'/'+state.questions.length:null;
 state={questions:questions,index:0,done:false,started:Date.now(),deadline:config.minutes?Date.now()+config.minutes*60000:null,mode:'test',previousScore:overrides&&overrides.length?previous:null,source:'assessment-generator',paperView:true,autoGraded:true,unsupportedExcluded:skipped};
 save();show();
}
function problemHTML(q){var p=q.problem;return '<div class="pt-problem">'+fmt(p.prompt)+(p.fig&&N.figHtml?N.figHtml(p.fig):'')+(p.parts||[]).map((part,i)=>part.prompt?'<div class="pt-part">'+(part.label?esc(part.label)+' ':'')+fmt(part.prompt)+'</div>':'').join('')+'</div>';}
function solutionMath(value){
 var source=String(value==null?'':value).trim();
 if(!source)return '';
 if(source.indexOf('⟨')>=0)return fmt(source);
 // Use the site's own marked-math renderer, rather than relying on raw TeX as HTML.
 // If KaTeX is unavailable, preserve readable math instead of exposing commands.
 if(G.katex&&typeof G.katex.renderToString==='function'){
   try{return G.katex.renderToString(source,{throwOnError:false,output:'html',trust:false});}catch(e){}
 }
 var plain=source.replace(/\\\\cdot/g,' × ').replace(/\\\\times/g,' × ')
   .replace(/\\\\div/g,' ÷ ').replace(/\\\\pm/g,' ± ')
   .replace(/\\^\\{([^{}]*)\\}/g,'^($1)')
   .replace(/\\\\frac\\{([^{}]*)\\}\\{([^{}]*)\\}/g,'($1)/($2)');
 return esc(plain);
}
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
  if(G.MKEXPGRAPH&&G.MKEXPGRAPH.target(q))return '<div class="pt-graph-answer"><strong>Question '+(i+1)+'</strong>'+G.MKEXPGRAPH.render(q,i)+'</div>';
  if(G.MKSYSTEM&&G.MKSYSTEM.target(q))return '<div class="pt-graph-answer"><strong>Question '+(i+1)+'</strong>'+G.MKSYSTEM.render(q,i)+'</div>';
  if(G.MKLINE&&G.MKLINE.target(q))return '<div class="pt-graph-answer"><strong>Question '+(i+1)+'</strong>'+G.MKLINE.render(q,i)+'</div>';
  if(G.MKPARABOLA&&G.MKPARABOLA.target(q))return '<div class="pt-graph-answer"><strong>Question '+(i+1)+'</strong>'+G.MKPARABOLA.render(q,i)+'</div>';
  if(G.MKGRAPH&&G.MKGRAPH.supports(q))return '<div class="pt-graph-answer"><strong>Question '+(i+1)+'</strong>'+G.MKGRAPH.render(q,i)+'</div>';
  if(G.MKGRAPH&&G.MKGRAPH.pointTarget(q))return '<div class="pt-graph-answer"><strong>Question '+(i+1)+'</strong>'+G.MKGRAPH.pointHTML(q,i)+'</div>';
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
 if(G.MKGRAPH){G.MKGRAPH.bind(root,state,save);G.MKGRAPH.bindPoints(root,state,save);}if(G.MKLINE)G.MKLINE.bind(root,state,save);if(G.MKSYSTEM)G.MKSYSTEM.bind(root,state,save);if(G.MKEXPGRAPH)G.MKEXPGRAPH.bind(root,state,save);if(G.MKPARABOLA)G.MKPARABOLA.bind(root,state,save);
 root.querySelector('#pt-submit').onclick=()=>submit();
 tickTimer();
}
function go(i){state.index=Math.max(0,Math.min(state.questions.length-1,i));save();show();}
function submit(forced){var missing=state.questions.filter(q=>q.response===null||q.response==='').length;if(!forced&&!confirm('Submit assessment now? '+missing+' question(s) are unanswered. '+state.questions.filter(q=>q.review).length+' marked for review.'))return;state.questions.forEach(q=>{if(q.kind==='mc')q.correct=typeof q.response==='number'&&q.response===q.choices.key;if(G.MKEXPGRAPH&&G.MKEXPGRAPH.target(q)){q.correct=G.MKEXPGRAPH.grade(q).status==='correct';}else if(G.MKSYSTEM&&G.MKSYSTEM.target(q)){q.correct=G.MKSYSTEM.grade(q).status==='correct';}else if(G.MKLINE&&G.MKLINE.target(q)){q.correct=G.MKLINE.grade(q).status==='correct';}else if(G.MKPARABOLA&&G.MKPARABOLA.target(q)){q.correct=G.MKPARABOLA.grade(q).status==='correct';}else if(G.MKGRAPH&&G.MKGRAPH.pointTarget(q)){var gg=G.MKGRAPH.pointGrade(q);q.correct=gg.status==='correct';}else if(G.MKGRAPH&&G.MKGRAPH.supports(q)){var gg=G.MKGRAPH.grade(q);q.correct=gg.status==='correct';}else if(q.kind==='auto'){var g=G.MKPRACTICE.grade(q.problem,q.response);q.correct=g.status==='correct';if(g.status==='self')q.invalidResponse='This response could not be graded automatically.';else q.invalidResponse=g.status==='invalid'?g.message:null;}if(q.kind==='self'&&(q.response===null||q.response===''))q.correct=false;q.checked=true;});state.done=true;state.finished=Date.now();save();results();}
function stats(){var buckets={};state.questions.forEach(q=>{var b=buckets[q.skill]||(buckets[q.skill]={name:q.skillName,correct:0,graded:0,missing:0});if(q.correct===null)b.missing++;else{b.graded++;if(q.correct)b.correct++;}});return Object.entries(buckets).map(([id,b])=>Object.assign({id:id},b));}
function recommendations(){
 var list=stats().filter(b=>b.graded>0).sort((a,b)=>a.correct/a.graded-b.correct/b.graded);
 if(!list.length)return 'Review your written responses to see which skills need more practice.';
 var weak=list.filter(b=>b.correct/b.graded<0.8).slice(0,3);
 if(!weak.length)return 'Strong results on the skills assessed. Try another version to confirm your understanding.';
 return 'Focus next on: '+weak.map(b=>b.name).join('; ')+'. Select Practice my weak skills for fresh questions.';
}
function results(){var qs=state.questions,graded=qs.filter(q=>q.correct!==null),good=graded.filter(q=>q.correct).length,remaining=qs.length-graded.length;root.innerHTML='<section class="pt-card"><span class="pt-eyebrow">ASSESSMENT REPORT</span><h1>Assessment Readiness Report</h1><p class="pt-score">'+(graded.length?Math.round(good/graded.length*100)+'%':'Self-review required')+'</p><p>'+good+' / '+graded.length+' graded correctly'+(remaining?' · '+remaining+' awaiting self-assessment':'')+'</p><h2>Your study plan</h2><p>'+esc(recommendations())+'</p><h2>Skills breakdown</h2>'+stats().map(b=>'<div class="pt-skillbar"><div><strong>'+esc(b.name)+'</strong><span>'+b.correct+'/'+b.graded+' graded'+(b.missing?' · '+b.missing+' unreviewed':'')+'</span></div><div class="pt-track"><div style="width:'+(b.graded?100*b.correct/b.graded:0)+'%"></div></div></div>').join('')+'<div class="pt-actions"><button id="pt-weak">Practice my weak skills</button><button id="pt-retry" class="pt-secondary">New version</button><button id="pt-print" class="pt-secondary">Print report</button><button id="pt-new" class="pt-secondary">New setup</button></div><h2>Review answers</h2>'+qs.map((q,i)=>'<details class="pt-review"><summary>Question '+(i+1)+' · '+esc(q.skillName)+' · '+(q.correct===null?'Self-check':q.correct?'Correct':'Incorrect')+'</summary>'+problemHTML(q)+'<p><strong>Your response: </strong>'+(q.kind==='mc'&&typeof q.response==='number'?fmt(q.choices.opts[q.response]):esc(q.response&&q.response.startsWith('expplot:')?'Plotted exponential function':q.response.startsWith('system:')?'Two plotted lines':q.response.startsWith('line:')?'Drawn line and shading':q.response.startsWith('parabola:')?'Five-point parabola':q.response.startsWith('graph:')?'Interactive number-line graph':q.response.startsWith('point:')?'Plotted point '+q.response.slice(6):q.response||'(blank)'))+'</p>'+feedback(q)+(q.invalidResponse?'<p class="pt-bad">'+esc(q.invalidResponse)+'</p>':'')+(q.kind==='self'?'<div class="pt-actions"><button data-self="'+i+'" data-val="yes">Correct</button><button data-self="'+i+'" data-val="no" class="pt-secondary">Needs practice</button></div>':'')+'</details>').join('')+'</section>';
 root.querySelector('#pt-weak').onclick=()=>{var weak=stats().filter(b=>(b.graded>0&&b.correct/b.graded<0.8)||b.missing>0).map(b=>b.id);if(!weak.length){alert('No weak skills identified. Try a new version!');return;}config.count=Math.min(10,Math.max(5,weak.length*3));config.minutes=0;config.mode='test';build(weak);};
 root.querySelector('#pt-retry').onclick=()=>build();root.querySelector('#pt-print').onclick=()=>{root.querySelectorAll('details.pt-review').forEach(d=>d.open=true);print();};root.querySelector('#pt-new').onclick=()=>{state=null;save();setup();};
 root.querySelectorAll('[data-self]').forEach(b=>b.onclick=()=>{qs[+b.dataset.self].correct=b.dataset.val==='yes';save();results();});
}
read();var params=new URLSearchParams((G.location.hash||'').replace(/^#/,''));var student=params.get('student')==='1';if(student&&N.skillSets[params.get('unit')]){config.unit=params.get('unit');config.level=['cp2','cp1','honors'].includes(params.get('level'))?params.get('level'):'cp1';config.count=[5,10,15,20,25].includes(+params.get('count'))?+params.get('count'):10;config.format=['mixed','mc','self'].includes(params.get('format'))?params.get('format'):'mixed';config.minutes=[0,20,30,45].includes(+params.get('minutes'))?+params.get('minutes'):0;config.skills=(params.get('skills')||'').split(',').filter(id=>N.skillSets[config.unit].byId[id]);if(!config.skills.length)config.skills=N.skillSets[config.unit].skills.map(x=>x.id);state=null;}config.mode='test';if(state&&!state.done){state.mode='test';save();}var requested=/unit=([a-z0-9-]+)/.exec(G.location.hash||'');if(requested&&N.skillSets[requested[1]]&&(!state||state.done)){config.unit=requested[1];config.skills=N.skillSets[config.unit].skills.map(s=>s.id);state=null;}
if(!N.skillSets[config.unit])config.unit=units()[0][0];
if(state&&!state.done){root.innerHTML='<section class="pt-card"><h1>Continue your practice test?</h1><p>Your previous assessment is saved in this browser.</p><div class="pt-actions"><button id="resume">Resume test</button><button id="fresh" class="pt-secondary">Start fresh</button></div></section>';root.querySelector('#resume').onclick=show;root.querySelector('#fresh').onclick=()=>{state=null;save();setup();};}
else if(state&&state.done)results();else setup();
})(window);