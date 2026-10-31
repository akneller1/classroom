/* Browser-side staging eligibility checks; not an authorization token or production gate. */
(function(root){'use strict';
function evaluate(data,reviewer,confirmed){
 var issues=[],rows=data&&Array.isArray(data.results)?data.results:[];
 if(!data||data.schemaVersion!==1||data.type!=='legacy-question-review'||data.approved!==false)issues.push('Invalid review export');
 if(rows.length<6)issues.push('Review at least six distinct questions');
 if(new Set(rows.map(function(r){return r.tier})).size<2)issues.push('Review at least two difficulty tiers');
 var seen={};
 rows.forEach(function(r){
  if(!r||typeof r.reviewKey!=='string'||seen[r.reviewKey])issues.push('Duplicate or missing question identifier');
  if(r&&r.reviewKey)seen[r.reviewKey]=true;
  if(!r||!r.review||r.review.status!=='appropriate'||typeof r.review.note!=='string'||!r.review.note.trim())issues.push('Every question needs an appropriate decision and rationale');
  if(r&&r.reviewKey){
   var parts=r.reviewKey.split('|'),lvl={cp2:'remedial',cp1:'standard',honors:'advanced'}[data.level]||data.level;
   if(parts.length!==5||parts[0]!==data.topic||parts[1]!==data.courseId||parts[2]!==lvl||parts[3]!==String(r.tier)||parts[4]!==String(r.sourceId))issues.push('Question identifier does not match review scope');
  }
 });
 if(typeof reviewer!=='string'||reviewer.trim().length<3)issues.push('Enter the reviewer name');
 if(confirmed!==true)issues.push('Confirm staging-only review');
 return {eligibleForStaging:issues.length===0,productionEnabled:false,issues:issues.filter(function(x,i,a){return a.indexOf(x)===i}),scope:{courseId:data&&data.courseId,topic:data&&data.topic,level:data&&data.level}};
}
root.MK_BROWSER_STAGE_REVIEW={evaluate:evaluate};
})(typeof window!=='undefined'?window:globalThis);
