/* Dedicated flashcards for independently approved shared-bank questions.
 * Keeps legacy game engines untouched; no unapproved content is shown.
 */
(function(root){
'use strict';
var doc=root.document, params=new URLSearchParams(root.location.search);
var courseId=params.get('course')||'', unitId=params.get('unit')||'';
var catalog=root.MK_COURSE_CATALOG,banks=root.MK_QUESTION_BANKS;
var status=doc.getElementById('afStatus'),container=doc.getElementById('afApp');
var course=root.LIBRARY.courses.find(function(c){return c.id===courseId;});
var unit=course&&course.units.find(function(u){return u.id===unitId;});
if(!unit){status.textContent='Unknown course or unit. Return to the classroom and choose a unit.';return;}
var skills=catalog.getSkillRecords(courseId,unitId), skillNames={};
skills.forEach(function(s){skillNames[s.id]=s.name;var opt=doc.createElement('option');opt.value=s.id;opt.textContent=s.name;doc.getElementById('afSkill').appendChild(opt)});
var S={level:'cp1',skill:'',cards:[],order:[],index:0,flipped:false,missedOnly:false,ratings:{}};
var selectors={level:doc.getElementById('afLevel'),skill:doc.getElementById('afSkill')};
function el(id){return doc.getElementById(id)}
function text(tag,value,parent){var n=doc.createElement(tag);n.textContent=value;parent.appendChild(n);return n}
function imagePath(q) {
 if(!q.diagram)return '';
 if(q.diagram.type!=='image'||!q.diagram.spec||typeof q.diagram.spec.src!=='string')return null;
 var src=q.diagram.spec.src;
 return /^question-banks\/assets\/[a-zA-Z0-9_/-]+\.(?:png|jpg|jpeg|webp)$/.test(src)&&src.indexOf('..')<0?'../'+src:null;
}
function diagram(q,card){
 var src=imagePath(q);
 if(src===null){text('p','This question requires an unsupported diagram and cannot be displayed.',card);return false;}
 if(src){
  var figure=doc.createElement('figure'),im=doc.createElement('img');
  im.src=src;im.alt=q.diagram.spec.alt;im.loading='lazy';
  im.addEventListener('error',function(){figure.replaceChildren();text('p','Diagram image unavailable. Do not use this question until the asset is repaired.',figure)});
  figure.appendChild(im);if(q.diagram.spec.caption)text('figcaption',q.diagram.spec.caption,figure);
  card.appendChild(figure);
 }return true;
}
function refresh(){
 S.cards=banks.select({courseId:courseId,unitId:unitId,level:S.level,formats:['short-answer','multiple-choice'],skillIds:S.skill?[S.skill]:undefined}).filter(function(q){return imagePath(q)!==null;});
 S.order=S.cards.map(function(_,i){return i}).filter(function(i){return !S.missedOnly||S.ratings[S.cards[i].id]==='need'});
 S.index=Math.min(S.index,Math.max(0,S.order.length-1));S.flipped=false;render();
}
function current(){return S.cards[S.order[S.index]]}
function render(){
 var q=current(),card=el('afCard');card.replaceChildren();
 el('afProgress').textContent=S.order.length?'Card '+(S.index+1)+' of '+S.order.length:'No approved cards for these settings';
 if(q){
 text('h2',S.flipped?'Answer':'Question',card);
 if(S.flipped){
  text('div',Array.isArray(q.answer)?q.answer.join(', '):String(q.answer),card).className='af-answer';
  if(q.solutionSteps&&q.solutionSteps.length){text('strong','Worked solution',card);var sol=doc.createElement('ol');sol.className='af-solution';q.solutionSteps.forEach(function(s){text('li',s,sol)});card.appendChild(sol)}
 }else{
  text('p',q.prompt,card).className='af-prompt';
  diagram(q,card);
  if(q.options&&q.options.length){var ul=doc.createElement('ol');ul.className='af-options';q.options.forEach(function(o){text('li',o.text,ul)});card.appendChild(ul)}
 }
 text('small',skillNames[q.skillId]||q.skillId,card);
 }else text('p',S.missedOnly?'No missed cards for these settings.':'No approved flashcards available for this difficulty and skill.',card);
 el('afPrev').disabled=S.index===0||!q;el('afNext').disabled=S.index>=S.order.length-1||!q;
 el('afFlip').hidden=S.flipped;el('afFlip').disabled=!q;el('afNeed').hidden=!S.flipped||!q;el('afGot').hidden=!S.flipped||!q;
 el('afMissed').textContent=S.missedOnly?'Show all cards':'Practice missed';
}
function flip(){if(current()){S.flipped=!S.flipped;render()}}
function move(n){S.index=Math.max(0,Math.min(S.order.length-1,S.index+n));S.flipped=false;render()}
function rate(value){var q=current();if(!q)return;S.ratings[q.id]=value;if(S.missedOnly){refresh()}else if(S.index<S.order.length-1)move(1);else render()}
selectors.level.addEventListener('change',function(){S.level=this.value;S.index=0;refresh()});
selectors.skill.addEventListener('change',function(){S.skill=this.value;S.index=0;refresh()});
el('afCard').addEventListener('click',flip);el('afCard').addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();flip()}});
el('afFlip').addEventListener('click',flip);el('afPrev').addEventListener('click',function(){move(-1)});
el('afNext').addEventListener('click',function(){move(1)});
el('afNeed').addEventListener('click',function(){rate('need')});el('afGot').addEventListener('click',function(){rate('got')});
el('afReset').addEventListener('click',function(){S.ratings={};S.missedOnly=false;refresh()});
el('afMissed').addEventListener('click',function(){S.missedOnly=!S.missedOnly;S.index=0;refresh()});
el('afShuffle').addEventListener('click',function(){for(var i=S.order.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=S.order[i];S.order[i]=S.order[j];S.order[j]=t}S.index=0;S.flipped=false;render()});
root.MK_BANK_LOADER.loadFromSite().then(function(){
 if(!banks.available(courseId,unitId)){status.textContent='No independently approved flashcard bank is available for '+course.name+' — '+unit.name+'. Existing classroom resources are unaffected.';return;}
 status.textContent=course.name+' · '+unit.name+' · approved questions only';
 container.hidden=false;refresh();
}).catch(function(err){status.textContent='Unable to load approved flashcards: '+err.message});
})(window);