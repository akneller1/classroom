// Writes the Discrete Math site-integration patch: one data.js block (games, generators, partner checks, cheat sheets,
// Interactive Math, planned=false) inserted right after the Precalculus/Calculus "planned=false" line so the existing
// Millionaire block picks the course up, plus resource-details.js entries. Idempotent: re-running replaces the block.
// Usage (repository root): node tools/discrete-math/integration.cjs
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
global.window = global; require(path.join(ROOT, 'data.js'));
const course = LIBRARY.courses.find(c => c.id === 'discrete');
const ADDED = '2026-11-09';
const cap = s => s[0].toUpperCase() + s.slice(1);
const partner = [], sheets = {}, details = {};
course.units.forEach((u, i) => {
  for (const n of [1, 2]) {
    const p = `artifacts/discrete-${u.id}-partner-check-${n}/worksheet.pdf`;
    if (!fs.existsSync(path.join(ROOT, p))) throw Error('missing ' + p);
    partner.push({ unit: u.id, a: { title: `Partner Check ${n}: ${u.name}`, path: p, thumb: `thumbs/discrete-${u.id}-partner-check-${n}.jpg`,
      description: 'Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.',
      type: 'Printable', level: ['CP2', 'CP1', 'Honors'], topics: ['Partner Check', u.name], added: ADDED } });
    details[p] = { pages: 6, answerKey: 'artifacts/discrete-partner-checks/teacher-key.pdf', keyPages: 30 };
  }
  const cs = require(path.join(ROOT, 'scripts/cheat-sheets/content/discrete-' + u.id + '.cjs'));
  const p = `artifacts/discrete-${u.id}-cheat-sheet/worksheet.pdf`;
  if (!fs.existsSync(path.join(ROOT, p))) throw Error('missing ' + p);
  sheets[u.id] = { title: u.name + ' Cheat Sheet', path: p, thumb: `thumbs/discrete-${u.id}-cheat-sheet.jpg`,
    description: `Two-page printable cheat sheet. Front: ${cs.focus}. Back: ${cs.morefocus}. Key vocabulary, worked examples with every answer checked, and common mistakes.`,
    type: 'Printable', topics: ['Cheat sheet', 'Reference', u.name, 'Unit ' + (i + 1)], added: ADDED };
  details[p] = { pages: 2, referenceSheet: true };
});
const M = require(path.join(ROOT, 'tools/interactive-math-discrete/manifest.json'));
const tools = M.tools.map(t => ({ unit: t.unit, a: { title: t.title, path: `artifacts/${t.slug}/index.html`, bankFormat: 'interactive-math', type: 'Interactive', thumb: `thumbs/${t.slug}.jpg`,
  description: t.description, topics: t.topics, worksheet: `artifacts/${t.slug}/worksheet.pdf`, answerKey: `artifacts/${t.slug}/teacher-key.pdf`, added: ADDED } }));
tools.push({ unit: 'linear-programming', a: { title: 'Feasible Region Optimizer', path: 'artifacts/algebra2-feasible-region-optimizer/index.html', bankFormat: 'interactive-math', type: 'Interactive', thumb: 'thumbs/algebra2-feasible-region-optimizer.jpg',
  description: 'Explore a linear programming problem: see the feasible region, slide the objective line, and discover why the maximum and minimum occur at vertices.', topics: ['Linear programming', 'Feasible region', 'Optimization'],
  worksheet: 'artifacts/algebra2-feasible-region-optimizer/worksheet.pdf', answerKey: 'artifacts/algebra2-feasible-region-optimizer/teacher-key.pdf', added: ADDED } });
const block = `/* Discrete Math (2026-11-09): approved question banks in every shared game, generator and study guide, plus partner checks,
   unit cheat sheets and Interactive Math (built by the discrete-math and interactive-math-discrete tools). Must stay above the
   Math Millionaire block, which only adds games to courses that are no longer planned. */
(function(G){
 var c=G.LIBRARY.courses.find(function(x){return x.id==='discrete';});if(!c)return;
 var P=${JSON.stringify(partner)};
 var S=${JSON.stringify(sheets)};
 var T=${JSON.stringify(tools)};
 var add=function(u,a){if(u&&!u.artifacts.some(function(x){return x.path===a.path;}))u.artifacts.push(a);};
 var unit=function(id){return c.units.find(function(u){return u.id===id;});};
 c.units.forEach(function(u){
  [['showdown','Showdown','showdown'],['connect-four','Connect 4','connect-four'],['tic-tac-toe','Tic-Tac-Toe','tic-tac-toe'],['escape-room','Escape Room','escape-rooms'],['detective','Detective','detective-games'],['picture-reveal','Picture Reveal','picture-reveal'],['flashcards','Flashcards','flashcards']].forEach(function(g){
   add(u,{title:u.name+' '+g[1],path:'worksheet-generator/'+(['escape-room','detective'].indexOf(g[0])>=0?'course-activity':'course-game')+'.html?course=discrete&unit='+u.id+'&game='+g[0],bankFormat:g[2],type:g[0]==='flashcards'?'Study Guide':'Game',thumb:'thumbs/foundations-algebra-'+(g[0]==='flashcards'?'flashcards':['detective','escape-room'].indexOf(g[0])>=0?'showdown':g[0])+'.jpg',description:'Choose Discrete Math skills and CP2, CP1, or Honors questions from the approved bank.',level:['CP2','CP1','Honors'],topics:[u.name],added:'${ADDED}'});
  });
  add(u,{title:'Vocabulary Activities and Crosswords',path:'worksheet-generator/printables.html#unit=discrete-'+u.id+'&kind=vocabulary',type:'Printable',thumb:'thumbs/vocabulary-prealgebra.svg',description:'Matching, fill-in-the-blank, examples, and crosswords using the unit vocabulary.',level:['CP2','CP1','Honors'],topics:[u.name],added:'${ADDED}'});
  [['error','Error Analysis','error-generator-foundations.svg','Find, explain, and correct mistakes using authored Discrete Math questions. Includes teacher solutions.'],['tarsia','Tarsia Puzzle','tarsia-generator-foundations.svg','Match problems and answers to assemble a triangle puzzle. Includes work pages and a solved teacher key.'],
   ['maze','Maze','maze-generator-foundations.svg','Follow a route of correctly answered questions through a mathematical maze. Uses Discrete Math questions and a teacher key.'],['color','Color by Number','geometry-color-generator-basics-reasoning.svg','Solve problems to reveal a color-coded picture. Uses Discrete Math questions and a teacher key.'],
   ['partner','Partner Check','partner-generator-foundations.svg','Solve and compare matched-answer problems in pairs. Uses Discrete Math questions and a teacher key.'],['stations','Station Work','stations-generator-foundations.svg','Rotate through independent stations with mixed problem types. Uses Discrete Math questions and a teacher key.'],
   ['who','Whodunnit','foundations-algebra-whodunnit.jpg','Solve clues and narrow down the mystery. Uses Discrete Math questions and a teacher key.']].forEach(function(k){
   add(u,{title:k[1]+' Generator',path:'worksheet-generator/printables.html#unit=discrete-'+u.id+'&kind='+k[0],bankFormat:'printable-generator',type:'Printable',thumb:'thumbs/'+k[2],description:k[3],level:['CP2','CP1','Honors'],topics:[u.name],added:'${ADDED}'});
  });
  add(u,{title:'Assessment Readiness Check',path:'worksheet-generator/practice-test.html#unit=discrete-'+u.id,bankFormat:'interactive-practice-test',type:'Study Guide',thumb:'thumbs/practice-test.svg',description:'Practice Discrete Math skills, review worked solutions, and target skills for reassessment.',level:['CP2','CP1','Honors'],topics:[u.name],added:'${ADDED}'});
  if(S[u.id])add(u,S[u.id]);
 });
 P.forEach(function(it){add(unit(it.unit),it.a);});
 T.forEach(function(it){add(unit(it.unit),it.a);});
 c.planned=false;
})(window);
`;
fs.writeFileSync(path.join(__dirname, 'patches/data.discrete-block.js'), block);
const dp = path.join(ROOT, 'data.js'); let d = fs.readFileSync(dp, 'utf8');
d = d.replace(/\/\* Discrete Math \(2026-11-09\)[\s\S]*?\n\}\)\(window\);\n\n/, '');
const anchor = '(function(G){ G.LIBRARY.courses.filter(c=>["precalculus","calculus"].includes(c.id)).forEach(c=>{c.planned=false;}); })(window);\n';
if (!d.includes(anchor)) throw Error('anchor not found in data.js');
d = d.replace(anchor, anchor + '\n' + block + '\n');
fs.writeFileSync(dp, d);
const rp = path.join(ROOT, 'resource-details.js'); let r = fs.readFileSync(rp, 'utf8');
const lines = Object.entries(details).filter(([k]) => !r.includes(JSON.stringify(k) + ':')).map(([k, v]) => '  ' + JSON.stringify(k) + ': ' + JSON.stringify(v, null, 2).replace(/\n/g, '\n  '));
if (lines.length) { r = r.replace(/\n\};\s*$/, ',\n' + lines.join(',\n') + '\n};\n'); fs.writeFileSync(rp, r); }
fs.writeFileSync(path.join(__dirname, 'patches/resource-details.discrete-entries.json'), JSON.stringify(details, null, 2));
console.log('data.js block written;', partner.length, 'partner checks,', Object.keys(sheets).length, 'cheat sheets,', tools.length, 'interactive tools; resource-details +' + lines.length);
