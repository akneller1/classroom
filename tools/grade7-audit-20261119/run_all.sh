#!/usr/bin/env bash
# Rebuilds every Grade 7 bank and vocabulary change of the 2026-11-19 audit, in order. Rerunning changes nothing.
set -euo pipefail
T="$(cd "$(dirname "$0")" && pwd)"
R="$(cd "$T/../.." && pwd)"
python3 $T/fix_text.py      # G1: 20
python3 $T/place_value.py   # G1: 12
python3 $T/retag.py         # G1: 11
python3 $T/new_items.py     # G2: 4-10, 13
python3 $T/honors.py        # G2: 3
python3 $T/vocab.py         # G1: 19
node $R/scripts/build_standards_map.cjs
