/* Geometry flashcard parity: every skill must yield usable cards at each
   Easy/Medium/Hard tier, with a correct, independently verified answer. */
'use strict';
const assert=require('node:assert/strict');
const load=require('../../menu/tests/load.cjs');
const env=load(['games/bank.js']);
const M=env.MKMENU, GB=env.MKGAMES;
const units=M.CATALOG.find(c=>c.course==='Geometry').units.map(u=>u[0]);
const levels=['cp2','cp1','honors'];
const repeats=+(process.env.FLASH_REPEATS||2);
let checked=0, failed=[], rows=[];
assert.equal(units.length,10,'Expected all 10 Geometry units');
for(const unit of units){
 const set=M.skillSets[unit];
 assert.ok(set,'Missing Geometry bank: '+unit);
 assert.ok(set.skills.length,'Empty skill bank: '+unit);
 for(const level of levels){
  const tiers=GB.LEVELS[level].tiers;
  let successes=0, attempted=0;
  for(const skill of set.skills){
   for(const c of tiers){
    let found=false;
    for(let i=0;i<repeats;i++){
     attempted++;
     const items=GB.makeItems(unit,skill.id,c,{intOnly:c<=5,level:'game'},'flash-qa|'+unit+'|'+level+'|'+skill.id+'|'+c+'|'+i,null);
     for(const item of items){
      checked++;
      if(!item.answer||!item.q)failed.push(unit+'/'+skill.id+' '+level+' c'+c+': blank answer or question');
      if(item.options.filter(o=>o.ok).length!==1)failed.push(unit+'/'+skill.id+' '+level+' c'+c+': wrong correct-choice count');
      if(!GB.answerOk(item.p,item.k,item.answer).ok)failed.push(unit+'/'+skill.id+' '+level+' c'+c+': answer rejected by independent verifier');
      for(const opt of item.options){
       if(GB.answerOk(item.p,item.k,opt.a).ok!==opt.ok)failed.push(unit+'/'+skill.id+' '+level+' c'+c+': invalid distractor');
      }
      if(item.typed){
       const typed=GB.typedForm(item.p.parts[item.k]);
       if(typed&&!GB.checkTyped(item,typed).ok)failed.push(unit+'/'+skill.id+' '+level+' c'+c+': typed key rejected');
      }
     }
     if(items.length){found=true;successes++;break;}
    }
    if(!found)failed.push(unit+'/'+skill.id+' '+level+' c'+c+': NO verified flashcard after '+repeats+' attempts');
   }
  }
  rows.push({unit,level,skills:set.skills.length,successfulTiers:successes,expectedTiers:set.skills.length*tiers.length,attempted});
 }
}
rows.forEach(r=>console.log(r.unit+' '+r.level+': '+r.successfulTiers+'/'+r.expectedTiers+' skill tiers generated'));
if(failed.length){
 console.error('FAIL: '+failed.length+' findings across '+checked+' cards');
 [...new Set(failed)].slice(0,100).forEach(s=>console.error(' - '+s));
 process.exitCode=1;
}else console.log('PASS: '+units.length+' Geometry units x '+levels.length+' difficulty levels; '+checked+' independently checked cards');
