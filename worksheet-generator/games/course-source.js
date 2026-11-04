/* Course-neutral access to existing content. Empty banks remain empty. */
(function(G){'use strict';
const p=new URLSearchParams(location.search),courseId=p.get('course')||'algebra2';
const course=G.LIBRARY.courses.find(c=>c.id===courseId),unit=course?.units.find(u=>u.id===p.get('unit'))||course?.units[0];
const aliases={algebra:{'foundations-algebra':'foundations','exponents-exponential-functions':'exponents-scientific-notation','polynomials-factoring':'polynomials'},geometry:{'foundations-geometry':'basics-reasoning','triangle-congruence':'triangles-congruence'}};
const setId=(courseId==='algebra'?'algebra1-':courseId+'-')+(aliases[courseId]?.[unit?.id]||unit?.id),set=G.MKMENU.skillSets[setId];
function records(){return G.MK_QUESTION_BANKS.available(courseId,unit?.id)?G.MK_COURSE_CATALOG.getSkillRecords(courseId,unit.id):(set?set.skills.map(s=>({id:s.id,name:s.name})):G.MK_COURSE_CATALOG.getSkillRecords(courseId,unit?.id))}
// Convert a verified graph-key answer into visual multiple-choice panels.
// The same boundary geometry is used for the correct graph and each misconception.
function graphOptions(item){
 const key=item.p?.parts?.[0]?.answerFig;
 if(item.p?.parts?.[0]?.check?.type!=='graph-key'||!key?.halfplanes?.length)return null;
 const clone=()=>JSON.parse(JSON.stringify(key));
 const figures=[clone(),clone(),clone(),clone()];
 function reverseShade(f,i){
   const h=f.halfplanes[i],a=h.a,b=h.b,side=h.side;
   // Reflect the side marker across its actual boundary line (works for any slope).
   const dx=b[0]-a[0],dy=b[1]-a[1],den=dx*dx+dy*dy;
   if(!den)return;
   const t=((side[0]-a[0])*dx+(side[1]-a[1])*dy)/den;
   const px=a[0]+t*dx,py=a[1]+t*dy;
   h.side=[2*px-side[0],2*py-side[1]];
 }
 reverseShade(figures[1],0);
 figures[2].halfplanes[0].dashed=!figures[2].halfplanes[0].dashed;
 if(key.halfplanes.length>1)reverseShade(figures[3],1);
 else {reverseShade(figures[3],0);figures[3].halfplanes[0].dashed=!figures[3].halfplanes[0].dashed;}
 const offset=Math.floor(Math.random()*4);
 return figures.slice(offset).concat(figures.slice(0,offset)).map((fig,i)=>({
   html:G.MKMENU.figHtml(fig),
   correct:i===(4-offset)%4
 }));
}
function select(level,ids,n){
 if(G.MK_QUESTION_BANKS.available(courseId,unit?.id)){
  const groups=ids.map(id=>G.MK_QUESTION_BANKS.select({courseId,unitId:unit.id,skillIds:[id],level,formats:['multiple-choice','short-answer']}));
  const rng=G.MKWS.rng.make(G.MKWS.rng.hash(String(Date.now())));groups.forEach((g,i)=>groups[i]=rng.shuffle(g));const out=[];
  while(out.length<n&&groups.some(g=>g.length))for(const g of groups)if(g.length&&out.length<n)out.push(g.pop());return out;
 }
 if(!['algebra','geometry'].includes(courseId)||!set)return [];
 const used={keys:new Set(),sigs:new Set()},out=[];for(let i=0;i<n*6&&out.length<n;i++){
  const c=G.MKGAMES.LEVELS[level].tiers[i%3],id=ids[i%ids.length];
  const it=G.MKGAMES.makeItems(setId,id,c,{level,intOnly:level!=='honors'},'course-game-'+Date.now()+'-'+i,used)[0];if(!it)continue;
  const visual=graphOptions(it);
  const prompt=visual?String(it.q.prompt||'').replace(/^Graph the solution to the system:/,'Which graph shows the solution to the system:').replace(/^Graph /,'Which graph represents ') : [it.q.prompt,it.q.ask].filter(Boolean).join(' ');
  out.push({id:it.id,skillId:id,prompt,answer:it.answer,format:'multiple-choice',
   options:visual?visual.map((o,i)=>({text:'Graph '+String.fromCharCode(65+i),correct:o.correct})):it.options.map(o=>({text:o.a,correct:o.ok})),
   solutionSteps:it.steps.map(s=>[s.t,s.m?'⟨'+s.m+'⟩':''].filter(Boolean).join(' ')),
   _figure:visual?null:it.q.fig,_graphOptions:visual?visual.map(o=>o.html):null});
 }return out;
}
function html(t){return G.MK_MATH_DISPLAY.html(t)}
function question(q){let h='<div class="prompt">'+html(q.prompt)+'</div>';if(q.diagram?.type==='image')h+='<img style="max-width:100%;max-height:280px" src="../'+q.diagram.spec.src+'" alt="'+String(q.diagram.spec.alt).replace(/"/g,'&quot;')+'">';else if(q._figure)h+=G.MKMENU.figHtml(q._figure);return h}
G.MK_COURSE_ACTIVITY_SOURCE={course,unit,courseId,get setId(){return G.MK_QUESTION_BANKS.available(courseId,unit?.id)?(courseId==='algebra'?'algebra1-':courseId+'-')+unit.id:setId},records,select,html,question};
})(window);
