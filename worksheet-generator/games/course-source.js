/* Course-neutral access to existing content. Empty banks remain empty. */
(function(G){'use strict';
const p=new URLSearchParams(location.search),courseId=p.get('course')||'algebra2';
const course=G.LIBRARY.courses.find(c=>c.id===courseId),unit=course?.units.find(u=>u.id===p.get('unit'))||course?.units[0];
const aliases={algebra:{'foundations-algebra':'foundations','exponents-exponential-functions':'exponents-scientific-notation','polynomials-factoring':'polynomials'},geometry:{'foundations-geometry':'basics-reasoning','triangle-congruence':'triangles-congruence'}};
const setId=(courseId==='algebra'?'algebra1-':courseId+'-')+(aliases[courseId]?.[unit?.id]||unit?.id),set=G.MKMENU.skillSets[setId];
function records(){return G.MK_QUESTION_BANKS.available(courseId,unit?.id)?G.MK_COURSE_CATALOG.getSkillRecords(courseId,unit.id):(set?set.skills.map(s=>({id:s.id,name:s.name})):G.MK_COURSE_CATALOG.getSkillRecords(courseId,unit?.id))}
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
  out.push({id:it.id,skillId:id,prompt:[it.q.prompt,it.q.ask].filter(Boolean).join(' '),answer:it.answer,format:'multiple-choice',options:it.options.map(o=>({text:o.a,correct:o.ok})),solutionSteps:it.steps.map(s=>[s.t,s.m?'⟨'+s.m+'⟩':''].filter(Boolean).join(' ')),_figure:it.q.fig});
 }return out;
}
function html(t){return G.MK_MATH_DISPLAY.html(t)}
function question(q){let h='<div class="prompt">'+html(q.prompt)+'</div>';if(q.diagram?.type==='image')h+='<img style="max-width:100%;max-height:280px" src="../'+q.diagram.spec.src+'" alt="'+String(q.diagram.spec.alt).replace(/"/g,'&quot;')+'">';else if(q._figure)h+=G.MKMENU.figHtml(q._figure);return h}
G.MK_COURSE_ACTIVITY_SOURCE={course,unit,courseId,get setId(){return G.MK_QUESTION_BANKS.available(courseId,unit?.id)?(courseId==='algebra'?'algebra1-':courseId+'-')+unit.id:setId},records,select,html,question};
})(window);
