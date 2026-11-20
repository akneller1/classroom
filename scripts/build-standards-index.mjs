#!/usr/bin/env node
// Site UX audit (2026-11-20): one index of every standard the site practices, for search and the standards finder.
// Reads the built site (all courses, Grades 1-12) and writes standards-index.js:
//   MK_STANDARDS_INDEX = { courses: [[id, name, band]], units: { "course.unit": [courseId, unitId, unitName, [[kind, title, url]]] },
//                          std: { code: [[unitKey, skillName], ...] }, desc: { code: text } }
// Skill standards come from the generator standards map (secondary), the Grades 1-4 catalogs and the Grade 5 map
// (built from the bank's question tags by apply-site-audit.mjs). Usage: node scripts/build-standards-index.mjs [_site]
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";

const SITE = path.resolve(process.argv[2] || "_site");
const w = { console }; w.window = w; w.self = w;
w.document = { addEventListener() {}, querySelector() { return null; }, querySelectorAll() { return []; }, createElement() { return { style: {}, setAttribute() {}, appendChild() {} }; } };
vm.createContext(w);
const load = (rel) => { const f = path.join(SITE, rel); if (fs.existsSync(f)) vm.runInContext(fs.readFileSync(f, "utf8"), w, { filename: rel }); };
for (const rel of ["data.js", "course-catalog.js", "worksheet-generator/menu/standards.js", "worksheet-generator/menu/standards-map.js",
  "grade1-main-catalog.js", "grade2-main-catalog.js", "grade3-main-catalog.js", "grade4-main-catalog.js", "grade5/grade5-main-catalog.js", "grade5/grade5-standards-map.js",
  "worksheet-generator/core/rng.js", "worksheet-generator/core/frac.js", "worksheet-generator/core/tex.js", "worksheet-generator/core/graph.js", "worksheet-generator/core/framework.js",
  "worksheet-generator/menu/mathcheck.js", "worksheet-generator/menu/engine.js", "worksheet-generator/menu/skills/kit.js"]) {
  try { load(rel); } catch (e) { console.warn("standards index: skipped " + rel + ": " + e.message.slice(0, 80)); }
}
const skillDir = path.join(SITE, "worksheet-generator/menu/skills");
if (fs.existsSync(skillDir)) for (const f of fs.readdirSync(skillDir).filter((f) => /^(algebra1|geometry)-.*\.js$/.test(f))) {
  try { load("worksheet-generator/menu/skills/" + f); } catch (e) { /* a figure-only helper */ }
}
const L = w.LIBRARY, MAP = w.MKSTD_SKILLS || {}, STD = w.MKSTD, CAT = w.MK_COURSE_CATALOG, SETS = (w.MKMENU && w.MKMENU.skillSets) || {};
if (!L || !STD) throw Error("standards index: the course library or MKSTD did not load");

const band = (id) => (/^grade[1-5]$/.test(id) ? "K-5" : /^(math6|prealgebra7|prealgebra)$/.test(id) ? "6-8" : "9-12");
const courses = L.courses.filter((c) => c.units && c.units.length).map((c) => [c.id, c.name, band(c.id)]);
function url(path) {
  if (/^(https?:|\/|grade[1-5]\/|worksheet-generator\/|financial\/)/.test(path)) return path;
  return "activity.html?path=" + encodeURIComponent(path);
}
function kind(a) {
  const t = [].concat(a.type || "").join(" "), f = a.bankFormat || "";
  if (/generator/.test(f) || /lesson-planner|worksheet\.html|menu-assessment|printables\.html/.test(a.path)) return "Make";
  if (/Game/.test(t)) return "Play";
  if (/Interactive/.test(t) || f === "interactive-math") return "Explore";
  if (/Study Guide/.test(t)) return "Study";
  return "";
}
// skill-set id ("algebra2-polynomial-functions", "grade4-fractions") → course and unit, from the unit's own links
const units = {}, setToUnit = {};
for (const c of L.courses) for (const u of c.units || []) {
  const key = c.id + "." + u.id;
  const res = (u.artifacts || []).map((a) => [kind(a), a.title, url(a.path || "")]).filter((r) => r[0]);
  units[key] = [c.id, u.id, u.name, res.filter((r) => r[0] !== "Study").slice(0, 16)];
  setToUnit[c.id + "-" + u.id] = key;
  for (const a of u.artifacts || []) { const m = /[#?&]unit=([a-z0-9-]+)/.exec(a.path || ""); if (m && /-/.test(m[1]) && !setToUnit[m[1]]) setToUnit[m[1]] = key; }
}
const std = {};
function add(code, unitKey, skill) {
  const list = (std[code] = std[code] || []);
  if (!list.some((x) => x[0] === unitKey && x[1] === skill)) list.push([unitKey, skill]);
}
let skills = 0;
for (const [set, bySkill] of Object.entries(MAP)) {
  const unitKey = setToUnit[set] || setToUnit[set.replace(/^grade(\d)-/, "grade$1-")];
  if (!unitKey) continue;
  const [courseId, unitId] = units[unitKey];
  const records = (CAT && CAT.getSkillRecords ? CAT.getSkillRecords(courseId, unitId) : []) || [];
  const named = {};
  records.forEach((r) => { named[r.id] = r.name; });
  ((SETS[set] && SETS[set].skills) || []).forEach((s) => { named[s.id] = s.name; });
  for (const [skill, codes] of Object.entries(bySkill)) {
    const name = named[skill] || named[unitId + "-" + skill];
    if (!name) continue;
    skills++;
    for (const code of STD.split(codes)) add(code, unitKey, name);
  }
}
const desc = {};
const ELEM = JSON.parse(fs.readFileSync(new URL("../tools/site-audit-20261120/elementary-standards.json", import.meta.url), "utf8"));
for (const code of Object.keys(std)) { const d = STD.describe(code) || ELEM[code]; if (d) desc[code] = d; }
const index = { courses, units: Object.fromEntries(Object.entries(units).filter(([k]) => Object.values(std).some((l) => l.some((x) => x[0] === k)))), std, desc };
fs.writeFileSync(path.join(SITE, "standards-index.js"), "/* Built by scripts/build-standards-index.mjs. */\nwindow.MK_STANDARDS_INDEX=" + JSON.stringify(index) + ";\n");
console.log(`Standards index: ${Object.keys(std).length} standards, ${skills} skills, ${Object.keys(index.units).length} units, ${Object.keys(desc).length} descriptions`);
