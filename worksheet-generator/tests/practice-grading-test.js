/* Run: node worksheet-generator/tests/practice-grading-test.js */
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const base=path.join(__dirname,'..');const context={};context.window=context;vm.createContext(context);
for(const file of ['menu/mathcheck.js','practice/grading.js'])vm.runInContext(fs.readFileSync(path.join(base,file),'utf8'),context,{filename:file});
const checker=context.MKPRACTICE;let passed=0;
function check(answer,input,expected){
 const problem={parts:[{answer}]};
 assert.strictEqual(checker.supports(problem),true,'unsupported '+answer);
 assert.strictEqual(checker.grade(problem,input).status,expected,answer+' / '+input);passed++;
}
check('⟨x=\\frac{1}{2}⟩','x=0.5','correct');
check('⟨x=\\frac{1}{2}⟩','x=2','incorrect');
check('⟨-3⟩','-3','correct');
check('⟨-3⟩','3','incorrect');
check('⟨(2,-3)⟩','(2, -3)','correct');
check('⟨(2,-3)⟩','(-3,2)','incorrect');
check('⟨x=2⟩ or ⟨x=-3⟩','x=-3 or x=2','correct');
check('⟨x=2⟩ or ⟨x=-3⟩','x=2 or x=3','incorrect');
check('No solution','No solution','correct');
check('All real numbers','No solution','incorrect');
check('⟨y=2x+4⟩','y=2(x+2)','correct');
check('⟨y=2x+4⟩','y=2x+3','incorrect');
check('⟨2x+4⟩','4+2x','correct');
check('⟨2x+4⟩','2x+5','incorrect');
check('⟨x\\le 3⟩','x <= 3','correct');
check('⟨x\\le 3⟩','x > 3','incorrect');
check('⟨4⟩','2+2','correct');
check('⟨4⟩','3','incorrect');
assert.strictEqual(checker.supports({parts:[{answer:'⟨3⟩',answerFig:{kind:'plane'}}]}),false);
assert.strictEqual(checker.supports({parts:[{answer:'⟨3⟩'},{answer:'⟨4⟩'}]}),false);
assert.strictEqual(checker.grade({parts:[{answer:'⟨3⟩'}]},'not algebra').status,'invalid');
check('⟨x=2⟩ or ⟨x=-3⟩','x=2 or x=2','incorrect');
check('⟨(2,-3)⟩','(2,-2)','incorrect');
check('⟨y=2x+4⟩','y=2x+4','correct');
check('⟨x\\ge -2⟩','x >= -2','correct');
assert.strictEqual(checker.grade({parts:[{answer:'⟨x=3⟩'}]},'x=abc').status,'invalid');
assert.strictEqual(checker.grade({parts:[{answer:'⟨x=3⟩'}]},'').status,'empty');
console.log('Practice grader: '+passed+' exact-math assertions passed; unsupported formats remain self-checked.');


/* Regression tests for interactive graph answer checkers, not just numeric responses. */
for(const file of ['practice/graph-input.js','practice/line-input.js','practice/parabola-input.js','practice/exponential-input.js','practice/system-input.js'])
  vm.runInContext(fs.readFileSync(path.join(base,file),'utf8'),context,{filename:file});
function graphProblem(answer,check){return {prompt:'Graph the given function or inequality.',parts:[{answer,check}]};}
const L=context.MKLINE,P=context.MKPARABOLA,E=context.MKEXPGRAPH,S=context.MKSYSTEM;
const lq={problem:graphProblem('y=2x+1'),response:'line:'+JSON.stringify({points:[[0,1],[1,3]],dashed:false,shade:null})};
assert.strictEqual(L.target(lq).a,-2);
assert.strictEqual(L.grade(lq).status,'correct');passed++;
const li={problem:graphProblem('y<2x+1'),response:'line:'+JSON.stringify({points:[[0,1],[1,3]],dashed:true,shade:-1})};
assert.strictEqual(L.grade(li).status,'correct');passed++;
assert.strictEqual(L.grade({...li,response:'line:'+JSON.stringify({points:[[0,1],[1,3]],dashed:true,shade:1})}).status,'incorrect');passed++;
const pq={problem:graphProblem('y=(x-1)^2+2'),response:'parabola:'+JSON.stringify([[1,2],[-1,6],[0,3],[2,3],[3,6]])};
assert.strictEqual(P.grade(pq).status,'correct');passed++;
assert.strictEqual(P.grade({...pq,response:'parabola:'+JSON.stringify([[1,2],[-1,6],[0,3],[2,4],[3,6]])}).status,'incorrect');passed++;
const expq={problem:graphProblem('⟨y=4\cdot 2^{x}+1⟩',{type:'exp-graph-points',a:4,n:2,d:1,k:1}),response:'expplot:'+JSON.stringify({'-1':3,0:5,1:9})};
assert.strictEqual(E.grade(expq).status,'correct');passed++;
assert.strictEqual(E.grade({...expq,response:'expplot:'+JSON.stringify({'-1':2,0:5,1:9})}).status,'incorrect');passed++;
const sq={problem:graphProblem('',{type:'graph-key',eqs:['y=2x+1','y=-x+4']}),response:'system:'+JSON.stringify([[[0,1],[1,3]],[[0,4],[1,3]]])};
assert.strictEqual(S.grade(sq).status,'correct');passed++;
assert.strictEqual(S.grade({...sq,response:'system:'+JSON.stringify([[[0,1],[1,3]],[[0,4],[1,4]]])}).status,'incorrect');passed++;
console.log('Interactive graph graders: 9 additional exact-check assertions passed.');


/* Ensure the report never crashes on unanswered questions or serialized graph answers. */
const practiceSource=fs.readFileSync(path.join(base,'practice/practice.js'),'utf8');
const labelStart=practiceSource.indexOf('function responseLabel(q){');
const labelEnd=practiceSource.indexOf('\nfunction results(){',labelStart);
assert(labelStart>=0&&labelEnd>labelStart,'Response label helper must exist');
const responseLabel=new Function(practiceSource.slice(labelStart,labelEnd)+';return responseLabel;')();
assert.strictEqual(responseLabel({response:null}),'(blank)');
assert.strictEqual(responseLabel({response:''}),'(blank)');
assert.strictEqual(responseLabel({response:'line:{"points":[]}'}),'Drawn line and shading');
assert.strictEqual(responseLabel({response:'point:-2,3'}),'Plotted point -2,3');
assert(practiceSource.includes("if(q.kind==='mc'){q.correct="),'Multiple-choice must not be graded again as a free-response question');
console.log('Report and multiple-choice regression assertions passed.');


/* Number-line answer semantics: direction, endpoint inclusion, and compound rays. */
const NG=context.MKGRAPH;
function numberlineQ(pieces,response){return {kind:'auto',problem:{parts:[{answerFig:{kind:'numberline',min:-10,max:10,pieces}}]},response:'graph:'+JSON.stringify(response)};}
assert.strictEqual(NG.grade(numberlineQ([{lo:2,hi:null,loC:false,hiC:false}],[{lo:2,hi:null,loC:false,hiC:false}])).status,'correct');
assert.strictEqual(NG.grade(numberlineQ([{lo:2,hi:null,loC:false,hiC:false}],[{lo:null,hi:2,loC:false,hiC:false}])).status,'incorrect');
assert.strictEqual(NG.grade(numberlineQ([{lo:2,hi:null,loC:true,hiC:false}],[{lo:2,hi:null,loC:false,hiC:false}])).status,'incorrect');
assert.strictEqual(NG.grade(numberlineQ([{lo:null,hi:-3,loC:false,hiC:false},{lo:2,hi:null,loC:true,hiC:false}],[{lo:2,hi:null,loC:true,hiC:false},{lo:null,hi:-3,loC:false,hiC:false}])).status,'correct');
console.log('Number-line rays: direction, open/closed endpoints, and compound intervals checked.');

/* Student-facing assessment UX: responses live in each question card. */
const uxSource=fs.readFileSync(path.join(base,'practice/practice.js'),'utf8');
assert(uxSource.includes("function assessmentHTML(){"),'Every question should have an inline response surface');
assert(uxSource.includes("problemHTML(q)+'<div class=\"pt-inline-control\">'+answerControl(q,i)"),'Inline response immediately follows question');
assert(uxSource.includes("q.choices.opts.map(function(opt,j)"),'Multiple-choice buttons show the actual choice text');
assert(uxSource.includes("function updateProgress(){"),'Student progress needs an update handler');
assert(uxSource.includes("data-review-toggle"),'Students need mark-for-review controls');
assert(uxSource.includes("id=\"pt-print-paper\""),'Printable assessment remains separate');
console.log('Direct-answer student UX static regression assertions passed.');


/* Diagnostic feedback tests: distinguish slope, intercept, boundary and vertex errors. */
const lineBase={problem:graphProblem('y=2x+1'),response:'line:'+JSON.stringify({points:[[0,1],[1,3]],dashed:false,shade:null})};
assert.match(L.diagnose({...lineBase,response:'line:'+JSON.stringify({points:[[0,2],[1,4]],dashed:false,shade:null})}),/shifted/);
assert.match(L.diagnose({...lineBase,response:'line:'+JSON.stringify({points:[[0,1],[1,4]],dashed:false,shade:null})}),/slope/);
const parabolaBase={problem:graphProblem('y=(x-1)^2+2'),response:'parabola:'+JSON.stringify([[2,2],[-1,6],[0,3],[3,6],[4,11]])};
assert.match(P.diagnose(parabolaBase),/vertex/);
const feedbackSource=fs.readFileSync(path.join(base,'practice/practice.js'),'utf8');
assert(feedbackSource.includes('function diagnosticFeedback(q){'));
assert(feedbackSource.includes("return diagnosticFeedback(q)+'<div class="));
console.log('Individual graphing mistake diagnostics verified.');


/* Inline math keypad must insert supported, readable input and update autosaved answers. */
const padSource=fs.readFileSync(path.join(base,'practice/practice.js'),'utf8');
assert(padSource.includes('data-math-pad'), 'student short-answer keypad missing');
assert(padSource.includes('data-math-insert'), 'math keypad buttons missing');
assert(padSource.includes('G.MKMATHINPUT.insert(input.value,at,end,kind)'),'keys must use selection-aware math input helper');
assert(padSource.includes("input.dispatchEvent(new Event('input',{bubbles:true}))"),'keypad must notify autosave/grading');
assert(padSource.includes("['−','-']"), 'signed answer key missing');
assert(padSource.includes("['≤','<=']")&&padSource.includes("['≥','>=']"), 'inequality symbols missing');
console.log('Math keypad insertion, signed answers and autosave integration checks passed.');


/* Share controls appear on every unit self-assessment phase and remain setting-aware. */
const shareSource=fs.readFileSync(path.join(base,'practice/practice.js'),'utf8');
assert(shareSource.includes('function shareControls()'), 'missing reusable student link component');
assert(shareSource.includes('function bindShare()'), 'student share must bind to clipboard');
assert(shareSource.includes('function refreshStudentLink()'), 'changing skills and settings must update shared link');
assert((shareSource.match(/shareControls\(\)/g)||[]).length>=6, 'student link is not present in all assessment screens');
assert(shareSource.includes("params.set('unit'")||shareSource.includes("['unit',config.unit]"),'unit must be included in student URL');
for(const key of ['level','count','format','minutes','skills']){
 assert(shareSource.includes("['"+key+"',"), 'student URL missing '+key);
}
assert(shareSource.includes("root.querySelector('#pt-print-paper')")&&shareSource.includes('bindShare();root.querySelector'), 'share action should appear during the live test too');
console.log('Student link sharing and configurable assessment URL checks passed.');


/* Live preview is a display-only representation of submitted input. */
vm.runInContext(fs.readFileSync(path.join(base,'practice/math-preview.js'),'utf8'),context,{filename:'practice/math-preview.js'});
const PV=context.MKMATHPREVIEW;
assert.match(PV.toTex('3/4'),/\\frac\{3\}\{4\}/);
assert.match(PV.toTex('x^2'),/x\^\{2\}/);
assert.match(PV.toTex('x<=-2'),/\\le/);
assert.match(PV.toTex('sqrt(9)'),/\\sqrt\{9\}/);
assert.match(PV.toTex('2*3'),/\\cdot/);
assert.strictEqual(PV.preview('').empty,true);
assert(PV.preview('<img src=x onerror=alert(1)>').html.includes('&lt;img'), 'must escape fallback HTML');
const liveSource=fs.readFileSync(path.join(base,'practice/practice.js'),'utf8');
assert(liveSource.includes('data-preview='), 'inline preview slot missing');
assert(liveSource.includes('G.MKMATHPREVIEW.update(el'), 'live input handler missing');
console.log('Live math preview formatting and safe fallback checks passed.');

/* Editable templates: cursor selection, fraction denominator, square-root and powers. */
vm.runInContext(fs.readFileSync(path.join(base,'practice/math-input.js'),'utf8'),context,{filename:'practice/math-input.js'});
const MI=context.MKMATHINPUT;
const f0=MI.insert('',0,0,'fraction');assert.equal(f0.text,'0/1');assert.equal(f0.start,0);assert.equal(f0.end,1);
const f1=MI.insert('3',0,1,'fraction');assert.equal(f1.text,'3/1');assert.equal(f1.start,2);assert.equal(f1.end,3);
const next=MI.insert('3/1',1,1,'next');assert.equal(next.start,2);assert.equal(next.end,3);
const sq=MI.insert('',0,0,'sqrt');assert.equal(sq.text,'sqrt(0)');assert.equal(sq.start,5);assert.equal(sq.end,6);
const pw=MI.insert('x',1,1,'power');assert.equal(pw.text,'x^(2)');assert.equal(pw.start,3);assert.equal(pw.end,4);
const exp=MI.insert('x',1,1,'square');assert.equal(exp.text,'x^2');
assert.equal(MI.insert('1/2',3,3,'backspace').text,'1/');
assert.equal(MI.insert('x',1,1,'<=')['text'],'x<=');
console.log('Editable math fraction/radical/exponent caret and next-slot tests passed.');
