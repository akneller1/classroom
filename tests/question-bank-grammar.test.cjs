'use strict';
// Regression: singular grammar must be polished before any bank consumer selects a question.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const sandbox = {
  MK_COURSE_CATALOG: { getSkillRecords: () => [{ id: 'skill-01', name: 'Counting' }] }
};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '..', 'question-bank-adapter.js'), 'utf8'), sandbox);
const adapter = sandbox.MK_QUESTION_BANKS;
const prompts = [
  ['There are 3 bags with 10 cars in each. There are 1 more car. How many?', 'There are 3 bags with 10 cars in each. There is 1 more car. How many?'],
  ['There are 1 empty boxes.', 'There is 1 empty box.'],
  ['There are 1 red and 3 yellow counters.', 'There is 1 red counter and 3 yellow counters.'],
  ['There are 1 dot and 5 dots.', 'There is 1 dot and 5 dots.'],
  ['There are 1 yellow stickers in a bag.', 'There is 1 yellow sticker in a bag.'],
  ['There are 8 more crayons.', 'There are 8 more crayons.']
];
const bank = { schemaVersion: 1, courseId: 'grade1', unitId: 'sample', questions: prompts.map(([prompt], i) => ({
  id: 'q-' + i, skillId: 'skill-01', level: 'cp1', format: 'short-answer',
  prompt, answer: '31 cars', solutionSteps: [prompt],
  options: [{ text: prompt, correct: true }],
  check: { expression: '30+1', value: 31 }
})) };
assert.equal(adapter.register(bank, { verified: true }).ok, true);
const actual = adapter.select({ courseId: 'grade1', unitId: 'sample' });
for (let i = 0; i < prompts.length; i++) {
  assert.equal(actual[i].prompt, prompts[i][1], 'prompt ' + i);
  assert.equal(actual[i].solutionSteps[0], prompts[i][1], 'solution ' + i);
  assert.equal(actual[i].options[0].text, prompts[i][1], 'option ' + i);
  assert.equal(actual[i].answer, '31 cars', 'answer remains unchanged');
  assert.equal(actual[i].check.expression, '30+1', 'math check remains unchanged');
}
assert.equal(bank.questions[0].prompt, prompts[0][0], 'authored source is not mutated');
console.log('Question-bank singular grammar regression passed.');
