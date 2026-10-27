/* Regression: printable proof layouts never leak teacher answers to student copies. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const context = {
  MKMENU: {},
  MKWS: {render:{math:function(s){return String(s);}}},
  document: {}
};
context.window = context;
context.globalThis = context;
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'..','render.js'),'utf8'),context);
const layout = context.MKMENU.proofLayout;
const printQuestion = context.MKMENU.promptHtml;
context.MKMENU.figHtml = function(fig){return '<figure data-case="'+fig.case+'"></figure>';};
assert.equal(typeof printQuestion,'function','Full question renderer should be available');
assert.equal(typeof layout,'function','Proof renderer should be available');
for (const scenario of ['shared','vertical']) {
  for (const format of ['flow','columns']) {
    const p = {
      variant:'geo-structured-proof-'+scenario+'-'+format+'-5',
      fig:{kind:'geo-proof',case:scenario},
      parts:[
        {answer:scenario==='shared'?'REFLEXIVE PROPERTY':'VERTICAL ANGLES THEOREM'},
        {answer:scenario==='shared'?'SSS':'SAS'},
        {answer:'CPCTC'},
        {answer:'⟨x=23⟩'}
      ]
    };
    p.prompt = 'Complete the proof using the diagram.';
    assert.equal(context.MKMENU.isWideProblem(p),true,'Proof must occupy the full printable width');
    assert.equal(context.MKMENU.workspaceHtml(p,{layout:{density:'standard',format:'worksheet',grid:'none'}}),'','Proof already provides writing space');
    const student = printQuestion(p,false),teacher = printQuestion(p,true);
    assert.ok(student.includes('<figure data-case="'+scenario+'"'),'Student question must include diagram');
    assert.ok(teacher.includes('<figure data-case="'+scenario+'"'),'Teacher question must include diagram');
    assert.ok(student.includes('__________________'),'Student proof must contain answer blanks');
    assert.ok(!student.includes('CPCTC'),'Student layout must not reveal the proof reasons');
    assert.ok(!student.includes('x=23'),'Student layout must not reveal x');
    assert.ok(teacher.includes('CPCTC'),'Teacher layout must contain proof reasons');
    assert.ok(teacher.includes('x=23'),'Teacher layout must contain the solution');
    assert.ok(student.includes(format==='flow'?'mm-proof-flow':'mm-proof-table'),'Correct format');
    assert.ok(teacher.includes(format==='flow'?'mm-proof-flow':'mm-proof-table'),'Teacher format');
  }
}
console.log('Proof print layout checks passed: four scenarios, student and teacher versions.');
