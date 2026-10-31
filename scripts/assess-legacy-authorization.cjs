#!/usr/bin/env node
/* Fail-closed staging authorization: review exports are evidence, never publication approval. */
'use strict';
const {validate}=require('./validate-legacy-review.cjs');
const fs=require('node:fs');
function assess(exportData,options={}){
 const checked=validate(exportData);
 const issues=checked.issues.slice();
 const rows=Array.isArray(exportData?.results)?exportData.results:[];
 const minimum=Number.isInteger(options.minimum)&&options.minimum>=3?options.minimum:6;
 const tiers=new Set(rows.map(r=>r.tier));
 if(rows.length<minimum)issues.push('At least '+minimum+' distinct samples required');
 if(tiers.size<2)issues.push('Review must cover at least two difficulty tiers');
 if(rows.some(r=>r.review?.status!=='appropriate'))issues.push('Every sampled question must be marked appropriate; resolve all flags');
 if(rows.some(r=>!r.review?.note?.trim()))issues.push('Each sample requires a reviewer rationale');
 if(!options.reviewer||typeof options.reviewer!=='string'||options.reviewer.trim().length<3)issues.push('Named reviewer required');
 if(options.confirmed!==true)issues.push('Explicit scope confirmation required');
 return {eligibleForStaging:issues.length===0,productionEnabled:false,issues,scope:{courseId:exportData?.courseId||null,topic:exportData?.topic||null,level:exportData?.level||null},reviewer:options.reviewer||null,samples:rows.length};
}
if(require.main===module){
 const [file,reviewer,confirmation]=process.argv.slice(2);
 if(!file){console.error('Usage: node scripts/assess-legacy-authorization.cjs review.json "Reviewer name" CONFIRM_STAGING');process.exit(2)}
 const result=assess(JSON.parse(fs.readFileSync(file,'utf8')),{reviewer,confirmed:confirmation==='CONFIRM_STAGING'});
 console.log(JSON.stringify(result,null,2));if(!result.eligibleForStaging)process.exitCode=1;
}
module.exports={assess};
