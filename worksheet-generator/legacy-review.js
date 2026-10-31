(function(root){'use strict';
var doc=root.document,$=function(id){return doc.getElementById(id)};
var entries=root.MK_LEGACY_CROSSWALK_AUDIT.inspect(root.MK_SKILL_CROSSWALK,root.MKMENU);
var current=[],notes={},stageIndex=0,stageCorrect=0;
function node(tag,parent,content,className){var n=doc.createElement(tag);if(content!==undefined&&content!==null)n.textContent=String(content);if(className)n.className=className;if(parent)parent.appendChild(n);return n;}
function relevant(){return entries.filter(function(e){return e.targets.some(function(t){return t&&t.courseId===$('reviewCourse').value;});});}
function refreshTopics(){
 var previous=$('reviewTopic').value,select=$('reviewTopic');select.replaceChildren();
 relevant().forEach(function(e){var o=node('option',select,e.key.replace(/-/g,' '));o.value=e.key;});
 if(relevant().some(function(e){return e.key===previous}))select.value=previous;
}
function addFinding(parent,q){
 var row=node('div',parent,null,'controls');
 var label=node('label',row,'Review status');
 var select=node('select',label);
 [['unreviewed','Not reviewed'],['appropriate','Appropriate for this course'],['revise','Needs revision'],['exclude','Exclude from reuse']].forEach(function(pair){var o=node('option',select,pair[1]);o.value=pair[0];});
 var noteLabel=node('label',row,'Reviewer notes');
 var input=node('input',noteLabel);input.placeholder='Math errors, complexity, diagrams, etc.';
 var existing=notes[q.reviewKey]||{};select.value=existing.status||'unreviewed';input.value=existing.note||'';
 function update(){notes[q.reviewKey]={status:select.value,note:input.value};}
 select.addEventListener('change',update);input.addEventListener('input',update);
}
function render(){
 $('reviewList').replaceChildren();current.forEach(function(q,i){
 var article=node('article',$('reviewList'),null,'review-card');
 node('h2',article,'Question '+(i+1)+' · '+q.topic+' · tier '+q.tier);
 node('p',article,q.prompt,'prompt');
 if(q.partPrompt)node('p',article,q.partPrompt);
 if(q.figure)node('p',article,'Diagram-dependent question: inspect the original figure in the source generator. A text-only preview is insufficient.','muted');
 var details=node('details',article);node('summary',details,'View answer, options and worked steps');
 node('p',details,'Answer: '+q.answer,'answer');
 var list=node('ol',details);q.options.forEach(function(o){node('li',list,o.text+(o.correct?' ✓':''));});
 node('pre',details,JSON.stringify(q.steps,null,2));
 addFinding(article,q);
 });$('reviewExport').hidden=!current.length;
}
function stageRender(){
 var area=$('stagePanel');if(!area)return;area.replaceChildren();
 if(!current.length){area.hidden=true;return;}area.hidden=false;
 node('h2',area,'Private practice simulation — NOT approved');
 node('p',area,'Answer only in this developer preview. These questions are not available to students.','muted');
 var q=current[stageIndex];node('p',area,'Question '+(stageIndex+1)+' of '+current.length+' · Correct '+stageCorrect);
 node('p',area,q.prompt,'prompt');if(q.partPrompt)node('p',area,q.partPrompt);
 if(q.figure){node('p',area,'Diagram-required question: cannot safely simulate without its rendered diagram.','muted');}
 else {var choices=node('div',area,null,'controls');q.options.forEach(function(o){
 var b=node('button',choices,o.text);b.type='button';b.addEventListener('click',function(){
  if(o.correct)stageCorrect++;node('p',area,o.correct?'Correct.':'Incorrect. Correct answer: '+q.answer);
  Array.prototype.forEach.call(choices.querySelectorAll('button'),function(x){x.disabled=true;});
 });});}
 var next=node('button',area,stageIndex===current.length-1?'Restart practice':'Next question');next.type='button';next.addEventListener('click',function(){if(stageIndex===current.length-1){stageIndex=0;stageCorrect=0;}else stageIndex++;stageRender();});
}
function load(){
 var entry=entries.filter(function(e){return e.key===$('reviewTopic').value})[0];
 if(!entry){$('reviewStatus').textContent='No mapped skills for this course.';current=[];render();return;}
 var result=root.MK_LEGACY_REVIEW_SAMPLES.sample(entry,$('reviewCourse').value,$('reviewLevel').value,'manual-review',Number($('reviewCount').value));
 current=result.questions;stageIndex=0;stageCorrect=0;render();stageRender();
 $('reviewStatus').textContent=result.ready?current.length+' generated samples. These are NOT approved.':'Unavailable: '+result.reason;
}
$('reviewCourse').addEventListener('change',function(){refreshTopics();load();});
$('reviewTopic').addEventListener('change',load);$('reviewLevel').addEventListener('change',load);
$('reviewLoad').addEventListener('click',load);
function reviewData(){return {schemaVersion:1,type:'legacy-question-review',approved:false,courseId:$('reviewCourse').value,topic:$('reviewTopic').value,level:$('reviewLevel').value,results:current.map(function(q){return {sourceId:q.sourceId,reviewKey:q.reviewKey,tier:q.tier,review:notes[q.reviewKey]||{status:'unreviewed',note:''}};})};}
$('stageCheck').addEventListener('click',function(){
 var result=root.MK_BROWSER_STAGE_REVIEW.evaluate(reviewData(),$('reviewerName').value,$('stageConfirm').checked);
 $('stageStatus').textContent=result.eligibleForStaging?'Eligible for staging review only. No production access enabled.':result.issues.join('; ');
});
$('reviewExport').addEventListener('click',function(){
 var exportData=reviewData();
 var blob=new Blob([JSON.stringify(exportData,null,2)],{type:'application/json'});
 var url=URL.createObjectURL(blob),a=node('a',doc.body);a.href=url;a.download='legacy-reuse-review.json';a.click();a.remove();root.setTimeout(function(){URL.revokeObjectURL(url);},1000);
});
refreshTopics();load();
})(window);
