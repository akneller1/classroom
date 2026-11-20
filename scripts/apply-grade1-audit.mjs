// 1st Grade Math audit (2026-11-19): Classroom-owned overlays on the pinned Grade 1 release (see elementary-audit.mjs).
// Runs after apply-content-updates.mjs and apply-kid-friendly.mjs. Usage: node scripts/apply-grade1-audit.mjs [_site]
import path from 'node:path';
import { applyElementaryAudit } from './elementary-audit.mjs';

const r = applyElementaryAudit({ grade: 1, player: "math1", date: "2026-11-19", version: "g1-audit-20261119", out: path.resolve(process.argv[2] || '_site') });
console.log(`Grade 1 audit overlay: ${r.edits} field edits, ${r.added} new question copies, ${r.metas} metadata entries, ${r.total} questions, pacing ${r.pacing ? 'yes' : 'no'}.`);
