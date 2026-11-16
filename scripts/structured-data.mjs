// schema.org JSON-LD for the static course and unit pages (/u/<course>/ and /u/<course>/<unit>/).
// Breadcrumbs give search results a Home > Course > Unit trail; Course and LearningResource describe what a
// page teaches using data the site already holds (skill names and the standards tagged on bank questions).
import fs from "node:fs";
import path from "node:path";

const SITE_NAME = "Mr. K's Classroom";
const PROVIDER = { "@type": "Person", name: "Andrey Kneller" };

// Common Core codes look like 3.OA.A.1, 6.EE.B.6 or A-CED.A.2 (high school, with or without the HS prefix).
const CCSS = /^(?:CCSS\.MATH\.CONTENT\.)?(?:[1-8]\.[A-Z]{1,3}\.[A-Z]\.\d+[a-z.]*|(?:HS)?[ANFGS]-[A-Z]{1,3}\.[A-Z]\.\d+[a-z.]*)$/i;

// Unique Common Core codes tagged on a unit's published bank questions (empty when the unit has no bank).
export function unitStandards(root, courseId, unitId) {
  const candidates = [path.join(root, "question-banks", courseId, unitId + ".json")];
  try { // the manifest knows banks stored under other folders (for example grade1/question-banks/...)
    const m = JSON.parse(fs.readFileSync(path.join(root, "question-banks", "manifest.json"), "utf8"));
    const hit = (m.banks || []).find((b) => b.courseId === courseId && b.unitId === unitId);
    if (hit && typeof hit.path === "string") candidates.unshift(path.join(root, hit.path));
  } catch { /* no manifest: fall back to the conventional path */ }
  for (const file of candidates) {
    if (!fs.existsSync(file)) continue;
    try {
      const bank = JSON.parse(fs.readFileSync(file, "utf8"));
      const codes = new Set();
      for (const q of bank.questions || []) for (const s of q.standards || []) if (CCSS.test(s)) codes.add(s.replace(/^CCSS\.MATH\.CONTENT\./i, "").replace(/^HS(?=[ANFGS]-)/, ""));
      return [...codes].sort();
    } catch { return []; }
  }
  return [];
}

function crumbs(items) {
  return { "@type": "BreadcrumbList", itemListElement: items.map(([name, item], i) => ({ "@type": "ListItem", position: i + 1, name, item })) };
}

function script(graph) {
  // "</" must not close the script element early.
  return `<script type="application/ld+json">${JSON.stringify({ "@context": "https://schema.org", "@graph": graph }).replace(/<\//g, "<\\/")}</script>`;
}

export function courseJsonLd({ siteUrl, courseName, courseUrl, description }) {
  return script([
    crumbs([[SITE_NAME, siteUrl], [courseName, courseUrl]]),
    { "@type": "Course", name: courseName, description, url: courseUrl, provider: PROVIDER, isAccessibleForFree: true, inLanguage: "en",
      educationalLevel: courseName, offers: { "@type": "Offer", price: 0, priceCurrency: "USD", category: "Free" }},
  ]);
}

export function unitJsonLd({ siteUrl, courseName, courseUrl, unitName, unitUrl, description, skills = [], standards = [], resourceCount }) {
  const resource = { "@type": "LearningResource", name: `${unitName} – ${courseName}`, description, url: unitUrl, inLanguage: "en",
    isAccessibleForFree: true, educationalLevel: courseName, learningResourceType: ["Worksheet", "Game", "Lesson plan", "Assessment"],
    provider: PROVIDER, isPartOf: { "@type": "Course", name: courseName, url: courseUrl } };
  if (skills.length) resource.teaches = skills.slice(0, 30);
  if (standards.length) resource.educationalAlignment = standards.slice(0, 40).map((code) => ({ "@type": "AlignmentObject", alignmentType: "teaches", educationalFramework: "Common Core State Standards for Mathematics", targetName: code }));
  if (resourceCount) resource.numberOfItems = resourceCount;
  return script([crumbs([[SITE_NAME, siteUrl], [courseName, courseUrl], [unitName, unitUrl]]), resource]);
}
