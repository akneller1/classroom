#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict'),{assess}=require('./assess-legacy-authorization.cjs');
const results=Array.from({length:6},(_,i)=>({sourceId:'item'+i,reviewKey:'evaluating-expressions|prealgebra7|standard|'+(i<3?2:3)+'|item'+i,tier:i<3?2:3,review:{status:'appropriate',note:'Checked arithmetic and grade suitability'}}));
const data={schemaVersion:1,type:'legacy-question-review',approved:false,courseId:'prealgebra7',topic:'evaluating-expressions',level:'cp1',results};
const options={reviewer:'Test Reviewer',confirmed:true};
assert.equal(assess(data,options).eligibleForStaging,true);
assert.equal(assess(data,options).productionEnabled,false);
assert.equal(assess(data,{...options,confirmed:false}).eligibleForStaging,false);
assert.equal(assess(data,{...options,reviewer:''}).eligibleForStaging,false);
assert.equal(assess({...data,results:results.slice(0,3)},options).eligibleForStaging,false);
assert.equal(assess({...data,results:results.map(x=>({...x,tier:2,reviewKey:x.reviewKey.replace('|3|','|2|') }))},options).eligibleForStaging,false);
assert.equal(assess({...data,results:[{...results[0],review:{status:'exclude',note:'too difficult'}},...results.slice(1)]},options).eligibleForStaging,false);
assert.equal(assess({...data,approved:true},options).eligibleForStaging,false);
console.log('PASS staging review authorization gates, failure scenarios, and production disabled');
