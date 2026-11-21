#!/usr/bin/env node
// Quantitative Modeling units for Financial Algebra (2026-11-21).
//
// Financial Algebra is built from a pinned copy of its own repository, which this repo does not change. This step
// makes an extended copy of that source: it adds the unit content, projects, Decision Labs, standards and cheat-sheet
// content kept in tools/fa-modeling/, then runs Financial Algebra's own build scripts (banks, flashcards, resource
// manifest, pacing guide) so the new units get every resource the first ten have. Cheat-sheet PDFs, project pages and
// thumbnails need a browser, so they are built once with --print by the same scripts and kept in this repo's artifacts/
// and thumbs/financial-algebra/, where the first ten units' copies are too.
// scripts/integrate-financial-algebra.mjs then assembles the extended copy as usual.
//
// Usage: node scripts/build-fa-extension.mjs <pinned FA source> <output dir> [--print]
//   --print also rebuilds the browser-made files (cheat sheets, project pages, previews) into artifacts/ and thumbs/.
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const EXT = path.join(ROOT, "tools/fa-modeling");
const [src, out] = process.argv.slice(2).filter((a) => !a.startsWith("--")).map((p) => path.resolve(p));
const PRINT = process.argv.includes("--print");
if (!src || !out) throw Error("Usage: node scripts/build-fa-extension.mjs <pinned FA source> <output dir> [--print]");
const must = (c, m) => { if (!c) throw Error("FA extension: " + m); };
const UNITS = JSON.parse(fs.readFileSync(path.join(EXT, "units.json"), "utf8")).units;

// 1. Copy the pinned source.
fs.rmSync(out, { recursive: true, force: true });
fs.cpSync(src, out, { recursive: true, filter: (p) => !/[\\/](\.git|node_modules)$/.test(p) });
const F = (rel) => path.join(out, rel);
const patch = (rel, find, insert, where = "before") => {
  const s = fs.readFileSync(F(rel), "utf8"), i = s.lastIndexOf(find);
  must(i >= 0, `${rel}: anchor not found: ${find}`);
  fs.writeFileSync(F(rel), where === "before" ? s.slice(0, i) + insert + s.slice(i) : s.slice(0, i + find.length) + insert + s.slice(i + find.length));
};

// 2. Content modules, cheat-sheet content and projects.
for (const f of fs.readdirSync(path.join(EXT, "content"))) if (f.endsWith(".mjs")) fs.copyFileSync(path.join(EXT, "content", f), F("financial/content/" + f));
for (const f of fs.readdirSync(path.join(EXT, "content/projects"))) fs.copyFileSync(path.join(EXT, "content/projects", f), F("financial/content/projects/" + f));
const ready = UNITS.filter((u) => fs.existsSync(path.join(EXT, "content", u.id + ".mjs")));
must(ready.length, "no unit content in tools/fa-modeling/content");

// 3. Course units (src/course.js), in the order of units.json.
const unitLines = ready.map((u) => `,\n    ${JSON.stringify({ id: u.id, name: u.name, status: "ready", skills: u.skills })}`).join("");
patch("src/course.js", "\n  ]\n};", unitLines);

// 4. Standards: personal-finance codes and Common Core math codes for every new skill.
const sid = (u, k) => `${u.id}-skill-${String(k + 1).padStart(2, "0")}`;
const std = ready.flatMap((u) => u.standards.map((s, k) => `, ${JSON.stringify(sid(u, k))}: S(${s.map((c) => JSON.stringify(c)).join(", ")})`)).join("");
const mathStd = ready.flatMap((u) => u.math.map((s, k) => `, ${JSON.stringify(sid(u, k))}: ${JSON.stringify(s)}`)).join("");
{
  let s = fs.readFileSync(F("financial/content/standards.mjs"), "utf8");
  const a = s.indexOf("export const SKILL_STANDARDS"), aEnd = s.indexOf("\n};", a);
  must(a >= 0 && aEnd > a, "SKILL_STANDARDS not found");
  s = s.slice(0, aEnd) + std + s.slice(aEnd);
  const b = s.indexOf("export const MATH_STANDARDS"), bEnd = s.indexOf("};", b);
  must(b >= 0 && bEnd > b, "MATH_STANDARDS not found");
  s = s.slice(0, bEnd) + mathStd + s.slice(bEnd);
  fs.writeFileSync(F("financial/content/standards.mjs"), s);
}

// 5. Decision Labs (one per new unit), added to the same FA_LABS object as the first ten.
patch("financial/decision-lab/scenarios.js", "  G.FA_LABS = L;", fs.readFileSync(path.join(EXT, "labs.js"), "utf8") + "\n");

// 6. Pacing guide: the semester and full-year plans stay the ten personal-finance units; the modeling units get
//    their own section with a ready block of days, so a Quantitative Modeling course can swap them in.
{
  const rel = "scripts/build-pacing.mjs";
  let s = fs.readFileSync(F(rel), "utf8");
  const loop = "  for (const u of units) {\n    const U = `Unit ${u.n}`;";
  must(s.split(loop).length === 3, "build-pacing.mjs: unit loops changed");
  s = s.split(loop).join("  for (const u of units.filter((u) => u.n <= 10)) {\n    const U = `Unit ${u.n}`;");
  const qm = `const qmUnits = units.filter((u) => u.n > 10);
const qmSection = qmUnits.length ? \`<section id="modeling"><h2>Quantitative Modeling units (Units 11–\${10 + qmUnits.length})</h2><p>These units add the modeling topics of a Quantitative Modeling or Quantitative Reasoning course: percents and consumer math, linear and exponential models, data and regression, and probability. Each has the same resources as the personal-finance units. Teach them after Unit \${10}, or swap them in for personal-finance units in a modeling course. Each block below is one unit.</p><div class="fa-table-wrap"><table class="fa-table"><thead><tr><th scope="col">Unit</th><th scope="col">Semester block (7 days)</th><th scope="col">Full-year block (12 days)</th></tr></thead><tbody>\${qmUnits.map((u) => \`<tr><th scope="row">Unit \${u.n}: \${esc(u.name)}</th><td>\${u.skills.map((s) => 'Lesson: ' + esc(s.name)).join('<br>')}<br>Decision Lab: \${esc(u.lab || '')}<br>Review: Practice Test, Error Analysis, games<br>Unit \${u.n} assessment</td><td>Two days per skill (lesson, then practice and modeling)<br>Decision Lab: \${esc(u.lab || '')}\${u.project ? '<br>Project: ' + esc(u.project) + ' (2 days)' : ''}<br>Review day and assessment</td></tr>\`).join('')}</tbody></table></div></section>\` : '';
`;
  s = s.replace("const html = `<!doctype html>", qm + "const html = `<!doctype html>");
  s = s.replace('<section id="standards">', '${qmSection}\n<section id="standards">');
  s = s.replace('<a class="fa-btn" href="#standards">Standards map</a>', '<a class="fa-btn" href="#modeling">Modeling units</a><a class="fa-btn" href="#standards">Standards map</a>');
  fs.writeFileSync(F(rel), s);
}

// 7. Financial Algebra's own build scripts.
const run = (script, args = []) => execFileSync(process.execPath, [F("scripts/" + script), ...args], { cwd: out, stdio: ["ignore", "pipe", "inherit"] }).toString();
run("build-banks.mjs");
// Worked steps for concept and claim items (the Classroom audit asks every question for at least two steps):
//   concept: [the concept's "how" line, its explanation]; claim: [model answer, worked example, verdict].
for (const u of ready) {
  const content = (await import(pathToFileURL(F(`financial/content/${u.id}.mjs`)).href)).default;
  for (const rel of [`financial/banks/${u.id}.json`, `question-banks/financial-algebra/${u.id}.json`]) {
    const bank = JSON.parse(fs.readFileSync(F(rel), "utf8"));
    for (const q of bank.questions) {
      if ((q.solutionSteps || []).length > 1) continue;
      const c = /-concept-(\d+)$/.exec(q.id), cl = /-claim(?:-cer)?-(\d+)$/.exec(q.id);
      if (c) { const x = content.concepts[Number(c[1]) - 1]; must(x && x.how, `${q.id}: concept has no how line`); q.solutionSteps = [x.how, ...q.solutionSteps]; }
      else if (cl) { const x = content.claims[Number(cl[1]) - 1]; q.solutionSteps = [...q.solutionSteps, ...(x.example ? ["Example: " + x.example] : []), "Verdict: " + ["Always true", "Sometimes true — it depends on the situation", "Never true"][x.verdict] + "."]; }
    }
    fs.writeFileSync(F(rel), JSON.stringify(bank, null, 1));
  }
}
run("build-hub.mjs");
run("build-pacing.mjs");
const ids = ready.map((u) => u.id);
if (PRINT) {
  // Playwright for the print scripts comes from this repo's node_modules.
  if (!fs.existsSync(F("node_modules"))) fs.symlinkSync(path.join(ROOT, "node_modules"), F("node_modules"));
  run("build-print.mjs", ids);
  execFileSync("python3", [F("scripts/build_office.py")], { cwd: out, stdio: ["ignore", "pipe", "inherit"] });   // editable Word and PowerPoint
  // Resource previews: the same script as the first ten units, with a topic line and a picture for each new unit.
  let py = fs.readFileSync(F("scripts/build-resource-thumbnails.py"), "utf8");
  py = py.replace("TOPICS={\n", "TOPICS={\n" + ready.map((u) => `${JSON.stringify(u.id)}:${JSON.stringify(u.thumb).replace(/^\[/, "(").replace(/\]$/, ")")},\n`).join(""));
  py = py.replace("def scene(uid,c):\n", "def scene(uid,c):\n" + ready.map((u) => ` if uid==${JSON.stringify(u.id)}:return ${u.scene}\n`).join(""));
  fs.writeFileSync(F("scripts/build-resource-thumbnails.py"), py);
  execFileSync("python3", [F("scripts/build-resource-thumbnails.py")], { cwd: out, stdio: ["ignore", "pipe", "inherit"] });
  for (const u of ready) {
    // Game previews: the first ten units' game cards carry only the unit name.
    for (const g of ["showdown", "connect-four", "tic-tac-toe", "picture-reveal", "detective"]) {
      const t = fs.readFileSync(F(`thumbs/financial-algebra/insurance-${g}.svg`), "utf8");
      fs.writeFileSync(F(`thumbs/financial-algebra/${u.id}-${g}.svg`), t.replace("Insurance &amp; Risk", u.name.replace(/&/g, "&amp;")));
    }
    // Cheat-sheet preview: both PDF pages side by side, like the first ten.
    const pdf = F(`artifacts/financial-algebra-${u.id}-cheat-sheet/cheat-sheet.pdf`), tmp = path.join(out, "tmp-cs-" + u.id);
    execFileSync("pdftoppm", ["-r", "40", "-png", pdf, tmp]);
    execFileSync("python3", ["-c", `from PIL import Image;import glob;ps=[Image.open(p).convert('RGB') for p in sorted(glob.glob('${tmp}*.png'))][:2];W,H=720,450;bg=Image.new('RGB',(W,H),(238,240,246));w=(W-36)//2
for k,p in enumerate(ps):
 h=int(p.height*w/p.width);im=p.resize((w,h));bg.paste(im,(12+k*(w+12),max(6,(H-h)//2)))
bg.save('${F(`thumbs/financial-algebra/${u.id}-cheat-sheet.jpg`)}',quality=88)`]);
    for (const f of fs.readdirSync(out).filter((f) => f.startsWith("tmp-cs-"))) fs.rmSync(path.join(out, f));
  }
  // Keep the browser-made files in this repo, where the Classroom site publishes them too (like the first ten units).
  for (const u of ready) {
    for (const d of [`financial-algebra-${u.id}-cheat-sheet`, ...projectSlugs(u.id).map((s) => "financial-algebra-project-" + s)]) {
      fs.rmSync(path.join(ROOT, "artifacts", d), { recursive: true, force: true });
      fs.cpSync(F("artifacts/" + d), path.join(ROOT, "artifacts", d), { recursive: true });
    }
    for (const t of fs.readdirSync(F("thumbs/financial-algebra")).filter((t) => t.startsWith(u.id + "-"))) fs.copyFileSync(F("thumbs/financial-algebra/" + t), path.join(ROOT, "thumbs/financial-algebra", t));
  }
}
// 8. Browser-made files for the new units, kept in this repo's artifacts/ and thumbs/financial-algebra/.
for (const u of ready) {
  for (const d of [`financial-algebra-${u.id}-cheat-sheet`, ...projectSlugs(u.id).map((s) => "financial-algebra-project-" + s)]) {
    const from = path.join(ROOT, "artifacts", d);
    if (fs.existsSync(from)) fs.cpSync(from, F("artifacts/" + d), { recursive: true });
  }
  for (const t of fs.readdirSync(path.join(ROOT, "thumbs/financial-algebra")).filter((t) => t.startsWith(u.id + "-"))) fs.copyFileSync(path.join(ROOT, "thumbs/financial-algebra", t), F("thumbs/financial-algebra/" + t));
}

// 9. Checks: every new unit has its resources, and every computed question recomputes from its printed prompt.
const v = execFileSync(process.execPath, [path.join(EXT, "verify.mjs"), out, ...ids], { stdio: ["ignore", "pipe", "inherit"] }).toString().trim();
console.log(v);
const manifest = JSON.parse(fs.readFileSync(F("financial/resources.json"), "utf8"));
for (const id of ids) {
  const u = manifest.units.find((x) => x.unitId === id);
  must(u && u.questionCount >= 80, `${id}: missing or too few questions`);
  must(u.resources.decisionLab, `${id}: no Decision Lab`);
  must(u.resources.projects.length, `${id}: no project`);
  for (const p of [u.resources.cheatSheet, ...u.resources.projects.map((p) => p.path)]) must(fs.existsSync(F(p.split("?")[0])), `${id}: missing ${p}`);
}
console.log(`FA extension: ${ids.length} Quantitative Modeling units (${ids.join(", ")}) added; ${manifest.units.length} units in all.`);

function projectSlugs(id) {
  const f = path.join(EXT, "content/projects", id + ".mjs");
  return fs.existsSync(f) ? [...fs.readFileSync(f, "utf8").matchAll(/slug: '([^']+)'/g)].map((m) => m[1]) : [];
}
