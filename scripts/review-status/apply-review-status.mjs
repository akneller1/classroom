#!/usr/bin/env node
// Marks owner-reviewed question banks as reviewed (approved by the site owner on 2026-11-15: "Yes, mark all as reviewed").
// Usage:
//   node apply-review-status.mjs --classroom <path> [--financial-algebra <path>] [--check]
// Either repository flag may be given alone; only that repository's entries are processed.
// Changes ONLY the quoted phrase in each listed file:
//   "Awaiting teacher review." -> "Teacher reviewed 2026-11-15."
//   "Awaiting human review"    -> "Teacher reviewed 2026-11-15"
// Text around the phrase ("family: ...", "Partner Check pair ...", "Content package ...") is untouched.
// Fails closed: if any file's count differs from the manifest, nothing is written. Re-running it does nothing.
import fs from 'node:fs'; import path from 'node:path'; import {fileURLToPath} from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const manifest = JSON.parse(fs.readFileSync(path.join(here, 'review-status-manifest.json'), 'utf8'));
const arg = n => { const i = process.argv.indexOf(n); return i > 0 ? path.resolve(process.argv[i + 1]) : null; };
const roots = {classroom: arg('--classroom'), FinancialAlgebra: arg('--financial-algebra')};
const check = process.argv.includes('--check');
if (!roots.classroom && !roots.FinancialAlgebra) { console.error('Give --classroom and/or --financial-algebra'); process.exit(2); }

const problems = [], writes = new Map(), totals = {};
for (const e of manifest.entries) {
  const root = roots[e.repo]; if (!root) continue;
  const file = path.join(root, e.path);
  if (!fs.existsSync(file)) { problems.push(`${e.repo}:${e.path} missing`); continue; }
  const text = writes.get(file) ?? fs.readFileSync(file, 'utf8');
  const before = text.split(e.find).length - 1;
  if (before === 0) continue;                                   // already applied
  if (before !== e.expectedCount) { problems.push(`${e.repo}:${e.path}: expected ${e.expectedCount} "${e.find}", found ${before}`); continue; }
  const next = text.split(e.find).join(e.replace);
  try { JSON.parse(next); } catch (x) { problems.push(`${e.repo}:${e.path}: invalid JSON after replace`); continue; }
  writes.set(file, next);
  const k = `${e.repo} · "${e.find}"`; totals[k] = (totals[k] || 0) + before;
}
if (problems.length) { console.error('FAIL (nothing written)\n' + problems.join('\n')); process.exit(1); }
if (!check) for (const [file, text] of writes) fs.writeFileSync(file, text);
const lines = Object.entries(totals).map(([k, n]) => `  ${k}: ${n}`);
console.log(`${check ? 'CHECK OK' : 'APPLIED'}: ${writes.size} files${lines.length ? '\n' + lines.join('\n') : ' (nothing left to change)'}`);
