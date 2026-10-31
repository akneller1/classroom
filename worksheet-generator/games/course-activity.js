/* Established Algebra 1 activity formats, fed only by existing course content. */
(async function(G){'use strict';
await G.MK_ALGEBRA2_NATIVE_READY;
const source=G.MK_COURSE_ACTIVITY_SOURCE,p=new URLSearchParams(location.search),escape=p.get('game')==='escape-room',kind=escape?'Escape Room':'Detective';
const app=document.getElementById('app');document.title=(source.unit?.name||'Classroom')+' '+kind;
if(!source.unit){app.textContent='Select a valid course and unit.';return}
const all=source.records();let ids=all.map(s=>s.id);
function el(tag,host,text){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;host.appendChild(n);return n}
function setup(selected){
 ids=selected;app.replaceChildren();el('h1',app,source.unit.name+' '+kind);
 const label=el('label',app,'Difficulty '),level=el('select',label);level.id='activityLevel';level.className='gm-sel';for(const [v,t] of [['cp2','CP2'],['cp1','CP1'],['honors','Honors']]){const o=el('option',level,t);o.value=v}level.value='cp1';
 el('p',app,escape?'Five rooms, interactive locks, a cipher, hints, key cards, and a final password. Work as a team: ten minutes, with a 30-second penalty for incorrect submissions.':'Solve problems to collect evidence. Clear suspects, locations, and methods, then make your final accusation.');
 const start=el('button',app,'Start '+kind);start.id='activityStart';start.className='gm-btn primary';const status=el('p',app);status.id='activityStatus';status.setAttribute('role','status');
 start.onclick=async()=>{const qs=source.select(level.value,ids,G.MK_QUESTION_BANKS.available(source.courseId,source.unit.id)?120:20);const mc=qs.filter(q=>q.format==='multiple-choice');if((escape?qs.length:mc.length)<(escape?5:10)){status.textContent=qs.length?'Choose more skills at this difficulty to fill this activity.':'Questions are not available for this course and unit yet. The activity settings are ready for a future bank.';return}start.disabled=true;try{if(escape)await startEscape(qs);else await startMystery(mc,level.value)}catch(e){status.textContent='Unable to open activity: '+e.message;start.disabled=false}};
 if(!['algebra','geometry'].includes(source.courseId)&&!G.MK_QUESTION_BANKS.available(source.courseId,source.unit.id))status.textContent='Questions are not available for this course and unit yet. The activity settings are ready for a future bank.';
}
function loadCSS(path){const l=el('link',document.head);l.rel='stylesheet';l.href=path+'?v=class-parity-20261031'}
function script(path){return new Promise((resolve,reject)=>{const s=el('script',document.body);s.src=path+'?v=class-parity-20261031';s.onload=resolve;s.onerror=()=>reject(Error('Activity engine unavailable'))})}
async function startMystery(qs,level){
 const data=await fetch('games/mystery-case.json',{cache:'no-store'}).then(r=>r.json());data.unit=source.courseId+'-'+source.unit.id+'-'+level;data.eyebrow=source.course.name+' · Detective';data.title=source.unit.name+' Detective';data.tagline='Solve each problem to earn evidence and crack the case.';data.inputHint='Choose an answer, then check it to unlock your evidence.';data.symbols=[];
 data.questions=qs.slice(0,10).map(q=>({sourceId:q.id,skill:all.find(s=>s.id===q.skillId)?.name||q.skillId,instr:'',html:source.question(q),answer:{t:'source-choice',v:q.options.findIndex(o=>o.correct)},options:q.options.map(o=>source.html(o.text)),hint:source.html(q.solutionSteps[0]||''),steps:q.solutionSteps.map(source.html)}));
 G.MK_ACTIVE_MYSTERY_CASE=data;loadCSS('games/mystery.css');app.className='';document.getElementById('activityHeader').hidden=true;await script('games/mystery-runtime.js');
}
async function startEscape(qs){
 const base=await fetch('games/escape-room.json',{cache:'no-store'}).then(r=>r.json()),used=new Set();
 function take(test){const q=qs.find(q=>!used.has(q.id)&&test(q));if(q)used.add(q.id);return q}
 function numeric(q){return /^[-+]?\d+(?:\.\d+)?$/.test(String(q.answer).trim())&&Number.isFinite(Number(q.answer))}
 function scene(q){return q.diagram?.type==='image'?{kind:'image',src:q.diagram.spec.src,alt:q.diagram.spec.alt.replace(/"/g,'&quot;')}:{kind:'emoji',bg:'#1d1530',floor:'#3a2b4a',items:[{e:'🏺',x:80,y:170,s:60},{e:'🖼️',x:170,y:150,s:56},{e:'📜',x:250,y:160,s:50},{e:'🗝️',x:330,y:170,s:50}]}}
 function prompt(q,includeOptions){return source.question(q)+(includeOptions&&q.options?'<ol type="A">'+q.options.map(o=>'<li>'+source.html(o.text)+'</li>').join('')+'</ol>':'')}
 function stage(q,i){return {name:all.find(s=>s.id===q.skillId)?.name||'Gallery '+(i+1),sourceId:q.id,stamp:[41,12,87,23,55][i],letter:['M','C','T','O','E'][i],story:'Solve the gallery challenge to unlock the next door and collect its key card.',scene:scene(q),hints:q.solutionSteps.slice(0,3).map(source.html),key:source.html(String(q.answer))}}
 function choice(q,i){return {...stage(q,i),type:'bankChoice',title:'Unlock the door',prompt:prompt(q,false),options:q.options.map(o=>source.html(o.text)),answer:q.options.findIndex(o=>o.correct)}}
 const q1=take(numeric)||take(q=>q.format==='multiple-choice');if(!q1)throw Error('This selection needs a numeric or multiple-choice lock question.');
 const first=numeric(q1)?{...stage(q1,0),type:'fields',title:'The Gallery Lock',prompt:prompt(q1,true),fields:[{label:'Answer =',answer:Number(q1.answer)}],button:'Open the door'}:choice(q1,0);
 const q2=take(q=>numeric(q)&&Number.isInteger(Number(q.answer))&&Number(q.answer)>=0&&Number(q.answer)<=25)||take(q=>q.format==='multiple-choice');if(!q2)throw Error('Choose more skills for the cipher room.');
 const numberShift=numeric(q2)&&Number.isInteger(Number(q2.answer))&&Number(q2.answer)>=0&&Number(q2.answer)<=25;
 const cipher={...stage(q2,1),type:'cipher',title:'The Cipher',prompt:prompt(q2,true)+(numberShift?'<p>The answer gives the decoder shift. Calculate it, then lock it in.</p>':'<p>Solve the question and lock your answer, then use the shift on the key card: <b>7</b>.</p>'),plain:'THE NEXT KEY IS BEHIND THE PLANETS',shift:numberShift?Number(q2.answer):7,answer:'PLANETS',askLabel:'Where is the next key?',sourceChoices:numberShift?null:q2.options.map(o=>source.html(o.text)),sourceCorrect:numberShift?null:q2.options.findIndex(o=>o.correct)};
 const q3=take(q=>q.format==='multiple-choice');if(!q3)throw Error('Choose more skills for the classification room.');const classify={...stage(q3,2),type:'classify',title:'The Answer Panels',prompt:prompt(q3,false),items:['Choose the correct panel.'],options:q3.options.map(o=>source.html(o.text)),answer:[q3.options.findIndex(o=>o.correct)]};
 const q4=take(q=>q.solutionSteps.length>=2);if(!q4)throw Error('Choose more skills for the step-order room.');const order={...stage(q4,3),type:'order',title:'Put the Work in Order',prompt:prompt(q4,true),steps:q4.solutionSteps.map(source.html)};
 const q5=take(q=>numeric(q)&&Number.isInteger(Number(q.answer))&&Number(q.answer)>=0&&Number(q.answer)<=9)||take(numeric)||take(q=>q.format==='multiple-choice');if(!q5)throw Error('Choose more skills for the final lock.');
 const last=numeric(q5)?{...stage(q5,4),type:'fields',ui:Number.isInteger(Number(q5.answer))&&Number(q5.answer)>=0&&Number(q5.answer)<=9?'dial':'fields',title:'The Exit Vault',prompt:prompt(q5,true),fields:[{label:'Answer',answer:Number(q5.answer)}],button:'Turn the handle'}:choice(q5,4);
 const room={...base,id:source.courseId+'-'+source.unit.id,title:source.unit.name+' Escape Room',intro:'The museum is locked for the night. Solve five gallery challenges, collect the key cards, and open the final door before the alarms reset.',stages:[first,cipher,classify,order,last]};G.MK_ACTIVE_ESCAPE_ROOM=room;
 loadCSS('games/escape.css');const header=document.getElementById('activityHeader');header.innerHTML='<h1>'+source.unit.name+' Escape Room</h1><div id="dots"></div><div>Hints used: <b id="hu">0</b> &nbsp; <span id="clock">10:00</span></div>';
 const host=document.createElement('div');host.id='app';app.replaceWith(host);el('div',document.body).id='key';await script('games/escape-runtime.js');
}
G.TeacherSkills.choose(all,setup);
})(window).catch(e=>{document.getElementById('app').textContent='Unable to load activity: '+e.message});
