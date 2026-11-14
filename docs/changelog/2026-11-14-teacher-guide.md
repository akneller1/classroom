# 2026-11-14 — Teacher Guide rewrite and privacy page

## guide.html (rewritten)
- Covers Grades 1–12. New sections: course bands (with Pre-Algebra = accelerated Grade 7) and "What's on a unit page" (the seven shortcuts).
- Games are split by band: the Grades 6–12 table, Financial Algebra (no Millionaire or Escape Room), the Grades 1–4 and Grade 5 rosters, Post-it games, and topic games (Mini Golf, Zombie Fence, Asteroid Blaster, Matching Game).
- Readiness check names: "Practice Test" (6–12) and "Understanding Check" (1–5).
- Levels: CP2/CP1/Honors = Remedial/Standard/Advanced = Easy/Medium/Hard; Post-it games add Expert.
- Interactive Math: every 6–12 unit now has a tool (the 2026-11-14 tools are listed), and Grades 1–5 are included.
- Removed outdated claims: "every unit has the same games", "course names across the top", and "four generators".
- FAQ links to Back Up Saved Work and the new privacy page.

## privacy.html (new)
- Explains no accounts, no student data, Umami cookie-free visit counts, the `?analytics=off` switch, local browser storage, and Google Fonts / GitHub Pages.
- Linked from the home-page footer (`feedback.js` adds it, like the Teacher guide link) and from the guide footer. It is listed in the sitemap (`scripts/build-site.mjs`).

## Fixes found while testing
- `massachusetts-framework-strands.js`: added a record for the new Precalculus unit `sequences-series-limits` (PC.F-BF). Without it, test-public-site fails with 92 units vs 91 records.
- `scripts/test-public-site.cjs`: now expects 92 units, a sitemap with privacy.html, and the feedback.js cache string `privacy-20261114`.
- Cache strings: `feedback.js?v=privacy-20261114` and `massachusetts-framework-strands.js?v=precalc-gap-20261114`.

Checks: the full deploy pipeline was rebuilt locally. test-public-site, test-site-hygiene, the Grade 1/2/5 release tests and the elementary tests all pass. Every link in the guide resolves, and neither page has script errors.
