#!/usr/bin/env python3
"""Split teacher-key suffixes from printable PDFs with explicit key headings.

Conservative: leaves ambiguous PDFs unchanged and reports them for manual review.
"""
import json
import re
from pathlib import Path
import fitz

root = Path(__file__).resolve().parents[1]
meta = root / "resource-details.js"
raw = meta.read_text()
prefix = "window.RESOURCE_DETAILS = "
details = json.loads(raw[len(prefix):].rstrip().removesuffix(";"))
changed = []
unresolved = []
for relative, info in details.items():
    if not info.get("embeddedKey"):
        continue
    file = root / relative
    if not file.exists():
        unresolved.append((relative, "missing file"))
        continue
    src = fitz.open(file)
    hits = []
    for idx, page in enumerate(src):
        text = page.get_text().lower().replace("\n", " ")
        # Only recognize explicit teacher-key headings at the beginning of a page.
        head = text[:300]
        if re.search(r"\b(?:teacher(?:'s)?\s+(?:answer\s+)?key|answer\s+key|solutions?\s+key)\b", head):
            hits.append(idx)
    # We must preserve all student pages and avoid choosing a non-final key section.
    if not hits or hits[0] == 0 or any(i < hits[0] for i in hits[1:]):
        unresolved.append((relative, "no unambiguous separate key heading"))
        src.close()
        continue
    first = hits[0]
    student = fitz.open()
    teacher = fitz.open()
    student.insert_pdf(src, from_page=0, to_page=first-1)
    teacher.insert_pdf(src, from_page=first, to_page=len(src)-1)
    key_rel = str(Path(relative).with_name("teacher-key.pdf"))
    key_file = root / key_rel
    if key_file.exists():
        unresolved.append((relative, "separate key already exists"))
        src.close()
        continue
    # Recheck text on student-side pages for explicit keys before writing.
    if any(re.search(r"\b(?:teacher(?:'s)?\s+(?:answer\s+)?key|answer\s+key)\b", student[i].get_text().lower()[:300]) for i in range(len(student))):
        unresolved.append((relative, "key heading within student pages"))
        src.close()
        continue
    src.close()
    student.save(file.with_suffix(".tmp.pdf"), garbage=4, deflate=True)
    teacher.save(key_file, garbage=4, deflate=True)
    student.close(); teacher.close()
    file.with_suffix(".tmp.pdf").replace(file)
    info.pop("embeddedKey", None)
    info["pages"] = first
    info["answerKey"] = key_rel
    info["keyPages"] = len(fitz.open(key_file))
    changed.append(relative)
meta.write_text(prefix + json.dumps(details, ensure_ascii=False, indent=2) + ";\n")
print("SPLIT", len(changed), *changed, sep="\n")
print("REQUIRES REVIEW", len(unresolved), *unresolved, sep="\n")
(root / "teacher-key-audit.txt").write_text("SPLIT\n" + "\n".join(changed) + "\n\nREQUIRES REVIEW\n" + "\n".join(f"{p}: {why}" for p,why in unresolved)+"\n")
