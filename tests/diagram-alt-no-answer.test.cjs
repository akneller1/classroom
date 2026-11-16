// "Which graph shows X?" items must not name X in the diagram's alt text.
const test = require('node:test'), assert = require('node:assert/strict'), fs = require('node:fs'), path = require('node:path');
function* banks(dir) { for (const e of fs.readdirSync(dir, { withFileTypes: true })) { const f = path.join(dir, e.name);
  if (e.isDirectory()) { if (e.name !== 'meta' && e.name !== 'assets') yield* banks(f); } else if (e.name.endsWith('.json') && !e.name.startsWith('manifest')) yield f; } }
const norm = s => String(s).replace(/\s+/g, '').replace(/−/g, '-').toLowerCase();
const ask = /which (graph|picture|model|number line|diagram|table|line plot|bar graph|clock)[^?]*?(shows|represents|matches|has)\s+(.+?)\?/i;
test('diagram alt text never contains the expression the question asks for', () => {
  const leaks = [];
  for (const f of banks('question-banks')) {
    const d = JSON.parse(fs.readFileSync(f, 'utf8'));
    for (const q of d.questions || []) {
      const m = q.diagram && q.format === 'multiple-choice' && ask.exec(q.prompt || '');
      if (!m || norm(m[3]).length < 3) continue;
      if (norm(q.diagram.spec && q.diagram.spec.alt).includes(norm(m[3]))) leaks.push(q.id);
    }
  }
  assert.deepEqual(leaks, []);
});
