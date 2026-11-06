# Site update i: Interactive Math for Geometry

This update adds one Interactive Math tool to each of the 10 Geometry units. The setup matches Algebra 1 and Algebra 2:

- Each tool has a "Try this" list of challenges that check themselves.
- Each comes with a 2-page Explore & Reflect worksheet, a teacher key and a card thumbnail.
- The tools appear in each unit's Interactive Math section, with Copy student link.

This update is built on the live site (commit d23dbd1). Unzip it at the repository root.

## Changed files

| File | Change |
| --- | --- |
| `data.js` | One block added at the end that lists the 10 Geometry tools. Nothing above it changed. |
| `guide.html` | The Interactive Math section now says there are 10 tools for Geometry and uses a Geometry tool as an example. |
| `index.html`, `activity.html` | The `data.js` cache version was bumped. |
| `tools/interactive-math-20261105/*` | The build scripts now cover Geometry. `print_pdfs.cjs` takes an optional slug prefix (for example `geometry-`) so it only reprints those PDFs. |

`app.js` is unchanged; the Interactive Math section and shortcut already appear wherever a unit has tools. None of the Algebra tool pages or PDFs changed.

## New files

- `artifacts/interactive-math/geo.js`: geometry helpers (angle arcs, tick marks, vertex labels). Only the Geometry tools load it.
- `artifacts/geometry-<tool>/index.html`, `worksheet.pdf` and `teacher-key.pdf` for each tool.
- `thumbs/geometry-<tool>.jpg`: one card thumbnail per tool.
- `tools/interactive-math-20261105/src/geometry-*.js` (the tools) and `worksheets_geometry.py` (the worksheet content).

## The tools

| Unit | Tool | What students do |
| --- | --- | --- |
| Foundations of Geometry | Distance & Midpoint Explorer | Drag the endpoints. The distance comes from a right triangle and the midpoint is an average. A second tab covers segment addition. |
| Angles and Parallel Lines | Parallel Lines & Transversal | Turn the transversal and highlight each angle-pair type. Tilt one line to see the relationships break. |
| Triangle Congruence | Triangle Congruence Builder | Set SSS, SAS, ASA, AAS, SSA or AAA values and see whether they make one triangle, two, none or many. |
| Triangle Relationships | Triangle Explorer | Check the angle sum, exterior angles and side–angle order, and show the four triangle centers. A second tab tests the triangle inequality. |
| Similarity | Dilation & Similarity Lab | Move the center and change the scale factor. Compare side ratios, angles, perimeter (× k) and area (× k²). |
| Right Triangles and Trigonometry | Trig Ratio Explorer | See that sin, cos and tan depend on the angle only, not the size. A second tab covers the 45°-45°-90° and 30°-60°-90° triangles. |
| Quadrilaterals and Polygons | Polygon & Quadrilateral Explorer | Split polygons into triangles to find angle sums. A quadrilateral "detective" names a shape from its sides, angles and diagonals. |
| Transformations | Transformation Studio | Translate, reflect, rotate or dilate a triangle. See the coordinate rule, a coordinate table, and whether it's rigid and keeps orientation. |
| Circles | Circle Angle Explorer | Compare inscribed and central angles on the same arc. A second tab covers arc length and sector area as fractions of the circle. |
| Area, Surface Area and Volume | Solids Volume Lab | Explore a prism, cylinder, square pyramid, cone and sphere with their volume and surface area formulas. Compare a cone with its cylinder and see how volume scales by k³. |

## Tested

- Every tool opens with no script errors and fits a phone screen in both light and dark mode.
- An automated walkthrough completed all 50 "Try this" challenges, including dragging points.
- All 20 PDFs are 2 pages.
- Each Geometry unit page shows its tool, with Copy student link and the worksheet and key links.
- `python3 scripts/check_library.py` reports 0 problems.
