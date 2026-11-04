'use strict';
/* Ensure every playable Escape Room sorting puzzle has >=4 meaningful cards. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const base=path.join(root,'artifacts');
let standalone=0,sorted=0;
for(const folder of fs.readdirSync(base).filter(x=>x.endsWith('-escape-room'))){
 const file=path.join(base,folder,'index.html');
 if(!fs.existsSync(file))continue;
 const source=fs.readFileSync(file,'utf8');
 const scripts=[...source.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map(m=>m[1]);
 const code=scripts.find(s=>s.includes('const ROOM='));
 assert.ok(code,folder+': missing ROOM configuration');
 const marker=code.indexOf('const TOTAL=');
 assert.ok(marker>0,folder+': missing game initialization');
 const room=vm.runInNewContext(code.slice(0,marker)+'\nROOM;',{
  URLSearchParams,location:{search:''},Math
 },{timeout:3000});
 standalone++;
 for(const stage of room.stages.filter(s=>s.type==='order')){
  assert.ok(Array.isArray(stage.steps),folder+': order stage has array');
  assert.ok(stage.steps.length>=4,folder+': expected at least 4, found '+stage.steps.length);
  assert.ok(stage.steps.every(x=>typeof x==='string'&&x.trim().length>=8),
   folder+': all steps have actual content');
  sorted++;
 }
}
const source=fs.readFileSync(path.join(root,'worksheet-generator/games/course-activity.js'),'utf8');
const at=source.indexOf(' function orderedSteps(q){'),end=source.indexOf(' function scene(q){',at);
assert.ok(at>=0&&end>at,'shared Escape Room must enforce minimum in orderedSteps');
const choose=new Function(source.slice(at,end)+'\nreturn orderedSteps;')();
const samples=[
 {prompt:'Are the lines parallel or perpendicular?',answer:'Parallel',
  solutionSteps:['Find both slopes: -1/4 and -1/4.','Equal: parallel. Product -1: perpendicular. Otherwise: neither.']},
 {prompt:'Solve for x',answer:'8',solutionSteps:['First isolate the expression','Solve the equation']},
 {prompt:'Solve for x',answer:'8',solutionSteps:['Apply the formula','Substitute the values','Solve']},
 {prompt:'Prove triangles congruent',answer:'SAS',
  solutionSteps:['Given','Find corresponding sides','Identify angle','Apply SAS','Check conclusion']}
];
for(const [i,q] of samples.entries()){
 const steps=choose(q);
 assert.ok(Array.isArray(steps)&&steps.length>=4,'shared sample '+i+': minimum four steps');
 assert.equal(new Set(steps.map(x=>x.toLowerCase())).size,steps.length,
  'shared sample '+i+': no duplicate cards');
}
assert.equal(choose({prompt:'Find x',answer:'3',solutionSteps:['x=3']}),null,
 'do not fabricate a sorting puzzle from a one-step problem');
assert.match(source,/take\(q=>orderedSteps\(q\)\?\.length>=4/, 'shared selection prefers four-step questions');
assert.match(source,/sortedSteps\.length<4/, 'shared output validates minimum');
console.log('PASS: '+standalone+' standalone rooms, '+sorted+' standalone sorting challenges; shared generated rooms require >=4 cards.');
