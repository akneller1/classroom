/* Geometry regression: every skill verifies at every tier, and repeated cards stay available. */
'use strict';
const assert = require('node:assert/strict');
const menu = require('./load.cjs')().MKMENU;
const units = Object.keys(menu.skillSets).filter(id => id.startsWith('geometry-'));
assert.equal(units.length, 10, 'Expected all ten Geometry units');
const GF = menu.geoFigures;
// A figure is acceptable only if it is a data-driven kind that passes its own geometric check and renders printable SVG.
function okFig(fig, kinds, what) {
  assert.ok(fig && kinds.includes(fig.kind), (what||'figure')+' must use one of '+kinds.join('/')+', got '+(fig&&fig.kind));
  const c = GF.check(fig);
  assert.ok(c.ok, (what||'figure')+' must pass its geometric check: '+c.msg);
  const svg = GF.render(fig);
  assert.ok(svg && svg.includes('<svg'), (what||'figure')+' must render');
  assert.ok(!/#(?!111|555|bbb|fff)[0-9a-f]{3,6}\b/i.test(svg), (what||'figure')+' must be print-safe');
}
let checks = 0;
for (const unit of units) {
  for (const skill of menu.skillSets[unit].skills) {
    for (let c = 1; c <= 7; c++) {
      // Independent seed coverage: a skill with only three exact-angle
      // outcomes cannot produce 25 distinct cards in a single used-set.
      const count = [1,3,5,7].includes(c) ? 25 : 1;
      for (let n = 0; n < count; n++) {
        const used = {keys: new Set(), sigs: new Set()};
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
// Unit 5 similarity must retain criterion coverage and printable figures.
const simUnit = menu.skillSets['geometry-similarity'];
for(const [id,figureCase] of [
  ['similarity-missing-side','sides'],
  ['similarity-angle','sides'],
  ['similarity-aa-criterion','aa'],
  ['similarity-sas-criterion','sas'],
  ['similarity-sss-criterion','sss']
]){
  assert.ok(simUnit.skills.some(skill=>skill.id===id),'Missing similarity skill '+id);
  for(const c of [1,3,5,7]){
    const p=menu.generateProblem('geometry-similarity',id,c,
      {intOnly:true,level:'game'},'similarity-diagram:'+id+':'+c,
      {keys:new Set(),sigs:new Set()});
    assert.ok(!p.failed,'Similarity question must generate: '+id+' c'+c);
    assert.equal(p.verify.status,'verified');
    okFig(p.fig,['geo-sim'],'Similarity figure '+id);
    assert.ok(menu.geoDiagram.validate(p.fig),'Similarity diagram must validate');
  }
}
// Shadow word problems: the figure is a true picture and the answer is recomputed from the printed numbers.
for(const c of [1,3,5,7]){
  const p=menu.generateProblem('geometry-similarity','similarity-shadow',c,{intOnly:true,level:'game'},'shadow-regression:'+c,{keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,'Shadow problem must generate at tier '+c);
  okFig(p.fig,['geo-shadow'],'Shadow figure');
  for(const re of [/(pole )(\d+)/,/(casts a )(\d+)(?=-foot shadow\.)/,/(nearby tree casts a )(\d+)/]){
    const t=JSON.parse(JSON.stringify(p));t.prompt=t.prompt.replace(re,(_,a,n)=>a+(Number(n)+1));
    assert.notEqual(t.prompt,p.prompt);
    assert.equal(menu.verifyProblem(t,{intOnly:true,level:'game'}).ok,false,'Changed printed shadow measurement must be rejected');
  }
}
// Two-step transformations: the key is recomputed from the printed vertices and both printed steps, and the three drawn triangles must agree.
for(const c of [1,3,5,7])for(let n=0;n<10;n++){
  const p=menu.generateProblem('geometry-transformations','compose-triangle-figure',c,{intOnly:true,level:'game'},'compose-regression:'+c+':'+n,{keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,'Composition must generate');
  okFig(p.fig,['geo-grid'],'Composition figure');
  assert.equal(p.fig.shapes.length,3,'Composition shows the original, the middle and the final triangle');
  for(const re of [/\((-?\d+), /,/translated (\d+)/,/(\d+) units? (?:up|down)/]){
    const t=JSON.parse(JSON.stringify(p));t.prompt=t.prompt.replace(re,(m0,d)=>m0.replace(d,String(Number(d)+1)));
    assert.notEqual(t.prompt,p.prompt);
    assert.equal(menu.verifyProblem(t,{intOnly:true,level:'game'}).ok,false,'Changed printed composition must be rejected');
  }
  const t=JSON.parse(JSON.stringify(p));t.fig.shapes[2].pts[0][0]+=1;
  assert.equal(menu.verifyProblem(t,{intOnly:true,level:'game'}).ok,false,'A drawn final triangle that disagrees with the steps must be rejected');
}
// Symmetry: the side count is read from the drawing (never printed), and the key follows it.
for(const id of ['symmetry-lines-regular','symmetry-rotation-regular'])for(const c of [1,3,5,7]){
  const p=menu.generateProblem('geometry-transformations',id,c,{intOnly:true,level:'game'},'symmetry-regression:'+id+':'+c,{keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,id+' must generate');
  okFig(p.fig,['geo-regular'],'Symmetry figure');
  assert.ok(!/\d+[- ]?(sides|gon)/.test(p.prompt),'The side count must not be printed');
  const t=JSON.parse(JSON.stringify(p));t.fig.n+=1;
  assert.equal(menu.verifyProblem(t,{intOnly:true,level:'game'}).ok,false,'A figure with a different number of sides must invalidate the key');
}
// Unit 10: every answer key is recomputed from the printed numbers (or, for nets and stacked solids, from the drawing alone).
for(const sk of menu.skillSets['geometry-area-surface-area-volume'].skills)for(const c of [1,3,5,7])for(let n=0;n<4;n++){
  const p=menu.generateProblem('geometry-area-surface-area-volume',sk.id,c,{intOnly:true,level:'game'},'measure-tamper:'+sk.id+':'+c+':'+n,{keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,sk.id+' must generate');
  const t=JSON.parse(JSON.stringify(p));
  if(p.fig.kind==='geo-net')t.fig.l+=1;else if(p.fig.kind==='geo-stack')t.fig.a.l+=1;else t.prompt=t.prompt.replace(/\d+/,m0=>String(Number(m0)+1));
  assert.equal(menu.verifyProblem(t,{intOnly:true,level:'game'}).ok,false,sk.id+' must reject a changed printed or drawn measurement');
}
// Parallel-segment proportionality and connected Honors investigation.
for(const id of ['similarity-parallel-segment','similarity-parallel-honors']){
  assert.ok(simUnit.skills.some(skill=>skill.id===id),'Missing similarity skill '+id);
  for(const c of [1,3,5,7]){
    const p=menu.generateProblem('geometry-similarity',id,c,
      {intOnly:true,level:'game'},'parallel-similarity:'+id+':'+c,
      {keys:new Set(),sigs:new Set()});
    assert.ok(!p.failed,'Parallel similarity must generate: '+id+' c'+c);
    assert.equal(p.verify.status,'verified');
    okFig(p.fig,['geo-tri-par'],'Parallel-segment figure');
    if(id==='similarity-parallel-honors'){
      assert.equal(p.parts.length,4,'Honors investigation must have four parts');
      assert.ok(p.parts.every(part=>part.check.type==='solve'));
    }
  }
}
// Unit 6 must retain exact special-triangle and elevation applications.
const rightUnit=menu.skillSets['geometry-right-triangles-trigonometry'];
for(const id of ['right-special-45-45-90','right-special-30-60-90','right-angle-elevation']){
  assert.ok(rightUnit.skills.some(skill=>skill.id===id),'Missing right-triangle skill '+id);
  for(const c of [1,3,5,7]){
    const p=menu.generateProblem('geometry-right-triangles-trigonometry',id,c,
      {intOnly:true,level:'game'},'right-special:'+id+':'+c,
      {keys:new Set(),sigs:new Set()});
    assert.ok(!p.failed,'Special right-triangle question must generate: '+id+' c'+c);
    assert.equal(p.verify.status,'verified');
    assert.equal(p.parts.length,1);
  }
}
// Unit 6 diagrams must be printable and correspond to the generated skill.
for(const [id,kind] of [
 ['right-pythagorean-hypotenuse','hyp'],
 ['right-pythagorean-leg','leg'],
 ['right-sine-side','sin'],
 ['right-cosine-side','cos'],
 ['right-tangent-side','tan'],
 ['right-special-45-45-90','45'],
 ['right-special-30-60-90','30'],
 ['right-angle-elevation','elevation']
]){
  for(const c of [1,3,5,7]){
    const p=menu.generateProblem('geometry-right-triangles-trigonometry',id,c,
      {intOnly:true,level:'game'},'right-diagram:'+id+':'+c,
      {keys:new Set(),sigs:new Set()});
    assert.ok(!p.failed,'Right-triangle diagram fixture must generate: '+id+' c'+c);
    assert.equal(p.verify.status,'verified');
    okFig(p.fig,['geo-rt'],'Right-triangle figure '+id);
    const markup=GF.render(p.fig);
    assert.ok(markup.includes('<svg')&&markup.includes('#fff'),
      'Right-triangle figure must be printable with a white label halo');
    if(kind==='elevation')assert.ok(p.fig.ang&&p.fig.ang.B!==undefined,'Elevation figure must carry its angle');
  }
}
// Connected Honors surveying: four verified parts, with a matching figure.
for(const c of [1,3,5,7]){
  const p=menu.generateProblem('geometry-right-triangles-trigonometry',
    'right-honors-survey',c,{intOnly:true,level:'game'},
    'honors-survey-regression:'+c,{keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,'Honors surveying investigation must generate at tier '+c);
  assert.equal(p.verify.status,'verified');
  assert.equal(p.parts.length,4,'Honors surveying requires four parts');
  okFig(p.fig,['geo-rt'],'Survey figure');
}
// Inverse-trig checks must derive the angle from the printed ratio.
for(const c of [1,3,5,7]){
  const p=menu.generateProblem('geometry-right-triangles-trigonometry',
    'right-inverse-trig',c,{intOnly:true,level:'game'},
    'inverse-trig-regression:'+c,{keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,'Inverse trig must generate at tier '+c);
  assert.equal(p.verify.status,'verified');
  assert.equal(p.parts[0].check.type,'geo-inverse-trig');
  assert.ok(menu.geoDiagram.validate(p.fig));
  const changed=Object.assign({},p,{prompt:p.prompt.replace(/x = (\d+)\/(\d+)/,
    (_,a,b)=>'x = '+(Number(a)+1)+'/'+b)});
  assert.notEqual(menu.verifyProblem(changed).status,'verified',
    'Changing the printed inverse-trig ratio must invalidate the answer');
}
// Calculator inverse trig: decimal answers and tamper resistance.
for(const c of [1,3,5,7]){
  const p=menu.generateProblem('geometry-right-triangles-trigonometry',
    'right-inverse-trig-decimal',c,{intOnly:true,level:'game'},
    'inverse-decimal-regression:'+c,{keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,'Decimal inverse trig must generate at tier '+c);
  assert.equal(p.verify.status,'verified');
  assert.equal(p.parts[0].check.roundTo,1);
  assert.match(p.prompt,/nearest tenth of a degree/);
  assert.ok(menu.geoDiagram.validate(p.fig));
  const changed=Object.assign({},p,{prompt:p.prompt.replace(/x = (\d+)\/(\d+)/,
    (_,a,b)=>'x = '+(Number(a)+1)+'/'+b)});
  assert.notEqual(menu.verifyProblem(changed).status,'verified',
    'Changing the printed decimal inverse-trig ratio must invalidate the answer');
}
// Exact radical checks must reject tampered side lengths.
for(const id of ['right-special-radical','right-angle-depression']){
 for(const c of [1,3,5,7]){
  const p=menu.generateProblem('geometry-right-triangles-trigonometry',id,c,
   {intOnly:true,level:'game'},'special-radical:'+id+':'+c,
   {keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed,'New right triangle skill must generate '+id);
  assert.equal(p.verify.status,'verified');
  assert.ok(menu.geoDiagram.validate(p.fig));
  if(id==='right-special-radical'){
   assert.equal(p.parts[0].check.type,'geo-special-radical');
   assert.match(p.parts[0].answer,/sqrt/);
   const changed=Object.assign({},p,{prompt:p.prompt.replace(/of length (\d+) units/,
    (_,n)=>'of length '+(Number(n)+1)+' units')});
   assert.notEqual(menu.verifyProblem(changed).status,'verified',
    'Changing printed special-triangle side must invalidate radical answer');
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
  ['triangle-midsegment-length','midseg'],
  ['triangle-centroid-median','centroid'],
  ['triangle-perpendicular-bisector','perpbis'],
  ['triangle-altitude-area','altitude']
]) {
  for (const c of [1,3,5,7]) {
    const p = menu.generateProblem('geometry-triangle-relationships',id,c,
      {intOnly:true,level:'game'},'unit4-diagram:'+id+':'+c,
      {keys:new Set(),sigs:new Set()});
    assert.ok(!p.failed,'Expected valid '+id+' at tier '+c);
    okFig(p.fig,['geo-tri'],'Unit 4 figure '+id);
    assert.equal(p.fig.mode,caseName,'Unit 4 figure must match its skill');
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
    if(!candidate.failed&&GF.cong.proofKind(candidate.fig)===scenario)p=candidate;
  }
  assert.ok(p,'Proof mutation fixture must generate: '+scenario);
  const changed=JSON.parse(JSON.stringify(p));
  changed.prompt=changed.prompt.replace(/(⟨[^⟩]*?)(\d+)/,
    (_,prefix,digits)=>prefix+(Number(digits)+2));
  assert.notEqual(changed.prompt,p.prompt);
  assert.equal(menu.verifyProblem(changed,{intOnly:true,level:'game'}).ok,false,
    'Proof verifier must reject changed angle expression: '+scenario);
}
// A changed printed dimension must never pass simply because the
// hidden check equation and saved answer have not changed.
for (const skillId of ['right-pythagorean-hypotenuse','right-pythagorean-leg','right-distance-formula']) {
  const p = menu.generateProblem('geometry-right-triangles-trigonometry',skillId,1,
    {intOnly:true,level:'game'},'mutation:'+skillId,
    {keys:new Set(),sigs:new Set()});
  assert.ok(!p.failed, skillId+' must generate');
  const tampered = JSON.parse(JSON.stringify(p));
  if (skillId === 'right-pythagorean-hypotenuse')
    tampered.prompt = tampered.prompt.replace(/(has legs )(\d+)/,(_,prefix,n)=>prefix+(Number(n)+1));
  else if (skillId === 'right-pythagorean-leg')
    tampered.prompt = tampered.prompt.replace(/(hypotenuse )(\d+)/,(_,prefix,n)=>prefix+(Number(n)+1));
  else
    tampered.prompt = tampered.prompt.replace(/(and B\()(\d+)/,(_,prefix,n)=>prefix+(Number(n)+1));
  assert.notEqual(tampered.prompt,p.prompt,'Mutation must change a printed measurement');
  assert.equal(menu.verifyProblem(tampered,{intOnly:true,level:'game'}).ok,false,
    skillId+' must reject a modified printed measurement');
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
// Inspect the actual markings: the criterion is derived from the marks, never from the generator's claim.
for (const kind of ['sss','sas','asa','aas','hl','ssa','aaa']) {
  for (const flip of [false,true]) {
    const fig = GF.cong.pair(kind,flip);
    okFig(fig,['geo-cong'],kind+' pair');
    assert.equal(GF.cong.derive(fig).toLowerCase(),kind,kind+' markings must imply '+kind);
  }
}
// Tampering with the marks must change the derived criterion or break the figure.
{
  const fig = JSON.parse(JSON.stringify(GF.cong.pair('sss',false)));
  fig.sides[0].s[1] = fig.sides[1].s[1];   // claim two unequal sides are equal
  assert.equal(GF.check(fig).ok,false,'False tick marks must be refused');
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
    if (!p.failed && p.fig && GF.cong.proofKind(p.fig) === scenario) sample = p;
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
  wrongFigure.fig = scenario === 'shared' ? GF.cong.cross() : GF.cong.shared();
  // Proof reasons derive from the student-facing givens, not the drawing alone.
  assert.equal(menu.verifyProblem(wrongFigure,{intOnly:true,level:'game'}).ok,false,
    'Proof verifier must not silently use diagram type as the answer key');
}
require('./proof-print-layout.cjs');
console.log('Geometry generator regression passed: '+checks+' verified cards across '+units.length+' units.');
