// 2nd Grade Math audit (2026-11-19): Classroom-owned overlays on the pinned Grade 2 release (see elementary-audit.mjs).
// Runs after apply-content-updates.mjs and apply-kid-friendly.mjs. Usage: node scripts/apply-grade2-audit.mjs [_site]
import path from 'node:path';
import { applyElementaryAudit } from './elementary-audit.mjs';

const r = applyElementaryAudit({ grade: 2, player: "math2", date: "2026-11-19", version: "g2-audit-20261119", out: path.resolve(process.argv[2] || '_site') });
console.log(`Grade 2 audit overlay: ${r.edits} field edits, ${r.added} new question copies, ${r.metas} metadata entries, ${r.total} questions, pacing ${r.pacing ? 'yes' : 'no'}.`);
