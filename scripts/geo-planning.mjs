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
/* Algebra 2 (2026-11-17, Algebra 2 audit #3): the planner builds its lesson sequence in scope-algebra2.js from the
   course catalog (one lesson per skill, then practice, review, quiz and test days). The pacing guide pads that sequence
   to 180 days with a mid-unit practice day and a flex day per unit, extra practice in the longest units, a semester
   review and exam, and a final review and exam. Lesson titles, standards and notes are the planner's own. */
function algebra2Scope() {
  const w = { console, Math, Date, JSON }; w.window = w; w.globalThis = w; vm.createContext(w);
  for (const rel of ["data.js", "course-catalog.js", "worksheet-generator/menu/standards.js", "worksheet-generator/menu/standards-map.js",
    "worksheet-generator/planner/notes-teach-algebra2.js", "worksheet-generator/planner/scope-algebra2.js"])
    vm.runInContext(fs.readFileSync(path.join(ROOT, rel), "utf8"), w, { filename: rel });
  const base = w.MKPLAN_SCOPE_ALGEBRA2, lessonsMap = w.MKPLAN_SKILLS_ALGEBRA2.lessons, teach = (w.MKPLAN_TEACH || {}).algebra2 || {};
  const extraPractice = base.units.map((u) => ({ u: u.unit, n: u.lesson_ids.length })).sort((a, b) => b.n - a.n || a.u - b.u).slice(0, 7).map((x) => x.u);
  const days = [], units = [];
  let day = 0, semesterDone = false;
  const push = (d) => { day += 1; days.push({ ...d, day }); };
  for (const u of base.units) {
    const own = base.days.filter((d) => d.unit === u.unit), lessons = own.filter((d) => d.day_type === "Lesson"), rest = own.filter((d) => d.day_type !== "Lesson");
    const start = day + 1, half = Math.ceil(lessons.length / 2);
    lessons.forEach((d, i) => {
      push(d);
      if (i === half - 1) push({ unit: u.unit, unit_title: u.title, day_type: "Practice", title: u.title + " · Mid-unit practice", lesson_id: d.lesson_id.replace(/-S\d+$/, "-MIDPRACTICE"), standards: d.standards, content_objective: "Practice the first half of the unit." });
    });
    if (extraPractice.includes(u.unit)) push({ unit: u.unit, unit_title: u.title, day_type: "Practice", title: u.title + " · Extra practice", lesson_id: "A2-U" + u.unit + "-EXTRA", standards: "", content_objective: "Mixed practice before review." });
    rest.forEach(push);
    push({ unit: u.unit, unit_title: u.title, day_type: "Flex", title: u.title + " · Flex day", lesson_id: "A2-U" + u.unit + "-FLEX", standards: "", content_objective: "Corrections, reteaching and enrichment." });
    units.push({ unit: u.unit, title: u.title, start_day: start, end_day: day, total_days: day - start + 1, lesson_ids: u.lesson_ids });
    if (!semesterDone && day >= 84) {
      semesterDone = true;
      push({ unit: null, day_type: "Review", title: "Semester 1 Review", lesson_id: "A2-SEM-REVIEW-1", standards: "" });
      push({ unit: null, day_type: "Review", title: "Semester 1 Review", lesson_id: "A2-SEM-REVIEW-2", standards: "" });
      push({ unit: null, day_type: "Assessment", title: "Semester Exam", lesson_id: "A2-SEM-EXAM", standards: "" });
    }
  }
  while (day < 177) push({ unit: null, day_type: "Review", title: "Final Review", lesson_id: "A2-FINAL-REVIEW-" + (day + 1), standards: "" });
  push({ unit: null, day_type: "Review", title: "Final Review", lesson_id: "A2-FINAL-REVIEW-LAST", standards: "" });
  push({ unit: null, day_type: "Assessment", title: "Final Exam", lesson_id: "A2-FINAL-EXAM", standards: "" });
  push({ unit: null, day_type: "Flex", title: "Course reflection", lesson_id: "A2-FINAL-FLEX", standards: "" });
  const ideas = {}, names = {};
  for (const d of days) if (d.day_type === "Lesson") {
    const sk = lessonsMap[d.lesson_id] && lessonsMap[d.lesson_id].skills[0];
    if (sk && teach[sk[1]]) ideas[d.lesson_id] = teach[sk[1]].idea;
  }
  const C = w.MK_COURSE_CATALOG;
  for (const u of w.LIBRARY.courses.find((c) => c.id === "algebra2").units) for (const sk of C.getSkillRecords("algebra2", u.id)) names["algebra2-" + u.id + "/" + sk.id] = { name: sk.name, unit: u.name };
  return { scope: { meta: base.meta, units, days }, ideas, names };
}

/* Per-course sources (Algebra 1 joined 2026-11-17, audit #8 and #9; Algebra 2 joined 2026-11-17, Algebra 2 audit #3). */
const COURSES = {
  geometry: { name: "Geometry", scope: "worksheet-generator/planner/geometry_scope_sequence.json", sets: /^geometry-/, page: "geometry-pacing/",
    ideas: () => (win("worksheet-generator/planner/notes-data-geometry.js").MKPLAN_GEOMETRY_NOTES || {}).ideas || {} },
  algebra: { name: "Algebra 1", scope: "worksheet-generator/planner/algebra1_scope_sequence.json", sets: /^algebra1-/, page: "algebra-1-pacing/",
    ideas: () => (win("worksheet-generator/planner/notes-content.js").MKPLAN || {}).KEY_IDEAS || {} },
  algebra2: { name: "Algebra 2", load: algebra2Scope, sets: /^algebra2-/, page: "algebra-2-pacing/", framework: "Massachusetts Model Algebra II", bank: true }
};
const cache = {};
let names = null;
function data(course = "geometry") {
  if (cache[course]) return cache[course];
  const C = COURSES[course];
  if (C.load) {
    const got = C.load();
    const stdSkills = win("worksheet-generator/menu/standards-map.js").MKSTD_SKILLS || {};
    return (cache[course] = { C, scope: got.scope, notes: { ideas: got.ideas }, stdSkills, names: got.names });
  }
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
// Massachusetts Model Algebra II [AII] content standards (2017 framework); (+) marks the advanced ones.
const ALL_ALGEBRA2 = [["N-CN.A.1"], ["N-CN.A.2"], ["N-CN.C.7"], ["N-CN.C.8", "+"], ["N-CN.C.9", "+"], ["A-SSE.A.1a"], ["A-SSE.A.1b"], ["A-SSE.A.2"], ["A-SSE.B.4"],
  ["A-APR.A.1"], ["A-APR.B.2"], ["A-APR.B.3"], ["A-APR.C.4"], ["A-APR.C.5", "+"], ["A-APR.D.6"], ["A-APR.D.7", "+"], ["A-CED.A.1"], ["A-CED.A.2"], ["A-CED.A.3"],
  ["A-REI.A.2"], ["A-REI.D.11"], ["F-IF.B.4"], ["F-IF.B.5"], ["F-IF.B.6"], ["F-IF.C.7b"], ["F-IF.C.7c"], ["F-IF.C.7e"], ["F-IF.C.8a"], ["F-IF.C.9"], ["F-IF.C.10"],
  ["F-BF.A.1b"], ["F-BF.B.3"], ["F-BF.B.4a"], ["F-LE.A.4"], ["F-TF.A.1"], ["F-TF.A.2"], ["F-TF.B.5"], ["F-TF.C.8"], ["S-ID.A.4"],
  ["S-IC.A.1"], ["S-IC.A.2"], ["S-IC.B.3"], ["S-IC.B.4"], ["S-IC.B.5"], ["S-IC.B.6"], ["S-MD.B.6", "+"], ["S-MD.B.7", "+"]];
export function geoPacingMain(course = "geometry", unitHref) {
  const { scope, stdSkills, names, C } = data(course), ALL = course === "algebra2" ? ALL_ALGEBRA2 : course === "algebra" ? ALL_ALGEBRA : ALL_GEOMETRY;
  const framework = C.framework || "Common Core " + C.name, source = C.bank ? "question-bank skill" : "generator skill";
  const slug = (t) => ({ "Foundations of Geometry": "foundations-geometry", "Area, Surface Area and Volume": "area-surface-area-volume", "Right Triangles and Trigonometry": "right-triangles-trigonometry", "Quadrilaterals and Polygons": "quadrilaterals-polygons", "Angles and Parallel Lines": "angles-parallel-lines" }[t] || t.toLowerCase().replace(/ /g, "-"));
  const href = unitHref || ((t) => "../u/geometry/" + slug(t) + "/");
  const wk = (d) => Math.ceil(d / 5);
  let h = `<h1>${esc(C.name)} Pacing Guide and Standards Coverage</h1>
<p class="lede">A 180-day full-year plan in two semesters, a compressed one-semester (90-day block) plan, and a table showing which ${source}s practice each ${esc(framework)} standard. Every lesson has a ready plan in the Lesson Planner.</p>
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
  h += `<h2 id="standards">Standards coverage</h2>\n<p>Each ${source} is tagged with the standards it practices. Standards marked (+) are for advanced courses.</p>\n<table><thead><tr><th>Standard</th><th>What it asks</th><th>Skills that practice it</th></tr></thead><tbody>\n`;
  let gaps = 0;
  for (const [code, plus] of ALL) {
    const sk = bySkill.filter((s) => s.codes.some((x) => x === code || (x.indexOf(code) === 0 && /^[a-e]$/.test(x.slice(code.length))))).map((s) => (names[s.key] ? esc(names[s.key].name) : esc(s.key.split("/")[1])));
    if (!sk.length) gaps++;
    h += `<tr><td><strong>${esc(code)}</strong>${plus ? " (+)" : ""}</td><td>${esc(STD.describe(code))}</td><td>${sk.length ? `${sk.length} skill${sk.length > 1 ? "s" : ""}: ${sk.slice(0, 8).join("; ")}${sk.length > 8 ? "; …" : ""}` : "<em>Taught in lessons and activities; no generator skill yet</em>"}</td></tr>\n`;
  }
  h += `</tbody></table>\n<p>${ALL.length - gaps} of ${ALL.length} standards have ${C.bank ? "question-bank" : "generator"} practice.</p>\n`;
  return h;
}
