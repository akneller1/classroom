/* Interactive Practice Test — shares the menu generator's independently checked questions. */
(function(G){
'use strict';
var N=G.MKMENU, W=G.MKWS, root=document.getElementById('practice'), STORE='mk-practice-v1';
var state=null,config={unit:'algebra1-expressions-equations',level:'cp1',count:10,mode:'test',format:'mixed',skills:[]};
var esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
var fmt=s=>N.mathSafe(String(s||''));
var levels={cp2:2,cp1:4,honors:6};
function save(){try{localStorage.setItem(STORE,JSON.stringify({state:state,config:config}));}catch(e){}}
function read(){try{var d=JSON.parse(localStorage.getItem(STORE)||'null');if(d&&d.config){config=d.config;state=d.state||null;}}catch(e){}}
function units(){return N.CATALOG[0].units.filter(u=>N.skillSets[u[0]]);}
function chosen(){return N.skillSets[config.unit];}
function skills(){return chosen().skills.filter(s=>config.skills.indexOf(s.id)!==-1);}
function controls(){return '<section class="pt-card"><span class="pt-eyebrow">ALGEBRA 1 · STUDY GUIDES</span><h1>Interactive Practice Test</h1><p>Generate a fresh assessment from the same verified problem bank as our worksheet and menu assessment generators.</p><div class="pt-fields"><label>Unit<select id="pt-unit">'+units().map(u=>'<option value="'+esc(u[0])+'" '+(config.unit===u[0]?'selected':'')+'>'+esc(u[1])+'</option>').join('')+'</select></label><label>Level<select id="pt-level">'+['cp2','cp1','honors'].map(l=>'<option value="'+l+'" '+(config.level===l?'selected':'')+'>'+l.toUpperCase()+'</option>').join('')+'</select></label><label>Questions<select id="pt-count">'+[5,10,15,20,25].map(n=>'<option '+(config.count===n?'selected':'')+'>'+n+'</option>').join('')+'</select></label><label>Mode<select id="pt-mode"><option value="test" '+(config.mode==='test'?'selected':'')+'>Test — feedback at end</option><option value="practice" '+(config.mode==='practice'?'selected':'')+'>Practice — instant feedback</option></select></label><label>Format<select id="pt-format"><option value="mixed" '+(config.format==='mixed'?'selected':'')+'>Mixed</option><option value="mc" '+(config.format==='mc'?'selected':'')+'>Multiple choice</option><option value="self" '+(config.format==='self'?'selected':'')+'>Short answer / auto-check where supported</option></select></label></div><h2>Choose skills</h2><div class="pt-skills">'+chosen().skills.map(s=>'<label><input type="checkbox" data-skill="'+esc(s.id)+'" '+(config.skills.includes(s.id)?'checked':'')+'> '+esc(s.name)+'</label>').join('')+'</div><div class="pt-actions"><button id="pt-all" class="pt-secondary">Select all</button><button id="pt-build">Generate practice test</button></div><p class="pt-muted">Results stay on this device. Numeric answers and supported inequalities are graded exactly; complex written responses use self-check.</p></section>';}
function setup(){if(state&&!state.done){root.innerHTML='<section class="pt-card"><h1>Assessment saved</h1><p>Your unfinished assessment is saved in this browser.</p><div class="pt-actions"><button id="pt-resume">Resume assessment</button><button id="pt-discard" class="pt-secondary">Discard and create new</button></div></section>';root.querySelector('#pt-resume').onclick=show;root.querySelector('#pt-discard').onclick=()=>{if(confirm('Discard your saved assessment?')){state=null;save();setup();}};return;}if(!N.skillSets[config.unit])config.unit=units()[0][0];root.innerHTML=controls();root.querySelector('#pt-unit').onchange=e=>{config.unit=e.target.value;config.skills=chosen().skills.map(s=>s.id);save();setup();};['level','count','mode','format'].forEach(f=>root.querySelector('#pt-'+f).onchange=e=>{config[f]=f==='count'?+e.target.value:e.target.value;save();});root.querySelectorAll('[data-skill]').forEach(x=>x.onchange=()=>{config.skills=Array.from(root.querySelectorAll('[data-skill]:checked')).map(el=>el.dataset.skill);save();});root.querySelector('#pt-all').onclick=()=>{config.skills=chosen().skills.map(s=>s.id);save();setup();};root.querySelector('#pt-build').onclick=()=>build();}
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
 if(!skills().length&&!(overrides&&overrides.length)){alert('Select at least one skill.');return;}
 var selected=overrides&&overrides.length?chosen().skills.filter(s=>overrides.includes(s.id)):skills();
 if(!selected.length){alert('No supported skill is selected.');return;}
 var seed=Date.now()+Math.floor(Math.random()*1000000),used={keys:new Set(),sigs:new Set()},questions=[],failures=0;
 for(var i=0;i<config.count;i++){
   var q=null;
   for(var k=0;k<selected.length*3&&!q;k++)q=makeQuestion(selected[(i+k)%selected.length],seed+i*1009+k,i,used);
   if(q)questions.push(q);else failures++;
 }
 if(!questions.length){alert('No verified problems could be generated for these skills and requested format. Choose other skills or another format.');return;}
 if(failures){alert('Generated '+questions.length+' verified questions. '+failures+' question slots could not be filled with the selected skills and format.');}
 state={questions:questions,index:0,done:false,started:Date.now(),generationErrors:failures,mode:config.mode};save();show();
}
function problemHTML(q){var p=q.problem;return '<div class="pt-problem">'+fmt(p.prompt)+(p.fig&&N.figHtml?N.figHtml(p.fig):'')+(p.parts||[]).map((part,i)=>part.prompt?'<div class="pt-part">'+(part.label?esc(part.label)+' ':'')+fmt(part.prompt)+'</div>':'').join('')+'</div>';}
function feedback(q){var p=q.problem,part=p.parts[0];var lines=(p.steps||[]).map(x=>'<li>'+(x.t?fmt(x.t):'')+(x.m?'<div>'+fmt(x.m)+'</div>':'')+'</li>').join('');return '<div class="pt-explain"><strong>Answer:</strong> '+(p.parts||[]).map(x=>fmt(x.answer)).join(' · ')+(lines?'<h3>Worked solution</h3><ol>'+lines+'</ol>':'<p>Compare your process with the verified answer above.</p>')+(p.parts||[]).map(x=>x.answerFig&&N.figHtml?N.figHtml(x.answerFig):'').join('')+'</div>';}
function item(q,i){var answered=q.response!==null&&q.response!=='';var visible=state.done||state.mode==='practice'&&q.checked;return '<section class="pt-card"><div class="pt-top"><span class="pt-eyebrow">'+esc(q.skillName)+'</span><strong>Question '+(i+1)+' of '+state.questions.length+'</strong></div>'+problemHTML(q)+(q.kind==='mc'?'<div class="pt-options">'+q.choices.opts.map((v,j)=>'<label class="pt-option"><input type="radio" name="pt-answer" value="'+j+'" '+(+q.response===j&&answered?'checked':'')+' '+(visible?'disabled':'')+'> '+fmt(v)+'</label>').join('')+'</div>':'<label class="pt-response">Show your work and enter your response<textarea id="pt-written" rows="4" '+(visible?'disabled':'')+' placeholder="Explain your solution...">'+esc(q.response||'')+'</textarea></label>')+(visible?'<div class="pt-status '+(q.correct===true?'pt-good':q.correct===false?'pt-bad':'')+'">'+(q.correct===true?'Correct':q.correct===false?'Needs review':'Compare your work')+'</div>'+feedback(q)+(q.kind==='self'&&q.correct===null?'<div class="pt-actions"><button data-grade="yes">My work is correct</button><button data-grade="no" class="pt-secondary">I need more practice</button></div>':''):'')+'</section>';}
function show(){
 if(!state){setup();return;}
 if(state.done){results();return;}
 var i=state.index,q=state.questions[i],locked=state.mode==='practice'&&q.checked;
 root.innerHTML='<section class="pt-header"><div><span class="pt-eyebrow">'+esc(chosen().unitName||'Algebra 1')+'</span><h1>'+(state.mode==='test'?'Practice Test':'Guided Practice')+'</h1></div><button id="pt-exit" class="pt-secondary">Save & exit</button></section><div class="pt-progress"><div style="width:'+Math.round(100*(i+1)/state.questions.length)+'%"></div></div><nav class="pt-nav" aria-label="Questions">'+state.questions.map((x,j)=>'<button class="'+(j===i?'active ':'')+(x.response!==null?'answered':'')+'" data-jump="'+j+'">'+(j+1)+(x.review?' ★':'')+'</button>').join('')+'</nav>'+item(q,i)+'<div class="pt-actions"><button id="pt-prev" class="pt-secondary" '+(!i?'disabled':'')+'>Previous</button><button id="pt-mark" class="pt-secondary">'+(q.review?'Unmark':'Mark for review')+'</button>'+(state.mode==='practice'&&!locked?'<button id="pt-check">Check answer</button>':'')+'<button id="pt-next">'+(i===state.questions.length-1?'Submit test':'Next →')+'</button></div><p class="pt-muted">'+state.questions.filter(x=>x.response!==null).length+' answered of '+state.questions.length+' · '+state.questions.filter(x=>x.review).length+' marked for review</p>';
 root.querySelectorAll('[data-jump]').forEach(b=>b.onclick=()=>go(+b.dataset.jump));
 root.querySelectorAll('input[name="pt-answer"]').forEach(e=>e.onchange=()=>{q.response=+e.value;save();});
 var t=root.querySelector('#pt-written');if(t)t.oninput=e=>{q.response=e.target.value;save();};
 root.querySelector('#pt-prev').onclick=()=>go(i-1);root.querySelector('#pt-next').onclick=()=>i===state.questions.length-1?submit():go(i+1);
 root.querySelector('#pt-mark').onclick=()=>{q.review=!q.review;save();show();};
 root.querySelector('#pt-exit').onclick=()=>{state.paused=true;save();setup();};
 var check=root.querySelector('#pt-check');if(check)check.onclick=()=>{if(q.response===null||q.response===''){alert('Enter an answer first.');return;}if(q.kind==='auto'){var result=G.MKPRACTICE.grade(q.problem,q.response);if(result.status==='invalid'||result.status==='empty'){alert(result.message||'Enter your answer.');return;}if(result.status==='self'){q.kind='self';q.correct=null;}else q.correct=result.status==='correct';}q.checked=true;if(q.kind==='mc')q.correct=q.response===q.choices.key;save();show();};
 root.querySelectorAll('[data-grade]').forEach(b=>b.onclick=()=>{q.correct=b.dataset.grade==='yes';save();show();});
}
function go(i){state.index=Math.max(0,Math.min(state.questions.length-1,i));save();show();}
function submit(){var missing=state.questions.filter(q=>q.response===null||q.response==='').length;if(missing&&!confirm(missing+' unanswered questions. Submit anyway?'))return;state.questions.forEach(q=>{if(q.kind==='mc')q.correct=q.response===null?false:q.response===q.choices.key;if(q.kind==='auto'){var g=G.MKPRACTICE.grade(q.problem,q.response);q.correct=g.status==='correct'?true:g.status==='incorrect'?false:null;if(g.status==='self')q.kind='self';q.invalidResponse=g.status==='invalid'?g.message:null;}if(q.kind==='self'&&(q.response===null||q.response===''))q.correct=false;q.checked=true;});state.done=true;state.finished=Date.now();save();results();}
function stats(){var buckets={};state.questions.forEach(q=>{var b=buckets[q.skill]||(buckets[q.skill]={name:q.skillName,correct:0,graded:0,missing:0});if(q.correct===null)b.missing++;else{b.graded++;if(q.correct)b.correct++;}});return Object.entries(buckets).map(([id,b])=>Object.assign({id:id},b));}
function recommendations(){
 var list=stats().filter(b=>b.graded>0).sort((a,b)=>a.correct/a.graded-b.correct/b.graded);
 if(!list.length)return 'Review your written responses to see which skills need more practice.';
 var weak=list.filter(b=>b.correct/b.graded<0.8).slice(0,3);
 if(!weak.length)return 'Strong results on the skills assessed. Try another version to confirm your understanding.';
 return 'Focus next on: '+weak.map(b=>b.name).join('; ')+'. Select Practice my weak skills for fresh questions.';
}
function results(){var qs=state.questions,graded=qs.filter(q=>q.correct!==null),good=graded.filter(q=>q.correct).length,remaining=qs.length-graded.length;root.innerHTML='<section class="pt-card"><span class="pt-eyebrow">ASSESSMENT REPORT</span><h1>Test Readiness</h1><p class="pt-score">'+(graded.length?Math.round(good/graded.length*100)+'%':'Self-review required')+'</p><p>'+good+' / '+graded.length+' graded correctly'+(remaining?' · '+remaining+' awaiting self-assessment':'')+'</p><h2>Recommended next step</h2><p>'+esc(recommendations())+'</p><h2>Skills breakdown</h2>'+stats().map(b=>'<div class="pt-skillbar"><div><strong>'+esc(b.name)+'</strong><span>'+b.correct+'/'+b.graded+' graded'+(b.missing?' · '+b.missing+' unreviewed':'')+'</span></div><div class="pt-track"><div style="width:'+(b.graded?100*b.correct/b.graded:0)+'%"></div></div></div>').join('')+'<div class="pt-actions"><button id="pt-weak">Practice my weak skills</button><button id="pt-retry" class="pt-secondary">New version</button><button id="pt-print" class="pt-secondary">Print report</button><button id="pt-new" class="pt-secondary">New setup</button></div><h2>Review answers</h2>'+qs.map((q,i)=>'<details class="pt-review"><summary>Question '+(i+1)+' · '+esc(q.skillName)+' · '+(q.correct===null?'Self-check':q.correct?'Correct':'Incorrect')+'</summary>'+problemHTML(q)+'<p><strong>Your response: </strong>'+(q.kind==='mc'&&q.response!==null?fmt(q.choices.opts[q.response]):esc(q.response||'(blank)'))+'</p>'+feedback(q)+(q.invalidResponse?'<p class="pt-bad">'+esc(q.invalidResponse)+'</p>':'')+(q.kind==='self'?'<div class="pt-actions"><button data-self="'+i+'" data-val="yes">Correct</button><button data-self="'+i+'" data-val="no" class="pt-secondary">Needs practice</button></div>':'')+'</details>').join('')+'</section>';
 root.querySelector('#pt-weak').onclick=()=>{var weak=stats().filter(b=>(b.graded>0&&b.correct/b.graded<0.8)||b.missing>0).map(b=>b.id);if(!weak.length){alert('No weak skills identified. Try a new version!');return;}build(weak);};
 root.querySelector('#pt-retry').onclick=()=>build();root.querySelector('#pt-print').onclick=()=>{root.querySelectorAll('details.pt-review').forEach(d=>d.open=true);print();};root.querySelector('#pt-new').onclick=()=>{state=null;save();setup();};
 root.querySelectorAll('[data-self]').forEach(b=>b.onclick=()=>{qs[+b.dataset.self].correct=b.dataset.val==='yes';save();results();});
}
read();var requested=/unit=([a-z0-9-]+)/.exec(G.location.hash||'');if(requested&&N.skillSets[requested[1]]&&(!state||state.done)){config.unit=requested[1];config.skills=N.skillSets[config.unit].skills.map(s=>s.id);state=null;}
if(!N.skillSets[config.unit])config.unit=units()[0][0];
if(state&&!state.done){root.innerHTML='<section class="pt-card"><h1>Continue your practice test?</h1><p>Your previous assessment is saved in this browser.</p><div class="pt-actions"><button id="resume">Resume test</button><button id="fresh" class="pt-secondary">Start fresh</button></div></section>';root.querySelector('#resume').onclick=show;root.querySelector('#fresh').onclick=()=>{state=null;save();setup();};}
else if(state&&state.done)results();else setup();
})(window);