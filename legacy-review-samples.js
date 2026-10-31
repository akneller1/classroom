/* Generate bounded, unapproved legacy samples for human curriculum review.
 * Call only with a loaded MKMENU + MKGAMES and curated crosswalk. No registration or publishing.
 */
(function(root){'use strict';
function sample(entry,courseId,level,seed,count){
 var policy=root.MK_CROSS_COURSE_DIFFICULTY.plan(entry,courseId,level);
 if(!policy.eligible)return {ready:false,reason:policy.reason,questions:[]};
 if(!root.MKGAMES||typeof root.MKGAMES.makeItems!=='function')return {ready:false,reason:'Legacy question engine unavailable',questions:[]};
 count=Math.max(1,Math.min(12,Number(count)||3));var items=[],errors=[];
 for(var tier=policy.tiers[0];tier<=policy.tiers[1]&&items.length<count;tier++){
  for(var n=0;n<10&&items.length<count;n++){
   try{
    var batch=root.MKGAMES.makeItems(policy.source.setId,policy.source.skillId,tier,{intOnly:true,level:'review'},String(seed||'review')+'|'+tier+'|'+n,null);
    batch.forEach(function(item){
     if(items.length>=count)return;
     // Keep the original question, verifier, figure and steps intact, not an unsafe text-only conversion.
     if(!item||!item.p||!item.options||item.options.filter(function(o){return o.ok===true}).length!==1)return;
     var checked=item.options.every(function(o){return root.MKGAMES.answerOk(item.p,item.k,o.a).ok===o.ok});
     if(!checked)return;
     items.push({sourceId:item.id,reviewKey:[entry.key,courseId,policy.level,tier,item.id].join('|'),topic:entry.key,courseId:courseId,level:policy.level,tier:tier,
       prompt:item.q.prompt,partPrompt:item.q.ask||'',answer:item.answer,figure:item.q.fig||null,
       steps:item.steps,options:item.options.map(function(o){return {text:o.a,correct:o.ok}}),
       approved:false,publishable:false});
    });
   }catch(e){errors.push(String(e.message||e))}
  }
 }
 return {ready:items.length>0,reason:items.length?'Unapproved review samples only':'No verified samples generated',questions:items,errors:errors};
}
root.MK_LEGACY_REVIEW_SAMPLES={version:1,sample:sample};
})(typeof window!=='undefined'?window:globalThis);
