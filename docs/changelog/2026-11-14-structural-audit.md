# Structural audit implementation — November 14, 2026

## Routing
- `resource-standards.js`: canonicalize only established shared-player courses; preserve native elementary/financial resource paths. Exclude Project artifacts and project paths from game recognition.
- `scripts/test-no-dead-end-cards.cjs`: Chromium visits every course/unit view and unique local card target; rejects page errors, HTTP failures, unavailable resources and loading states lasting over ten seconds. Blocking deployment step after assembly.
- `scripts/test-dynamic-routing.cjs`: derive expected view totals from the loaded catalog; include generated course catalogs. Blocking after course integration.

## Feedback and raw preview
- `app.js`: normalize reported URLs using URL resolution.
- `activity.js`, `activity.html`, `feedback.js`: same report dialog in the viewer and unit cards, including student focus without navigation. Category, details and page context; Gmail/Outlook/native email drafts. Owner selected email for now; no submission endpoint is configured.
- `index.html`, `scripts/integrate-approved-courses.mjs`: inject generated Grade 5 catalog only during assembly; raw preview no longer requests a nonexistent file. README explains assembled production output.
- Cache versions refreshed on both entry points.

## Staging and deploy
- FinancialAlgebra commits restore reviewed Grade 4 runtime/assembler metadata removed from staging main, while retaining current banks in `math4/`. Grade 4 assembler and production importer support current and historical bank paths.
- Repaired outline schema handling, missing coverage/standards dependencies, root-relative staging links, outdated status text and README unit counts.
- Staging loader accepts the current elementary bank directories.
- Every production course checkout pins the same reviewed staging commit; daily unpinned refresh removed. Workflow documents how to promote a new reviewed snapshot.

## Hygiene
- Generated practice-test tools are exempt from duplicate display-title checks.
- Cleanup folders and INSTALL.txt excluded; build left-out-file check passes.
- Runtime legacy-crosswalk-audit.js, legacy-review-samples.js and browser-stage-review.js retained: grade-practice.html, legacy-review.html and middle-school-game.html still import them, confirmed by build dependency check.
- Root update notes moved to docs/changelog; unreferenced loose Geometry PDFs archived under artifacts/geometry-reference-archive. Duplicate Geometry PDF removed.
- Root diagram PNGs and course-copy folders retained: bank diagram fields are explicitly outside structural scope, and old diagram URLs must remain valid. No diagram-path rewrite was applied.

## Validation
- FinancialAlgebra: 94/94 Node tests; Grade 5 independent verifier TOTAL ERRORS 0; Grade 5 resource validator passes after loader directory fix.
- Classroom build completes; all six course integrations complete.
- Library audit: 0 problems. Dynamic routing: 16 courses, 157 units, 177 views, no broken rendered links.
- Grade 1/2 release, Grade 1 projects, elementary Asteroid, shared catalog, Grade 5 deployment/audit and elementary generator checks pass. Public-site test passes before final integrated page generation, as required by workflow ordering.
- Post-it catalog: 49 games, 54 placements. Integrated unit pages and shared headers generated.
- Final site hygiene: 3,329 cards, all files and thumbnails present, no off-site links or stray text.
- Local browser tests were attempted but Chromium cannot create its Unix socket in this execution sandbox. They remain blocking in GitHub Actions; deployment must not be considered verified until those jobs pass.
