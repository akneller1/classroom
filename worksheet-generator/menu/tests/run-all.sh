#!/bin/sh
# The library first: every activity in exactly one unit, distinct titles, files present
python3 "$(dirname "$0")/../../../scripts/check_library.py" | tail -1
# Menu Assessment Generator tests. Browser tests need Playwright + Chromium (skipped if unavailable).
set -e
cd "$(dirname "$0")"
N=${N:-200} node math-tests.cjs | tail -3
node model-tests.cjs | tail -1
node test-mode-tests.cjs | tail -1
node worksheet-tests.cjs | tail -1
node printables-tests.cjs | tail -1
if node -e "require(process.env.PW || 'playwright')" 2>/dev/null; then node browser-test.cjs | tail -1; node printables-browser.cjs | tail -1; else echo "(browser tests skipped: install playwright or set PW and CHROME)"; fi
# Daily Lesson Planner: every lesson mapped, every day × level builds with verified problems; browser check needs the server at BASE
node ../../planner/tests/planner-tests.cjs | tail -1
if node -e "require(process.env.PW || 'playwright')" 2>/dev/null && curl -s -o /dev/null "${BASE:-http://localhost:8765}/index.html"; then node ../../planner/tests/planner-browser.cjs | tail -1; else echo "(planner browser test skipped: no Playwright or no server at BASE)"; fi
# Generated games: the question bank (Node) and every game played in a browser (needs a server at BASE, default localhost:8765)
node ../../games/tests/games-tests.cjs | tail -1
if node -e "require(process.env.PW || 'playwright')" 2>/dev/null && curl -s -o /dev/null "${BASE:-http://localhost:8765}/index.html"; then node ../../games/tests/games-browser.cjs | tail -1; else echo "(game browser tests skipped: no Playwright or no server at BASE)"; fi
