#!/usr/bin/env bash
# Rebuilds every Grade 6 bank and vocabulary change of the 2026-11-19 audit, in order. Rerunning changes nothing.
set -euo pipefail
T="$(cd "$(dirname "$0")" && pwd)"
R="$(cd "$T/../.." && pwd)"
export PYTHONDONTWRITEBYTECODE=1
python3 $T/fix_items.py     # 6A: #3, #20
python3 $T/retag.py         # 6A: #9, #10
python3 $T/vocab.py         # 6A: #15
python3 $T/honors.py        # 6B: #4
python3 $T/new_items.py     # 6B: #5-#9, #17, #18
python3 $T/levels.py        # whole-site audit #9: Standard and Honors stop reusing lower templates
node $R/scripts/build_standards_map.cjs
