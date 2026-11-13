/* Algebra 1-style skill selection for integrated-course student links. */
(function(G){
'use strict';
const catalog=G.MK_INTEGRATED_STUDENT_SKILLS||{};
function supports(resource) {
 if(!resource || !['grade4','grade5','financial-algebra'].includes(resource.courseId))return false;
 const type=String(resource.type||''),path=String(resource.path||'');
 if(resource.courseId==='grade4'||resource.courseId==='grade5'){
  if(type==='Game')return !/[?&]game=fraction-frenzy(?:&|$)/.test(path);
  return type==='Study Guide'&&resource.title==='Understanding Check';
 }
 return type==='Game'||(type==='Study Guide'&&['Practice Test','Flashcards'].includes(resource.title));
}
function open(resource){
 if(!supports(resource))return false;
 const target=new URL(resource.path,G.location.href);
 const unit=target.searchParams.get('unit');
 const records=resource.courseId==='grade4'&&G.MK_COURSE_CATALOG&&G.MK_COURSE_CATALOG.getSkillRecords?G.MK_COURSE_CATALOG.getSkillRecords('grade4',unit):null;
 const skills=resource.courseId==='grade4'?records:(catalog[resource.courseId]||{})[unit];
 if(!unit||!Array.isArray(skills)||!skills.length){G.alert('The unit skill list could not be loaded.');return false;}
 const previous=G.document.activeElement,doc=G.document;
 const existing=doc.getElementById('integrated-skill-share-dialog');if(existing)existing.close();
 const dialog=doc.createElement('dialog');dialog.id='integrated-skill-share-dialog';
 dialog.setAttribute('aria-label','Choose skills and generate student link');
 dialog.style.cssText='box-sizing:border-box;width:min(650px,94vw);max-height:90vh;overflow:auto;border:2px solid #3456d1;border-radius:16px;padding:22px;background:#fff;color:#17233b;font:16px/1.5 system-ui;';
 const h=doc.createElement('h2');h.textContent='Choose skills for this activity';h.style.margin='0 0 8px';dialog.appendChild(h);
 const context=doc.createElement('p');context.textContent=resource.title+' · '+(resource.courseId==='grade4'?'Grade 4':resource.courseId==='grade5'?'Grade 5':'Financial Algebra');context.style.fontWeight='700';dialog.appendChild(context);
 const intro=doc.createElement('p');intro.textContent='Select the skills students should practice. The generated link will use only those skills.';dialog.appendChild(intro);
 const bar=doc.createElement('div');bar.style.cssText='display:flex;flex-wrap:wrap;gap:8px;margin:12px 0';dialog.appendChild(bar);
 function button(text,parent,fn){const b=doc.createElement('button');b.type='button';b.textContent=text;b.className='btn btn-ghost';b.style.cssText='padding:8px 13px;cursor:pointer';b.addEventListener('click',fn);parent.appendChild(b);return b;}
 const fieldset=doc.createElement('fieldset');fieldset.style.cssText='border:1px solid #c9d4e8;border-radius:10px;padding:12px;margin:8px 0';const legend=doc.createElement('legend');legend.textContent='Skills in this unit';fieldset.appendChild(legend);
 const inputs=skills.map(function(skill){const label=doc.createElement('label');label.style.cssText='display:flex;align-items:baseline;gap:10px;padding:7px 3px;cursor:pointer';const input=doc.createElement('input');input.type='checkbox';input.checked=true;input.value=skill.id;input.style.cssText='width:18px;height:18px;flex:none';label.append(input,doc.createTextNode(skill.name));fieldset.appendChild(label);return input;});
 dialog.appendChild(fieldset);
 let level=null;
 if(resource.courseId==='grade4'||resource.courseId==='grade5'){
  const label=doc.createElement('label');label.textContent='Student level ';label.style.cssText='display:block;font-weight:700;margin:14px 0';
  level=doc.createElement('select');level.style.cssText='display:block;padding:9px;margin:5px 0;width:100%;max-width:260px';
  [['cp2','Remedial'],['cp1','Standard'],['honors','Advanced']].forEach(function(pair){const o=doc.createElement('option');o.value=pair[0];o.textContent=pair[1];o.selected=pair[0]==='cp1';level.appendChild(o);});
  label.appendChild(level);dialog.appendChild(label);
 }
 const status=doc.createElement('p');status.setAttribute('role','status');dialog.appendChild(status);
 const actions=doc.createElement('div');actions.style.cssText='display:flex;gap:10px;flex-wrap:wrap;margin-top:14px';dialog.appendChild(actions);
 const go=button('Generate student link',actions,generate);const close=button('Cancel',actions,function(){dialog.close();});
 function update(){const n=inputs.filter(x=>x.checked).length;status.textContent=n?n+' of '+skills.length+' skills selected':'Select at least one skill.';go.disabled=!n;}
 button('Select All',bar,function(){inputs.forEach(x=>x.checked=true);update();});
 button('Clear All',bar,function(){inputs.forEach(x=>x.checked=false);update();});
 inputs.forEach(x=>x.addEventListener('change',update));
 const result=doc.createElement('div');dialog.appendChild(result);
 function generate(){
  const ids=inputs.filter(x=>x.checked).map(x=>x.value);if(!ids.length)return;
  const url=new URL(target.href);
  url.searchParams.delete('teacher');url.searchParams.delete('teacherShare');url.searchParams.delete('mode');url.searchParams.delete('present');
  url.searchParams.set('student','1');url.searchParams.set('skills',JSON.stringify(ids));
  if(level)url.searchParams.set('level',level.value);
  result.replaceChildren();
  const summary=doc.createElement('p');summary.textContent='Ready: '+ids.length+' selected '+(ids.length===1?'skill':'skills')+(level?' · '+level.options[level.selectedIndex].text:'')+'.';result.appendChild(summary);
  const label=doc.createElement('label');label.textContent='Student link';label.style.fontWeight='700';result.appendChild(label);
  const field=doc.createElement('input');field.readOnly=true;field.value=url.href;field.setAttribute('aria-label','Student link');field.style.cssText='display:block;box-sizing:border-box;width:100%;padding:10px;margin:8px 0';label.appendChild(field);
  button('Copy student link',result,function(){
   function fallback(){field.focus();field.select();status.textContent='Select and copy the link above.';}
   if(G.navigator.clipboard&&G.navigator.clipboard.writeText)G.navigator.clipboard.writeText(url.href).then(function(){status.textContent='Student link copied!';},fallback);else fallback();
  });
  field.focus();field.select();
 }
 dialog.addEventListener('close',function(){dialog.remove();if(previous&&previous.isConnected)previous.focus();});
 doc.body.appendChild(dialog);update();dialog.showModal();return true;
}
G.MK_INTEGRATED_STUDENT_SHARE={supports,open};
})(window);
