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
/* Precalculus (2026-11-18, Precalculus audit #3) uses the same planner sequence and padding. */
/* Discrete Math (2026-11-18, Discrete Math audit #6) uses it too; its standards list is read from the bank's own tags. */
/* 8th Grade Math (2026-11-19, 8th Grade Math audit #2) uses the same sequence and padding as Algebra 2. */
/* Calculus (2026-11-18, Calculus audit #7) is an AP course: new content (units 1-8) ends about day 130 (mid-April),
   the AP Review unit and practice exams run to the AP Calculus AB exam in early-to-mid May (about day 153), and the
   rest of the year is the course's calculus projects. There is no extra final exam. */
function bankScope(course, prefix, opts = {}) {
  const w = { console, Math, Date, JSON }; w.window = w; w.globalThis = w; vm.createContext(w);
  for (const rel of ["data.js", "course-catalog.js", "worksheet-generator/menu/standards.js", "worksheet-generator/menu/standards-map.js",
    "worksheet-generator/planner/notes-teach-" + course + ".js", "worksheet-generator/planner/scope-algebra2.js"])
    if (fs.existsSync(path.join(ROOT, rel))) vm.runInContext(fs.readFileSync(path.join(ROOT, rel), "utf8"), w, { filename: rel });
  const KEY = course.toUpperCase();
  const base = w["MKPLAN_SCOPE_" + KEY], lessonsMap = w["MKPLAN_SKILLS_" + KEY].lessons, teach = (w.MKPLAN_TEACH || {})[course] || {};
  // Extra practice days: at least one in each of the 7 longest units, and more (longest units first) when the
  // course has fewer lessons, so the plan reaches day 180 with about a week of final review rather than a long gap.
  // An AP course's last unit is its AP Review unit (Calculus); a course without one (Statistics) spreads the extra days over every unit.
  const reviewUnit = opts.ap && !opts.noReviewUnit ? base.units[base.units.length - 1].unit : null;
  const bySize = base.units.filter((u) => u.unit !== reviewUnit).map((u) => ({ u: u.unit, n: u.lesson_ids.length })).sort((a, b) => b.n - a.n || a.u - b.u).map((x) => x.u);
  // + mid-unit practice and flex per unit, semester review/exam, final review/exam/flex, and (Grade 7) MCAS review and testing days
  const planned = base.days.length + base.units.length * 2 + 3 + 3 + (opts.mcas ? opts.mcas.review + opts.mcas.testing : 0);
  const lastUnit = base.units[base.units.length - 1].unit;
  const beforeReview = base.days.filter((d) => d.unit !== reviewUnit).length + (base.units.length - (reviewUnit === null ? 0 : 1)) * 2 + 3;
  const spare = opts.mcas ? 0 : opts.ap ? Math.max(0, 130 - beforeReview) : Math.max(7, 177 - planned - 3), extraCount = {};
  // Grade 7 has 116 lessons: no extra or mid-unit practice days (each unit keeps the planner's own practice day), review
  // skills are taught two to a day, and only the largest units keep a flex day, so the year still fits in 180 days.
  const flexUnits = opts.mcas ? bySize.slice(0, opts.mcas.flex) : null;
  for (let i = 0; i < spare; i++) extraCount[bySize[i % bySize.length]] = (extraCount[bySize[i % bySize.length]] || 0) + 1;
  const days = [], units = [];
  let day = 0, semesterDone = false;
  const push = (d) => { day += 1; days.push({ ...d, day }); };
  for (const u of base.units) {
    const own = base.days.filter((d) => d.unit === u.unit), rest = own.filter((d) => d.day_type !== "Lesson");
    let lessons = own.filter((d) => d.day_type === "Lesson");
    if (opts.mcas) {
      const merged = []; let open = null;
      for (const d of lessons) {
        if (!/ \(review\)$/.test(d.title)) { merged.push(d); continue; }
        if (!open) { open = { ...d, lessons_covered: [d.lesson_id] }; merged.push(open); continue; }
        open.title = open.title.replace(/ \(review\)$/, "") + " + " + d.title; open.lessons_covered.push(d.lesson_id);
        open.standards = [...new Set((open.standards + ", " + d.standards).split(/,\s*/).filter(Boolean))].join(", "); open = null;
      }
      lessons = merged;
    }
    const start = day + 1, half = Math.ceil(lessons.length / 2);
    lessons.forEach((d, i) => {
      push(d);
      if (i === half - 1 && !opts.mcas) push({ unit: u.unit, unit_title: u.title, day_type: "Practice", title: u.title + " · Mid-unit practice", lesson_id: d.lesson_id.replace(/-S\d+$/, "-MIDPRACTICE"), standards: d.standards, content_objective: "Practice the first half of the unit." });
    });
    for (let k = 1; k <= (extraCount[u.unit] || 0); k++) push({ unit: u.unit, unit_title: u.title, day_type: "Practice", title: u.title + " · Extra practice", lesson_id: prefix + "-U" + u.unit + "-EXTRA" + (k > 1 ? k : ""), standards: "", content_objective: "Mixed practice before review." });
    rest.forEach(push);
    if (!flexUnits || flexUnits.includes(u.unit)) push({ unit: u.unit, unit_title: u.title, day_type: "Flex", title: u.title + " · Flex day", lesson_id: prefix + "-U" + u.unit + "-FLEX", standards: "", content_objective: "Corrections, reteaching and enrichment." });
    units.push({ unit: u.unit, title: u.title, start_day: start, end_day: day, total_days: day - start + 1, lesson_ids: u.lesson_ids });
    if (opts.mcas && u.unit === opts.mcas.afterUnit) {
      for (let k = 1; k <= opts.mcas.review; k++) push({ unit: null, day_type: "Review", title: "MCAS review · " + opts.mcas.titles[(k - 1) % opts.mcas.titles.length], lesson_id: prefix + "-MCAS-REVIEW-" + k, standards: "" });
      for (let k = 1; k <= opts.mcas.testing; k++) push({ unit: null, day_type: "Assessment", title: "MCAS Grade 7 Mathematics · Session " + k, lesson_id: prefix + "-MCAS-" + k, standards: "" });
    }
    if (!semesterDone && day >= 84) {
      semesterDone = true;
      push({ unit: null, day_type: "Review", title: "Semester 1 Review", lesson_id: prefix + "-SEM-REVIEW-1", standards: "" });
      push({ unit: null, day_type: "Review", title: "Semester 1 Review", lesson_id: prefix + "-SEM-REVIEW-2", standards: "" });
      push({ unit: null, day_type: "Assessment", title: "Semester Exam", lesson_id: prefix + "-SEM-EXAM", standards: "" });
    }
  }
  if (opts.ap) {
    let k = 0;
    while (day < 152) push({ unit: null, day_type: "Review", title: (k++ % 2 ? "AP review · Free-response practice" : "AP review · Timed multiple-choice practice"), lesson_id: prefix + "-AP-REVIEW-" + (day + 1), standards: "" });
    push({ unit: null, day_type: "Assessment", title: (opts.exam || "AP Calculus AB Exam") + " (early-to-mid May)", lesson_id: prefix + "-AP-EXAM", standards: "" });
    const projects = opts.projects || [];
    k = 0;
    while (day < 179) push({ unit: null, day_type: "Practice", title: "Post-exam project" + (projects.length ? " · " + projects[Math.floor(k++ / 4) % projects.length] : ""), lesson_id: prefix + "-PROJECT-" + (day + 1), standards: "" });
    push({ unit: null, day_type: "Flex", title: "Course reflection", lesson_id: prefix + "-FINAL-FLEX", standards: "" });
  } else {
  while (day < 177) push({ unit: null, day_type: "Review", title: "Final Review", lesson_id: prefix + "-FINAL-REVIEW-" + (day + 1), standards: "" });
  push({ unit: null, day_type: "Review", title: "Final Review", lesson_id: prefix + "-FINAL-REVIEW-LAST", standards: "" });
  push({ unit: null, day_type: "Assessment", title: "Final Exam", lesson_id: prefix + "-FINAL-EXAM", standards: "" });
  push({ unit: null, day_type: "Flex", title: "Course reflection", lesson_id: prefix + "-FINAL-FLEX", standards: "" });
  }
  const ideas = {}, names = {};
  for (const d of days) if (d.day_type === "Lesson") {
    const sk = lessonsMap[d.lesson_id] && lessonsMap[d.lesson_id].skills[0];
    if (sk && teach[sk[1]]) ideas[d.lesson_id] = teach[sk[1]].idea;
  }
  const C = w.MK_COURSE_CATALOG;
  for (const u of w.LIBRARY.courses.find((c) => c.id === course).units) for (const sk of C.getSkillRecords(course, u.id)) names[course + "-" + u.id + "/" + sk.id] = { name: sk.name, unit: u.name };
  return { scope: { meta: base.meta, units, days }, ideas, names };
}

/* Per-course sources (Algebra 1 joined 2026-11-17, audit #8 and #9; Algebra 2 joined 2026-11-17, Algebra 2 audit #3). */
const COURSES = {
  geometry: { name: "Geometry", scope: "worksheet-generator/planner/geometry_scope_sequence.json", sets: /^geometry-/, page: "geometry-pacing/",
    ideas: () => (win("worksheet-generator/planner/notes-data-geometry.js").MKPLAN_GEOMETRY_NOTES || {}).ideas || {} },
  algebra: { name: "Algebra 1", scope: "worksheet-generator/planner/algebra1_scope_sequence.json", sets: /^algebra1-/, page: "algebra-1-pacing/",
    ideas: () => (win("worksheet-generator/planner/notes-content.js").MKPLAN || {}).KEY_IDEAS || {} },
  algebra2: { name: "Algebra 2", load: () => bankScope("algebra2", "A2"), sets: /^algebra2-/, page: "algebra-2-pacing/", framework: "Massachusetts Model Algebra II", bank: true },
  precalculus: { name: "Precalculus", load: () => bankScope("precalculus", "PC"), sets: /^precalculus-/, page: "precalculus-pacing/", framework: "Common Core (+) standards for precalculus", bank: true },
  discrete: { name: "Discrete Math", load: () => bankScope("discrete", "DM"), sets: /^discrete-/, page: "discrete-math-pacing/", framework: "Discrete Mathematics strand or Common Core", bank: true },
  prealgebra: { name: "8th Grade Math", load: () => bankScope("prealgebra", "PA8"), sets: /^prealgebra-/, page: "8th-grade-math-pacing/", framework: "Common Core Grade 8", bank: true },
  calculus: { name: "Calculus", load: () => bankScope("calculus", "CA", { ap: true, projects: calculusProjects() }), sets: /^calculus-/, page: "calculus-pacing/", framework: "AP Calculus AB learning objectives", bank: true, ap: true },
  /* Pre-Algebra, Grade 7 (2026-11-19, Grade 7 audit #17): an accelerated course (all of Grade 7 and most of Grade 8)
     planned around the spring Grade 7 MCAS: review days with the two cumulative practice tests and the testing sessions
     come after Data Analysis and Probability (unit 12), and unit 13 (Nonlinear Functions and Polynomials, high-school
     algebra) follows the test. The coverage table lists every Grade 7 and Grade 8 standard. */
  prealgebra7: { name: "Pre-Algebra (Grade 7)", load: () => bankScope("prealgebra7", "PA7", { mcas: { afterUnit: 12, review: 6, testing: 2, flex: 4,
    titles: ["Practice Test A", "Practice Test A review", "Practice Test B", "Practice Test B review", "Reference sheet and open response", "Targeted reteach"] } }),
    sets: /^prealgebra7-/, page: "grade-7-pacing/", framework: "Massachusetts Grade 7 and Grade 8 mathematics", bank: true, mcas: true },
  /* Statistics (2026-11-18, Statistics audit #5): an AP course like Calculus. The four course units cover the five units of
     the AP Statistics framework effective fall 2026; new content ends about mid-April, AP review and the two practice exams
     run to the exam in May, and the four Statistics projects fill the weeks after it. */
  statistics: { name: "Statistics", load: () => bankScope("statistics", "ST", { ap: true, noReviewUnit: true, exam: "AP Statistics Exam", projects: calculusProjects("statistics") }), sets: /^statistics-/, page: "statistics-pacing/", framework: "AP Statistics learning objectives (framework effective fall 2026)", bank: true, ap: true, apName: "AP Statistics",
    apNote: "The four course units cover the five units of the AP Statistics framework effective fall 2026: Exploring Data covers AP Units 1 and 5 (one-variable data and regression); Sampling and Experimentation covers the data-collection topics of AP Unit 1; Anticipating Patterns covers AP Unit 2 (probability, random variables and distributions) with the sampling-distribution topics of Units 3 and 4; Statistical Inference covers AP Units 3 and 4 (inference for proportions and for means). Skills marked “Beyond AP” (geometric distributions, combining random variables, chi-square goodness of fit and inference for slope) are no longer on the AP exam and can be shortened or skipped. Use the two AP Statistics practice exams in the final review weeks." }
};
function calculusProjects(course = "calculus") {
  const re = new RegExp("^" + course + "-project-");
  try {
    return fs.readdirSync(path.join(ROOT, "artifacts")).filter((d) => re.test(d)).sort()
      .map((d) => d.replace(re, "").split("-").map((w) => w[0].toUpperCase() + w.slice(1)).join(" "));
  } catch (e) { return []; }
}
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
// Common Core (+) standards a precalculus course covers (Precalculus audit #3, 2026-11-18), with the non-(+) trigonometry and conics it extends.
const ALL_PRECALCULUS = [["N-CN.A.3", "+"], ["N-CN.B.4", "+"], ["N-CN.B.5", "+"], ["N-CN.B.6", "+"], ["N-CN.C.8", "+"], ["N-CN.C.9", "+"],
  ["N-VM.A.1", "+"], ["N-VM.A.2", "+"], ["N-VM.A.3", "+"], ["N-VM.B.4", "+"], ["N-VM.B.5", "+"], ["N-VM.C.6", "+"], ["N-VM.C.7", "+"], ["N-VM.C.8", "+"], ["N-VM.C.9", "+"],
  ["N-VM.C.10", "+"], ["N-VM.C.11", "+"], ["N-VM.C.12", "+"], ["A-APR.C.5", "+"], ["A-APR.D.7", "+"], ["A-REI.C.8", "+"], ["A-REI.C.9", "+"],
  ["F-IF.C.7d", "+"], ["F-BF.A.1c", "+"], ["F-BF.B.4b", "+"], ["F-BF.B.4c", "+"], ["F-BF.B.4d", "+"], ["F-BF.B.5", "+"],
  ["F-TF.A.3", "+"], ["F-TF.A.4", "+"], ["F-TF.B.5"], ["F-TF.B.6", "+"], ["F-TF.B.7", "+"], ["F-TF.C.8"], ["F-TF.C.9", "+"],
  ["G-SRT.D.9", "+"], ["G-SRT.D.10", "+"], ["G-SRT.D.11", "+"], ["G-GPE.A.2"], ["G-GPE.A.3", "+"],
  ["S-MD.A.1", "+"], ["S-MD.A.2", "+"], ["S-MD.A.3", "+"], ["S-MD.A.4", "+"], ["S-MD.B.5", "+"], ["S-MD.B.6", "+"], ["S-MD.B.7", "+"], ["S-CP.B.8", "+"], ["S-CP.B.9", "+"]];
// AP Calculus AB learning objectives from the Course and Exam Description (Calculus audit #7 and #11, 2026-11-18).
const ALL_CALCULUS = [["AP CHA-1.A"], ["AP LIM-1.A"], ["AP LIM-1.B"], ["AP LIM-1.C"], ["AP LIM-1.D"], ["AP LIM-1.E"], ["AP LIM-2.A"], ["AP LIM-2.B"], ["AP LIM-2.C"], ["AP LIM-2.D"], ["AP FUN-1.A"], ["AP CHA-2.A"], ["AP CHA-2.B"], ["AP CHA-2.C"], ["AP CHA-2.D"], ["AP FUN-2.A"], ["AP FUN-3.A"], ["AP LIM-3.A"], ["AP FUN-3.B"], ["AP FUN-3.C"], ["AP FUN-3.D"], ["AP FUN-3.E"], ["AP FUN-3.F"], ["AP CHA-3.A"], ["AP CHA-3.B"], ["AP CHA-3.C"], ["AP CHA-3.D"], ["AP CHA-3.E"], ["AP CHA-3.F"], ["AP LIM-4.A"], ["AP FUN-1.B"], ["AP FUN-1.C"], ["AP FUN-4.A"], ["AP FUN-4.B"], ["AP FUN-4.C"], ["AP FUN-4.D"], ["AP FUN-4.E"], ["AP CHA-4.A"], ["AP LIM-5.A"], ["AP LIM-5.B"], ["AP LIM-5.C"], ["AP FUN-5.A"], ["AP FUN-6.A"], ["AP FUN-6.B"], ["AP FUN-6.C"], ["AP FUN-6.D"], ["AP FUN-7.A"], ["AP FUN-7.B"], ["AP FUN-7.D"], ["AP FUN-7.E"], ["AP FUN-7.F"], ["AP FUN-7.G"], ["AP CHA-4.B"], ["AP CHA-4.C"], ["AP CHA-4.D"], ["AP CHA-4.E"], ["AP CHA-5.A"], ["AP CHA-5.B"], ["AP CHA-5.C"]];
// Common Core Grade 8 standards (8th Grade Math audit #2, 2026-11-19), sub-standards where the bank tags them separately.
const ALL_GRADE8 = [["8.NS.A.1"], ["8.NS.A.2"], ["8.EE.A.1"], ["8.EE.A.2"], ["8.EE.A.3"], ["8.EE.A.4"], ["8.EE.B.5"], ["8.EE.B.6"], ["8.EE.C.7a"], ["8.EE.C.7b"],
  ["8.EE.C.8a"], ["8.EE.C.8b"], ["8.EE.C.8c"], ["8.F.A.1"], ["8.F.A.2"], ["8.F.A.3"], ["8.F.B.4"], ["8.F.B.5"], ["8.G.A.1"], ["8.G.A.2"], ["8.G.A.3"], ["8.G.A.4"], ["8.G.A.5"],
  ["8.G.B.6"], ["8.G.B.7"], ["8.G.B.8"], ["8.G.C.9"], ["8.SP.A.1"], ["8.SP.A.2"], ["8.SP.A.3"], ["8.SP.A.4"]];
// Discrete Math has no single published framework: list every code the bank's skills are tagged with, DM strands first.
function discreteStandards(stdSkills) {
  const codes = new Set();
  for (const [set, skills] of Object.entries(stdSkills)) if (/^discrete-/.test(set)) for (const list of Object.values(skills)) for (const c of list) if (!/^MP\./.test(c)) codes.add(c);
  return [...codes].sort((a, b) => (/^DM/.test(b) - /^DM/.test(a)) || a.localeCompare(b, "en", { numeric: true })).map((c) => [c]);
}
// Grade 7 (Grade 7 audit #17, 2026-11-19): every Common Core Grade 7 and Grade 8 standard at its finest level.
const ALL_PREALGEBRA7 = [..."7.RP.A.1 7.RP.A.2a 7.RP.A.2b 7.RP.A.2c 7.RP.A.2d 7.RP.A.3 7.NS.A.1a 7.NS.A.1b 7.NS.A.1c 7.NS.A.1d 7.NS.A.2a 7.NS.A.2b 7.NS.A.2c 7.NS.A.2d 7.NS.A.3 7.EE.A.1 7.EE.A.2 7.EE.B.3 7.EE.B.4a 7.EE.B.4b 7.G.A.1 7.G.A.2 7.G.A.3 7.G.B.4 7.G.B.5 7.G.B.6 7.SP.A.1 7.SP.A.2 7.SP.B.3 7.SP.B.4 7.SP.C.5 7.SP.C.6 7.SP.C.7a 7.SP.C.7b 7.SP.C.8a 7.SP.C.8b 7.SP.C.8c".split(" "),
  ..."8.NS.A.1 8.NS.A.2 8.EE.A.1 8.EE.A.2 8.EE.A.3 8.EE.A.4 8.EE.B.5 8.EE.B.6 8.EE.C.7a 8.EE.C.7b 8.EE.C.8a 8.EE.C.8b 8.EE.C.8c 8.F.A.1 8.F.A.2 8.F.A.3 8.F.B.4 8.F.B.5 8.G.A.1 8.G.A.2 8.G.A.3 8.G.A.4 8.G.A.5 8.G.B.6 8.G.B.7 8.G.B.8 8.G.C.9 8.SP.A.1 8.SP.A.2 8.SP.A.3 8.SP.A.4".split(" ")].map((c) => [c]);
// AP Statistics learning objectives, framework effective fall 2026 (Statistics audit #3 and #5, 2026-11-18).
const ALL_STATISTICS = [["APSTATS.1.1.A"], ["APSTATS.1.1.B"], ["APSTATS.1.2.A"], ["APSTATS.1.2.B"], ["APSTATS.1.2.C"], ["APSTATS.1.3.A"], ["APSTATS.1.3.B"], ["APSTATS.1.4.A"], ["APSTATS.1.4.B"], ["APSTATS.1.4.C"], ["APSTATS.1.5.A"], ["APSTATS.1.6.A"], ["APSTATS.1.6.B"], ["APSTATS.1.7.A"], ["APSTATS.1.7.B"], ["APSTATS.1.7.C"], ["APSTATS.1.7.D"], ["APSTATS.1.7.E"], ["APSTATS.1.7.F"], ["APSTATS.1.8.A"], ["APSTATS.1.8.B"], ["APSTATS.1.9.A"], ["APSTATS.1.9.B"], ["APSTATS.1.9.C"], ["APSTATS.1.9.D"], ["APSTATS.1.9.E"], ["APSTATS.1.10.A"], ["APSTATS.1.10.B"], ["APSTATS.1.10.C"], ["APSTATS.1.10.D"], ["APSTATS.1.10.E"], ["APSTATS.1.11.A"], ["APSTATS.1.11.B"], ["APSTATS.1.12.A"], ["APSTATS.1.13.A"], ["APSTATS.1.13.B"], ["APSTATS.1.13.C"], ["APSTATS.1.13.D"], ["APSTATS.2.1.A"], ["APSTATS.2.1.B"], ["APSTATS.2.2.A"], ["APSTATS.2.2.B"], ["APSTATS.2.2.C"], ["APSTATS.2.3.A"], ["APSTATS.2.4.A"], ["APSTATS.2.5.A"], ["APSTATS.2.6.A"], ["APSTATS.2.7.A"], ["APSTATS.2.8.A"], ["APSTATS.2.9.A"], ["APSTATS.2.9.B"], ["APSTATS.2.10.A"], ["APSTATS.2.10.B"], ["APSTATS.2.10.C"], ["APSTATS.2.10.D"], ["APSTATS.2.10.E"], ["APSTATS.2.11.A"], ["APSTATS.2.11.B"], ["APSTATS.2.11.C"], ["APSTATS.2.11.D"], ["APSTATS.2.11.E"], ["APSTATS.2.11.F"], ["APSTATS.2.12.A"], ["APSTATS.3.1.A"], ["APSTATS.3.1.B"], ["APSTATS.3.2.A"], ["APSTATS.3.2.B"], ["APSTATS.3.2.C"], ["APSTATS.3.3.A"], ["APSTATS.3.3.B"], ["APSTATS.3.3.C"], ["APSTATS.3.3.D"], ["APSTATS.3.4.A"], ["APSTATS.3.4.B"], ["APSTATS.3.4.C"], ["APSTATS.3.5.A"], ["APSTATS.3.5.B"], ["APSTATS.3.5.C"], ["APSTATS.3.6.A"], ["APSTATS.3.7.A"], ["APSTATS.3.7.B"], ["APSTATS.3.8.A"], ["APSTATS.3.8.B"], ["APSTATS.3.8.C"], ["APSTATS.3.8.D"], ["APSTATS.3.9.A"], ["APSTATS.3.9.B"], ["APSTATS.3.9.C"], ["APSTATS.3.10.A"], ["APSTATS.3.10.B"], ["APSTATS.3.10.C"], ["APSTATS.3.10.D"], ["APSTATS.3.11.A"], ["APSTATS.3.11.B"], ["APSTATS.3.12.A"], ["APSTATS.3.12.B"], ["APSTATS.3.12.C"], ["APSTATS.3.13.A"], ["APSTATS.3.13.B"], ["APSTATS.3.13.C"], ["APSTATS.3.14.A"], ["APSTATS.3.14.B"], ["APSTATS.3.14.C"], ["APSTATS.3.14.D"], ["APSTATS.3.15.A"], ["APSTATS.3.15.B"], ["APSTATS.3.15.C"], ["APSTATS.3.15.D"], ["APSTATS.4.1.A"], ["APSTATS.4.1.B"], ["APSTATS.4.1.C"], ["APSTATS.4.2.A"], ["APSTATS.4.2.B"], ["APSTATS.4.2.C"], ["APSTATS.4.2.D"], ["APSTATS.4.2.E"], ["APSTATS.4.3.A"], ["APSTATS.4.3.B"], ["APSTATS.4.3.C"], ["APSTATS.4.4.A"], ["APSTATS.4.4.B"], ["APSTATS.4.4.C"], ["APSTATS.4.5.A"], ["APSTATS.4.5.B"], ["APSTATS.4.5.C"], ["APSTATS.4.6.A"], ["APSTATS.4.6.B"], ["APSTATS.4.6.C"], ["APSTATS.4.7.A"], ["APSTATS.4.7.B"], ["APSTATS.4.7.C"], ["APSTATS.4.7.D"], ["APSTATS.4.8.A"], ["APSTATS.4.8.B"], ["APSTATS.4.9.A"], ["APSTATS.4.9.B"], ["APSTATS.4.9.C"], ["APSTATS.4.10.A"], ["APSTATS.4.10.B"], ["APSTATS.4.10.C"], ["APSTATS.5.1.A"], ["APSTATS.5.1.B"], ["APSTATS.5.1.C"], ["APSTATS.5.2.A"], ["APSTATS.5.3.A"], ["APSTATS.5.4.A"], ["APSTATS.5.4.B"], ["APSTATS.5.4.C"], ["APSTATS.5.5.A"], ["APSTATS.5.5.B"]];
export function geoPacingMain(course = "geometry", unitHref) {
  const { scope, stdSkills, names, C } = data(course), ALL = { algebra2: ALL_ALGEBRA2, precalculus: ALL_PRECALCULUS, algebra: ALL_ALGEBRA, calculus: ALL_CALCULUS, statistics: ALL_STATISTICS, prealgebra: ALL_GRADE8, discrete: discreteStandards(stdSkills), prealgebra7: ALL_PREALGEBRA7 }[course] || ALL_GEOMETRY;
  const framework = C.framework || "Common Core " + C.name, source = C.bank ? "question-bank skill" : "generator skill";
  const slug = (t) => ({ "Foundations of Geometry": "foundations-geometry", "Area, Surface Area and Volume": "area-surface-area-volume", "Right Triangles and Trigonometry": "right-triangles-trigonometry", "Quadrilaterals and Polygons": "quadrilaterals-polygons", "Angles and Parallel Lines": "angles-parallel-lines" }[t] || t.toLowerCase().replace(/ /g, "-"));
  const href = unitHref || ((t) => "../u/geometry/" + slug(t) + "/");
  const wk = (d) => Math.ceil(d / 5);
  let h = `<h1>${esc(C.name)} Pacing Guide and Standards Coverage</h1>
<p class="lede">A 180-day full-year plan in two semesters, a compressed one-semester (90-day block) plan, and a table showing which ${source}s practice each ${C.ap ? esc(C.apName || "AP Calculus AB") + " learning objective" : esc(framework) + " standard"}. Every lesson has a ready plan in the Lesson Planner.</p>
${C.ap ? `<p>The year is built around the ${esc(C.apName || "AP Calculus AB")} exam in May: new content ends about mid-April, ${C.apName ? "AP review and practice exams" : "the AP Review unit and practice exams"} fill the weeks before the exam, and the weeks after it go to the course projects. ${C.apNote ? esc(C.apNote) : "Euler’s method (Differential Equations) is a BC topic and can be skipped in an AB-only class."}</p>\n` : ""}${C.mcas ? `<p>The year is built around the spring Grade 7 MCAS. Units 1–12 come first, so every Grade 7 standard is taught before the test; six review days use the two cumulative practice tests and the Grade 7 reference sheet, then come the two testing sessions (about days ${(scope.days.find((d) => /^MCAS Grade 7/.test(d.title)) || {}).day}–${(scope.days.filter((d) => /^MCAS Grade 7/.test(d.title)).pop() || {}).day}; check your district’s testing window). Unit 13, high-school algebra, follows the test. Review skills (Grade 6 and earlier standards) are taught two to a day; the last column lists the Grade 7 and Grade 8 standards each unit practices.</p>\n` : ""}<p><a href="#year">Full year</a> · <a href="#block">One-semester block</a> · <a href="#standards">Standards coverage</a></p>
<h2 id="year">Full year (180 days, 36 weeks)</h2>
${C.mcas ? '<div style="overflow-x:auto">' : ""}<table><thead><tr><th>Unit</th><th>Days</th><th>Weeks</th><th>Lessons</th>${C.mcas ? "<th>Grade 7 and 8 standards</th>" : ""}</tr></thead><tbody>
`;
  const cols = C.mcas ? 5 : 4;
  const row = (u) => {
    const ls = scope.days.filter((d) => d.unit === u.unit && d.day_type === "Lesson").map((d) => esc(d.title));
    const g78 = C.mcas ? STD.sort([...new Set(STD.content(STD.split(scope.days.filter((d) => d.unit === u.unit && d.day_type === "Lesson").map((d) => d.standards).join(", "))).filter((c) => /^[78]\./.test(c)))]) : [];
    return `<tr><td><a href="${href(u.title)}">Unit ${u.unit}: ${esc(u.title)}</a></td><td>${u.start_day}–${u.end_day} (${u.total_days})</td><td>${wk(u.start_day)}–${wk(u.end_day)}</td><td>${ls.join("; ")}</td>${C.mcas ? `<td>${g78.length ? esc(g78.join(", ")) : "—"}</td>` : ""}</tr>\n`;
  };
  const sem = scope.days.find((d) => /^Semester Exam/.test(d.title));
  for (const u of scope.units) {
    h += row(u);
    if (sem && u.end_day < sem.day && (scope.units.find((x) => x.unit === u.unit + 1) || {}).start_day > sem.day)
      h += `<tr><td colspan="${cols}"><strong>Semester 1 review and exam</strong> (days ${sem.day - 2}–${sem.day})</td></tr>\n`;
    const mr = scope.days.filter((d) => d.unit === null && /^MCAS/.test(d.title));
    if (C.mcas && mr.length && mr[0].day === u.end_day + 1)
      h += `<tr><td colspan="${cols}"><strong>MCAS review and testing</strong> (days ${mr[0].day}–${mr[mr.length - 1].day}): ${esc(mr.map((d) => d.title.replace(/^MCAS (review · )?/, "")).join("; "))}</td></tr>\n`;
  }
  if (C.ap) {
    const apr = scope.days.filter((d) => /^AP review/.test(d.title)), exam = scope.days.find((d) => /^AP (?:Calculus AB|Statistics) Exam/.test(d.title)), proj = scope.days.filter((d) => /^Post-exam project/.test(d.title));
    if (apr.length) h += `<tr><td colspan="4"><strong>AP review and practice exams</strong> (days ${apr[0].day}–${apr[apr.length - 1].day}): alternate timed multiple-choice and free-response practice</td></tr>\n`;
    if (exam) h += `<tr><td colspan="4"><strong>${esc(C.apName || "AP Calculus AB")} Exam</strong> (about day ${exam.day}, early-to-mid May; check the College Board date for your year)</td></tr>\n`;
    if (proj.length) h += `<tr><td colspan="4"><strong>Post-exam projects</strong> (days ${proj[0].day}–${proj[proj.length - 1].day}): ${esc([...new Set(proj.map((d) => d.title.split(" · ")[1]).filter(Boolean))].join("; "))}</td></tr>\n`;
  } else {
  const fin = scope.days.filter((d) => d.unit === null && d.day > 170);
  if (fin.length) h += `<tr><td colspan="${cols}"><strong>Final review and exam</strong> (days ${fin[0].day}–${fin[fin.length - 1].day})</td></tr>\n`;
  }
  h += `</tbody></table>\n${C.mcas ? "</div>\n" : ""}`;
  // one semester (block): each 90-minute block covers two days of the full-year plan
  h += `<h2 id="block">One semester (90-day block)</h2>\n<p>On a block schedule each 90-minute class covers two days of the full-year plan: a lesson and its practice, or two lessons. Day 1 is the launch and diagnostic.</p>\n<table><thead><tr><th>Unit</th><th>Block days</th></tr></thead><tbody>\n`;
  let day = 1;
  for (const u of scope.units) {
    const keep = Math.ceil(u.total_days / 2); h += `<tr><td>Unit ${u.unit}: ${esc(u.title)}</td><td>${day + 1}–${day + keep} (${keep})</td></tr>\n`; day += keep;
    if (C.mcas && u.unit === 12) { h += `<tr><td>MCAS review and testing</td><td>${day + 1}–${day + 4} (4)</td></tr>\n`; day += 4; }
  }
  h += `<tr><td>${C.ap ? "AP review and practice exams" : "Final review and exam"}</td><td>${day + 1}${day + 1 < 90 ? "–90" : ""}</td></tr>\n</tbody></table>\n`;
  // standards coverage
  const bySkill = [];
  for (const [set, skills] of Object.entries(stdSkills)) if (C.sets.test(set)) for (const [sk, codes] of Object.entries(skills)) bySkill.push({ key: set + "/" + sk, codes });
  h += `<h2 id="standards">Standards coverage</h2>\n<p>Each ${source} is tagged with the standards it practices.${ALL.some(([, plus]) => plus) ? " Standards marked (+) are for advanced courses." : ""}${C.ap ? " Learning objectives are listed in the order the AP Course and Exam Description teaches them." : ""}</p>\n<table><thead><tr><th>Standard</th><th>What it asks</th><th>Skills that practice it</th></tr></thead><tbody>\n`;
  let gaps = 0;
  for (const [code, plus] of ALL) {
    const sk = bySkill.filter((s) => s.codes.some((x) => x === code || (x.indexOf(code) === 0 && /^[a-e]$/.test(x.slice(code.length))))).map((s) => (names[s.key] ? esc(names[s.key].name) : esc(s.key.split("/")[1])));
    if (!sk.length) gaps++;
    h += `<tr><td><strong>${esc(code)}</strong>${plus ? " (+)" : ""}</td><td>${esc(STD.describe(code))}</td><td>${sk.length ? `${sk.length} skill${sk.length > 1 ? "s" : ""}: ${sk.slice(0, 8).join("; ")}${sk.length > 8 ? "; …" : ""}` : "<em>Taught in lessons and activities; no generator skill yet</em>"}</td></tr>\n`;
  }
  h += `</tbody></table>\n<p>${ALL.length - gaps} of ${ALL.length} standards have ${C.bank ? "question-bank" : "generator"} practice.</p>\n`;
  return h;
}
