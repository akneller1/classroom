'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const env=require('./load.cjs')(),NS=env.MKMENU;
const app=fs.readFileSync(require('node:path').join(__dirname,'../app.js'),'utf8');
Object.assign(env,{NS,esc:String,topicCourse:null,topicCart:[],G:{history:{replaceState(){}}},autosave(){}});
vm.runInContext(app.slice(app.indexOf('  function classGroup('),app.indexOf('  function viewSetup(')),env);
for(const group of NS.CATALOG){
 const options=env.unitOptions(group.units[0][0],group);
 const ids=Array.from(options.matchAll(/<option value="([^"]+)"/g),m=>m[1]);
 assert.deepEqual(ids,Array.from(group.units,u=>u[0]));
 for(const other of NS.CATALOG.filter(g=>g!==group))for(const unit of other.units)assert(!ids.includes(unit[0]));
}
assert.equal((env.unitOptions('topic-all').match(/<optgroup/g)||[]).length,1);
vm.runInContext(app.slice(app.indexOf('  function prepareUnitBrowse('),app.indexOf('  function render() {')),env);
const geometry=NS.CATALOG.find(g=>g.course==='Geometry');
env.topicCourse=geometry;env.cfg=()=>({unitId:'topic-all',level:'cp1'});env.loadUnit=(id,level)=>{env.chosenUnit=id;env.chosenLevel=level;};
env.prepareUnitBrowse();assert(geometry.units.some(u=>u[0]===env.chosenUnit));assert.equal(env.chosenLevel,'cp1');
env.topicCourse='all';env.topicCart=[{unit:geometry.units[1][0]}];env.chosenUnit=null;env.prepareUnitBrowse();assert(geometry.units.some(u=>u[0]===env.chosenUnit));
env.cfg=()=>({unitId:geometry.units[1][0],level:'cp1'});env.chosenUnit=null;env.prepareUnitBrowse();assert.equal(env.chosenUnit,null);
console.log('Unit browsing passed: class-scoped lists, no all-class fallback, mixed-topic transition, native-unit preservation.');
