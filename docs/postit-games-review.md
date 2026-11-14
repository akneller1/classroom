# Post-it games integration — November 14, 2026

49 Claude-created games are preserved as readable per-game JavaScript with one shared runtime, CSS, original thumbnails, and a standalone game hub. The exact class/unit mapping is in `postit-games.js`.

45 games have 49 placements across released Grades 2–8, Algebra 1, Geometry and Algebra 2. Four Grade 1 games are playable in the hub and their unit mappings activate when the Grade 1 course is released; this change does not publish the unfinished course.

Cards use Individual Review and open directly. Student sharing opens Customize and preserves mode, level, options, round length and code. Shared links hide teacher breadcrumbs. Grade 5 Fraction Operation Match opens on Easy in addition/subtraction and Expert in multiplication/division.

## Corrections

- Skip-Count Snap now generates valid needed multiples directly instead of occasionally exhausting its random search.
- Factor Builder preserves plus signs when a positive coefficient card also fills a binomial constant slot.
- Empty multi-select URL options fall back to valid defaults.
- Share links handle rejected clipboard promises and omit the teacher share-dialog flag.
- Catalog supplement is repositioned after assembled elementary catalogs; catalog-loading and static page tools recognize it.

## Validation

- 12,480 generated-round and option checks passed across all 49 games and four levels, including answer-card availability, checker consistency, ambiguous matches and changing drop rules.
- 6,250 independent symbolic checks passed for displayed polynomial/complex-number/expression groups, fraction matches, expression targets and factor products. These independently evaluate rendered math rather than relying on each game's own checker.
- Assembled site: all 45 released games and 49 placements resolve to their own pages and thumbnails; final site hygiene passed for 3,062 cards.
- Existing routing/math-display/Asteroid regression suite passed.
- Deployment also runs all-game completion tests in three modes and desktop/phone UI checks. Local Chromium launch is unavailable in this execution environment; CI is the browser test gate.
