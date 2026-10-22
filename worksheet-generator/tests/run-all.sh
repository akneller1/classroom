#!/bin/sh
# Math + framework tests need only Node. Browser tests also need playwright-core and Chromium:
#   PW=/path/to/node_modules/playwright-core CHROME=/path/to/chromium sh tests/run-all.sh
set -e
cd "$(dirname "$0")/.."
N=${N:-1000} node tests/run-tests.js | tail -3
node tests/framework-tests.js | tail -2
N=${STRESS:-2000} node tests/seed-stress.js | tail -2
if [ -n "$CHROME" ]; then node tests/browser-test.js | tail -8; node tests/ui-test.js | tail -3; else echo "(browser tests skipped: set PW and CHROME)"; fi
