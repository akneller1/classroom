/* Geometry regression: every skill verifies at every tier, and repeated cards stay available. */
'use strict';
const assert = require('node:assert/strict');
const menu = require('./load.cjs')().MKMENU;
const units = Object.keys(menu.skillSets).filter(id => id.startsWith('geometry-'));
assert.equal(units.length, 10, 'Expected all ten Geometry units');
let checks = 0;
for (const unit of units) {
  for (const skill of menu.skillSets[unit].skills) {
    for (let c = 1; c <= 7; c++) {
      const used = {keys: new Set(), sigs: new Set()};
      const count = [1,3,5,7].includes(c) ? 25 : 1;
      for (let n = 0; n < count; n++) {
        const p = menu.generateProblem(unit, skill.id, c,
          {intOnly: true, level: 'game'},
          ['geometry-regression', unit, skill.id, c, n].join(':'), used);
        assert.ok(!p.failed, [unit, skill.id, 'tier '+c, 'card '+n, p.reason].join(' / '));
        assert.equal(p.verify.status, 'verified', unit + '/' + skill.id);
        checks++;
      }
    }
  }
}
// Unit 4 must retain the expanded curriculum, including four-part Open Response.
const triangleUnit = menu.skillSets['geometry-triangle-relationships'];
for (const id of ['triangle-inequality-max-integer','triangle-midsegment-length',
  'triangle-centroid-median','triangle-side-angle-order','triangle-perpendicular-bisector',
  'triangle-altitude-area','triangle-open-response-investigation']) {
  assert.ok(triangleUnit.skills.some(s => s.id === id),'Missing Unit 4 skill: '+id);
}
for (const c of [1,3,5,7]) {
  const p = menu.generateProblem('geometry-triangle-relationships',
    'triangle-open-response-investigation',c,{intOnly:true,level:'game'},
    'unit4-open-response:'+c,{keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,'Four-part triangle investigation must generate at tier '+c);
  assert.equal(p.parts.length,4,'Open Response must contain four independently checked parts');
  assert.equal(p.verify.status,'verified','All four parts must verify');
}
// Unit 4 diagrams must remain attached, render as SVG, and match their skill.
for (const [id,caseName] of [
  ['triangle-midsegment-length','midsegment'],
  ['triangle-centroid-median','centroid'],
  ['triangle-perpendicular-bisector','bisector'],
  ['triangle-altitude-area','altitude']
]) {
  for (const c of [1,3,5,7]) {
    const p = menu.generateProblem('geometry-triangle-relationships',id,c,
      {intOnly:true,level:'game'},'unit4-diagram:'+id+':'+c,
      {keys:new Set(),sigs:new Set()});
    assert.ok(!p.failed,'Expected valid '+id+' at tier '+c);
    assert.equal(p.fig && p.fig.kind,'geo-triangle-landmark');
    assert.equal(p.fig.case,caseName);
    assert.ok(menu.geoDiagram.validate(p.fig),'Unit 4 diagram must validate');
    assert.ok(menu.geoDiagram.render(p.fig).includes('<svg'),'Unit 4 diagram must render');
  }
}
// Honors triangle investigation must be one connected four-part problem.
for (const c of [5,6,7]) {
  const p = menu.generateProblem('geometry-triangle-relationships',
    'triangle-honors-connected-investigation',c,{intOnly:false,level:'honors'},
    'honors-triangle-chain:'+c,{keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,'Honors investigation must generate at tier '+c);
  assert.equal(p.parts.length,4,'Honors investigation needs four parts');
  assert.equal(p.verify.status,'verified','All Honors steps must verify');
  for (const part of p.parts) {
    assert.equal(part.check.type,'solve','Each part must have an independent answer check');
  }
}
// A changed student-facing triangle measurement must invalidate the saved key.
for (const id of ['triangle-midsegment-length','triangle-centroid-median',
  'triangle-side-angle-order','triangle-perpendicular-bisector']) {
  const p = menu.generateProblem('geometry-triangle-relationships',id,3,
    {intOnly:true,level:'game'},'visible-triangle-mutation:'+id,
    {keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,'Triangle mutation fixture must generate: '+id);
  const changed = JSON.parse(JSON.stringify(p));
  changed.prompt = changed.prompt.replace(/(⟨[^⟩]*?)(\d+)/,
    (_,prefix,digits) => prefix + (Number(digits)+2));
  assert.notEqual(changed.prompt,p.prompt,'Fixture must alter visible triangle expression');
  assert.equal(menu.verifyProblem(changed,{intOnly:true,level:'game'}).ok,false,
    'Triangle verifier must reject a modified printed measure: '+id);
}
for (const scenario of ['shared','vertical']) {
  let p;
  for(let n=0;n<50&&!p;n++){
    const candidate=menu.generateProblem('geometry-triangles-congruence',
      'congruence-structured-proof',3,{intOnly:true,level:'game'},
      'proof-visible-mutation:'+scenario+':'+n,{keys:new Set(),sigs:new Set()});
    if(!candidate.failed&&candidate.fig.case===scenario)p=candidate;
  }
  assert.ok(p,'Proof mutation fixture must generate: '+scenario);
  const changed=JSON.parse(JSON.stringify(p));
  changed.prompt=changed.prompt.replace(/(⟨[^⟩]*?)(\d+)/,
    (_,prefix,digits)=>prefix+(Number(digits)+2));
  assert.notEqual(changed.prompt,p.prompt);
  assert.equal(menu.verifyProblem(changed,{intOnly:true,level:'game'}).ok,false,
    'Proof verifier must reject changed angle expression: '+scenario);
}
// A changed printed equation must never pass simply because the original
// dimensions still imply the saved answer.
for (const skillId of ['right-pythagorean-hypotenuse','right-pythagorean-leg','right-distance-formula']) {
  const p = menu.generateProblem('geometry-right-triangles-trigonometry',skillId,1,
    {intOnly:true,level:'game'},'mutation:'+skillId,
    {keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed, skillId+' must generate');
  const tampered = JSON.parse(JSON.stringify(p));
  const original = tampered.parts[0].check.eq;
  tampered.prompt = tampered.prompt.replace('⟨'+original+'⟩','⟨'+original.replace('^2','^4')+'⟩');
  assert.notEqual(tampered.prompt,p.prompt,'Mutation must change the printed equation');
  assert.equal(menu.verifyProblem(tampered,{intOnly:true,level:'game'}).ok,false,
    skillId+' must reject a modified printed equation');
}
// A visible side expression must agree with the equation used to verify x.
for (const kind of ['sss','sas','asa','aas','hl']) {
  const p = menu.generateProblem('geometry-triangles-congruence','congruence-'+kind,1,
    {intOnly:true,level:'game'},'congruence-equation-mutation:'+kind,
    {keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,'Expected verified '+kind+' congruence question');
  const changed = JSON.parse(JSON.stringify(p));
  changed.prompt = changed.prompt.replace(/⟨([^⟩]+)⟩/,function(_,expr){
    return '⟨'+expr.replace(/[0-9]+/,function(n){return String(+n+2);})+'⟩';
  });
  assert.notEqual(changed.prompt,p.prompt,'Visible side length must change');
  assert.equal(menu.verifyProblem(changed,{intOnly:true,level:'game'}).ok,false,
    'Verifier must reject mismatched printed side length for '+kind);
}
// Inspect actual SVG markings, not just the generator's claimed theorem.
// Tick counts include one/two/three stroke marks on each matching side pair.
const expectedMarks = {
  sss:[12,0], sas:[6,2], asa:[2,4], aas:[2,4],
  hl:[6,0], ssa:[6,2], aaa:[0,6]
};
for (const [criterion, expected] of Object.entries(expectedMarks)) {
  const fig = {kind:'geo-triangle-pair',criterion};
  const svg = menu.geoDiagram.render(fig);
  assert.ok(menu.geoDiagram.validate(fig),criterion+' diagram should be valid');
  const ticks = svg.split('stroke-width="1.7"').length - 1;
  const arcs = svg.split('stroke-width="1.5"').length - 1;
  assert.deepEqual([ticks,arcs],expected,criterion+' side/angle markings must match givens');
}
// Diagram-classification answers must fail if the labeled theorem is wrong.
for (let n = 0; n < 30; n++) {
  const p = menu.generateProblem('geometry-triangles-congruence','congruence-identify',5,
    {intOnly:true,level:'game'},'criterion-mutation:'+n,
    {keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,'Diagram classification should generate');
  const wrong = JSON.parse(JSON.stringify(p));
  wrong.parts[0].answer = p.parts[0].answer === 'SSS' ? 'SAS' : 'SSS';
  assert.equal(menu.verifyProblem(wrong,{intOnly:true,level:'game'}).ok,false,
    'Incorrect theorem must be rejected');
}
// Proof diagrams and independently checked reasons must agree with the printed givens.
for (const scenario of ['shared','vertical']) {
  let sample;
  for (let n = 0; n < 100 && !sample; n++) {
    const p = menu.generateProblem('geometry-triangles-congruence','congruence-structured-proof',5,
      {intOnly:true,level:'game'},'proof-regression:'+scenario+':'+n,
      {keys:new Set(),sigs:new Set()});
    if (!p.failed && p.fig && p.fig.case === scenario) sample = p;
  }
  assert.ok(sample,'Expected a '+scenario+' proof');
  assert.ok(menu.geoDiagram.validate(sample.fig),'Proof diagram must render');
  assert.equal(sample.verify.status,'verified','Proof must verify');
  const changed = JSON.parse(JSON.stringify(sample));
  changed.parts[0].answer = 'INCORRECT REASON';
  assert.equal(menu.verifyProblem(changed,{intOnly:true,level:'game'}).ok,false,
    'Incorrect proof reason must be rejected');
  const wrongScaffold = JSON.parse(JSON.stringify(sample));
  wrongScaffold.proofStatements[2] = 'Angle ABC is congruent to angle ADB';
  assert.equal(menu.verifyProblem(wrongScaffold,{intOnly:true,level:'game'}).ok,false,
    'Incorrect corresponding angle labels must be rejected');
  const wrongEquation = JSON.parse(JSON.stringify(sample));
  wrongEquation.proofStatements[3] = 'Solve ⟨x+9=99⟩ for x';
  assert.equal(menu.verifyProblem(wrongEquation,{intOnly:true,level:'game'}).ok,false,
    'Scaffold equation must agree with the original question');
  const wrongFigure = JSON.parse(JSON.stringify(sample));
  wrongFigure.fig.case = scenario === 'shared' ? 'vertical' : 'shared';
  // Proof reasons derive from the student-facing givens, not the drawing alone.
  assert.equal(menu.verifyProblem(wrongFigure,{intOnly:true,level:'game'}).ok,false,
    'Proof verifier must not silently use diagram type as the answer key');
}
require('./proof-print-layout.cjs');
console.log('Geometry generator regression passed: '+checks+' verified cards across '+units.length+' units.');
