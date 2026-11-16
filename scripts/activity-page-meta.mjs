// Gives every activity page in the built site the basics a search visitor needs:
//   - a descriptive title with the course and the site name (no internal slugs like "G6 Fdp Oddout"),
//   - a meta description,
//   - a self-referencing canonical URL.
// Project pages follow one indexing policy: they are indexable in every grade (Grades 1-3 used to be noindex
// while Grades 4-5 were not). Legacy duplicate pages keep their noindex.
// Run by .github/workflows/deploy-site.yml after every course is assembled (after add-site-header.mjs).
// Local preview: node scripts/build-site.mjs && node scripts/activity-page-meta.mjs
import fs from "node:fs";
import path from "node:path";
import { loadSiteCatalog, sitePath } from "./load-site-catalog.mjs";

const OUT = path.resolve(process.env.SITE_DIR || "_site");
const SITE_URL = (process.env.SITE_URL || "https://mrksclassroom.com/").replace(/\/?$/, "/");
const BRAND = "Mr. K's Classroom";
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const unesc = (s) => String(s ?? "").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'");

// Internal-looking titles: Post-it slugs ("G6 Fdp Oddout"), bare file names, or empty.
export function isSlugTitle(t) {
  t = String(t || "").trim();
  return !t || /^G\d+\s/.test(t) || /^[a-z0-9-]+$/.test(t) || /\.html?$/i.test(t);
}

export function pageTitle(current, item, courseName) {
  current = String(current || "").trim();
  if (/Mr\. K/.test(current) && !isSlugTitle(current.split(/ [|·] /)[0])) return current;
  let base = isSlugTitle(current) ? item.title : current.replace(/\s*[|·]\s*Mr\. K.*$/, "");
  base = String(base || "").trim();
  if (courseName && !base.toLowerCase().includes(courseName.toLowerCase())) base += " · " + courseName;
  return base + " | " + BRAND;
}

export function pageDescription(item, unitName, courseName) {
  let d = String(item.description || "").replace(/\s+/g, " ").trim();
  if (!d) d = `Free ${String(item.type || "classroom").toLowerCase()} resource for ${unitName} in ${courseName}.`;
  if (d.length > 158) {
    const sentence = d.slice(0, 158).match(/^.{60,157}[.!?](?=\s|$)/);
    d = sentence ? sentence[0] : d.slice(0, 155).replace(/\s+\S*$/, "") + "…";
  }
  return d;
}

// Rewrite one HTML document. Pure, so it can be tested without a built site.
export function applyMeta(html, { url, item, courseName, unitName, image }) {
  const head = html.match(/<head[^>]*>/i);
  if (!head) return html;
  let out = html;
  const titleMatch = out.match(/<title>([\s\S]*?)<\/title>/i);
  const want = pageTitle(titleMatch ? unesc(titleMatch[1]) : "", item, courseName);
  if (titleMatch) out = out.replace(titleMatch[0], "<title>" + esc(want) + "</title>");
  else out = out.replace(head[0], head[0] + "<title>" + esc(want) + "</title>");
  const add = [];
  if (!/<meta\s+name=["']description["']/i.test(out)) add.push(`<meta name="description" content="${esc(pageDescription(item, unitName, courseName))}">`);
  if (!/<link\s+rel=["']canonical["']/i.test(out)) add.push(`<link rel="canonical" href="${esc(url)}">`);
  // Link previews (Google Classroom, email, chat): title, description, URL and an image.
  if (!/<meta\s+property=["']og:title["']/i.test(out)) {
    const ogDesc = (out.match(/<meta\s+name=["']description["']\s+content=["']([^"']*)["']/i) || [])[1] || esc(pageDescription(item, unitName, courseName));
    add.push(`<meta property="og:type" content="website"><meta property="og:site_name" content="${esc(BRAND)}">` +
      `<meta property="og:title" content="${esc(want.replace(/\s*\|\s*Mr\. K's Classroom$/, ""))}"><meta property="og:description" content="${ogDesc}">` +
      `<meta property="og:url" content="${esc(url)}"><meta property="og:image" content="${esc(image || SITE_URL + "assets/social-preview.png")}">` +
      `<meta name="twitter:card" content="summary_large_image">`);
  }
  if (/-project-/.test(url)) out = out.replace(/<meta\s+name=["']robots["']\s+content=["']noindex[^"']*["']\s*\/?>/gi, "");
  if (add.length) {
    const charset = out.match(/<meta\s+charset=[^>]*>/i);
    out = charset ? out.replace(charset[0], charset[0] + add.join("")) : out.replace(/<head[^>]*>/i, (h) => h + add.join(""));
  }
  return out;
}

function main() {
  const { library } = loadSiteCatalog(OUT, { quiet: true });
  const owners = new Map(); // page -> first catalog entry that links it
  for (const c of library.courses) for (const u of c.units || []) for (const a of u.artifacts || []) {
    if (!a || !a.path || /^(https?:)?\/\//.test(a.path)) continue;
    const rel = sitePath(a.path);
    if (!/\.html?$/i.test(rel) || /^worksheet-generator\//.test(rel) || /^financial\//.test(rel)) continue;
    if (!owners.has(rel)) owners.set(rel, { item: a, courseName: c.name || c.title || "", unitName: u.name || u.title || "" });
  }
  let changed = 0, missing = 0;
  for (const [rel, info] of owners) {
    const file = path.join(OUT, rel);
    if (!fs.existsSync(file)) { missing++; continue; }
    const html = fs.readFileSync(file, "utf8");
    // A raster thumbnail from the catalog makes a better preview than the generic site image (SVG is not used by most previews).
    const thumb = info.item.thumb ? sitePath(info.item.thumb) : "";
    const image = thumb && /\.(png|jpe?g|webp)$/i.test(thumb) && fs.existsSync(path.join(OUT, thumb)) ? SITE_URL + thumb : "";
    const next = applyMeta(html, { url: SITE_URL + rel, image, ...info });
    if (next !== html) { fs.writeFileSync(file, next); changed++; }
  }
  console.log(`Activity page metadata: ${changed} of ${owners.size} catalog pages updated` + (missing ? `, ${missing} not in this build` : "") + ".");
}

if (import.meta.url === new URL(process.argv[1], "file://").href) main();
