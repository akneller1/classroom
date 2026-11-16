// Shared copy and layout helpers for the static /u/ course and unit pages.
// Used by build-site.mjs (secondary courses) and build-integrated-unit-pages.mjs (Grades 1-5, Financial Algebra)
// so both page sets read the same: public level names, short titles and descriptions, H2 groups and skill lists.

export const SITE_NAME = "Mr. K's Classroom";
const BRAND = ` | ${SITE_NAME}`;

export const htmlEsc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

// Public level vocabulary (codes cp2/cp1/honors stay as they are in data and links).
const LEVEL_WORD = { CP2: "Support", CP1: "Standard", HONORS: "Advanced" };
export function levelText(s) {
  return String(s ?? "")
    .replace(/CP2\s*\/\s*CP1\s*\/\s*Honors/g, (m) => m.replace("CP2", "Support").replace("CP1", "Standard").replace("Honors", "Advanced"))
    .replace(/CP2, CP1,? (or|and) Honors/g, (m) => m.replace("CP2", "Support").replace("CP1", "Standard").replace("Honors", "Advanced"))
    .replace(/CP2, CP1, Honors/g, "Support, Standard, Advanced");
}
export function levelList(level) {
  const list = Array.isArray(level) ? level : level ? [level] : [];
  return list.map((l) => LEVEL_WORD[String(l).toUpperCase()] || levelText(l));
}

const fit = (options, max) => options.find((t) => t.length <= max) || options[options.length - 1];
// Titles stay near 60 characters so search results show them whole.
export function unitPageTitle(courseTitle, unitTitle) {
  return fit([
    `${unitTitle}: ${courseTitle} Worksheets & Games${BRAND}`,
    `${unitTitle} – ${courseTitle} Worksheets${BRAND}`,
    `${unitTitle} – ${courseTitle}${BRAND}`,
    `${unitTitle}${BRAND}`,
    `${unitTitle} – ${courseTitle}`,
    unitTitle
  ], 65);
}
export function coursePageTitle(courseTitle, preferred) {
  return fit([preferred ? `${preferred}${BRAND}` : "", `Free ${courseTitle} Worksheets & Games${BRAND}`, `${courseTitle} Worksheets & Games${BRAND}`, `${courseTitle}${BRAND}`].filter(Boolean), 65);
}
// Descriptions stay at or under 155 characters and never end in a cut-off "…".
export function unitDescription(courseTitle, unitTitle, items) {
  const has = (re) => items.some((a) => re.test(`${a.type || ""} ${a.title || ""}`));
  const kinds = ["worksheets", ...(has(/game/i) ? ["games"] : []), "lesson plans", ...(has(/flashcard|cheat sheet|study guide/i) ? ["study guides"] : [])];
  const list = (k) => k.length <= 1 ? k.join("") : k.slice(0, -1).join(", ") + " and " + k[k.length - 1];
  const n = items.length;
  return fit([
    `Free ${courseTitle} ${unitTitle} ${list(kinds)}: ${n} classroom activities and generators with answer keys.`,
    `Free ${courseTitle} ${unitTitle} ${list(kinds)}: ${n} classroom activities with answer keys.`,
    `Free ${unitTitle} ${list(kinds)} for ${courseTitle}: ${n} classroom activities.`,
    `Free ${unitTitle} worksheets, games and lesson plans for ${courseTitle}.`,
    `Free ${unitTitle} worksheets and games.`
  ], 155);
}
export function courseDescription(courseTitle, preferred) {
  return fit([preferred || "", `Free ${courseTitle} worksheets, lesson plans, math games and assessments organized by unit for teachers.`, `Free ${courseTitle} worksheets, games and lesson plans.`].filter(Boolean), 155);
}

// Resource groups shown as H2 sections on unit pages, in this order.
const GROUPS = [
  ["Plan, practice and assess", (a) => /^(Planning|Generator|Practice)$/.test(a.type || "")],
  ["Classroom games", (a) => a.type === "Game"],
  ["Printable activities", (a) => a.type === "Printable"],
  ["Study guides", (a) => a.type === "Study Guide"],
  ["Interactive math", (a) => a.type === "Interactive"],
  ["Projects", (a) => a.type === "Project"],
  ["Teacher guides", (a) => /Teacher Guide/i.test(a.type || "")]
];
export function groupItems(items) {
  const left = [...items], out = [];
  for (const [name, test] of GROUPS) {
    const mine = left.filter(test);
    if (mine.length) { out.push([name, mine]); mine.forEach((a) => left.splice(left.indexOf(a), 1)); }
  }
  if (left.length) out.push(["More resources", left]);
  return out;
}

export function itemHtml(a, depth, href) {
  const meta = [a.type, levelList(a.level).join(" / ")].filter(Boolean).join(", ");
  const topics = Array.isArray(a.topics) && a.topics.length ? `<p class="mk-topics">Topics: ${htmlEsc(levelText(a.topics.join(", ")))}</p>` : "";
  return `<li>${a.path ? `<a href="${htmlEsc(href(a.path, depth))}">${htmlEsc(levelText(a.title || a.path))}</a>` : htmlEsc(levelText(a.title))}`
    + (meta ? ` <span class="mk-meta">(${htmlEsc(meta)})</span>` : "")
    + (a.description ? `<p>${htmlEsc(levelText(a.description))}</p>` : "") + topics + `</li>`;
}

// Unit page body below the lede: skills, then one H2 section per resource group.
export function unitBody({ courseTitle, unitTitle, skills, items, depth, href }) {
  const skillList = (skills || []).length
    ? `<h2>Skills in ${htmlEsc(unitTitle)}</h2>\n<ul class="mk-skills">\n${skills.map((s) => `<li>${htmlEsc(s)}</li>`).join("\n")}\n</ul>\n`
    : "";
  const groups = groupItems(items).map(([name, list]) =>
    `<h2>${htmlEsc(name)}</h2>\n<ul class="mk-items">\n${list.map((a) => itemHtml(a, depth, href)).join("\n")}\n</ul>`).join("\n");
  return skillList + groups;
}

// Who a course is for, shown on its hub page.
export const COURSE_LEVEL = {
  grade1: "1st grade", grade2: "2nd grade", grade3: "3rd grade", grade4: "4th grade", grade5: "5th grade",
  math6: "6th grade", prealgebra7: "7th grade, accelerated path (every Grade 7 standard plus most of Grade 8)", prealgebra: "8th grade",
  algebra: "high school, usually 9th grade", geometry: "high school, usually 9th or 10th grade", algebra2: "high school, usually 10th or 11th grade",
  precalculus: "high school, usually 11th or 12th grade", calculus: "AP Calculus AB, usually 11th or 12th grade", statistics: "AP Statistics, usually 11th or 12th grade",
  discrete: "high school elective, usually 11th or 12th grade", "financial-algebra": "high school elective, usually 11th or 12th grade"
};

// Course hub body: who it is for, what it holds, and every unit with its skills.
export function courseBody({ id, title, blurb, units }) {
  const nSkills = units.reduce((n, u) => n + (u.skills || []).length, 0);
  const nItems = units.reduce((n, u) => n + u.items.length, 0);
  const types = groupItems(units.flatMap((u) => u.items)).map(([name]) => name.toLowerCase()).filter((n) => n !== "more resources");
  const intro = [
    blurb ? `<p>${htmlEsc(levelText(blurb))}</p>` : "",
    `<p><strong>Grade level:</strong> ${htmlEsc(COURSE_LEVEL[id] || "see the course outline")}. `
      + `The course has ${units.length} units${nSkills ? `, ${nSkills} skills` : ""} and ${nItems} classroom resources.</p>`,
    types.length ? `<p>Each unit page collects ${htmlEsc(types.slice(0, -1).join(", ") + (types.length > 1 ? " and " : "") + types[types.length - 1])}. `
      + `Questions come in three levels, Support, Standard and Advanced, and every generator prints with an answer key.</p>` : ""
  ].join("\n");
  const list = units.map((u) => {
    const skills = u.skills || [];
    const shown = skills.slice(0, 5);
    const more = skills.length > shown.length ? `, and ${skills.length - shown.length} more` : "";
    return `<li><a href="${htmlEsc(u.slug)}/">${htmlEsc(u.title)}</a> <span class="mk-meta">(${u.items.length} classroom resources)</span>`
      + (shown.length ? `<p class="mk-topics">Skills: ${htmlEsc(shown.join(", "))}${more}.</p>` : "") + `</li>`;
  }).join("\n");
  return `${intro}\n<h2>${htmlEsc(title)} units</h2>\n<ul class="mk-items">\n${list}\n</ul>`;
}

export const EXTRA_CSS = `
h2{font:700 1.3rem/1.25 "Bricolage Grotesque",system-ui,sans-serif;margin:2.25rem 0 .5rem}
ul.mk-items li>a{display:inline-block;padding:.2rem 0;min-height:24px}
.crumbs a{display:inline-block;padding:.2rem 0;min-height:24px}
footer a,.open-app{display:inline-block;padding:.2rem 0;min-height:24px}
ul.mk-skills{columns:2 16rem;padding-left:1.25rem;margin:.5rem 0 0}
ul.mk-skills li{margin:.15rem 0;break-inside:avoid}
`;
