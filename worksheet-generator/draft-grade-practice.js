(function(root){'use strict';
var d=root.document, $=function(id){return d.getElementById(id)};
var entries=root.MK_LEGACY_CROSSWALK_AUDIT.inspect(root.MK_SKILL_CROSSWALK,root.MKMENU),questions=[],index=0,score=0;
function el(tag,parent,text){var e=d.createElement(tag);if(text!==undefined)e.textContent=String(text);if(parent)parent.appendChild(e);return e}
function topics(){var old=$('topic').value; $('topic').replaceChildren();entries.filter(function(e){return e.targets.some(function(t){return t.courseId===$('course').value})}).forEach(function(e){var o=el('option',$('topic'),e.key.replace(/-/g,' '));o.value=e.key});if(Array.from($('topic').options).some(function(x){return x.value===old}))$('topic').value=old}
function nextButton(area){var next=el('button',area,index===questions.length-1?'Start again':'Next question');next.type='button';next.addEventListener('click',function(){if(index===questions.length-1){index=0;score=0}else index++;render()})}
function render(){var area=$('practice');area.replaceChildren();$('printSheet').hidden=$('mode').value!=='worksheet';if(!questions.length){el('p',area,'No suitable questions available. Choose another topic or level.');return}
 var mode=$('mode').value,q=questions[index];
 if(mode==='worksheet'){el('h2',area,'Worksheet · '+$('topic').selectedOptions[0].textContent);questions.forEach(function(item,i){var block=el('div',area);block.className='print-item';el('strong',block,(i+1)+'. ');el('span',block,item.prompt);if(item.partPrompt)el('p',block,item.partPrompt);el('p',block,'Answer: ______________________________')});var key=el('section',area);key.className='print-key';el('h2',key,'Teacher answer key');questions.forEach(function(item,i){el('p',key,(i+1)+'. '+item.answer)});return}
 el('h2',area,mode==='flashcards'?'Flashcard '+(index+1)+' / '+questions.length:'Question '+(index+1)+' / '+questions.length+' · Score '+score);
 el('p',area,q.prompt);if(q.partPrompt)el('p',area,q.partPrompt);
 if(mode==='flashcards'){var reveal=el('button',area,'Flip card to reveal answer');reveal.type='button';reveal.addEventListener('click',function(){reveal.disabled=true;el('p',area,'Answer: '+q.answer).className='answer'});nextButton(area);return}
 var choices=el('div',area);q.options.forEach(function(o){var b=el('button',choices,o.text);b.type='button';b.addEventListener('click',function(){
 if(choices.dataset.answered)return;choices.dataset.answered='1';if(o.correct)score++;
 el('p',area,o.correct?'Correct!':'Not quite. Answer: '+q.answer).className='answer';
 Array.from(choices.querySelectorAll('button')).forEach(function(btn){btn.disabled=true})
 })});nextButton(area)
}
function generate(){var entry=entries.find(function(x){return x.key===$('topic').value});if(!entry){questions=[];$('status').textContent='No matching topics';render();return}
 var result=root.MK_LEGACY_REVIEW_SAMPLES.sample(entry,$('course').value,$('level').value,'grade-preview',8);
 questions=result.questions.filter(function(q){return !q.figure});index=0;score=0;
 $('status').textContent=questions.length?questions.length+' draft questions generated. Verify mathematics and level before student use.':'No text-only questions available for this combination. '+result.reason;render()}
$('course').addEventListener('change',function(){topics();generate()});
$('topic').addEventListener('change',generate);$('level').addEventListener('change',generate);
$('generate').addEventListener('click',generate);
$('mode').addEventListener('change',function(){index=0;score=0;render()});
$('printSheet').addEventListener('click',function(){root.print()});
var query=new URLSearchParams(root.location.search);
if(['math6','prealgebra7','prealgebra'].indexOf(query.get('course'))>=0)$('course').value=query.get('course');
topics();
if(Array.from($('topic').options).some(function(o){return o.value===query.get('topic')}))$('topic').value=query.get('topic');
if(['cp2','cp1','honors'].indexOf(query.get('level'))>=0)$('level').value=query.get('level');
if(['practice','flashcards','game','worksheet'].indexOf(query.get('mode'))>=0)$('mode').value=query.get('mode');
generate()
})(window);
