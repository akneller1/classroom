#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'worksheet-generator/approved-games.html'),'utf8');
const js=fs.readFileSync(path.join(root,'worksheet-generator/approved-games.js'),'utf8');
new vm.Script(js);
for(const id of ['agStatus','agApp','agGame','agLevel','agSkill','agReset','agTurn','agGrid','agQuestion','agPrompt','agOptions','agReveal','agSolution','agCorrect','agWrong'])
 assert.ok(html.includes('id="'+id+'"'),'Missing control: '+id);
for(const game of ['connect-4','tic-tac-toe','picture-reveal'])assert.ok(html.includes('value="'+game+'"'),'Missing game '+game);
assert.ok(js.includes('MK_APPROVED_GAME_ITEMS.prepare'),'Must use approved adapter');
assert.ok(js.includes('MK_QUESTION_BANKS.available'),'Do not serve unapproved unit');
assert.ok(!js.includes('innerHTML'),'Do not inject question text as HTML');
assert.ok(js.includes('row=5;row>=0;row--'),'Connect 4 gravity rule');
assert.ok(js.includes('selectedAnswer=-1'),'Clear answers between turns');
assert.ok(js.includes("x==='-'"),'Picture Reveal must complete only when all tiles are cleared');
assert.ok(js.includes("selectedAnswer>=0"),'Selected multiple choice must support automatic grading');
assert.ok(js.includes("judge(ok)"),'Multiple choice responses must affect the board');
console.log('PASS approved review game page structure and security gating');
