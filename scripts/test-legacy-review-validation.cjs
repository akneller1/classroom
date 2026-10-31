#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict'),validate=require('./validate-legacy-review.cjs').validate;
const base={schemaVersion:1,type:'legacy-question-review',approved:false,courseId:'prealgebra7',topic:'evaluating-expressions',level:'cp1',results:[{sourceId:'item1',reviewKey:'evaluating-expressions|prealgebra7|standard|2|item1',tier:2,review:{status:'appropriate',note:'Checked arithmetic'}}]};
assert.equal(validate(base).valid,true);
assert.equal(validate(base).summary.appropriate,1);
assert.equal(validate({...base,approved:true}).valid,false);
assert.equal(validate({...base,results:[{...base.results[0],reviewKey:'wrong'}]}).valid,false);
assert.equal(validate({...base,results:[base.results[0],base.results[0]]}).valid,false);
assert.equal(validate({...base,results:[{...base.results[0],review:{status:'approved',note:''}}]}).valid,false);
console.log('PASS reviewer export schema, stable IDs, duplicate detection and no auto-approval');
