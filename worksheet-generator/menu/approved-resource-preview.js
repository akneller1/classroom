/* Approved Claude bank preview inside the existing worksheet and assessment pages.
 * Isolated from verified procedural generation; no fabricated math/checks.
 */
(function (G) {
  'use strict';
  var api=G.MK_APPROVED_RESOURCE_BANKS, catalog=G.MK_COURSE_CATALOG, library=G.LIBRARY;
  if (!api || !catalog || !library) return;
  var mode=G.document.body.getAttribute('data-mode')==='worksheet'?'worksheet':'assessment';
  var grades=['math6','prealgebra7','prealgebra'];
  var courses=library.courses.filter(function(c){return grades.indexOf(c.id)>=0;});
  if (!courses.length) return;
  var container=G.document.createElement('section');
  container.className='card';
  container.id='approvedGradeResources';
  container.style.cssText='padding:18px;margin:16px auto;max-width:1100px';
  var main=G.document.getElementById('mmMain');
  if (main) main.parentNode.insertBefore(container,main);
  function el(tag,parent,value) {
    var e=G.document.createElement(tag);if(value!==undefined)e.textContent=String(value);
    if(parent)parent.appendChild(e);return e;
  }
  var heading=el('h2',container,'Approved Grades 6–8 '+(mode==='worksheet'?'Worksheet':'Assessment')+' Questions');
  heading.style.margin='0 0 8px';
  el('p',container,'Preview approved Claude-authored questions. These are separate from the procedural generator until a compatible native problem format is available.');
  var controls=el('div',container);
  controls.style.cssText='display:flex;flex-wrap:wrap;gap:12px;align-items:end';
  function select(label) {
    var wrap=el('label',controls,label);wrap.style.cssText='display:grid;gap:5px;font-weight:600';
    var sel=el('select',wrap);sel.style.cssText='padding:8px;border-radius:6px';return sel;
  }
  var courseSel=select('Course'),unitSel=select('Unit'),levelSel=select('Level');
  courses.forEach(function(c){var o=el('option',courseSel,c.name);o.value=c.id;});
  [['cp2','Remedial'],['cp1','Standard'],['honors','Advanced']].forEach(function(x){
    var o=el('option',levelSel,x[1]);o.value=x[0];
  });levelSel.value='cp1';
  var status=el('p',container,'Checking approved question banks…');
  status.setAttribute('role','status');
  var preview=el('div',container);preview.id='approvedGradePreview';
  var key=el('button',controls,'Show teacher answers');key.type='button';key.disabled=true;
  key.style.cssText='padding:8px 12px;cursor:pointer';
  var answers=false,active=[];
  function refreshUnits(){
    unitSel.replaceChildren();
    var course=courses.find(function(c){return c.id===courseSel.value;});
    (course?course.units:[]).forEach(function(u){var o=el('option',unitSel,u.name);o.value=u.id;});
    show();
  }
  function show(){
    preview.replaceChildren();answers=false;key.textContent='Show teacher answers';
    var state=api.status();
    if(state.state==='loading'){status.textContent='Checking approved question banks…';return;}
    if(state.state==='error'){status.textContent='Approved question-bank loading failed. No questions were imported: '+state.error;return;}
    active=api.select(mode,{courseId:courseSel.value,unitId:unitSel.value,level:levelSel.value});
    key.disabled=!active.length;
    if(!active.length){
      status.textContent='No approved '+levelSel.selectedOptions[0].textContent.toLowerCase()+' questions for this unit. No substitute questions will be generated.';
      return;
    }
    status.textContent=active.length+' approved question(s) available. Preview only; not yet inserted into the native generator.';
    active.forEach(function(q,i){
      var item=el('article',preview);item.style.cssText='border-top:1px solid #ddd;margin-top:14px;padding:14px 0';
      el('strong',item,'Question '+(i+1));el('p',item,q.prompt);
      if(q.diagram)el('p',item,'Diagram attached ('+q.diagram.type+'); inspect the original approved source for correct rendering.');
      if(Array.isArray(q.options))q.options.forEach(function(opt,j){el('p',item,String.fromCharCode(65+j)+'. '+opt.text);});
      if(Array.isArray(q.parts))q.parts.forEach(function(part,j){el('p',item,String.fromCharCode(97+j)+') '+part.prompt);});
      var solution=el('div',item);solution.className='approved-answer';solution.hidden=!answers;
      el('strong',solution,'Teacher answer');
      el('p',solution,Array.isArray(q.answer)?q.answer.join(', '):q.answer);
      (q.solutionSteps||[]).forEach(function(line){el('p',solution,line);});
    });
  }
  key.onclick=function(){answers=!answers;key.textContent=answers?'Hide teacher answers':'Show teacher answers';Array.from(preview.querySelectorAll('.approved-answer')).forEach(function(e){e.hidden=!answers;});};
  courseSel.onchange=refreshUnits;unitSel.onchange=show;levelSel.onchange=show;
  refreshUnits();
  api.ready.then(show);
})(window);
