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
  var printBtn=el('button',controls,'Print approved questions');
  printBtn.type='button';printBtn.disabled=true;
  printBtn.style.cssText='padding:8px 12px;cursor:pointer';
  // Do not print or mark teacher answers as independently verified. Publication
  // approval is a content review flag, not proof from the symbolic verifier.
  printBtn.onclick=function(){
    if(!active.length)return;
    if(active.some(function(q){return !!q.diagram;})) {
      status.textContent='Printing is disabled for this selection because one or more diagrams need a faithful approved rendering. Review those diagrams before creating student copies.';
      return;
    }
    var frame=G.document.createElement('iframe');
    frame.style.cssText='position:absolute;width:0;height:0;border:0';
    frame.setAttribute('title','Approved questions print view');
    G.document.body.appendChild(frame);
    var d=frame.contentDocument;
    d.open();d.write('<!doctype html><html><head><title>Approved questions</title>'+
      '<style>body{font:12pt/1.5 Arial,sans-serif;padding:24px;color:#111}'+
      'h1{font-size:18pt}.item{break-inside:avoid;margin:18px 0 28px}'+
      '.answer{margin-top:15px;border-top:1px solid #888;padding-top:10px}'+
      '.key{break-before:page}p{white-space:pre-wrap}</style></head><body></body></html>');d.close();
    var body=d.body;
    function put(tag,parent,text){var node=d.createElement(tag);node.textContent=String(text===undefined?'':text);parent.appendChild(node);return node;}
    put('h1',body,courseSel.selectedOptions[0].textContent+' · '+unitSel.selectedOptions[0].textContent);
    put('p',body,'Approved source content · '+levelSel.selectedOptions[0].textContent+' · '+mode);
    active.forEach(function(q,i){
      var item=put('section',body,'');item.className='item';
      put('h2',item,'Question '+(i+1));
      put('p',item,q.prompt);
      if(q.diagram)put('p',item,'Diagram from approved bank requires visual review before student distribution.');
      (q.options||[]).forEach(function(o,j){put('p',item,String.fromCharCode(65+j)+'. '+o.text);});
      (q.parts||[]).forEach(function(part,j){put('p',item,String.fromCharCode(97+j)+') '+part.prompt);});
      put('p',item,'Work: __________________________________________________________');
    });
    var keySection=put('section',body,'');keySection.className='key';
    put('h1',keySection,'Teacher key (approved source answers; not independently re-verified)');
    active.forEach(function(q,i){
      var part=put('section',keySection,'');part.className='item';
      put('h2',part,'Question '+(i+1));
      put('p',part,Array.isArray(q.answer)?q.answer.join(', '):q.answer);
      (q.solutionSteps||[]).forEach(function(step){put('p',part,step);});
    });
    frame.contentWindow.focus();
    frame.contentWindow.print();
    G.setTimeout(function(){frame.remove();},5000);
  };
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
    preview.replaceChildren();printBtn.disabled=true;answers=false;key.textContent='Show teacher answers';
    var state=api.status();
    if(state.state==='loading'){status.textContent='Checking approved question banks…';return;}
    if(state.state==='error'){status.textContent='Approved question-bank loading failed. No questions were imported: '+state.error;return;}
    active=api.select(mode,{courseId:courseSel.value,unitId:unitSel.value,level:levelSel.value});
    key.disabled=!active.length;printBtn.disabled=!active.length || active.some(function(q){return !!q.diagram;});
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
