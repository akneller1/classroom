#!/usr/bin/env python3
"""Import the Algebra 2 Unit 2 partner check from site_upload and link the encrypted teacher keys.

Usage: python scripts/import_algebra2_unit2_partner_check.py <path to site_upload>
Teacher keys must already be encrypted with qpdf and copied into artifacts/*-partner-checks/teacher-key.pdf.
"""
import json, re, sys
from pathlib import Path
import fitz
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
UPLOAD=Path(sys.argv[1])
slug="linear-functions-systems"
titles=["Linear Equations & Graphs","Systems of Equations & Inequalities"]
src=UPLOAD/"algebra-2"/"unit-2-linear-functions-systems"
raw=(ROOT/"data.js").read_text(encoding="utf-8")
start=raw.find("{"); end=raw.rfind("}")
data=json.loads(raw[start:end+1])
details_path=ROOT/"resource-details.js"
r=details_path.read_text(encoding="utf-8")
details=json.loads(r[r.find("{"):r.rfind("}")+1])
course=next(c for c in data["courses"] if c["id"]=="algebra2")
unit=next(u for u in course["units"] if u["id"]==slug)
key="artifacts/algebra2-partner-checks/teacher-key.pdf"
source_pdf=fitz.open(src/"partner-check-worksheets.pdf")
if len(source_pdf)!=4: raise ValueError("Expected 4 A/B worksheet pages")
# Thumbnail from the upload's thumbnail image, centered on the site's 720x450 card background.
img=Image.open(src/"thumbnail.png").convert("RGB")
scale=min(680/img.width,420/img.height)
img=img.resize((round(img.width*scale),round(img.height*scale)),Image.LANCZOS)
canvas=Image.new("RGB",(720,450),"#f3f6fb")
canvas.paste(img,((720-img.width)//2,(450-img.height)//2))
for n in (1,2):
    first=(n-1)*2
    head=source_pdf[first].get_text()[:180]
    other=source_pdf[first+1].get_text()[:180]
    if not re.search(r"Activity\s+2\."+str(n),head) or "\nB\n" not in other:
        raise ValueError("Unexpected A/B page order in activity "+str(n))
    dest="artifacts/algebra2-"+slug+"-partner-check-"+str(n)+"/worksheet.pdf"
    pdf=fitz.open()
    pdf.insert_pdf(source_pdf,from_page=first,to_page=first+1)
    path=ROOT/dest
    path.parent.mkdir(parents=True,exist_ok=True)
    pdf.save(path,garbage=4,deflate=True)
    pdf.close()
    thumb="thumbs/algebra2-"+slug+"-partner-check-"+str(n)+".jpg"
    canvas.save(ROOT/thumb,quality=82,optimize=True)
    details[dest]={"pages":2,"answerKey":key,"keyPages":4}
    item={"title":"Partner Check "+str(n)+": "+titles[n-1],
          "path":dest,"thumb":thumb,
          "description":"Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
          "type":"Printable","topics":["Partner Check",titles[n-1]],"added":"2026-10-24"}
    existing=next((i for i,a in enumerate(unit["artifacts"]) if a["path"]==dest),None)
    if existing is None:unit["artifacts"].append(item)
    else:unit["artifacts"][existing]=item
source_pdf.close()
# Shared keys: page counts come from the encrypted files themselves.
def pages(p):
    doc=fitz.open(ROOT/p); doc.authenticate("205"); n=len(doc); doc.close(); return n
a1key="artifacts/algebra1-partner-checks/teacher-key.pdf"
counts={k:pages(k) for k in (key,a1key,"artifacts/geometry-partner-checks/teacher-key.pdf")}
algebra1=next(c for c in data["courses"] if c["id"]=="algebra")
a1paths={a["path"] for u in algebra1["units"] for a in u["artifacts"] if "partner-check" in a["path"]}
for p,d in details.items():
    if p in a1paths:
        d.pop("studentOnly",None); d["answerKey"]=a1key
    if d.get("answerKey") in counts: d["keyPages"]=counts[d["answerKey"]]
(ROOT/"data.js").write_text(raw[:start]+json.dumps(data,ensure_ascii=False,indent=2)+raw[end+1:],encoding="utf-8")
details_path.write_text(r[:r.find("{")]+json.dumps(details,ensure_ascii=False,indent=2)+r[r.rfind("}")+1:],encoding="utf-8")
print("Imported Algebra 2 Unit 2 partner check; linked",len(a1paths),"Algebra 1 partner checks to",a1key,counts)
