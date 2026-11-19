"""Build the Grade 4 audit overlay: python3 tools/grade4-audit-20261119/build.py (G4_BASE = assembled site after
apply-content-updates.mjs and apply-kid-friendly.mjs)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import load_base, Overlay
import fixes

o = Overlay(*load_base())
fixes.run(o)
for name in sys.argv[1:] or ['advanced', 'openresp', 'selectall', 'plots']:
    try:
        mod = __import__(name)
    except ModuleNotFoundError:
        continue
    mod.run(o)
o.write()
print('edits', sum(len(v) for v in o.edits.values()), 'additions', sum(len(v) for v in o.adds.values()), 'meta', sum(len(v) for v in o.newmeta.values()))
