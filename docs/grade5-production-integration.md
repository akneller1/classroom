# Grade 5 production integration

## Architecture

- **Source of truth:** [akneller1/FinancialAlgebra](https://github.com/akneller1/FinancialAlgebra). Grade 5 generators, their bank files, diagrams, games, study guides and course page remain here.
- **Public catalog/navigation:** [akneller1/classroom](https://github.com/akneller1/classroom) via `course-integrations.js`.
- **Production assembly:** `.github/workflows/build-classroom-pages.yml` checks out both repositories, runs Grade 5 tests, then deploys one static site via GitHub Pages Actions. It places the Grade 5 source under `/grade5/`, including its approved banks and images, without checking copied files into the Classroom source repository.
- **Fallback while Pages still deploys from a branch:** Grade 5 entries in the main site link to the separate Grade 5 GitHub Pages players. The `/grade5/` branch route redirects to the Grade 5 course view on the main site.

## One-time activation

1. Go to **Classroom → Settings → Pages → Build and deployment** and set the source to **GitHub Actions**.
2. Open **Actions → Build unified Mr. K's Classroom site → Run workflow** if it has not run following the source change.
3. Confirm the workflow's **build** and **deploy** jobs succeeded.
4. Check `https://mrksclassroom.com/#grade5`, `https://mrksclassroom.com/grade5/`, and `https://mrksclassroom.com/grade5/worksheet-generator/grade5-generators.html?unit=place-value-number-sense&mode=worksheet`. Check teacher/student keys, stacked fractions, diagram images, all four modes and Ctrl+P.

## Promotion policy

The workflow pins the approved Grade 5 source commit:
`bc1b79d6cc5523f300eebc1e924e3fe519cfa886`.

**Do not replace the pinned commit with `main`.** FinancialAlgebra is also a staging environment for unfinished courses. To promote a later Grade 5 change, review and test that source revision, update the pinned commit SHA in the workflow, and merge the change to Classroom main. The build runs again and preserves the single-production-site model.

If the Pages build fails, keep the prior successful Pages artifact deployed; investigate the build log before advancing the pinned source. The user-facing source catalog can still use the staging links while Actions deployment is not configured.
