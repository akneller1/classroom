// Geometry planning content for the generated site (2026-11-17, audit #14 and #19).
//  • geoUnitGuide(unitTitle): the teacher briefing on each Geometry unit page (u/geometry/<unit>/): lessons with
//    their key idea, common mistakes, talk frames, standards and links to the pacing guide.
//  • geoPacingMain(): the body of u/geometry/pacing/: semester and full-year plans and a standards coverage table.
// Everything is read from the lesson planner (worksheet-generator/planner/geometry_scope_sequence.json, the
// generated notes and lesson-skill maps) and the generator's standards map, so the pages follow the course.
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { createRequire } from "node:module";

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const require = createRequire(import.meta.url);
const STD = require(path.join(ROOT, "worksheet-generator/menu/standards.js"));
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const list = (items) => `<ul class="mk-skills">\n${items.map((x) => `<li>${x}</li>`).join("\n")}\n</ul>\n`;

function win(rel) {
  const w = {}; w.window = w;
  vm.runInContext(fs.readFileSync(path.join(ROOT, rel), "utf8"), vm.createContext({ window: w, globalThis: w }), { filename: rel });
  return w;
}
let cache = null;
function data() {
  if (cache) return cache;
  const scope = JSON.parse(fs.readFileSync(path.join(ROOT, "worksheet-generator/planner/geometry_scope_sequence.json"), "utf8"));
  const notes = win("worksheet-generator/planner/notes-data-geometry.js").MKPLAN_GEOMETRY_NOTES || { ideas: {} };
  const map = win("worksheet-generator/planner/lesson-skills-geometry.js").MKPLAN_SKILLS_GEOMETRY;
  const stdSkills = win("worksheet-generator/menu/standards-map.js").MKSTD_SKILLS || {};
  let names = {};
  try {
    const M = require(path.join(ROOT, "worksheet-generator/menu/tests/load.cjs"))().MKMENU;
    for (const s of Object.values(M.skillSets)) if (/^geometry-/.test(s.id)) for (const k of s.skills) names[s.id + "/" + k.id] = { name: k.name, unit: s.unitName };
  } catch (e) { names = {}; }
  cache = { scope, notes, map, stdSkills, names };
  return cache;
}

/* ---------------- unit briefing ---------------- */
export function geoUnitGuide(unitTitle) {
  const { scope, notes } = data();
  const unit = scope.units.find((u) => u.title === unitTitle);
  if (!unit) return "";
  const days = scope.days.filter((d) => d.unit === unit.unit);
  const lessons = days.filter((d) => d.day_type === "Lesson");
  if (!lessons.length) return "";
  const std = STD.content(STD.split(lessons.map((l) => l.standards).join(", ")));
  const mistakes = lessons.filter((l) => l.common_misconception).map((l) => `<strong>${esc(l.title)}:</strong> ${esc(l.common_misconception)}`);
  const talk = lessons.filter((l) => l.sentence_frame).slice(0, 6).map((l) => `${esc(l.title)}: “${esc(l.sentence_frame)}”`);
  let html = `<h2>Teaching Unit ${unit.unit}: ${esc(unit.title)}</h2>\n`;
  html += `<p>About ${unit.total_days} class days (days ${unit.start_day}–${unit.end_day} of the full-year plan): ${lessons.length} lessons with practice days, a quiz, a review day, the unit test and a flex day. Every lesson has a ready plan in the <a href="../../../worksheet-generator/lesson-planner.html">Lesson Planner</a>.</p>\n`;
  html += `<h2>Lessons and key ideas</h2>\n` + list(lessons.map((l) => `<strong>${esc(l.title)}.</strong> ${esc(notes.ideas[l.lesson_id] || l.content_objective.replace(/^Students will be able to /, "Students "))}`));
  if (mistakes.length) html += `<h2>Common mistakes to watch for</h2>\n` + list(mistakes);
  if (talk.length) html += `<h2>Discussion frames</h2>\n` + list(talk);
  if (std.length) html += `<h2>Standards in this unit</h2>\n` + list(std.map((c) => `<strong>${esc(c)}</strong>${STD.describe(c) ? ": " + esc(STD.describe(c)) : ""}`));
  html += `<h2>Planning</h2>\n` + list([`<a href="../pacing/">Geometry pacing guide and standards coverage</a>: semester and full-year plans, and which skills practice each standard`]);
  return html;
}

/* ---------------- pacing guide and standards coverage ---------------- */
// Common Core high school Geometry standards ((+) marks the advanced ones).
const ALL = [["G-CO.A.1"], ["G-CO.A.2"], ["G-CO.A.3"], ["G-CO.A.4"], ["G-CO.A.5"], ["G-CO.B.6"], ["G-CO.B.7"], ["G-CO.B.8"], ["G-CO.C.9"], ["G-CO.C.10"], ["G-CO.C.11"], ["G-CO.D.12"], ["G-CO.D.13"],
  ["G-SRT.A.1"], ["G-SRT.A.2"], ["G-SRT.A.3"], ["G-SRT.B.4"], ["G-SRT.B.5"], ["G-SRT.C.6"], ["G-SRT.C.7"], ["G-SRT.C.8"], ["G-SRT.D.9", "+"], ["G-SRT.D.10", "+"], ["G-SRT.D.11", "+"],
  ["G-C.A.1"], ["G-C.A.2"], ["G-C.A.3"], ["G-C.A.4", "+"], ["G-C.B.5"], ["G-GPE.A.1"], ["G-GPE.A.2"], ["G-GPE.A.3", "+"], ["G-GPE.B.4"], ["G-GPE.B.5"], ["G-GPE.B.6"], ["G-GPE.B.7"],
  ["G-GMD.A.1"], ["G-GMD.A.2", "+"], ["G-GMD.A.3"], ["G-GMD.B.4"], ["G-MG.A.1"], ["G-MG.A.2"], ["G-MG.A.3"]];

export function geoPacingMain() {
  const { scope, stdSkills, names } = data();
  const slug = (t) => ({ "Foundations of Geometry": "foundations-geometry", "Area, Surface Area and Volume": "area-surface-area-volume", "Right Triangles and Trigonometry": "right-triangles-trigonometry", "Quadrilaterals and Polygons": "quadrilaterals-polygons", "Angles and Parallel Lines": "angles-parallel-lines" }[t] || t.toLowerCase().replace(/ /g, "-"));
  const wk = (d) => Math.ceil(d / 5);
  let h = `<h1>Geometry Pacing Guide and Standards Coverage</h1>
<p class="lede">A 180-day full-year plan in two semesters, a compressed one-semester (90-day block) plan, and a table showing which generator skills practice each Common Core Geometry standard. Every day links to a ready lesson plan in the Lesson Planner.</p>
<p><a href="#year">Full year</a> · <a href="#block">One-semester block</a> · <a href="#standards">Standards coverage</a></p>
<h2 id="year">Full year (180 days, 36 weeks)</h2>
<table><thead><tr><th>Unit</th><th>Days</th><th>Weeks</th><th>Lessons</th></tr></thead><tbody>
`;
  const row = (u) => {
    const ls = scope.days.filter((d) => d.unit === u.unit && d.day_type === "Lesson").map((d) => esc(d.title));
    return `<tr><td><a href="../${slug(u.title)}/">Unit ${u.unit}: ${esc(u.title)}</a></td><td>${u.start_day}–${u.end_day} (${u.total_days})</td><td>${wk(u.start_day)}–${wk(u.end_day)}</td><td>${ls.join("; ")}</td></tr>\n`;
  };
  const sem = scope.days.find((d) => /^Semester Exam/.test(d.title));
  for (const u of scope.units) {
    h += row(u);
    if (sem && u.end_day < sem.day && (scope.units.find((x) => x.unit === u.unit + 1) || {}).start_day > sem.day)
      h += `<tr><td colspan="4"><strong>Semester 1 review and exam</strong> (days ${sem.day - 2}–${sem.day})</td></tr>\n`;
  }
  const fin = scope.days.filter((d) => d.unit === null && d.day > 170);
  if (fin.length) h += `<tr><td colspan="4"><strong>Final review and exam</strong> (days ${fin[0].day}–${fin[fin.length - 1].day})</td></tr>\n`;
  h += `</tbody></table>\n`;
  // one semester (block): each unit's lessons and test, practice days halved
  h += `<h2 id="block">One semester (90-day block)</h2>\n<p>For a block schedule, teach each lesson as planned, keep one practice day per two lessons, the quiz, the review day and the test, and drop the mixed-practice and flex days.</p>\n<table><thead><tr><th>Unit</th><th>Block days</th></tr></thead><tbody>\n`;
  let day = 2;
  for (const u of scope.units) {
    const ds = scope.days.filter((d) => d.unit === u.unit);
    const n = ds.filter((d) => d.day_type === "Lesson").length, keep = n + Math.ceil(n / 4) + 3;
    h += `<tr><td>Unit ${u.unit}: ${esc(u.title)}</td><td>${day + 1}–${day + keep} (${keep})</td></tr>\n`; day += keep;
  }
  h += `<tr><td>Final review and exam</td><td>${day + 1}–${Math.max(day + 3, 90)}</td></tr>\n</tbody></table>\n`;
  // standards coverage
  const bySkill = [];
  for (const [set, skills] of Object.entries(stdSkills)) if (/^geometry-/.test(set)) for (const [sk, codes] of Object.entries(skills)) bySkill.push({ key: set + "/" + sk, codes });
  h += `<h2 id="standards">Standards coverage</h2>\n<p>Each worksheet-generator skill is tagged with the standards it practices. Standards marked (+) are for advanced courses.</p>\n<table><thead><tr><th>Standard</th><th>What it asks</th><th>Skills that practice it</th></tr></thead><tbody>\n`;
  let gaps = 0;
  for (const [code, plus] of ALL) {
    const sk = bySkill.filter((s) => s.codes.indexOf(code) >= 0).map((s) => (names[s.key] ? esc(names[s.key].name) : esc(s.key.split("/")[1])));
    if (!sk.length) gaps++;
    h += `<tr><td><strong>${esc(code)}</strong>${plus ? " (+)" : ""}</td><td>${esc(STD.describe(code))}</td><td>${sk.length ? `${sk.length} skill${sk.length > 1 ? "s" : ""}: ${sk.slice(0, 8).join("; ")}${sk.length > 8 ? "; …" : ""}` : "<em>Taught in lessons and activities; no generator skill yet</em>"}</td></tr>\n`;
  }
  h += `</tbody></table>\n<p>${ALL.length - gaps} of ${ALL.length} standards have generator practice.</p>\n`;
  return h;
}
