/* Non-mathematical game mechanics around unchanged, authored MC questions. */
(function(G){'use strict';
const doc=document,app=doc.getElementById('app'),params=new URLSearchParams(location.search),unit=params.get('unit'),escape=params.get('game')==='escape-room';
const records=G.MK_COURSE_CATALOG.getSkillRecords('algebra2',unit),title=escape?'Escape Room':'Detective',bank=G.MK_QUESTION_BANKS;
function el(tag,host,text){const n=doc.createElement(tag);if(text!==undefined)n.textContent=text;host.appendChild(n);return n}
function setup(ids){
 app.replaceChildren();el('h1',app,title);el('p',app,escape?'Solve five locks in ten minutes. Each incorrect answer costs 30 seconds.':'Solve five clues to eliminate five suspects. The remaining suspect solves the case.');
 const label=el('label',app,'Difficulty '),level=el('select',label);level.id='questLevel';for(const [v,t] of [['cp2','CP2'],['cp1','CP1'],['honors','Honors']]){const o=el('option',level,t);o.value=v}level.value='cp1';
 const start=el('button',app,'Start '+title);start.className='gm-btn primary';start.id='questStart';start.onclick=()=>run(ids,level.value);
}
let timer;
function run(ids,level){
 const qs=bank.select({courseId:'algebra2',unitId:unit,skillIds:ids,level,formats:['multiple-choice']});
 const shuffled=G.MKWS.rng.make(G.MKWS.rng.hash(String(Date.now()))).shuffle(qs),questions=shuffled.slice(0,5);
 if(questions.length<5){el('p',app,'Select more skills for five distinct multiple-choice questions at this difficulty.');return}
 let index=0,remaining=600,chosen=-1,solved=false,deadline=Date.now()+600000;
 app.replaceChildren();el('h1',app,title);const clock=el('p',app),progress=el('p',app),board=el('p',app),host=el('section',app);host.className='gm-panel';
 function tick(){remaining=Math.max(0,Math.ceil((deadline-Date.now())/1000));clock.textContent=escape?'Time remaining: '+Math.floor(remaining/60)+':'+String(remaining%60).padStart(2,'0'):'';if(escape&&remaining<=0){clearInterval(timer);host.replaceChildren();el('p',host,'Time is up. Start a new game to try again.');const restart=el('button',host,'New game');restart.onclick=()=>setup(ids)}}
 function render(){
  host.replaceChildren();chosen=-1;solved=false;progress.textContent=(escape?'Locks opened: ':'Clues solved: ')+index+'/5';board.textContent=escape?'':Array.from({length:6},(_,i)=>'Suspect '+String.fromCharCode(65+i)+(i<index?' — cleared':'')).join(' · ');
  if(index===5){clearInterval(timer);el('h2',host,escape?'You escaped!':'Case solved: Suspect F');const restart=el('button',host,'New game');restart.onclick=()=>setup(ids);return}
  const q=questions[index];host.dataset.sourceId=q.id;el('h2',host,(escape?'Lock ':'Clue ')+(index+1));el('p',host,q.prompt);
  if(q.diagram?.type==='image'){const img=el('img',host);img.src='../'+q.diagram.spec.src;img.alt=q.diagram.spec.alt;img.style.cssText='max-width:100%;max-height:280px'}
  const buttons=q.options.map((o,i)=>{const b=el('button',host,o.text);b.className='gm-btn';b.onclick=()=>{chosen=i;buttons.forEach((x,j)=>x.setAttribute('aria-pressed',String(j===i)));lock.disabled=false};return b});
  const lock=el('button',host,'Lock in answer');lock.id='questLock';lock.className='gm-btn primary';lock.disabled=true;const feedback=el('p',host);feedback.setAttribute('role','status');
  lock.onclick=()=>{
   if(solved||chosen<0)return;
   if(!q.options[chosen].correct){if(escape){deadline-=30000;tick()}feedback.textContent=escape?'Incorrect. 30-second penalty. Try again.':'That clue does not clear a suspect. Try again.';return}
   solved=true;buttons.forEach(b=>b.disabled=true);lock.disabled=true;feedback.textContent='Correct.';const steps=el('ol',host);q.solutionSteps.forEach(s=>el('li',steps,s));const next=el('button',host,'Continue');next.className='gm-btn primary';next.onclick=()=>{index++;render()};
  };
 }
 tick();if(escape)timer=setInterval(tick,1000);render();
}
G.TeacherSkills.choose(records.map(s=>({id:s.id,name:s.name})),setup);
})(window);
