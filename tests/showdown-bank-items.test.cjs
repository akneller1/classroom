'use strict';
// Showdown shows whole problems. Approved-bank questions in hybrid units (generated skills plus bank skills)
// carry a teacher-reviewed source key instead of a generator verification, and must still reach the board.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..');

test('Showdown accepts approved-bank questions and still rejects unverified generated ones', () => {
  const ctx = { console }; ctx.window = ctx; ctx.globalThis = ctx; vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(root, 'worksheet-generator/core/rng.js'), 'utf8'), ctx);
  ctx.MKMENU = { skillSets: { s: { byId: { k: { name: 'Law of Sines' } }, tags: {} } }, generateProblem: null };
  vm.runInContext(fs.readFileSync(path.join(root, 'worksheet-generator/games/bank.js'), 'utf8'), ctx);
  const GB = ctx.MKGAMES;
  GB.distractors = () => [];
  const make = (p) => { ctx.MKMENU.generateProblem = () => p; return GB.makeWholeItems('s', 'k', 4, {}, 'seed', { keys: new Set() }); };
  const base = { uid: 'q1', prompt: 'Find x.', tag: 'k', parts: [{ answer: '7', prompt: '' }], steps: [] };
  assert.equal(make(Object.assign({}, base, { source: 'authored-bank', verify: { status: 'source-key', issues: [] } })).length, 1);
  assert.equal(make(Object.assign({}, base, { verify: { status: 'verified' } })).length, 1);
  assert.equal(make(Object.assign({}, base, { verify: { status: 'source-key' } })).length, 0, 'a source key alone is only trusted on bank questions');
  assert.equal(make(Object.assign({}, base, { verify: { status: 'failed' } })).length, 0);
});
