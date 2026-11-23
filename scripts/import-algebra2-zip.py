#!/usr/bin/env python3
"""Import an Algebra 2 publication ZIP safely, verify it, and update the manifest.
Usage: python scripts/import-algebra2-zip.py /path/to/algebra2-publish-package.zip
Run from the repository root; commit/push the resulting files normally.
"""
import json, pathlib, subprocess, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALLOWED = ("question-banks/algebra2/", "question-banks/assets/algebra2/")
UNITS = {"functions-transformations", "linear-functions-systems", "quadratic-functions-complex-numbers"}

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/import-algebra2-zip.py PACKAGE.zip")
    archive = pathlib.Path(sys.argv[1]).resolve()
    staged = {}
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            path = pathlib.PurePosixPath(member.filename)
            if member.is_dir():
                continue
            if path.is_absolute() or ".." in path.parts or "\\" in member.filename:
                sys.exit("Unsafe ZIP path: " + member.filename)
            if not (member.filename.startswith(ALLOWED) or member.filename == "question-banks/manifest.json"):
                continue
            if member.filename in staged:
                sys.exit("Duplicate ZIP entry: " + member.filename)
            if (member.external_attr >> 16) & 0o170000 == 0o120000:
                sys.exit("Symlink disallowed: " + member.filename)
            staged[member.filename] = z.read(member)
    expected = {"question-banks/algebra2/" + u + ".json" for u in UNITS}
    if not expected.issubset(staged):
        sys.exit("Package missing banks: " + repr(sorted(expected - staged.keys())))
    manifest = json.loads(staged.get("question-banks/manifest.json", b"{}"))
    if manifest.get("version") != 1:
        sys.exit("Invalid package manifest")
    desired = {r["unitId"]: r for r in manifest.get("banks", []) if r.get("courseId") == "algebra2"}
    if set(desired) != UNITS or any(r.get("approved") is not True or r.get("path") != "question-banks/algebra2/"+u+".json" for u,r in desired.items()):
        sys.exit("Manifest doesn't name exactly the three intended Algebra 2 banks")
    for unit in UNITS:
        bank = json.loads(staged["question-banks/algebra2/"+unit+".json"])
        if bank.get("courseId") != "algebra2" or bank.get("unitId") != unit:
            sys.exit("Question-bank course/unit mismatch: "+unit)
        for q in bank.get("questions", []):
            d = q.get("diagram") or {}
            if d.get("type") == "image":
                src = (d.get("spec") or {}).get("src")
                if src not in staged and not (ROOT / str(src)).is_file():
                    sys.exit("Missing image referenced by "+str(q.get("id"))+": "+str(src))
    for name, data in staged.items():
        if name == "question-banks/manifest.json":
            continue
        out = ROOT / name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
    for unit in sorted(UNITS):
        subprocess.run(["node", "scripts/check-question-bank.cjs", "question-banks/algebra2/"+unit+".json"], cwd=ROOT, check=True)
    existing = ROOT / "question-banks/manifest.json"
    current = json.loads(existing.read_text())
    banks = [r for r in current.get("banks", []) if not (r.get("courseId") == "algebra2" and r.get("unitId") in UNITS)]
    banks.extend(desired[u] for u in sorted(UNITS))
    existing.write_text(json.dumps({"version":1,"banks":banks}, indent=2)+"\n")
    print("Imported 3 Algebra 2 banks, image assets, and manifest entries. Commit and push to publish.")
    print("WARNING: Structural validation is not independent mathematical review.")

if __name__ == "__main__":
    main()
