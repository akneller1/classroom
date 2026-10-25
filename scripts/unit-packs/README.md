# Unit packs

One content file per unit (`<unit-id>.cjs`) builds the hand-written activities that every Algebra 1 unit gets,
in the same style as the existing ones:

| Output | Path |
|---|---|
| Online mystery (detective game) | `artifacts/<unit>-<slug>/index.html` (engine copied from The Golden Whisk Caper) |
| Escape room | `artifacts/<unit>-escape-room/index.html` (engine copied from The Great Rigged Bake-Off; `#key` shows the key) |
| Cheat sheet (2 pages) | `artifacts/<unit>-cheat-sheet/worksheet.pdf` |
| Thumbnails | `thumbs/<name>.jpg` (720 × 450) |

`node scripts/unit-packs/build.cjs <unit-id>` checks every answer first (numbers by evaluation, expressions at
several points, every wrong mystery choice must really be wrong, the clues must leave exactly the culprit, the
escape-room stamps must spell the password) and stops on a mismatch. It reports any page whose content runs
past the page. Needs Playwright + Chromium. Add the `data.js` entries and `resource-details.js` (pages and
answer keys) after building.

Files are named after the unit id unless the content file sets `prefix` (Units 7 and 9 use `exponents-scientific-notation`
and `polynomials`, because their unit ids were already used as file prefixes by Units 8 and 10). The builder refuses to
write into a folder that `data.js` lists under another unit.

Done: Units 1 (foundations-algebra), 4 (relations-functions), 7 (exponents-exponential-functions), 9
(polynomials-factoring) and 12 (statistics-data-modeling). The other Algebra 1 units already had hand-made packs.
