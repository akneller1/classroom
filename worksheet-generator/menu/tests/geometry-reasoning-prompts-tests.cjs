/* Student prompts must not contain worked equations or future-part answers.
   Answer keys and independent verification equations remain unchanged. */
'use strict';
const assert=require('node:assert/strict');
const M=require('./load.cjs')().MKMENU;
let count=0;
for(const tier of [1,3,5,7]){
 for(let n=0;n<30;n++){
  const seed='reasoning:'+tier+':'+n;
  const h=M.generateProblem('geometry-similarity','similarity-parallel-honors',tier,{intOnly:true,level:'test'},seed,{keys:new Set(),sigs:new Set()});
  assert.ok(!h.failed,h.reason);
  assert.equal(h.parts.length,4);
  for(const part of h.parts){
   assert.doesNotMatch(part.prompt,/\\\(|\\\)|Use .*=/,'Student part supplies a worked equation');
   assert.doesNotMatch(part.prompt,/\d+\s*[+*]\s*\d+\s*=/,'Student part supplies a calculated expression');
  }
  assert.ok(h.steps.length>=4,'Teacher key must retain complete solution');
  for(const skill of ['congruent-perimeters','congruence-structured-proof']){
   const p=M.generateProblem('geometry-triangles-congruence',skill,tier,{intOnly:true,level:'test'},seed,{keys:new Set(),sigs:new Set()});
   assert.ok(!p.failed,p.reason);
   assert.doesNotMatch(p.prompt,/Use [^.!?]*=\d+[^.!?]* to find x/i,'Student prompt supplies the equation');
  }
  count+=3;
 }
}
console.log('Geometry student reasoning: '+count+' generated prompts checked.');
