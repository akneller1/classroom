'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.join(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8');
const context={window:{location:{href:'https://mrksclassroom.com/'}}};
vm.runInNewContext(read('integrated-student-skills.js'),context);
vm.runInNewContext(read('integrated-student-share.js'),context);
const catalog=context.window.MK_INTEGRATED_STUDENT_SKILLS;
const share=context.window.MK_INTEGRATED_STUDENT_SHARE;
const gradeUnits=['place-value-number-sense','multi-digit-multiplication-division','decimal-operations','numerical-expressions-patterns','fraction-addition-subtraction','fraction-multiplication-division','measurement-conversions','volume-three-dimensional-figures','coordinate-plane-graphing','classifying-two-dimensional-figures','data-line-plots-problem-solving'];
const financeUnits=['income','budgeting','banking','credit','borrowing','investing','housing','insurance','college','retirement'];
test('Grade 5 and Financial Algebra student share catalog includes exact unit skill IDs',()=>{
 assert.deepEqual(Object.keys(catalog.grade5),gradeUnits);
 assert.deepEqual(Object.keys(catalog['financial-algebra']),financeUnits);
 assert.equal(Object.values(catalog.grade5).flat().length,55);
 assert.equal(Object.values(catalog['financial-algebra']).flat().length,40);
 for(const [course,units] of [['grade5',gradeUnits],['financial-algebra',financeUnits]]){
  for(const unit of units){
   const skills=catalog[course][unit];
   assert.ok(skills.length>=4,course+'/'+unit);
   assert.equal(new Set(skills.map(x=>x.id)).size,skills.length);
   for(const [index,skill] of skills.entries()){
    assert.equal(skill.id,unit+'-skill-'+String(index+1).padStart(2,'0'));
    assert.ok(skill.name.length>4);
   }
  }
 }
});
test('all ten financial game banks match the student share skill IDs',()=>{
 for(const unit of financeUnits){
  const bank=JSON.parse(read('financial/banks/'+unit+'.json'));
  assert.deepEqual(bank.skills.map(x=>x.id),Array.from(catalog['financial-algebra'][unit],x=>x.id));
 }
});
test('skill chooser is used only on resources that honor skill IDs',()=>{
 const item=(course,type,title,path)=>({courseId:course,type,title,path});
 assert.equal(share.supports(item('financial-algebra','Game','Tic Tac Toe','financial/games/index.html?unit=banking&game=tic-tac-toe')),true);
 assert.equal(share.supports(item('financial-algebra','Study Guide','Practice Test','financial/practice/index.html?unit=income')),true);
 assert.equal(share.supports(item('financial-algebra','Study Guide','Flashcards','financial/flashcards/index.html?unit=income')),true);
 assert.equal(share.supports(item('financial-algebra','Interactive','Decision Lab','financial/decision-lab/index.html?lab=income')),false);
 assert.equal(share.supports(item('grade5','Game','Math Quest','https://akneller1.github.io/FinancialAlgebra/worksheet-generator/grade5-games.html?unit=decimal-operations&game=math-quest')),true);
 assert.equal(share.supports(item('grade5','Game','Fraction Frenzy','https://akneller1.github.io/FinancialAlgebra/worksheet-generator/grade5-games.html?unit=fraction-addition-subtraction&game=fraction-frenzy')),false);
 assert.equal(share.supports(item('grade5','Study Guide','Understanding Check','https://akneller1.github.io/FinancialAlgebra/worksheet-generator/grade5-understanding-check.html?unit=decimal-operations')),true);
 assert.equal(share.supports(item('grade5','Study Guide','Flashcards','https://akneller1.github.io/FinancialAlgebra/worksheet-generator/grade5-flashcards.html?unit=decimal-operations')),false);
 assert.equal(share.supports(item('grade5','Project','School Project','https://akneller1.github.io/FinancialAlgebra/math5-project-x/index.html')),false);
});
test('both main page and Financial Algebra page load the skill chooser before using the buttons',()=>{
 for(const page of ['index.html','financial-algebra.html']){
  const html=read(page);
  assert.ok(html.includes('integrated-student-skills.js'));
  assert.ok(html.includes('integrated-student-share.js'));
  assert.ok(html.indexOf('integrated-student-share.js')<html.indexOf(page==='index.html'?'student-share-cards.js':'financial/classroom-site.mjs'));
 }
 assert.match(read('student-share-cards.js'),/MK_INTEGRATED_STUDENT_SHARE\.open\(resource\)/);
 assert.match(read('financial/classroom-site.mjs'),/MK_INTEGRATED_STUDENT_SHARE\.open\(resource\)/);
});
