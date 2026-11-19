#!/usr/bin/env node
// Calculus audit #16 (2026-11-18): the Related Rates and Particle Motion labs are placed in their Calculus units with a
// worksheet, a teacher key and a thumbnail, load the shared lab runtime, and match their sources in tools/calculus-audit-20261118/labs.
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path'), assert = require('assert/strict');
const root = path.resolve(__dirname, '..'), ctx = { window: {} };
for (const file of ['data.js', 'student-game-share.js']) vm.runInNewContext(fs.readFileSync(path.join(root, file), 'utf8'), ctx, { filename: file });
const courses = ctx.window.LIBRARY.courses, calc = courses.find(c => c.id === 'calculus');
const M = JSON.parse(fs.readFileSync(path.join(root, 'tools/calculus-audit-20261118/labs/manifest.json'), 'utf8'));
assert.equal(M.tools.length, 2);
for (const t of M.tools) {
  for (const [c, u] of [[t.course, t.unit], ...(t.also || [])]) {
    const unit = courses.find(x => x.id === c).units.find(x => x.id === u);
    const a = unit.artifacts.find(a => a.path === `artifacts/${t.slug}/index.html`);
    assert(a && a.bankFormat === 'interactive-math' && a.type === 'Interactive', 'placement ' + t.slug + ' in ' + u);
    for (const f of [a.path, a.worksheet, a.answerKey, a.thumb]) assert(f && fs.existsSync(path.join(root, f)) && fs.statSync(path.join(root, f)).size > 2000, 'resource ' + f);
    assert.equal(ctx.window.TeacherGameShare.supports(a.path), false, 'a lab must not open a game skill picker');
  }
  const html = fs.readFileSync(path.join(root, 'artifacts', t.slug, 'index.html'), 'utf8');
  for (const src of ['../interactive-math/lab.js', '../interactive-math/lab-plus.js', '../interactive-math/lab.css']) assert(html.includes(src), 'runtime ' + src);
  const src = fs.readFileSync(path.join(root, 'tools/calculus-audit-20261118/labs/src', t.slug + '.js'), 'utf8');
  assert(html.includes(src.trim().split('\n').slice(-3).join('\n')), 'page built from the current source: ' + t.slug);
  assert(html.includes(JSON.stringify(t.title).slice(1, -1)), 'title ' + t.slug);
  new vm.Script(src, { filename: t.slug + '.js' });
  assert.equal((src.match(/check: function/g) || []).length, 5, 'five challenges ' + t.slug);
}
assert(calc.units.find(u => u.id === 'applications-derivatives').artifacts.some(a => a.path.includes('related-rates')), 'related rates in Applications of Derivatives');
console.log('PASS Calculus labs: ' + M.tools.map(t => t.title).join('; ') + ' placed with worksheets, keys and thumbnails');
