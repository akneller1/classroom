# Partner Check and Error Analysis content

## What was added
- Error Analysis: 114 new items, one for every skill × level (140 in total with the 26 earlier
  ones; every one of the 114 cells now has at least one, and every unit/level has 9–16).
  Each prompt shows a student's numbered steps with one wrong step; the answer names the
  step, explains the error, and gives the corrected result. sourceNotes contain
  "(family: u<unit>_s<skill>_ea_error)", which is the filter the bridge already uses
  (/family: [^)]*_error\)/), so no code change should be needed for selection.
- Partner Check: 114 pairs (228 short-answer items), one pair for every skill × level.
  Partner A and Partner B solve DIFFERENT problems with the SAME answer (identical answer
  strings). Prompts begin "Partner A." / "Partner B." and sourceNotes contain
  "Partner Check pair PC-u<unit>-s<skill>-<level> (A|B)". Every unit/level has 8–11 pairs.

## Verified
- Every computed answer (A, B, and error corrections) is recomputed independently.
- Every pair has exactly one A and one B, the same skill and level, identical answers, and
  different problems. A deliberately mismatched answer was caught.
- Full site validation passes (1,563 questions).

## Assumption the site code must match (not verifiable here)
The Partner Check generator (menu/printables.js) is not in the reference pack, so how it selects
authored items is unknown. These items work if the generator either
  (a) pairs items by the "Partner Check pair <id> (A|B)" label (recommended:
      /Partner Check pair (\S+) \((A|B)\)/ on sourceNotes), or
  (b) pairs any two short-answer items in a skill/level with identical answers.
If it currently draws random single items for both columns, it must be changed to (a) to
guarantee matching answers. That is a site-code change; no infrastructure file is included.

## Notes
- Partner items are short enough to also be Tarsia-eligible; a Tarsia deck must not use both
  members of a pair (the duplicate-answer rule in TARSIA-FIX.md prevents this).
- Bank size is now 1,563 — above the original 900–1,400 target because of 546 purpose-built
  activity items (Tarsia 204, Partner Check 228, Error Analysis 114).
