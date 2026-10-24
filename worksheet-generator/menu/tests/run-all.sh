#!/bin/sh
# Menu Assessment Generator tests. Browser tests need Playwright + Chromium (skipped if unavailable).
set -e
cd "$(dirname "$0")"
N=${N:-200} node math-tests.cjs | tail -3
node model-tests.cjs | tail -1
if node -e "require(process.env.PW || 'playwright')" 2>/dev/null; then node browser-test.cjs | tail -1; else echo "(browser tests skipped: install playwright or set PW and CHROME)"; fi
