#!/usr/bin/env bash
# Removes the retired files listed in cleanup-20261105d/DELETE-LIST.txt.
# Run from the repository root:  bash cleanup-20261105d/delete-old-files.sh   then commit and push.
# The list: thumbnails no page or data file uses, the old single-unit worksheet generator script
# (worksheet-generator/core/app.js) and its two tests, and the image of one replaced question.
set -euo pipefail
cd "$(dirname "$0")/.."
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if [ -e "$f" ]; then git rm -r -q -- "$f" 2>/dev/null || rm -rf -- "$f"; echo "removed $f"; fi
done < cleanup-20261105d/DELETE-LIST.txt
echo "Done. Review with 'git status', then commit."
