/* Isolated staging preview. Accepts only explicit review eligibility; never registers content. */
(function(root){'use strict';
function create(review,entries,courseId,level,topic){
 if(!review||review.eligibleForStaging!==true||review.productionEnabled!==false)return {ready:false,reason:'Staging authorization required',questions:[]};
 if(!review.scope||review.scope.courseId!==courseId||review.scope.topic!==topic||review.scope.level!==level)return {ready:false,reason:'Authorization scope mismatch',questions:[]};
 var entry=entries.filter(function(e){return e.key===topic})[0];
 if(!entry)return {ready:false,reason:'Unknown topic',questions:[]};
 var sample=root.MK_LEGACY_REVIEW_SAMPLES.sample(entry,courseId,level,'staging',6);
 if(!sample.ready)return {ready:false,reason:sample.reason,questions:[]};
 return {ready:true,productionEnabled:false,questions:sample.questions,reason:'Staging-only; new generated samples are not individually approved'};
}
root.MK_STAGED_REUSE={version:1,create:create};
})(typeof window!=='undefined'?window:globalThis);
