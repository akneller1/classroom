// Single source of truth for which units may show an Asteroid Blaster card.
// The browser applies the curated list in course-integrations.js; static pages
// built by scripts/build-site.mjs must apply the same list so search visitors
// never land on a game that falls back to another unit.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { asteroidUnits } from "./asteroid-resources.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

export function asteroidEligibleUnits(root = ROOT) {
  const src = fs.readFileSync(path.join(root, "course-integrations.js"), "utf8");
  const m = src.match(/var eligible=new Set\((\[[^\]]*\])\)/);
  if (!m) throw new Error("course-integrations.js: curated Asteroid unit list not found");
  const set = new Set(JSON.parse(m[1]));
  for (const [course, units] of Object.entries(asteroidUnits)) for (const u of units) set.add(course + "/" + u);
  if (set.size < 10) throw new Error("Asteroid eligibility list looks incomplete (" + set.size + " units)");
  return set;
}

const ASTEROID = /(^|\/)worksheet-generator\/asteroid-blaster\.html\?/;

export function isAsteroidItem(item) {
  return item && (item.bankFormat === "asteroid-blaster" || ASTEROID.test(item.path || ""));
}

// Remove Asteroid cards from units that the app itself hides.
export function filterAsteroidItems(courseId, unitId, items, eligible) {
  if (eligible.has(courseId + "/" + unitId)) return items;
  return items.filter((a) => !isAsteroidItem(a));
}
