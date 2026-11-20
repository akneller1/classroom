// 3rd Grade Math audit (2026-11-19): Classroom-owned overlays on the pinned Grade 3 release (see elementary-audit.mjs).
// Runs after apply-content-updates.mjs and apply-kid-friendly.mjs. Usage: node scripts/apply-grade3-audit.mjs [_site]
import path from 'node:path';
import { applyElementaryAudit } from './elementary-audit.mjs';

const r = applyElementaryAudit({ grade: 3, player: "math3", date: "2026-11-19", version: "g3-audit-20261119", out: path.resolve(process.argv[2] || '_site') });
console.log(`Grade 3 audit overlay: ${r.edits} field edits, ${r.added} new question copies, ${r.metas} metadata entries, ${r.total} questions, pacing ${r.pacing ? 'yes' : 'no'}.`);
