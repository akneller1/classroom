/* Geometry plausibility guards: correct algebra is not enough if the
   measurements cannot describe the geometric object in the prompt. */
'use strict';
const assert=require('node:assert/strict');
const M=require('./load.cjs')().MKMENU;
let checked=0;
for(const tier of [1,3,5,7]){
 for(let n=0;n<100;n++){
  const seed='plausibility:'+tier+':'+n;
  const perimeter=M.generateProblem('geometry-triangles-congruence','congruent-perimeters',tier,{intOnly:true,level:'test'},seed,{keys:new Set(),sigs:new Set()});
  assert.ok(!perimeter.failed,perimeter.reason);
  const match=perimeter.prompt.match(/side lengths of ABC are x, (\d+), and (\d+) units/);
  assert.ok(match,'Unexpected congruent perimeter prompt');
  const x=Number((perimeter.parts[0].answer.match(/x\s*=\s*(\d+)/)||[])[1]);
  const a=Number(match[1]),b=Number(match[2]);
  assert.ok(x>Math.abs(a-b)&&x<a+b,'Impossible triangle sides: '+[x,a,b]);
  const sss=M.generateProblem('geometry-similarity','similarity-sss-criterion',tier,{intOnly:true,level:'test'},seed,{keys:new Set(),sigs:new Set()});
  assert.ok(!sss.failed,sss.reason);
  const sides=sss.prompt.match(/AB = (\d+), DE = \d+, BC = (\d+), EF = \d+, AC = (\d+)/);
  assert.ok(sides,'Unexpected SSS similarity prompt');
  const [u,v,w]=sides.slice(1).map(Number);
  assert.ok(u+v>w&&u+w>v&&v+w>u,'Impossible SSS triangle: '+[u,v,w]);
  const proof=M.generateProblem('geometry-triangles-congruence','congruence-structured-proof',tier,{intOnly:true,level:'test'},seed,{keys:new Set(),sigs:new Set()});
  assert.ok(!proof.failed,proof.reason);
  const angles=[...proof.prompt.matchAll(/= (\d+) degrees/g)].map(x=>Number(x[1]));
  assert.ok(angles.length>=1&&angles.every(x=>x>0&&x<180),'Invalid proof angle: '+angles);
  checked+=3;
 }
}
console.log('Geometry plausibility: '+checked+' triangle/angle checks passed.');
