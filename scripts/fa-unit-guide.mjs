// Teacher guide section for Financial Algebra unit pages (u/financial-algebra/<unit>/), built from the unit's
// lesson plans in financial/banks/<unit>.json so the page always matches the course: the opening hook, key ideas
// and formulas, common mistakes and discussion questions. Used by scripts/build-integrated-unit-pages.mjs.
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
// FA text uses **bold** and [[numerator||denominator]] fractions; render both as plain readable text.
export const plain = (s) => String(s ?? "").replace(/\*\*(.+?)\*\*/g, "$1").replace(/\[\[(.+?)\|\|(.+?)\]\]/g, (_, a, b) => a.trim() + " ÷ " + b.trim()).trim();
const list = (items) => `<ul class="mk-skills">\n${items.map((x) => `<li>${x}</li>`).join("\n")}\n</ul>\n`;
const uniq = (a, key = (x) => x) => a.filter((x, i) => a.findIndex((y) => key(y) === key(x)) === i);

export function faUnitGuide(bank, unitTitle) {
  const lessons = (bank && bank.lessons) || [];
  if (!lessons.length) return "";
  const hook = lessons.find((l) => l.hook)?.hook, why = lessons.find((l) => l.realWorld)?.realWorld;
  const notes = uniq(lessons.flatMap((l) => (l.notes || []).slice(0, 2)), (n) => n.h).slice(0, 10);
  const mistakes = uniq(lessons.flatMap((l) => l.misconceptions || []), (m) => m[0]).slice(0, 6);
  const talk = uniq(lessons.flatMap((l) => l.discussion || [])).slice(0, 5);
  let html = `<h2>Teaching ${esc(unitTitle)}</h2>\n`;
  html += `<p>This unit has ${lessons.length} ready-to-teach lesson plans, one per skill${hook ? `. A good opener: ${esc(plain(hook))}` : "."}</p>\n`;
  if (why) html += `<p><strong>Why it matters:</strong> ${esc(plain(why))}</p>\n`;
  if (notes.length) html += `<h2>Key ideas and formulas</h2>\n` + list(notes.map((n) => `<strong>${esc(plain(n.h))}:</strong> ${esc(plain(n.body))}`));
  if (mistakes.length) html += `<h2>Common mistakes to watch for</h2>\n` + list(mistakes.map((m) => `<strong>Students may think:</strong> “${esc(plain(m[0]))}” <strong>In fact:</strong> ${esc(plain(m[1]))}`));
  if (talk.length) html += `<h2>Discussion questions</h2>\n` + list(talk.map((q) => esc(plain(q))));
  // Standards and planning (2026-11-17): national personal finance standards per skill, the pacing guide and any
  // Spreadsheet Lab, all read from the bank so the page matches the course.
  const skills = (bank.skills || []).filter((s) => (s.standards || []).length);
  if (skills.length) html += `<h2>National standards</h2>\n<p>Each skill is tagged to the grade 12 ${esc(bank.standardsSource?.title || "National Standards for Personal Financial Education")}.</p>\n` + list(skills.map((s) => `<strong>${esc(s.name)}:</strong> ${s.standards.map(esc).join("; ")}`));
  const plan = bank.planning || {}, root = "../../../", links = [];
  for (const l of plan.spreadsheetLabs || []) links.push(`<a href="${esc(root + l.path)}">${esc(l.title)}</a>: a Google Sheets and Excel template with step-by-step instructions and matching questions`);
  if (plan.pacingGuide) links.push(`<a href="${esc(root + plan.pacingGuide)}">Pacing guide and standards map</a>: 18-week semester and 36-week full-year plans`);
  if (links.length) html += `<h2>Planning</h2>\n` + list(links);
  return html;
}
