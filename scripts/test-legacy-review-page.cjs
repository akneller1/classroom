#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'worksheet-generator/legacy-review.html'),'utf8');
const js=fs.readFileSync(path.join(root,'worksheet-generator/legacy-review.js'),'utf8');
new vm.Script(js);
for(const id of ['reviewCourse','reviewTopic','reviewLevel','reviewCount','reviewLoad','reviewStatus','reviewList','reviewExport'])assert.ok(html.includes('id="'+id+'"'),id+' missing');
for(const script of ['../skill-crosswalk.js','../legacy-crosswalk-audit.js','../cross-course-difficulty.js','../legacy-review-samples.js','games/bank.js','legacy-review.js'])assert.ok(html.includes('src="'+script),script+' missing');
assert.ok(js.includes('approved:false'),'Export cannot grant question-bank approval');
assert.ok(js.includes('review:notes'),'Export must preserve reviewer decisions');
assert.ok(js.includes('text-only preview is insufficient'),'Diagrams must not be silently flattened');
console.log('PASS legacy teacher review page wiring, unapproved export contract, and diagram warning');
