#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'worksheet-generator/approved-flashcards.html'),'utf8');
const js=fs.readFileSync(path.join(root,'worksheet-generator/approved-flashcards.js'),'utf8');
new vm.Script(js);
for(const id of ['afStatus','afApp','afLevel','afSkill','afCard','afPrev','afNext','afFlip','afNeed','afGot','afShuffle','afMissed','afReset'])assert.ok(html.includes('id="'+id+'"'),'Missing '+id);
assert.ok(html.indexOf('question-bank-adapter.js')<html.indexOf('approved-flashcards.js'),'Question adapter must load first');
assert.ok(html.includes('question-bank-loader.js'),'Approved manifest loader required');
assert.ok(js.includes('banks.available(courseId,unitId)'),'Approval gating must be enforced');
assert.ok(js.includes("formats:['short-answer','multiple-choice']"),'Flashcards must filter compatible questions');
assert.ok(js.includes('function imagePath(q)') && js.includes('diagram(q,card)'), 'Safe diagram renderer required');
assert.ok(js.includes('question-banks') && js.includes('assets') && js.includes('imagePath(q)'), 'Only local diagram assets may be used');
assert.ok(!js.includes('innerHTML'),'Question content must render as text rather than injected HTML');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'question-banks/manifest.json'),'utf8'));
assert.deepEqual(manifest.banks,[],'No unreviewed content should be published');
console.log('PASS approved flashcard player structure, gating and content rendering safeguards');
