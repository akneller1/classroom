# Precalculus answer checker (audit #11)

`pc_verify.py` (with `pc_verify_more.py` and `mathx.py`) is the independent checker written for the 2026-11-18 audit.
It parses each printed short-answer and multiple-choice problem it recognizes (about 80 problem families),
recomputes the answer with its own formulas, and requires the key, every option and every find-the-mistake
student answer to agree. It shares no code with the authoring scripts.

    python3 tools/precalculus-audit-20261118/checker/pc_verify.py --min 2000

CI (Precalculus bank job) fails if any key, option or student answer disagrees, or if fewer than 2,000 items
are recomputed. Keys the checker cannot parse (words such as "The series diverges.") are counted, not failed.
