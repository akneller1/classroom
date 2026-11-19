#!/usr/bin/env bash
# Rebuilds every Statistics bank change of the 2026-11-18 audit from the published banks, in order. Rerunning changes nothing.
set -euo pipefail
T="$(cd "$(dirname "$0")" && pwd)"
python3 $T/fix_text.py      # 12, 13, 19
python3 $T/dedupe.py        # 14
python3 $T/new_items.py     # 6, 11
python3 $T/retag.py         # 3
python3 $T/steps.py         # 1
python3 $T/std_js.py        # 3 (descriptions)
node "$T/../../scripts/build_standards_map.cjs"
