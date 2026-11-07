/* Regression checks for the Statistics Interactive Math update (tools/interactive-math-statistics). */
'use strict';
const fs = require('node:fs'), vm = require('node:vm'), path = require('node:path'), assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..'), ctx = { window: {} };
for (const file of ['data.js', 'student-game-share.js']) vm.runInNewContext(fs.readFileSync(path.join(root, file), 'utf8'), ctx, { filename: file });
const courses = ctx.window.LIBRARY.courses, stats = courses.find(c => c.id === 'statistics');
assert(stats && stats.planned && stats.units.length === 4, 'Statistics must stay a planned course with 4 units');
assert.equal(stats.units.map(u => u.id).join(','), 'exploring-data,sampling-experimentation,anticipating-patterns,statistical-inference');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'tools/interactive-math-statistics/manifest.json'), 'utf8'));
assert.equal(manifest.tools.length, 7);
for (const tool of manifest.tools) {
  assert.equal(tool.course, 'statistics');
  const unit = stats.units.find(u => u.id === tool.unit), res = unit && unit.artifacts.find(a => a.path === `artifacts/${tool.slug}/index.html`);
  assert(res && res.bankFormat === 'interactive-math', 'Missing Statistics placement: ' + tool.slug);
  for (const f of [res.path, res.worksheet, res.answerKey, res.thumb]) assert(f && fs.existsSync(path.join(root, f)), 'Missing resource: ' + f);
  const html = fs.readFileSync(path.join(root, res.path), 'utf8');
  for (const src of ['../interactive-math/lab.js', '../interactive-math/lab-plus.js', '../interactive-math/lab-stats.js']) assert(html.includes(src), `Missing runtime ${src} for ${tool.slug}`);
  assert.equal(ctx.window.TeacherGameShare.supports(res.path), false, 'Interactive tool must not open the game skill picker: ' + res.path);
}
assert(stats.units.find(u => u.id === 'anticipating-patterns').artifacts.some(a => a.path === 'artifacts/algebra2-probability-simulation-lab/index.html'), 'Probability Simulation Lab reuse missing');
const app = fs.readFileSync(path.join(root, 'app.js'), 'utf8');
assert(/function plannedInteractive\(c, u\)/.test(app) && /var tools = plannedInteractive\(c, u\);/.test(app), 'Planned unit pages must list Interactive Math tools');
console.log(`PASS ${manifest.tools.length} Statistics tools placed with worksheets, keys, thumbnails and runtimes; course still planned; student links route directly`);
