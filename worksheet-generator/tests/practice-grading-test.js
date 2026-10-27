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
