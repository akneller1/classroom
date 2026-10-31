#!/usr/bin/env node
/* Validate reviewer exports for traceability. Does not publish or approve any bank. */
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict');
function validate(data){
 const issues=[];
 if(!data||data.schemaVersion!==1||data.type!=='legacy-question-review'||data.approved!==false)issues.push('Review export must be explicitly unapproved');
 if(!data||!Array.isArray(data.results)||!data.results.length)issues.push('Missing review results');
 const keys=new Set();
 for(const [i,r] of (data&&Array.isArray(data.results)?data.results:[]).entries()){
  if(typeof r.reviewKey!=='string'||!r.reviewKey.length)issues.push('Missing stable review key at '+i);
  else{
   if(keys.has(r.reviewKey))issues.push('Duplicate review key: '+r.reviewKey);
   keys.add(r.reviewKey);
   const parts=r.reviewKey.split('|');
   if(parts.length!==5||parts[0]!==data.topic||parts[1]!==data.courseId||parts[2]!==({cp2:'remedial',cp1:'standard',honors:'advanced'}[data.level]||data.level)||parts[3]!==String(r.tier)||parts[4]!==String(r.sourceId))issues.push('Review key does not match source context at '+i);
  }
  if(!r.review||!['unreviewed','appropriate','revise','exclude'].includes(r.review.status))issues.push('Unknown review status at '+i);
  if(r.review&&typeof r.review.note!=='string')issues.push('Invalid reviewer note at '+i);
 }
 return {valid:issues.length===0,issues,summary:{total:keys.size,appropriate:(data?.results||[]).filter(x=>x.review?.status==='appropriate').length,requiresFollowUp:(data?.results||[]).filter(x=>['revise','exclude'].includes(x.review?.status)).length}};
}
if(require.main===module){
 if(process.argv.length!==3){console.error('Usage: node scripts/validate-legacy-review.cjs <review-export.json>');process.exit(2);}
 const result=validate(JSON.parse(fs.readFileSync(process.argv[2],'utf8')));
 console.log(JSON.stringify(result,null,2));if(!result.valid)process.exitCode=1;
}
module.exports={validate};
