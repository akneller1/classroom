/* Production catalog regression tests: Grade 5 remains sourced from the
 * FinancialAlgebra repository, while the Classroom indexes its resources. */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const root = { LIBRARY: { courses: [] } };
root.window = root; root.globalThis = root;
vm.runInNewContext(fs.readFileSync(require('node:path').join(__dirname,'../course-integrations.js'),'utf8'),root);
const grade = root.LIBRARY.courses.find(c => c.id === 'grade5');
const expected = {
  lesson: 'lesson-planner', worksheet: 'worksheet-generator',
  assessment: 'assessment-generator', activity: 'printable-generator'
};
test('11 published units and no duplicated resources', () => {
  assert.equal(grade.units.length,11);
  for (const unit of grade.units) {
    assert.equal(new Set(unit.artifacts.map(a=>a.path)).size,unit.artifacts.length,unit.id);
  }
});
test('every Grade 5 unit indexes four core generators and Error Analysis', () => {
  for (const unit of grade.units) {
    const generators=unit.artifacts.filter(a=>a.type==='Generator');
    assert.equal(generators.length,5,unit.id);
    const error = generators.find(a=>a.title==='Error Analysis');
    assert.ok(error && error.visibleInBrowse, unit.id + ' Error Analysis');
    assert.equal(new URL(error.path,'https://mrksclassroom.com').searchParams.get('kind'),'error');
    for (const [mode, format] of Object.entries(expected)) {
      const found=generators.find(a=>a.bankFormat===format);
      assert.ok(found,unit.id+' '+mode);
      const url = new URL(found.path,'https://mrksclassroom.com');
      assert.equal(url.searchParams.get('unit'),unit.id);
      assert.equal(url.searchParams.get('mode'),mode);
      assert.equal(url.pathname,'/grade5/worksheet-generator/grade5-generators.html');
      assert.match(found.thumb,/math5-generator-.*\.svg$/);
    }
  }
});
test('Grade 5 homepage remains in the main course catalog', () => {
  assert.equal(grade.sourceUrl,undefined);
  assert.deepEqual(Array.from(root.MK_INTEGRATED_COURSE_IDS),['grade5','financial-algebra']);
});
