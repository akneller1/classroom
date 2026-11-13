// Builds the public course and unit pages (u/<course>/ and u/<course>/<unit>/) for the courses that are
// assembled into _site AFTER scripts/build-site.mjs runs: Grades 3, 4 and 5 and Financial Algebra.
// Run by .github/workflows/deploy-site.yml after the Grade 3 assembly step.
// Local preview (after the build and integration steps): node scripts/build-integrated-unit-pages.mjs
//
// What it does:
//  1. Loads the same catalog scripts as the home page, in the same order, and reads window.LIBRARY.
//  2. For each integrated course that has no u/<course>/ page yet, writes a course page and one page per unit,
//     styled exactly like the pages build-site.mjs writes (the style block is copied from one of them).
//  3. Adds the new pages to sitemap.xml and lists every course on the Courses page (courses/index.html).
// A course whose catalog cannot be read is skipped with a warning; the deploy continues.

import fs from "node:fs";
import path from "node:path";
import { loadSiteCatalog } from "./load-site-catalog.mjs";

const OUT = path.resolve(process.env.SITE_DIR || "_site");
const SITE_URL = (process.env.SITE_URL || "https://mrksclassroom.com/").replace(/\/?$/, "/");
const SITE_NAME = "Mr. K's Classroom";
const COURSES = (process.env.INTEGRATED_COURSES || "grade3,grade4,grade5,financial-algebra").split(",").map((s) => s.trim()).filter(Boolean);
const COLOR = { blue: "#1f5fbf", orange: "#c4570f", green: "#1d7a46", purple: "#6b3fb8" };

const htmlEsc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const slug = (s) => String(s || "").toLowerCase().normalize("NFKD").replace(/[̀-ͯ]/g, "")
  .replace(/&/g, " and ").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60) || "item";
const listNames = (a) => a.length <= 1 ? a.join("") : a.slice(0, -1).join(", ") + " and " + a[a.length - 1];

if (!fs.existsSync(path.join(OUT, "index.html"))) throw Error("Build the site first: " + OUT + "/index.html is missing");

// ---------- 1. Read the catalog the way the home page does ----------
const { library } = loadSiteCatalog(OUT, { siteUrl: SITE_URL });

// ---------- 2. Page template, copied from a page build-site.mjs wrote ----------
const sample = fs.readdirSync(path.join(OUT, "u")).map((d) => path.join(OUT, "u", d, "index.html")).find((f) => fs.existsSync(f));
if (!sample) throw Error("No existing u/<course>/index.html to copy the page style from");
const sampleHtml = fs.readFileSync(sample, "utf8");
const pageCss = (sampleHtml.match(/<style>([\s\S]*?)<\/style>/) || [])[1] || "";
const fontsLink = (sampleHtml.match(/<link rel="stylesheet" href="([^"]+)">/) || [])[1] || "";
const fontsHref = (depth) => !fontsLink ? "" : /^(https?:)?\/\//.test(fontsLink) ? fontsLink : "../".repeat(depth) + fontsLink.replace(/^(\.\.\/)+/, "");

function head({ title, description, url, depth }) {
  const pre = "../".repeat(depth);
  return `<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${htmlEsc(title)}</title>
<meta name="description" content="${htmlEsc(description)}">
<link rel="canonical" href="${htmlEsc(url)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="${htmlEsc(SITE_NAME)}">
<meta property="og:title" content="${htmlEsc(title)}">
<meta property="og:description" content="${htmlEsc(description)}">
<meta property="og:url" content="${htmlEsc(url)}">
<meta property="og:image" content="${SITE_URL}assets/social-preview.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="${pre}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="${pre}assets/apple-touch-icon.png">
${fontsHref(depth) ? `<link rel="stylesheet" href="${htmlEsc(fontsHref(depth))}">` : ""}
<style>${pageCss}</style>`;
}
const isExternal = (p) => /^(https?:)?\/\//i.test(p);
const href = (p, depth) => isExternal(p) || String(p).startsWith("/") ? String(p) : "../".repeat(depth) + String(p).replace(/^\.?\//, "");
function itemHtml(a, depth) {
  const meta = [a.type, Array.isArray(a.level) ? a.level.join(" / ") : a.level].filter(Boolean).join(", ");
  const topics = Array.isArray(a.topics) && a.topics.length ? `<p class="mk-topics">Topics: ${htmlEsc(a.topics.join(", "))}</p>` : "";
  return `<li>${a.path ? `<a href="${htmlEsc(href(a.path, depth))}">${htmlEsc(a.title || a.path)}</a>` : htmlEsc(a.title)}`
    + (meta ? ` <span class="mk-meta">(${htmlEsc(meta)})</span>` : "")
    + (a.description ? `<p>${htmlEsc(a.description)}</p>` : "") + topics + `</li>`;
}
const footer = `<footer>© ${new Date().getFullYear()} ${htmlEsc(SITE_NAME)} · <a href="https://github.com/akneller1/classroom/issues/new?title=Website%20feedback">Send feedback</a></footer>`;

// ---------- 3. Write the pages ----------
const added = [];
const written = [];
for (const id of COURSES) {
  const course = library.courses.find((c) => c.id === id);
  if (!course) { console.warn(`Course "${id}" is not in the catalog; no pages written for it.`); continue; }
  const cSlug = slug(course.id);
  const courseDir = path.join(OUT, "u", cSlug);
  if (fs.existsSync(path.join(courseDir, "index.html"))) { console.log(`u/${cSlug}/ already exists; left as is.`); written.push(course); continue; }
  const title = course.name || course.title || course.id;
  const units = (course.units || []).filter((u) => (u.artifacts || []).length).map((u, i, all) => {
    let s = slug(u.id || u.name);
    if (all.slice(0, i).some((v) => slug(v.id || v.name) === s)) s += "-" + (i + 1);
    return { id: u.id, title: u.name || u.title || "Unit", slug: s, items: (u.artifacts || []).filter((a) => a && (a.title || a.path)) };
  });
  if (!units.length) { console.warn(`Course "${id}" has no units with activities; skipped.`); continue; }
  const accent = COLOR[course.color] ? `<style>:root{--accent:${COLOR[course.color]}}@media (prefers-color-scheme:dark){:root{--accent:var(--link)}}</style>` : "";

  const courseUrl = SITE_URL + `u/${cSlug}/`;
  const courseDesc = `Free ${title} worksheets, lesson plans, math games and assessments organized by unit for teachers.`;
  fs.mkdirSync(courseDir, { recursive: true });
  fs.writeFileSync(path.join(courseDir, "index.html"), `<!doctype html>
<html lang="en">
<head>
${head({ title: `Free ${title} Worksheets, Games & Lesson Plans | ${SITE_NAME}`, description: courseDesc, url: courseUrl, depth: 2 })}${accent}
</head>
<body>
<div class="wrap">
<p class="crumbs"><a href="../../">${htmlEsc(SITE_NAME)}</a> / ${htmlEsc(title)}</p>
<main>
<h1>${htmlEsc(title)} Worksheets, Games &amp; Lessons</h1>
<p class="lede">${htmlEsc(courseDesc)}</p>
<h2>Explore ${htmlEsc(title)} units</h2>
<ul class="mk-items">
${units.map((u) => `<li><a href="${htmlEsc(u.slug)}/">${htmlEsc(u.title)}</a> <span class="mk-meta">(${u.items.length} classroom resources)</span></li>`).join("\n")}
</ul>
<a class="open-app" href="../../#${encodeURIComponent(course.id)}">Open ${htmlEsc(title)} in the full classroom site</a>
</main>
${footer}
</div>
</body>
</html>
`);
  added.push(courseUrl);

  for (const u of units) {
    const url = SITE_URL + `u/${cSlug}/${u.slug}/`;
    const hasGames = u.items.some((a) => a.type === "Game");
    const hasStudy = u.items.some((a) => /flashcard|cheat sheet|study guide/i.test(a.title || "") || a.type === "Study Guide");
    let desc = `Free ${title} resources for ${u.title}: lesson plans, worksheet and assessment generators, ${listNames([hasGames ? "math games" : "practice activities", ...(hasStudy ? ["study guides"] : [])])}. Browse ${u.items.length} classroom activities and tools.`;
    if (desc.length > 175) desc = desc.slice(0, 172).replace(/\s+\S*$/, "") + "…";
    const base = `${u.title} – ${title}`;
    const dir = path.join(courseDir, u.slug);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, "index.html"), `<!doctype html>
<html lang="en">
<head>
${head({ title: `${base} ${base.length < 56 ? "Worksheets & Activities" : "Resources"} | ${SITE_NAME}`, description: desc, url, depth: 3 })}${accent}
</head>
<body>
<div class="wrap">
<p class="crumbs"><a href="../../../">${htmlEsc(SITE_NAME)}</a> / <a href="../">${htmlEsc(title)}</a> / ${htmlEsc(u.title)}</p>
<main>
<h1>${htmlEsc(u.title)}: ${htmlEsc(title)} Worksheets &amp; Activities</h1>
<p class="lede">${htmlEsc(desc)}</p>
<ul class="mk-items">
${u.items.map((a) => itemHtml(a, 3)).join("\n")}
</ul>
<a class="open-app" href="${u.id ? `../../../#${encodeURIComponent(course.id + "." + u.id)}` : "../../../"}">Open this unit in the full classroom site</a>
</main>
${footer}
</div>
</body>
</html>
`);
    added.push(url);
  }
  written.push(course);
  console.log(`u/${cSlug}/: course page and ${units.length} unit pages written.`);
}

// ---------- 4. Sitemap ----------
const sitemapFile = path.join(OUT, "sitemap.xml");
if (added.length && fs.existsSync(sitemapFile)) {
  let xml = fs.readFileSync(sitemapFile, "utf8");
  const today = new Date().toISOString().slice(0, 10);
  const fresh = added.filter((u) => !xml.includes(`<loc>${htmlEsc(u)}</loc>`));
  xml = xml.replace("</urlset>", fresh.map((u) => `  <url><loc>${htmlEsc(u)}</loc><lastmod>${today}</lastmod></url>`).join("\n") + "\n</urlset>");
  fs.writeFileSync(sitemapFile, xml);
}

// ---------- 5. Courses page: list every course, in catalog order ----------
const coursesFile = path.join(OUT, "courses", "index.html");
if (fs.existsSync(coursesFile)) {
  let html = fs.readFileSync(coursesFile, "utf8");
  const list = html.match(/<div class="panel"><ul>([\s\S]*?)<\/ul><\/div>/);
  if (list) {
    const existing = [...list[1].matchAll(/<li>[\s\S]*?<\/li>/g)].map((m) => m[0]);
    const byName = new Map(existing.map((li) => [(li.match(/>([^<]+)<\/a>/) || [])[1], li]));
    const ready = new Set(written.map((c) => c.id));
    const ORDER = ["grade1", "grade2", "grade3", "grade4", "grade5", "math6", "prealgebra7", "prealgebra", "algebra", "geometry",
      "algebra2", "precalculus", "calculus", "statistics", "discrete", "financial-algebra"];
    const rank = (c) => (ORDER.indexOf(c.id) + 1) || ORDER.length + 1;
    const courses = library.courses.filter((c) => !c.comingSoon && (c.units || []).some((u) => (u.artifacts || []).length)).sort((a, b) => rank(a) - rank(b));
    const items = courses.map((c) => {
      const name = c.name || c.title || c.id;
      let li = byName.get(name);
      const target = ready.has(c.id) ? `/u/${slug(c.id)}/` : null;
      if (li && target && /href="\/#/.test(li)) li = li.replace(/href="\/#[^"]*"/, `href="${target}"`);
      if (!li && target) li = `<li><a href="${target}">${htmlEsc(name)}</a> — ${htmlEsc((c.blurb || "").replace(/\.?$/, "."))}</li>`;
      return li;
    }).filter(Boolean);
    for (const li of existing) if (!items.includes(li) && !items.some((x) => x.includes((li.match(/>([^<]+)<\/a>/) || [])[1] + "<"))) items.push(li);
    html = html.replace(list[0], `<div class="panel"><ul>${items.join("")}</ul></div>`);
    fs.writeFileSync(coursesFile, html);
  }
}
console.log(`Done. ${added.length} pages added for ${written.map((c) => c.id).join(", ") || "no courses"}.`);
