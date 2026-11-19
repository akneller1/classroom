#!/bin/bash
# Rebuild every Calculus audit change to the question banks from the pre-audit banks (main at fc15c88d), in order.
# Each script is idempotent, so running this on already-fixed banks changes nothing.
set -e
cd "$(dirname "$0")/../.."
T=tools/calculus-audit-20261118
python3 $T/fix_error_items.py      # 1  find-the-mistake diagnoses
python3 $T/fix_text.py             # 13, 18, 19  notation, Euler marked BC, IVT wording, motion units
python3 $T/stems.py                # 12 open-response stems
python3 $T/fix_off_skill.py        # 8  on-skill items
python3 $T/fix_ap_review.py        # 14 AP Review skills
python3 $T/frq.py                  # 5  free-response problems (slot 015)
python3 $T/retag.py                # 11 AP objective tags
python3 $T/level_up.py             # 9  Honors and CP2 levels
python3 $T/add_topics.py           # 10 AP topics
python3 $T/fix_text.py             # notation again for the new items
python3 $T/expand_steps.py         # 3  worked solutions
node scripts/build_standards_map.cjs
