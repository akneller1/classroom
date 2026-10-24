#!/usr/bin/env python3
"""Import the original Algebra2_Partner_Check_All.zip into existing course units."""
import io, json, re, zipfile
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
INCOMING=ROOT/"incoming"/"Algebra2_Partner_Check_All.zip"
units=[
("Unit1_Functions_and_Transformations","functions-transformations","Functions & Transformations",["Function Operations & Evaluation","Transformations of Functions"]),
("Unit2_Quadratics_and_Complex_Numbers","quadratic-functions-complex-numbers","Quadratic Functions & Complex Numbers",["Solving Quadratic Equations","Complex Numbers & Parabolas"]),
("Unit3_Polynomial_Functions","polynomial-functions","Polynomial Functions",["Polynomial Operations & Graphs","Zeros, Factoring & Inequalities"]),
("Unit4_Radicals_and_Rational_Exponents","radicals-rational-exponents","Radicals & Rational Exponents",["Simplifying Radicals & Exponents","Radical Equations & Functions"]),
("Unit5_Rational_Functions","rational-functions","Rational Functions",["Rational Expressions & Equations","Graphs of Rational Functions"]),
("Unit6_Exponential_and_Logarithmic_Functions","exponential-logarithmic-functions","Exponential & Logarithmic Functions",["Exponential & Log Basics","Exp & Log Equations and Graphs"]),
("Unit7_Sequences_and_Series","sequences-series","Sequences & Series",["Arithmetic & Geometric Sequences","Series, Binomials & Applications"]),
("Unit8_Trigonometry","trigonometric-functions","Trigonometric Functions",["Radians, Unit Circle & Right-Triangle Trig","Graphs of Trig Functions & Trig Equations"])
]
if not INCOMING.is_file(): raise SystemExit("Expected incoming/Algebra2_Partner_Check_All.zip")
raw=(ROOT/"data.js").read_text()
start=raw.find("{"); end=raw.rfind("}")
data=json.loads(raw[start:end+1])
details_path=ROOT/"resource-details.js"
r=details_path.read_text()
details=json.loads(r[r.find("{"):r.rfind("}")+1])
course=next(c for c in data["courses"] if c["id"]=="algebra2")
keypath=ROOT/"artifacts/algebra2-partner-checks/teacher-key.pdf"
keypath.parent.mkdir(parents=True,exist_ok=True)
expected={"Algebra2_Teacher_Answer_Key.pdf"} | {"Algebra2_"+u[0]+".pdf" for u in units}
with zipfile.ZipFile(INCOMING) as z:
    if set(z.namelist()) != expected: raise ValueError("Unexpected ZIP contents; refusing to import")
    keybytes=z.read("Algebra2_Teacher_Answer_Key.pdf")
    keydoc=fitz.open(stream=keybytes,filetype="pdf")
    if len(keydoc)!=3: raise ValueError("Unexpected teacher key page count")
    keypath.write_bytes(keybytes)
    keydoc.close()
    imported=[]
    for source,slug,unitname,titles in units:
        unit=next((u for u in course["units"] if u["id"]==slug),None)
        if unit is None: raise ValueError("Missing Algebra 2 unit "+slug)
        source_pdf=fitz.open(stream=z.read("Algebra2_"+source+".pdf"),filetype="pdf")
        if len(source_pdf)!=4: raise ValueError("Expected 4 A/B worksheet pages: "+source)
        for n in (1,2):
            first=(n-1)*2
            head=source_pdf[first].get_text()[:180]
            other=source_pdf[first+1].get_text()[:180]
            if not re.search(r"Activity\s+\d+\\."+str(n),head) or " B " not in other.replace("\n"," "):
                raise ValueError("Unexpected A/B page order in "+source+" activity "+str(n))
            dest="artifacts/algebra2-"+slug+"-partner-check-"+str(n)+"/worksheet.pdf"
            pdf=fitz.open()
            pdf.insert_pdf(source_pdf,from_page=first,to_page=first+1)
            path=ROOT/dest
            path.parent.mkdir(parents=True,exist_ok=True)
            pdf.save(path,garbage=4,deflate=True)
            png=pdf[0].get_pixmap(matrix=fitz.Matrix(1.1,1.1),alpha=False)
            # Thumbnail JPEG rendered from actual first worksheet page.
            from PIL import Image,ImageOps,ImageDraw
            img=Image.open(io.BytesIO(png.tobytes("png"))).convert("RGB")
            img.thumbnail((680,420))
            canvas=Image.new("RGB",(720,450),"#f3f6fb")
            canvas.paste(img,((720-img.width)//2,(450-img.height)//2))
            thumb="thumbs/algebra2-"+slug+"-partner-check-"+str(n)+".jpg"
            canvas.save(ROOT/thumb,quality=82,optimize=True)
            pdf.close()
            details[dest]={"pages":2,"answerKey":"artifacts/algebra2-partner-checks/teacher-key.pdf","keyPages":3}
            item={"title":"Partner Check "+str(n)+": "+titles[n-1],
                  "path":dest,"thumb":thumb,
                  "description":"Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
                  "type":"Printable","topics":["Partner Check",titles[n-1]],"added":"2026-10-24"}
            existing=next((i for i,a in enumerate(unit["artifacts"]) if a["path"]==dest),None)
            if existing is None:unit["artifacts"].append(item)
            else:unit["artifacts"][existing]=item
            imported.append(dest)
        source_pdf.close()
(ROOT/"data.js").write_text(raw[:start]+json.dumps(data,ensure_ascii=False,indent=2)+raw[end+1:])
details_path.write_text(r[:r.find("{")]+json.dumps(details,ensure_ascii=False,indent=2)+r[r.rfind("}")+1:])
INCOMING.unlink()
print("Imported",len(imported),"partner-check PDFs into",len(units),"Algebra 2 units, generated thumbnails and linked shared locked teacher key")
