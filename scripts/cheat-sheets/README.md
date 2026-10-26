# Cheat sheets

Every cheat sheet on the site is built here in one style: the newest unit-pack style. Andrey chose this on 2026-10-25.

- `style.cjs`: the page style, shared with `scripts/unit-packs/build.cjs`. It has a yellow title banner and a 2 × 3 grid of numbered, colored sections on each of the two Letter pages. The footer reads "Front/Back · <course> · Mr. K's Classroom".
- `content/<name>.cjs`: one file per sheet. The fields are `name`, `course`, `unitNo`, `unitName`, `focus` and `morefocus`, plus `front` and `back` (6 sections each). The output is `artifacts/<name>-cheat-sheet/worksheet.pdf` with the thumbnail `thumbs/<name>-cheat-sheet.jpg`. The five unit-pack sheets have small wrapper files here that read their content from `scripts/unit-packs/`.
- Section kinds:
  - `vocab`: rows of [word, meaning, example]
  - `table`: `head`, `rows`, optional `after`; `plain: true` for two rich columns
  - `example`: `text`, `example`, `steps`, `answer`
  - `words`: [statement, short answer]
  - `list`
  - `mistakes`: `good`, `bad`
  - `html`
- Any section can add a `fig`: an SVG from `figs.cjs` (number lines, coordinate planes with curves, shading and polygons) or from `geo.cjs` (angles, segments, parallel lines, triangles). `figFirst: true` puts the figure above the text.
- `check` on a section (or a list of checks) is verified before anything is written. Check types:
  - `{num, is}`
  - `{expr, is}` (expressions in x, y)
  - `{list, is}`
  - `{true: 'js'}`

## Usage
- `node scripts/cheat-sheets/build.cjs <name> …` or `all`. The build stops if any check fails or any page or section overflows; `FORCE=1` writes the files anyway so you can look at them.
- `CHECK_ONLY=1` checks without writing. `menu/tests/run-all.sh` runs it.
- `scripts/check_library.py` reports a listed cheat sheet that has no content file here.
- Section titles are printed in capitals, so keep math out of titles (write "Trinomials: the AC Method", not "ax² + bx + c").
