'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const env = require('./load.cjs')(['games/bank.js','vendor/katex/katex.min.js','core/render.js','menu/render.js']);
const M = env.MKMENU, basics = 'geometry-basics-reasoning', right = 'geometry-right-triangles-trigonometry';
function problem(unit,skill,c,seed){const p=M.generateProblem(unit,skill,c,{intOnly:false,level:'honors'},seed,null);assert.ok(!p.failed,p.reason);return p;}
// The reported part d cannot be detached from the parts defining M and N.
for(let seed=0;seed<12;seed++){
 const p=problem(basics,'coordinate-investigation',4,'orphan'+seed);
 assert.equal(p.parts.length,4);assert.ok(M.makeChoices(p).fail);
}
for(const level of ['cp2','cp1','honors']){
 const cfg=M.defaultConfig(basics,'worksheet');M.setLevel(cfg,level);cfg.seed=731;cfg.sections=M.worksheetSections('mc',cfg);
 const st=M.newAssessment(cfg);
 for(const item of st.versions[0].sections[0].items){assert.ok(!item.failed,item.reason);assert.equal(item.parts.length,1);if(item.mc)assert.ok(M.checkChoices(item));else assert.ok(item.mcFail);}
 const honors=M.skillSets[basics].skills.filter(s=>/^Honors:/.test(s.name));
 assert.equal(honors.filter(s=>cfg.skills[s.id]).length,level==='honors'?4:0);
 if(level!=='honors'){
  honors.forEach(s=>cfg.skills[s.id]=true); // stale or hand-edited configuration
  assert.ok(M.sectionSkills(cfg,0).every(id=>!/^Honors:/.test(M.skillSets[basics].byId[id].name)));
  M.normalizeLevelSkills(cfg);assert.ok(honors.every(s=>!cfg.skills[s.id]));
 }
 M.setLevel(cfg,'honors');M.setLevel(cfg,'cp1');assert.ok(honors.every(s=>!cfg.skills[s.id]));
}
// A saved extracted item is replaced, even though its numeric equation still verifies.
{
 const cfg=M.defaultConfig(basics,'worksheet');cfg.sections=M.worksheetSections('mc',cfg);cfg.seed=348;
 const st=M.newAssessment(cfg), item=st.versions[0].sections[0].items[0];
 const orphan=problem(basics,'coordinate-investigation',4,'saved-orphan');orphan.parts=[orphan.parts[3]];
 Object.assign(item,orphan,{skill:'coordinate-investigation',mcNote:'Made from part (d) of a multi-part problem.'});
 const restored=M.deserialize(M.serialize(st)), fresh=restored.versions[0].sections[0].items[0];
 assert.notEqual(fresh.skill,'coordinate-investigation');assert.ok(!fresh.failed);assert.ok(M.checkChoices(fresh));
}
// Independent property identities retain their MC format without carrying a connected investigation.
{
 const p=problem('algebra1-foundations','properties',7,'props7');
 const mc=M.makeChoices(p);assert.ok(!mc.fail);assert.equal(mc.derived.parts.length,1);
 assert.equal(mc.derived.prompt,'Name the property shown by this equation.');
}
// Higher levels require solving algebraic leg expressions, rather than repeating an equal-leg reading.
for(let c=1;c<=7;c++)for(let seed=0;seed<15;seed++){
 const p=problem(right,'right-special-45-45-90',c,'45:'+c+':'+seed);
 if(c<5){const n=Number(/length (\d+)/.exec(p.prompt)[1]);assert.equal(p.parts[0].answer,'⟨x='+n+'⟩');assert.equal(p.parts[0].check.eq,'x='+n);}
 else{
  const expressions=[...p.prompt.matchAll(/⟨([^⟩]+)⟩/g)].map(m=>m[1]);assert.equal(expressions.length,2);
  const x=Number(/x=(\d+)/.exec(p.parts[0].answer)[1]);
  const evaluate=t=>Function('x','return '+t.replace(/(\d)(x|\()/g,'$1*$2'))(x);
  assert.equal(evaluate(expressions[0]),evaluate(expressions[1]));assert.ok(evaluate(expressions[0])>0);
  if(c>=6)assert.ok(expressions[0].includes('('));if(c===7)assert.ok(expressions[1].includes('('));
 }
}
// Render with the shipped KaTeX, checking visible output rather than raw internal markup.
for(const input of ['24*x=18*24','⟨24*x=18*24⟩','⟨⟨2*x=12⟩⟩']){
 const html=M.mathSafe(M.stepMath(input));assert.ok(html.includes('katex'));assert.ok(!/[⟨⟩]/.test(html));
 const visible=html.replace(/<annotation[\s\S]*?<\/annotation>/g,'').replace(/<[^>]+>/g,'');
 assert.ok(!visible.includes('*'));assert.ok(visible.includes('⋅'));
}
let phrases=0;
for(let seed=0;seed<30;seed++){
 const p=problem('algebra1-expressions-equations','verbal',5,'phrase:'+seed);
 const phrase=/“(.+)”/.exec(p.prompt)[1];assert.ok(p.steps[0].t.includes('“'+phrase+'”'));assert.ok(!p.steps[0].t.includes('“The phrase”'));phrases++;
}
const app=fs.readFileSync(path.resolve(__dirname,'../app.js'),'utf8');
assert.match(app,/class="mmSecOff" min="1" max="20"/);assert.match(app,/Max 20 per part; add another part for more/);
console.log('PASS: Reddit feedback regressions: self-contained MC builds, saved-item repair, class filtering, 105 special triangles, rendered math, '+phrases+' phrase explanations and count limits.');
