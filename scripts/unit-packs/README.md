# Unit packs

One content file per unit (`<unit-id>.cjs`) builds the hand-written activities that every Algebra 1 unit gets,
in the same style as the existing ones:

| Output | Path |
|---|---|
| Online mystery (detective game) | `artifacts/<unit>-<slug>/index.html` (engine copied from The Golden Whisk Caper) |
| Printable whodunnit + teacher key | `artifacts/<unit>-whodunnit/worksheet.pdf`, `teacher-key.pdf` |
| Escape room | `artifacts/<unit>-escape-room/index.html` (engine copied from The Great Rigged Bake-Off; `#key` shows the key) |
| Stations (4 × 10) + key | `artifacts/algebra-<unit>-stations/worksheet.pdf`, `teacher-key.pdf` |
| Cheat sheet (2 pages) | `artifacts/<unit>-cheat-sheet/worksheet.pdf` |
| Thumbnails | `thumbs/<name>.png` (convert to 720 × 450 `.jpg`) |

`node scripts/unit-packs/build.cjs <unit-id>` checks every answer first (numbers by evaluation, expressions at
several points, every wrong mystery choice must really be wrong, the clues must leave exactly the culprit, the
escape-room stamps must spell the password) and stops on a mismatch. It reports any page whose content runs
past the page. Needs Playwright + Chromium. Add the `data.js` entries and `resource-details.js` (pages and
answer keys) after building.
