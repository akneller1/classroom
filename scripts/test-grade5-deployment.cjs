#!/usr/bin/env node
/* Regression guard for the exact public Grade 5 URL structure.
 * Both Pages workflows invoke this after assembly, before deploying.
 * The browser game page must resolve ../manifest.json to the packaged course
 * manifest and load the approved questions for all eleven units.
 */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const output = path.resolve(process.argv[2] || '_site');
const courseRoot = path.join(output, 'grade5');
const gameFile = 'worksheet-generator/grade5-games.html';
const gameUrl = new URL('https://example.test/grade5/' + gameFile);
const exists = rel => fs.existsSync(path.join(courseRoot, rel));
const read = rel => fs.readFileSync(path.join(courseRoot, rel), 'utf8');
const manifestPath = new URL('../manifest.json', gameUrl);
assert.equal(manifestPath.pathname, '/grade5/manifest.json', 'game manifest resolution');
for (const file of ['manifest.json','course-catalog.js','question-bank-adapter.js',
  'question-bank-loader.js',gameFile,'worksheet-generator/grade5/g5-core.js',
  'worksheet-generator/grade5/g5-games.js']) {
  assert.ok(exists(file), 'Grade 5 public artifact missing ' + file);
}
const legacy=read('grade5.html');
assert.match(legacy,/location\.replace\('\.\/index\.html'/,'Legacy Grade 5 page must redirect');
assert.ok(exists('index.html'),'Grade 5 public redirect missing');
assert.match(read('index.html'), /#grade5/, 'Grade 5 entry must use the main Classroom site shell');
assert.match(read('index.html'), /noindex,follow/, 'Duplicate Grade 5 entry must not be indexed');
assert.ok(exists('grade5-main-catalog.js'), 'Approved shared catalog missing');
const shell={LIBRARY:{courses:[{id:'grade5',units:[]}]},MK_COURSE_CATALOG:{getSkills:()=>[],getSkillRecords:()=>[]}};shell.window=shell;
vm.runInNewContext(read('grade5-main-catalog.js'),shell,{filename:'grade5-main-catalog.js'});
const grade=shell.LIBRARY.courses.find(c=>c.id==='grade5');
assert.equal(grade.units.length,11,'Canonical Grade 5 catalog has all units');
for(const unit of grade.units)assert.ok(unit.artifacts.some(a=>a.title==='Error Analysis'),unit.id+' missing Error Analysis');
assert.ok(shell.MK_GRADE5_STANDARDS,'CCSS tags missing from shared catalog');
const oldHome=new URL('../grade5.html#math5.multi-digit-multiplication-division',gameUrl);
assert.equal(oldHome.pathname,'/grade5/grade5.html','Legacy game home should resolve inside Grade 5');
assert.ok(exists(oldHome.pathname.slice('/grade5/'.length)),'Game home 404');
const html = read(gameFile);
assert.match(html, /grade5\/g5-core\.js/);
assert.match(html, /grade5\/g5-games\.js/);
assert.match(html,/g5-games\.js\?v=math-race-right-facing-20261112/,'Grade 5 game must use the right-facing car script');
assert.match(html,/g5-core\.js\?v=grade5-home-link-20261112/,'Game must load updated working-home chrome');
const raceSource=read('worksheet-generator/grade5/g5-games.js');
assert.match(raceSource,/var carX = 80 \+ pos\[t\]/,'Math Race car must follow its position');
assert.match(raceSource,/transform="translate\(' \+ \(2 \* carX\) \+ ' 0\) scale\(-1 1\)"/,'Math Race cars must face right');
assert.match(read('worksheet-generator/grade5/g5-core.js'),
  /loadUnitFromSite\(COURSE, unitId, null, '\.\.\/'\)/,
  'test expects the current browser-relative manifest loader');
assert.ok(read('worksheet-generator/grade5/g5-core.js').includes("home.href = 'https://mrksclassroom.com/'"), 'Game homepage must point to Classroom');
assert.match(read('worksheet-generator/grade5/g5-core.js'), /p\.meta\.questionType === 'multi-step'/,
  'Multi-step instruction must be presented from verified question metadata, not appended to bank prompts');
const manifest = JSON.parse(read('manifest.json'));
assert.equal(manifest.version, 1);
const selected = manifest.banks.filter(entry => entry.courseId === 'math5');
assert.equal(selected.length,11,'Grade 5 units must all be published');
assert.equal(new Set(selected.map(e=>e.unitId)).size,11,'duplicate Grade 5 units');
selected.forEach(entry => {
  assert.equal(entry.approved,true,entry.unitId+' was not approved');
  assert.match(entry.path,/^math5\/[a-z0-9-]+\.json$/);
  assert.ok(exists(entry.path),entry.path+' is not published');
  const bank = JSON.parse(read(entry.path));
  assert.equal(bank.courseId,'math5');
  assert.equal(bank.unitId,entry.unitId);
  assert.ok(Array.isArray(bank.questions)&&bank.questions.length>0,
    entry.unitId+' has no questions');
});
const siteBase = new URL('https://example.test/');
const runtime = {};
runtime.fetch = async function(ref){
  const resolved = new URL(ref,gameUrl);
  assert.equal(resolved.origin,siteBase.origin,'Unexpected cross-origin fetch');
  assert.ok(resolved.pathname.startsWith('/grade5/'),'Path escapes published Grade 5');
  const local = decodeURIComponent(resolved.pathname.slice('/grade5/'.length));
  const target = path.resolve(courseRoot,local);
  assert.ok(target.startsWith(courseRoot+path.sep),'Fetch escapes Grade 5 root');
  if (!fs.existsSync(target)) return {ok:false,status:404,json:async()=>{throw Error('404 '+resolved.pathname);}};
  return {ok:true,status:200,json:async()=>JSON.parse(fs.readFileSync(target,'utf8'))};
};
runtime.window = runtime;
const sandbox = {window:runtime,Promise,URL};
vm.runInNewContext(read('course-catalog.js'),sandbox,{filename:'course-catalog.js'});
vm.runInNewContext(read('question-bank-adapter.js'),sandbox,{filename:'question-bank-adapter.js'});
vm.runInNewContext(read('question-bank-loader.js'),sandbox,{filename:'question-bank-loader.js'});
Promise.all(selected.map(({unitId}) =>
  runtime.MK_BANK_LOADER.loadUnitFromSite('math5',unitId,null,'../')
)).then(results => {
  assert.equal(results.length,11);
  for (const {unitId} of selected) assert.ok(
    runtime.MK_QUESTION_BANKS.available('math5',unitId),
    unitId+' not loaded by browser question loader');
  console.log('PASS Grade 5 public games: manifest resolves; all 11 approved unit banks load.');
}).catch(error=>{console.error(error);process.exitCode=1;});
