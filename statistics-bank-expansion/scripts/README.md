# Scripts: rebuild and verify the Statistics banks

Dependencies: Python 3.10+ with numpy, scipy, matplotlib; Node.js 18+.
Schema validation also needs EITHER the Python `jsonschema` package (preferred)
OR Ajv 6 for Node (`npm install ajv@6`); `verification/ajv_shim/` lets
validate-reference.py run on Ajv when `jsonschema` is not installed.

Rebuild (from this folder's parent; REF = the unzipped Statistics_Claude_Reference):
    python3 scripts/authoring/build_expanded_banks.py "$REF" .
This regenerates question-banks/statistics/*.json, the PNG assets, and
scripts/verification/checks.json from the baseline + authoring modules
(u1–u4 per unit, u5_topup, u6_breadth).

Verify:
    python3 scripts/verification/verify_expansion.py .          # new computed items
    python3 scripts/verification/coverage_report.py . "$REF/statistics-course.json" --print
    # site checks: copy the 4 banks into $REF/question-banks/statistics/, then in $REF:
    python3 validate-reference.py --source-math                 # needs jsonschema, or:
    PYTHONPATH=<this>/scripts/verification/ajv_shim AJV_PATH=<path to ajv> python3 validate-reference.py --source-math

verify_expansion.py does not import the authoring code. For each id in checks.json it
recomputes the key with its own formulas (pure Python + scipy.special for t), requires the
recomputed numbers in the keyed answer, rejects any MC distractor that also matches, and
warns when an input is not printed in the prompt. checks.json is a sidecar for review only;
it is not part of the bank schema and must not be uploaded into the banks.
