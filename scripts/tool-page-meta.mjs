// Gives the shared tool pages (generators, game wrappers, practice tools) what a search visitor or link preview needs:
// an accurate description, a canonical URL without the unit parameters, lang/charset, and one H1 even before
// the page script draws its heading. Run by .github/workflows/deploy-site.yml after activity-page-meta.mjs.
// Local preview: node scripts/build-site.mjs && node scripts/tool-page-meta.mjs
import fs from "node:fs";
import path from "node:path";
import { addStaticH1 } from "./activity-page-meta.mjs";

const OUT = path.resolve(process.env.SITE_DIR || "_site");
const SITE_URL = (process.env.SITE_URL || "https://mrksclassroom.com/").replace(/\/?$/, "/");
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

// Descriptions written for what each tool does today (every course, public level names).
export const TOOL_DESCRIPTIONS = {
  "worksheet-generator/worksheet.html": "Build printable math worksheets for any unit, 1st Grade to Calculus and Financial Algebra: pick skills and a level, then print with an answer key.",
  "worksheet-generator/printables.html": "Make printable mazes, color-by-number pages, Tarsia puzzles, error analysis, partner checks and stations for any unit, 1st Grade to Calculus.",
  "worksheet-generator/menu-assessment.html": "Build a unit test or a choice menu for any course: pick skills and Support, Standard or Advanced questions, edit every problem, then print with keys.",
  "worksheet-generator/course-game.html": "Classroom review games for any unit: Showdown, Connect 4, Tic-Tac-Toe and Picture Reveal, with checked questions and worked solutions.",
  "worksheet-generator/course-activity.html": "Escape rooms and detective mysteries for any unit, built from checked questions at the Support, Standard or Advanced level.",
  "worksheet-generator/practice-test.html": "A self-checking practice test for any unit: answer, compare with worked solutions, see strengths by skill and take a targeted reassessment.",
  "worksheet-generator/algebra2-game.html": "Algebra 2 review games: Showdown, Connect 4, Tic-Tac-Toe and Picture Reveal with checked questions and worked solutions.",
  "worksheet-generator/algebra2-practice.html": "An Algebra 2 assessment readiness check: answer questions by skill, review worked solutions and see what to practice next.",
  "worksheet-generator/middle-school-game.html": "Review games for 6th Grade, 7th Grade Math and 8th Grade Math with checked questions and worked solutions.",
  "worksheet-generator/asteroid-blaster.html": "Asteroid Blaster: a fast arcade review game where students answer math questions to clear asteroids.",
  "worksheet-generator/millionaire.html": "Math Millionaire: a whole-class game show with checked questions, lifelines and worked solutions.",
  "worksheet-generator/plot-practice.html": "Graphing practice: plot points, lines and curves on a coordinate grid and get instant feedback.",
  "worksheet-generator/approved-flashcards.html": "Flashcards built from checked course questions, with worked solutions on the back.",
  "worksheet-generator/approved-games.html": "Review games built from checked course questions.",
  "worksheet-generator/vocabulary.html": "Vocabulary activities and crosswords for any unit: matching, fill-in-the-blank, examples and teacher keys.",
  "worksheet-generator/seating-chart.html": "Make a classroom seating chart: arrange desks, place students and print."
};

const isTool = (rel) => /^worksheet-generator\/[^/]+\.html$/.test(rel) || /^grade[1-5]\/worksheet-generator\/[^/]+\.html$/.test(rel) || /^financial\/[^/]+\/index\.html$/.test(rel);

export function applyToolMeta(html, rel) {
  if (/<title>\s*Moved:/i.test(html) || /http-equiv=["']refresh/i.test(html)) return html; // redirect stubs
  let out = html;
  const head = out.match(/<head[^>]*>/i);
  if (!head) return html;
  const title = ((out.match(/<title>([\s\S]*?)<\/title>/i) || [])[1] || "").replace(/&#39;/g, "'").replace(/&amp;/g, "&").trim();
  const name = title.split(/ [·|–] /)[0].trim();
  const want = TOOL_DESCRIPTIONS[rel];
  const add = [];
  const desc = out.match(/<meta\s+name=["']description["']\s+content=["']([^"']*)["']\s*\/?>/i);
  if (want && desc && desc[1] !== esc(want)) out = out.replace(desc[0], `<meta name="description" content="${esc(want)}">`);
  else if (!desc) add.push(`<meta name="description" content="${esc(want || `${name}: a free classroom math tool from Mr. K's Classroom.`)}">`);
  if (!/<link\s+rel=["']canonical["']/i.test(out)) add.push(`<link rel="canonical" href="${esc(SITE_URL + rel.replace(/index\.html$/, ""))}">`);
  if (!/<html[^>]*\slang=/i.test(out)) out = out.replace(/<html\b/i, '<html lang="en"');
  if (!/<meta\s+charset=/i.test(out)) add.unshift('<meta charset="utf-8">');
  if (add.length) out = out.replace(/<head[^>]*>/i, (h) => h + add.join(""));
  return addStaticH1(out, name);
}

function main() {
  let changed = 0, seen = 0;
  (function walk(dir) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const f = path.join(dir, e.name);
      if (e.isDirectory()) { if (!/^(vendor|node_modules|question-banks|assets|thumbs)$/.test(e.name)) walk(f); continue; }
      const rel = path.relative(OUT, f).split(path.sep).join("/");
      if (!isTool(rel)) continue;
      seen++;
      const html = fs.readFileSync(f, "utf8"), next = applyToolMeta(html, rel);
      if (next !== html) { fs.writeFileSync(f, next); changed++; }
    }
  })(OUT);
  console.log(`Tool page metadata: ${changed} of ${seen} tool pages updated.`);
}

if (import.meta.url === new URL(process.argv[1], "file://").href) main();
