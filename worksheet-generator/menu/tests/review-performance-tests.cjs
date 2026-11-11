const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const root=require('node:path').resolve(__dirname,'../..')+'/';
const env=require(root+'menu/tests/load.cjs')(['core/graph.js','core/render.js','games/bank.js','menu/render.js']),M=env.MKMENU;
env.katex=require(root+'vendor/katex/katex.min.js');
const app=fs.readFileSync(root+'menu/app.js','utf8');
Object.assign(env,{NS:M,WS:env.MKWS,doc:{},ui:{version:0,showAns:{},bankOpen:false},esc:s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])),mathSafe:M.mathSafe,classGroup(){},noun:()=> 'worksheet',S:null});
vm.runInContext(app.slice(app.indexOf('  // Topic worksheets'),app.indexOf('  /* ---------------- start ---------------- */'))+'\nregisterTopicSets();',env);
const c=M.defaultConfig('topic-all','worksheet');c.skills={};c.sections=[];const sections=[];
for(let i=0;i<10;i++){
 const src='algebra1-linear-equations-slope',skill=i%2?'slope':'graph-slope',set=M.skillSets[src];
 const id=set.byId[skill]?skill:set.skills[0].id;
 const cc=M.defaultConfig(src,'worksheet');cc.coverage.on=false;cc.skills={};cc.skills[id]=true;cc.sections=[{id:'s'+i,name:'Question '+i,points:1,offered:1,required:1,tier:1,adjust:0,skills:[id],qformat:i%2?'mc':'open'}];
 const a=M.newAssessment(cc),p=a.versions[0].sections[0].items[0];p.skill=src+':'+p.skill;p.tag=src+':'+p.tag;
 c.sections.push({...cc.sections[0],skills:[p.skill]});c.skills[p.skill]=true;sections.push({id:'s'+i,items:[p]});
}
env.S={config:c,versions:[{label:'A',sections}],bank:{items:[]}};
vm.runInContext(app.slice(app.indexOf('  function promptBlock('),app.indexOf('  function bankHtml()')),env);
let checks=0,generated=0;const check=M.skillFormatOk,gen=M.generateProblem;M.skillFormatOk=function(){checks++;return check.apply(this,arguments)};M.generateProblem=function(){generated++;return gen.apply(this,arguments)};
const t=performance.now();const html=env.viewReview();const ms=performance.now()-t;
console.log(JSON.stringify({ms:Math.round(ms),formatChecks:checks,generatedForDisplay:generated,htmlBytes:html.length}));

assert.equal(checks,0,'Review rendering must not probe format compatibility');assert.equal(generated,0,'Displaying questions must not generate extra questions');assert(html.length<150000,'Skill dropdowns should stay compact until opened');
