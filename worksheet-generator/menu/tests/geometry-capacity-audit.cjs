/* Diagnostic only: measure how many distinct verified Geometry cards a single
   25-question assessment can obtain. Does not weaken mathematics tests.
   Run: node worksheet-generator/menu/tests/geometry-capacity-audit.cjs */
'use strict';
const fs = require('node:fs');
const M = require('./load.cjs')().MKMENU;
const LIMIT = 25;
const rows = [];
for (const set of Object.values(M.skillSets).filter(s => s.id.startsWith('geometry-'))) {
  for (const skill of set.skills) {
    for (const tier of [1, 5]) {
      const used = {keys:new Set(), sigs:new Set()};
      let made = 0, reason = '';
      for (let n = 0; n < LIMIT; n++) {
        const p = M.generateProblem(set.id, skill.id, tier,
          {intOnly:true, level:'test'},
          'capacity:'+set.id+':'+skill.id+':'+tier+':'+n, used);
        if (p.failed) { reason = String(p.reason || 'generation failed'); break; }
        if (!p.verify || p.verify.status !== 'verified') {
          reason = 'unverified problem'; break;
        }
        made++;
      }
      rows.push({unit:set.id,skill:skill.id,tier,made,reason});
    }
  }
}
const low = rows.filter(r=>r.made<LIMIT);
const byUnit = {};
for(const r of low) (byUnit[r.unit] ||= []).push(r);
console.log('Geometry capacity audit: '+rows.length+' skill/tier settings; '+low.length+
  ' below '+LIMIT+' distinct verified questions.');
for(const [unit, rs] of Object.entries(byUnit)) {
  console.log('\n'+unit);
  for(const r of rs) console.log('  '+r.skill+' tier '+r.tier+': '+r.made+'/'+LIMIT+
    (r.reason ? ' ('+r.reason+')' : ''));
}
const lines = [
  '## Geometry question-bank capacity audit',
  '',
  'Diagnostic only: a low count does **not** mean the mathematics is wrong. '+
    'Finite concept banks may legitimately have fewer than 25 unique prompts.',
  '',
  'Checked '+rows.length+' skill/tier combinations (tiers 1 and 5, integer-answer policy).',
  '',
  '| Unit | Skill | Tier | Verified unique cards | First failure |',
  '|---|---|---:|---:|---|'
];
for(const r of low) lines.push('| '+r.unit+' | '+r.skill+' | '+r.tier+
  ' | '+r.made+'/'+LIMIT+' | '+r.reason.replace(/\|/g,'/')+' |');
if (!low.length) lines.push('| All Geometry units | All sampled skills | 1, 5 | 25/25 | None |');
lines.push('', 'This report is advisory. Existing regression tests remain authoritative for correctness.');
if(process.env.GITHUB_STEP_SUMMARY)
  fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,lines.join('\n')+'\n');
