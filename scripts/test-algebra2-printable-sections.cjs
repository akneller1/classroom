#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'worksheet-generator/bank-printable.html'),'utf8');
const js=fs.readFileSync(path.join(root,'worksheet-generator/bank-printable.js'),'utf8');
new vm.Script(js);
for(const id of ['sectionType','addSection','resetSections','saveLayout','loadLayout','exportLayout','importLayout','importFile','sectionList','versions','editor','currentVersion','editItems','build','print'])assert.ok(html.includes('id="'+id+'"'),id+' missing from HTML');
for(const fn of ['newSection','resetSections','renderSections','shiftSection','sectionQuestions','sectionsSnapshot'])assert.ok(js.includes('function '+fn+'('),fn+' missing');
for(const name of ['Do Now','Mixed Review','Notes','Examples','Practice','Challenge Problems','Summary','Exit Ticket'])assert.ok(js.includes("'"+name+"'"),name+' missing');
assert.ok(js.includes('sectionId:sec.id'),'Generated problems must retain section identity');
assert.ok(js.includes('versionSections[vi].forEach'),'Student and teacher previews must follow section order');
assert.ok(js.includes('mk-algebra2-section-layout-v1'),'Missing persistent configuration key');
assert.ok(js.includes('group.querySelectorAll(\'input:checked\')'),'Missing multiple skill selection');
assert.ok(js.includes('function snapshotLayout(') && js.includes('function applyLayout('),'Missing portable layout functions');
assert.ok(js.includes("sec.type==='Mixed Review'") && js.includes('grouped=new Map()'),'Mixed Review must balance across skills');
console.log('PASS Algebra 2 sections, mixed review, portable layouts, and syntax');
