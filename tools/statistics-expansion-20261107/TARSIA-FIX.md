# Tarsia overflow: cause and fix

## What the screenshot shows
Cell 22 holds stat-u3-s08-cp1-x02 (212-character prompt). The text overlapping it is
stat-u3-t1-011…015 (320–364 characters, a two-way table flattened into one line). Tarsia cells
are a fixed size and the generator does not filter or shrink long prompts, so text spills into
neighboring cells.

## Data fix (included)
204 new short items (family names end in `_tarsia`): prompt ≤ 110 characters, answer ≤ 20
characters, no line breaks, tables, or figures; answers distinct within each unit and level.
Every numeric one is recomputed by scripts/verification/verify_expansion.py.
Result (reports/tarsia-fit-statistics.txt): every Statistics unit/level now has 25–28 eligible
items with distinct answers (a 16-triangle Tarsia needs 18).

## Generator fix (NOT included — needs a site-code change)
The bank still contains 40–66 long items per unit/level, so the overflow will continue unless
the Tarsia generator only draws eligible items. Recommended rule, applied to every course:

    const tarsiaEligible = q =>
      (q.format === 'short-answer' || q.format === 'multiple-choice') &&
      typeof q.answer === 'string' && q.answer.length <= 20 &&
      q.prompt.length <= 110 && !q.prompt.includes('\n') && !q.diagram;
    // and reject a deck in which two items share an answer (case/space-insensitive)

Also add a layout safeguard (shrink-to-fit or clip with a warning) so one long item can never
overlap another cell. If the generator should prefer the purpose-written items, it can filter
on sourceNotes containing "_tarsia)", the same way Error Analysis filters on "_error)".

## Other courses
Not verifiable here: the reference pack lists 55 other-course banks in its manifest but includes
none of them, only two 8-item samples (Algebra 2 conics, Precalculus functions). Those samples
have short prompts (33–74 characters, no line breaks), so overflow risk looks low, but eligible
counts per unit/level are unknown. Run on the real repository:

    python3 scripts/verification/audit_tarsia_fit.py <repo_root>

It reads question-banks/manifest.json, audits every course/unit/level, counts items that would
overflow, and marks unit-levels with fewer than 18 distinct eligible answers as SHORT.
