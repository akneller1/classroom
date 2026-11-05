"""Independent verification of the new Algebra 2 items (the new-only banks a2build.py writes to MG_OUT).
Usage: MG_OUT=<scratch> python3 tools/middle-grades-authoring/a2verify.py [unit-id ...]  → must print TOTAL ERRORS 0"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], "precalculus"] + sys.argv[1:]   # makes gverify load the high-school SymPy checks
import a2build  # noqa: F401  registers the algebra2 course
import hschecks
import a2checks  # noqa: F401
import gverify
gverify.hschecks = hschecks
sys.exit(1 if gverify.main("algebra2", sys.argv[2:] or None) else 0)
