# Grade 5: elementary-course release model

Status: published Grade 5 is the model for future Grade 1–4 releases. Keep unfinished grades in the `FinancialAlgebra` staging repository until independently approved.

## Source of truth

- Curriculum, 11 approved Grade 5 banks, metadata, activities, diagrams, and thumbnails stay in `akneller1/FinancialAlgebra`.
- The Classroom Pages workflow checks out those approved files and runs `scripts/integrate-approved-courses.mjs`. That generates the *only production* Grade 5 card catalog at `_site/grade5/grade5-main-catalog.js`.
- `/#grade5` and `skills.html?course=grade5` use that generated catalog and its question-derived CCSS mapping; `/grade5/` redirects to the main Classroom shell.
- All Grade 5 games, generators, guides, projects, banks, and diagrams remain under `/grade5/`. Do not replace them with links to the staging GitHub Pages site.
- Keep `courses/grade5.html` indexable and schema-marked. Treat `/grade5/` as a noindex alias, not a second course catalog.
- `course-integrations.js` is a local fallback snapshot. Never treat its counts as the definitive deployed resource list.

## Verified release baseline (2026-11-12)

| Measure | Grade 5 |
| --- | ---: |
| Published units | 11 |
| Named skills | 55 |
| Approved bank entries | 11 |
| Questions | 4,950 |
| Questions per skill | 90 (30 per level) |
| Difficulty levels | Remedial / Standard / Advanced |
| Published resource cards | 209 |
| Games | 101 |
| Generator / printable tools | 55 |
| Study guides | 33 |
| Interactive models | 9 |
| Projects | 11 |
| Packaged question diagrams | 918 |
| Blocking defects in assembled audit | 0 |
| Editorial warnings | 1: 4,950 question provenance notes awaiting human review |

These are build-audit counts, not evidence of independent human editorial approval. They may change after subsequent source edits.

## Release gate

1. **One catalog**: The assembled Course / Unit cards agree with the approved source for all units, skills, and resource URLs; Error Analysis appears in each unit.
2. **Mathematical integrity**: Every published question has a stable unique ID, valid answer, worked solution, standards tags, and valid diagram alt text where applicable. Run the source question verification and source tests.
3. **Difficulty consistency**: Maintain 30 questions per skill in each of the three difficulty bands until a new bank design is expressly tested and approved.
4. **Working resources**: All local HTML links, PDFs, thumbnails, 918 diagram files, and game-bank manifest requests resolve within the final assembled `_site/` package.
5. **Navigation and discovery**: The main site, course picker, student links, unit selectors, next/previous navigation, Browse by Skill, and legacy return paths work. Grade 6 must remain visible from Grade 5.
6. **Metadata**: Course landing pages include canonical, description, Open Graph, favicon, schema.org Course data, and sitemap entry; do not index duplicate course URLs.
7. **Regression tests**: Run `node scripts/build-site.mjs`, then integrate the approved Grade 5 and Financial Algebra sources, then `node scripts/test-public-site.cjs`, `node scripts/test-grade5-deployment.cjs`, and `node scripts/audit-grade5-release.cjs`. All are configured in `.github/workflows/deploy-site.yml`.
8. **Publish only approved content**: Do not accidentally export Grades 1–4 or staging work into production.

## Curriculum editorial backlog

Track substantive work in the source-repository issue: https://github.com/akneller1/FinancialAlgebra/issues/2.

- Improve explicit fraction-as-decimal equivalence practice.
- Add optional cumulative mixed-unit review and Grade 6 readiness without inflating unit count.
- Expand genuine explain/justify open-response work with rubrics, without burdening auto-graded number-only games.
- Expand and human-review authentic multi-step scenarios; the UI can label verified multi-step items using their existing metadata.
- Retain “Awaiting human review” provenance until a teacher/editor actually reviews the corresponding question.

## Template for another grade

Before promoting Grade N from the staging site, supply the same contracts: course outline; approved, versioned, level-tagged banks with question metadata and standards; reusable game/generator/guide engines; unit-specific projects; thumbnails and accessible diagrams; student links; one production catalog generated from the approved source; a dedicated course landing page; and a blocking post-assembly audit. The Grade 5 sizes are a quality benchmark, **not** mandatory question counts for younger students.
