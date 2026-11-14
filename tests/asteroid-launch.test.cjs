const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const source=fs.readFileSync('worksheet-generator/games/course-source.js','utf8');
function setup(native=false,empty=false){
 const ids=Array.from({length:14},(_,i)=>'skill-'+i),unit={id:'linear-equations-slope'};let calls=0;const seen=new Set();
 const G={location:{search:'?course=algebra&unit=linear-equations-slope'},URLSearchParams,Date,LIBRARY:{courses:[{id:'algebra',units:[unit]}]},MKMENU:{skillSets:{'algebra1-linear-equations-slope':{skills:ids.map(id=>({id,name:id}))}}},MK_QUESTION_BANKS:{available:()=>native,select:()=>Array.from({length:300},(_,i)=>({id:i}))},MKWS:{rng:{hash:()=>1,make:()=>({shuffle:x=>x})}},MKGAMES:{LEVELS:{cp2:{tiers:[1,2,3]}},makeItems:(set,id)=>{calls++;seen.add(id);return empty?[]:[{id:calls,q:{prompt:'2 + 3 = ?'},options:[{a:'5',ok:true},{a:'4'},{a:'6'},{a:'7'}],answer:'5',steps:[]}]} }};G.window=G;vm.runInNewContext(source,G);
 return {G,ids,calls:()=>calls,seen};
}
test('Algebra 1 full-scan request is bounded and samples all 14 selected skills',()=>{const s=setup();const rows=s.G.MK_COURSE_ACTIVITY_SOURCE.select('cp2',s.ids,10000);assert.equal(rows.length,48);assert.equal(s.calls(),48);assert.equal(s.seen.size,14)});
test('unsupported procedural questions cannot cause unbounded retries',()=>{const s=setup(false,true);assert.equal(s.G.MK_COURSE_ACTIVITY_SOURCE.select('cp2',s.ids,10000).length,0);assert(s.calls()<=144)});
test('stored elementary banks retain their complete question pool',()=>{const s=setup(true);assert.equal(s.G.MK_COURSE_ACTIVITY_SOURCE.select('cp2',s.ids,10000).length,4200);assert.equal(s.calls(),0)});
