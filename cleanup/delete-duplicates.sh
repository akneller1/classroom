#!/usr/bin/env bash
# Removes the duplicate / unused root files listed in cleanup/DELETE-LIST.txt.
# Run from the repository root:  bash cleanup/delete-duplicates.sh
# Then commit and push. Every item on the list is either an identical copy of a file under
# question-banks/ or artifacts/, already merged into question-banks/manifest.json, or not loaded by any page.
set -euo pipefail
cd "$(dirname "$0")/.."
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if [ -e "$f" ]; then git rm -r -q -- "$f" 2>/dev/null || rm -rf -- "$f"; echo "removed $f"; fi
done < cleanup/DELETE-LIST.txt
echo "Done. Review with 'git status', then commit."
