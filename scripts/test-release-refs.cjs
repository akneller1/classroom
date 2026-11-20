'use strict';
// The elementary print previews must be built from the same course commits the site deploys. Each workflow checks out
// FinancialAlgebra commits into _course_sources/<dir> and assembles a grade with GRADEn_SOURCE_DIR=_course_sources/<dir>;
// this resolves, for each grade, the commit each workflow uses and fails if they differ (for example after a new
// GRADE5_SOURCE_REF in deploy-site.yml without the matching change in elementary-print.yml).
const fs = require('fs'), path = require('path'), assert = require('assert');
const ROOT = path.resolve(__dirname, '..');

function refsByGrade(file) {
  const text = fs.readFileSync(path.join(ROOT, file), 'utf8');
  const env = {};
  for (const m of text.matchAll(/^\s+([A-Z0-9_]+):\s*([0-9a-f]{40})\s*$/gm)) env[m[1]] = m[2];
  const dirRef = {};
  // each checkout step: a "ref:" line followed (within the same "with:" block) by "path: _course_sources/<dir>"
  for (const m of text.matchAll(/ref:[ \t]*([^\n]+?)[ \t]*\n(?:\s+#.*\n|\s+[a-z-]+:.*\n)*?\s+path:\s*_course_sources\/([\w-]+)/g)) {
    let ref = m[1];
    const e = /^\$\{\{\s*env\.([A-Z0-9_]+)\s*\}\}$/.exec(ref);
    if (e) ref = env[e[1]];
    assert(/^[0-9a-f]{40}$/.test(ref || ''), `${file}: unresolved ref ${m[1]} for ${m[2]}`);
    dirRef[m[2]] = ref;
  }
  const grades = {};
  for (const m of text.matchAll(/GRADE([1-5])_SOURCE_DIR[:=]\s*_course_sources\/([\w-]+)/g)) {
    assert(dirRef[m[2]], `${file}: Grade ${m[1]} uses _course_sources/${m[2]}, which is not checked out`);
    if (grades[m[1]]) assert.strictEqual(grades[m[1]], dirRef[m[2]], `${file}: Grade ${m[1]} assembled from two different commits`);
    grades[m[1]] = dirRef[m[2]];
  }
  return grades;
}

const deploy = refsByGrade('.github/workflows/deploy-site.yml');
const print = refsByGrade('.github/workflows/elementary-print.yml');
const graded = Object.keys(print).sort();
assert(graded.length >= 5, 'expected Grades 1-5 in the print workflow, found ' + graded.join(', '));
const bad = graded.filter(g => deploy[g] !== print[g]);
for (const g of bad) console.error(`Grade ${g}: deploy-site.yml uses ${deploy[g] || '(none)'}, elementary-print.yml uses ${print[g]}`);
assert.strictEqual(bad.length, 0, 'elementary-print.yml must build each grade from the commit deploy-site.yml releases');
console.log('PASS release refs: Grades ' + graded.join(', ') + ' print from the commits the site deploys (' +
  graded.map(g => g + ':' + print[g].slice(0, 7)).join(' ') + ')');
