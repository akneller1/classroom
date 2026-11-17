// Geometry planning content for the generated site (2026-11-17, audit #14 and #19).
//  • geoUnitGuide(unitTitle): the teacher briefing on each Geometry unit page (u/geometry/<unit>/): lessons with
//    their key idea, common mistakes, talk frames, standards and links to the pacing guide.
//  • geoPacingMain(): the body of geometry-pacing/: semester and full-year plans and a standards coverage table.
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
/* Per-course sources (Algebra 1 joined 2026-11-17, audit #8 and #9). */
const COURSES = {
  geometry: { name: "Geometry", scope: "worksheet-generator/planner/geometry_scope_sequence.json", sets: /^geometry-/, page: "geometry-pacing/",
    ideas: () => (win("worksheet-generator/planner/notes-data-geometry.js").MKPLAN_GEOMETRY_NOTES || {}).ideas || {} },
  algebra: { name: "Algebra 1", scope: "worksheet-generator/planner/algebra1_scope_sequence.json", sets: /^algebra1-/, page: "algebra-1-pacing/",
    ideas: () => (win("worksheet-generator/planner/notes-content.js").MKPLAN || {}).KEY_IDEAS || {} }
};
const cache = {};
let names = null;
function data(course = "geometry") {
  if (cache[course]) return cache[course];
  const C = COURSES[course];
  const scope = JSON.parse(fs.readFileSync(path.join(ROOT, C.scope), "utf8"));
  let ideas = {}; try { ideas = C.ideas(); } catch (e) { ideas = {}; }
  const stdSkills = win("worksheet-generator/menu/standards-map.js").MKSTD_SKILLS || {};
  if (!names) {
    names = {};
    try {
      const M = require(path.join(ROOT, "worksheet-generator/menu/tests/load.cjs"))().MKMENU;
      for (const s of Object.values(M.skillSets)) for (const k of s.skills) names[s.id + "/" + k.id] = { name: k.name, unit: s.unitName };
    } catch (e) { names = {}; }
  }
  return (cache[course] = { C, scope, notes: { ideas }, stdSkills, names });
}
export const planningPage = (course) => (COURSES[course] || {}).page;
export const planningCourses = Object.keys(COURSES);

/* ---------------- unit briefing ---------------- */
export function geoUnitGuide(unitTitle, course = "geometry") {
  const { scope, notes, C } = data(course);
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
  html += `<h2>Planning</h2>\n` + list([`<a href="../../../${C.page}">${esc(C.name)} pacing guide and standards coverage</a>: full-year and block plans, and which skills practice each standard`]);
  return html;
}

/* ---------------- pacing guide and standards coverage ---------------- */
// Common Core high school Geometry standards ((+) marks the advanced ones).
const ALL_GEOMETRY = [["G-CO.A.1"], ["G-CO.A.2"], ["G-CO.A.3"], ["G-CO.A.4"], ["G-CO.A.5"], ["G-CO.B.6"], ["G-CO.B.7"], ["G-CO.B.8"], ["G-CO.C.9"], ["G-CO.C.10"], ["G-CO.C.11"], ["G-CO.D.12"], ["G-CO.D.13"],
  ["G-SRT.A.1"], ["G-SRT.A.2"], ["G-SRT.A.3"], ["G-SRT.B.4"], ["G-SRT.B.5"], ["G-SRT.C.6"], ["G-SRT.C.7"], ["G-SRT.C.8"], ["G-SRT.D.9", "+"], ["G-SRT.D.10", "+"], ["G-SRT.D.11", "+"],
  ["G-C.A.1"], ["G-C.A.2"], ["G-C.A.3"], ["G-C.A.4", "+"], ["G-C.B.5"], ["G-GPE.A.1"], ["G-GPE.A.2"], ["G-GPE.A.3", "+"], ["G-GPE.B.4"], ["G-GPE.B.5"], ["G-GPE.B.6"], ["G-GPE.B.7"],
  ["G-GMD.A.1"], ["G-GMD.A.2", "+"], ["G-GMD.A.3"], ["G-GMD.B.4"], ["G-MG.A.1"], ["G-MG.A.2"], ["G-MG.A.3"]];

// Common Core Algebra 1 standards as the generator tags them (cluster level, sub-standards where they are taught separately).
const ALL_ALGEBRA = [["N-RN.A.1"], ["N-RN.A.2"], ["N-RN.B.3"], ["N-Q.A.1"], ["N-Q.A.2"], ["N-Q.A.3"], ["A-SSE.A.1"], ["A-SSE.A.2"], ["A-SSE.B.3a"], ["A-SSE.B.3b"], ["A-SSE.B.3c"],
  ["A-APR.A.1"], ["A-APR.B.3"], ["A-CED.A.1"], ["A-CED.A.2"], ["A-CED.A.3"], ["A-CED.A.4"], ["A-REI.A.1"], ["A-REI.B.3"], ["A-REI.B.4a"], ["A-REI.B.4b"], ["A-REI.C.5"], ["A-REI.C.6"],
  ["A-REI.C.7"], ["A-REI.D.10"], ["A-REI.D.11"], ["A-REI.D.12"], ["F-IF.A.1"], ["F-IF.A.2"], ["F-IF.A.3"], ["F-IF.B.4"], ["F-IF.B.5"], ["F-IF.B.6"], ["F-IF.C.7a"], ["F-IF.C.7b"], ["F-IF.C.7e"],
  ["F-IF.C.8a"], ["F-IF.C.8b"], ["F-IF.C.9"], ["F-BF.A.1a"], ["F-BF.A.2"], ["F-BF.B.3"], ["F-BF.B.4a"], ["F-LE.A.1a"], ["F-LE.A.1b"], ["F-LE.A.1c"], ["F-LE.A.2"], ["F-LE.A.3"], ["F-LE.B.5"],
  ["S-ID.A.1"], ["S-ID.A.2"], ["S-ID.A.3"], ["S-ID.B.5"], ["S-ID.B.6a"], ["S-ID.B.6b"], ["S-ID.B.6c"], ["S-ID.C.7"], ["S-ID.C.8"], ["S-ID.C.9"]];
export function geoPacingMain(course = "geometry", unitHref) {
  const { scope, stdSkills, names, C } = data(course), ALL = course === "algebra" ? ALL_ALGEBRA : ALL_GEOMETRY;
  const slug = (t) => ({ "Foundations of Geometry": "foundations-geometry", "Area, Surface Area and Volume": "area-surface-area-volume", "Right Triangles and Trigonometry": "right-triangles-trigonometry", "Quadrilaterals and Polygons": "quadrilaterals-polygons", "Angles and Parallel Lines": "angles-parallel-lines" }[t] || t.toLowerCase().replace(/ /g, "-"));
  const href = unitHref || ((t) => "../u/geometry/" + slug(t) + "/");
  const wk = (d) => Math.ceil(d / 5);
  let h = `<h1>${esc(C.name)} Pacing Guide and Standards Coverage</h1>
<p class="lede">A 180-day full-year plan in two semesters, a compressed one-semester (90-day block) plan, and a table showing which generator skills practice each Common Core ${esc(C.name)} standard. Every lesson has a ready plan in the Lesson Planner.</p>
<p><a href="#year">Full year</a> · <a href="#block">One-semester block</a> · <a href="#standards">Standards coverage</a></p>
<h2 id="year">Full year (180 days, 36 weeks)</h2>
<table><thead><tr><th>Unit</th><th>Days</th><th>Weeks</th><th>Lessons</th></tr></thead><tbody>
`;
  const row = (u) => {
    const ls = scope.days.filter((d) => d.unit === u.unit && d.day_type === "Lesson").map((d) => esc(d.title));
    return `<tr><td><a href="${href(u.title)}">Unit ${u.unit}: ${esc(u.title)}</a></td><td>${u.start_day}–${u.end_day} (${u.total_days})</td><td>${wk(u.start_day)}–${wk(u.end_day)}</td><td>${ls.join("; ")}</td></tr>\n`;
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
  // one semester (block): each 90-minute block covers two days of the full-year plan
  h += `<h2 id="block">One semester (90-day block)</h2>\n<p>On a block schedule each 90-minute class covers two days of the full-year plan: a lesson and its practice, or two lessons. Day 1 is the launch and diagnostic.</p>\n<table><thead><tr><th>Unit</th><th>Block days</th></tr></thead><tbody>\n`;
  let day = 1;
  for (const u of scope.units) { const keep = Math.ceil(u.total_days / 2); h += `<tr><td>Unit ${u.unit}: ${esc(u.title)}</td><td>${day + 1}–${day + keep} (${keep})</td></tr>\n`; day += keep; }
  h += `<tr><td>Final review and exam</td><td>${day + 1}${day + 1 < 90 ? "–90" : ""}</td></tr>\n</tbody></table>\n`;
  // standards coverage
  const bySkill = [];
  for (const [set, skills] of Object.entries(stdSkills)) if (C.sets.test(set)) for (const [sk, codes] of Object.entries(skills)) bySkill.push({ key: set + "/" + sk, codes });
  h += `<h2 id="standards">Standards coverage</h2>\n<p>Each worksheet-generator skill is tagged with the standards it practices. Standards marked (+) are for advanced courses.</p>\n<table><thead><tr><th>Standard</th><th>What it asks</th><th>Skills that practice it</th></tr></thead><tbody>\n`;
  let gaps = 0;
  for (const [code, plus] of ALL) {
    const sk = bySkill.filter((s) => s.codes.some((x) => x === code || (x.indexOf(code) === 0 && /^[a-e]$/.test(x.slice(code.length))))).map((s) => (names[s.key] ? esc(names[s.key].name) : esc(s.key.split("/")[1])));
    if (!sk.length) gaps++;
    h += `<tr><td><strong>${esc(code)}</strong>${plus ? " (+)" : ""}</td><td>${esc(STD.describe(code))}</td><td>${sk.length ? `${sk.length} skill${sk.length > 1 ? "s" : ""}: ${sk.slice(0, 8).join("; ")}${sk.length > 8 ? "; …" : ""}` : "<em>Taught in lessons and activities; no generator skill yet</em>"}</td></tr>\n`;
  }
  h += `</tbody></table>\n<p>${ALL.length - gaps} of ${ALL.length} standards have generator practice.</p>\n`;
  return h;
}
