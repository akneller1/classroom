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
console.log('Practice grader: '+passed+' exact-math assertions passed; unsupported formats remain self-checked.');
