# Escape Room, Detective/Millionaire, and teacher review

## Escape Room
114 new items (family `…_escape`), one per skill × level: short answer, a single whole-number
answer from 1 to 25, and four solution steps. Every unit/level now has 9–13 Escape Room
candidates (it had about 1). Answers are recomputed by the verifier.

## Detective and Millionaire (single-skill decks)
Every one of the 114 skill × level cells now has at least 10 multiple-choice items
(minimum 10), so a single-skill Detective deck can be filled. How:
- The 204 Tarsia items were converted to multiple choice. Their wrong options target named
  mistakes (left vs. right tail, n vs. n − 1, z* vs. t*, forgetting to pool, and so on).
  They remain Tarsia-eligible (short prompt, short answer).
- 236 new multiple-choice items (family `…_mcfill`) fill the remaining gaps.
Millionaire needs 15 per deck; a single skill × level does NOT reach 15 in most cells
(that would take about 560 more items). Unit-level Millionaire decks have 81–111 items.
The verifier now judges wrong numeric options at the key's precision, so "5" and "6" are
correctly treated as different from a key of "5.5"; a planted duplicate ("5.50") is caught.

## Teacher review
reports/review/review-packet.html (printable) and reports/review/review-sheet.csv list all
1,647 new or corrected items grouped by unit, skill, and level, each with its answer, solution,
how it was verified, flags, and Approve / Revise / Remove boxes. Regenerate with
`python3 scripts/verification/make_review_packet.py . <statistics-course.json>`.
Flags to prioritize:
- conceptual (808): not numerically checkable — confirm the key and that no distractor is defensible.
- key-longest (353): the correct option is the longest one, a guessing cue; consider lengthening a distractor.
- similar-to (139): near-duplicate of another item in the same cell; keep or remove.
- implied-input (11): a value is implied by wording (e.g., "fair die") rather than printed.
- corrected (9): baseline open responses whose part answers were replaced.
Approval flags were not changed; the banks stay unapproved until a teacher signs off.

## Size
The bank is now 1,913 questions (1,638 new + 275 baseline), well above the original 900–1,400
target. About 1,017 are general practice; the rest are activity-specific (Tarsia 204,
Partner Check 228, Error Analysis 140 total, Escape Room 114, MC fill 236). A reviewer may
prefer to trim near-duplicates flagged in the packet.
