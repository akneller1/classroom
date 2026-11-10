#!/usr/bin/env python3
"""Read-only, independent checks of unambiguous numeric math-bank questions."""
import csv,json,re
from pathlib import Path
from fractions import Fraction
from collections import Counter

root=Path(__file__).resolve().parent.parent
dest=root/"math-verification-results"
dest.mkdir(exist_ok=True)
manifest=json.loads((root/"question-banks/manifest.json").read_text())
num=r"[-−+]?\d+(?:\.\d+)?"
frac=r"[-−+]?\d+(?: \d+/\d+|/\d+)?"

def rational(s):
    if not isinstance(s,(str,int,float)):return None
    s=str(s).strip().replace("−","-")
    s=re.sub(r"^[a-zA-Z]\\s*=\\s*", "", s)
    try:
        m=re.fullmatch(r"([-+]?\d+) (\d+)/(\d+)",s)
        if m:
            a,b,c=map(int,m.groups())
            return Fraction(a)+(1 if a>=0 else -1)*Fraction(b,c)
        if re.fullmatch(r"[-+]?\d+(?:\.\d+|/\d+)?",s):return Fraction(s)
    except (ValueError,ZeroDivisionError):pass
    return None

def equal(expected,text):
    actual=rational(text)
    if actual is None:return None
    if expected==actual:return True
    m=re.fullmatch(r"[-−+]?\d+\.(\d+)",str(text).strip())
    if m:return abs(expected-actual)<=Fraction(1,2*10**len(m.group(1)))
    return False


def poly_terms(text):
    """Parse explicitly written integer polynomials, without authoring helpers."""
    power_map=str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹","0123456789")
    t=text.replace("−","-").replace(" ","")
    t=re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹]+",lambda m:"^"+m.group().translate(power_map),t)
    if not re.fullmatch(r"[0-9x+\-^]+",t):return None
    output={}
    for part in re.findall(r"[+-]?[^+-]+",t):
        m=re.fullmatch(r"([+-]?)(\d*)x(?:\^(\d+))?",part)
        if m:
            sign,co,ex=m.groups()
            degree=int(ex or 1)
            if degree>9:return None
            val=Fraction(int(co or "1"))*(-1 if sign=="-" else 1)
        elif re.fullmatch(r"[+-]?\d+",part):
            degree=0;val=Fraction(int(part))
        else:return None
        output[degree]=output.get(degree,Fraction(0))+val
    return output if output else None

def sequence_values(expr,start,count):
    import ast
    s=expr.replace("−","-").replace("·","*").replace("×","*").replace(" ","")
    s=re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹]+",lambda m:"**"+m.group().translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹","0123456789")),s)
    s=re.sub(r"(\d)n",r"\1*n",s)
    if not re.fullmatch(r"[0-9n+\-*/().]+",s):return None
    try:
        tree=ast.parse(s,mode="eval")
        def calc(node,n):
            if isinstance(node,ast.Constant) and type(node.value)==int:return Fraction(node.value)
            if isinstance(node,ast.Name) and node.id=="n":return Fraction(n)
            if isinstance(node,ast.UnaryOp):
                a=calc(node.operand,n)
                if isinstance(node.op,ast.USub):return -a
                if isinstance(node.op,ast.UAdd):return a
            if isinstance(node,ast.BinOp):
                a,b=calc(node.left,n),calc(node.right,n)
                if isinstance(node.op,ast.Add):return a+b
                if isinstance(node.op,ast.Sub):return a-b
                if isinstance(node.op,ast.Mult):return a*b
                if isinstance(node.op,ast.Div):return a/b
                if isinstance(node.op,ast.Pow) and b.denominator==1 and -12<=b<=12:return a**int(b)
            raise ValueError("unsupported")
        return [calc(tree.body,n) for n in range(start,start+count)]
    except (SyntaxError,ValueError,ZeroDivisionError,OverflowError):return None

def check_sequence(expected,answer):
    actual=[rational(x.strip()) for x in str(answer).split(",")]
    if len(actual)!=len(expected) or None in actual:return None
    return actual==expected

def solve(prompt):
    p=prompt.strip()
    m=re.fullmatch(r"Divide\. Write the answer in simplest form: ("+frac+r") ÷ ("+frac+r")",p)
    if m:
        a,b=map(rational,m.groups())
        if a is not None and b:return "fraction-division",a/b
    m=re.fullmatch(r"What is the slope of the line through \(\s*("+num+r"),\s*("+num+r")\s*\) and \(\s*("+num+r"),\s*("+num+r")\s*\)\?",p)
    if m:
        a,b,c,d=[Fraction(x.replace("−","-")) for x in m.groups()]
        if c!=a:return "two-point-slope",(d-b)/(c-a)
    m=re.fullmatch(r"Find the slope of the line ("+num+r")x\s*([+-])\s*("+num+r")y\s*=\s*("+num+r")\.",p)
    if m:
        a,sign,b,_=m.groups();b=Fraction(b)*(1 if sign=="+" else -1)
        if b:return "standard-form-slope",-Fraction(a.replace("−","-"))/b
    m=re.fullmatch(r"Use properties to find the sum mentally: ([\d+\s]+)",p)
    if m:
        n=[Fraction(x) for x in re.findall(r"\d+",m.group(1))]
        if len(n)>=2:return "sum",sum(n)
    m=re.fullmatch(r"Find the average rate of change of f\(x\) = x² from x = ("+num+r") to x = ("+num+r")\.",p)
    if m:
        a,b=[Fraction(x.replace("−","-")) for x in m.groups()]
        if a!=b:return "quadratic-rate",a+b
    if "Find the mean." in p:
        prefix=p.split("Find the mean.")[0]
        m=re.search(r":\s*("+num+r"(?:,\s*"+num+r"){3,})\.\s*$",prefix)
        if m:
            n=[Fraction(v.replace("−","-")) for v in re.split(r",\s*",m.group(1))]
            return "mean",sum(n)/len(n)
    if "z-score" in p.lower():
        m=re.search(r"\bwas ("+num+r")\s+\w+.*?\bmean was ("+num+r").*?\bstandard deviation ("+num+r")",p,re.I)
        if m:
            x,avg,sd=[Fraction(v.replace("−","-")) for v in m.groups()]
            if sd:return "z-score",(x-avg)/sd
    m=re.fullmatch(r"Let f\(x\) = ("+num+r")x\s*([+-])\s*("+num+r") and x₀ = ("+num+r")\. Find the third iterate x₃ .*",p)
    if m:
        a,sign,b,x=m.groups()
        a,b,x=Fraction(a.replace("−","-")),Fraction(b)*(1 if sign=="+" else -1),Fraction(x.replace("−","-"))
        for _ in range(3):x=a*x+b
        return "linear-third-iterate",x

    m=re.fullmatch(r"(?:Find f′\((" + num + r")\)|Use the definition f′\(a\) = lim \(h → 0\) \(f\(a \+ h\) - f\(a\)\)/h to find f′\((" + num + r")\)) for f\(x\) = ([^.\n]+)\.",p)
    if m:
        x=Fraction((m.group(1) or m.group(2)).replace("−","-"))
        poly=poly_terms(m.group(3))
        if poly is not None:
            return "polynomial-derivative",sum(k*v*x**(k-1) for k,v in poly.items() if k>0)
    m=re.fullmatch(r"Evaluate (\d+)!\.",p)
    if m and int(m.group(1))<=16:
        import math
        return "factorial",Fraction(math.factorial(int(m.group(1))))
    m=re.fullmatch(r"Evaluate (\d+)!/(\d+)!\.",p)
    if m and max(map(int,m.groups()))<=16:
        import math
        a,b=map(int,m.groups());return "factorial-ratio",Fraction(math.factorial(a),math.factorial(b))
    m=re.fullmatch(r"An arithmetic sequence has a₁ = ("+num+r") and common difference d = ("+num+r")\. Find a_(\d+)\.",p)
    if m:
        a,d,n=m.groups();return "arithmetic-sequence",Fraction(a.replace("−","-"))+(int(n)-1)*Fraction(d.replace("−","-"))
    m=re.fullmatch(r"With F₁ = 1, F₂ = 1 and F_n = F_\(n−1\) \+ F_\(n−2\), find F_(\d+)\.",p)
    if m:
        n=int(m.group(1))
        if n<=100:
            a,b=0,1
            for _ in range(n):a,b=b,a+b
            return "fibonacci",Fraction(a)
    m=re.fullmatch(r"Solve: ("+num+r")x \+ ("+num+r") = ("+num+r")x \+ ("+num+r")",p)
    if m:
        a,b,c,d=[Fraction(x.replace("−","-")) for x in m.groups()]
        if a!=c:return "linear-equation",(d-b)/(a-c)
    m=re.fullmatch(r"Solve: ("+num+r")\(x \+ ("+num+r")\) = ("+num+r")",p)
    if m:
        a,b,c=[Fraction(x.replace("−","-")) for x in m.groups()]
        if a:return "distributive-equation",c/a-b
    m=re.fullmatch(r"Solve: ("+num+r")x \+ ("+num+r") \+ ("+num+r")x = ("+num+r")",p)
    if m:
        a,b,c,d=[Fraction(x.replace("−","-")) for x in m.groups()]
        if a+c:return "combine-equation",(d-b)/(a+c)
    m=re.fullmatch(r"Write the first four terms of the sequence a_n = (.+), starting with n = ([01])\. Separate terms with commas \(fractions as a/b\)\.",p)
    if m:
        expr,start=m.groups()
        vals=sequence_values(expr,int(start),4)
        if vals is not None:return "sequence-terms",vals
    return None

def self_test():
    fixtures=[
        ("Divide. Write the answer in simplest form: 1/4 ÷ 1/2","fraction-division",Fraction(1,2)),
        ("What is the slope of the line through (1, 2) and (5, 10)?","two-point-slope",Fraction(2)),
        ("Find the slope of the line 5x + 4y = -6.","standard-form-slope",Fraction(-5,4)),
        ("Find the average rate of change of f(x) = x² from x = 1 to x = 4.","quadratic-rate",Fraction(5)),
        ("Use properties to find the sum mentally: 39 + 42 + 61","sum",Fraction(142)),
        ("Let f(x) = -3x + 2 and x₀ = 2. Find the third iterate x₃ (x₁ = f(x₀), x₂ = f(x₁), x₃ = f(x₂)).","linear-third-iterate",Fraction(-40)),
        ("KenKen completion times (seconds) for 9 students: 48, 52, 55, 61, 63, 67, 70, 74, 95. Find the mean.","mean",Fraction(65))
    ]
    for prompt,family,expected in fixtures:
        found=solve(prompt)
        if found != (family,expected):
            raise AssertionError("Independent verifier self-check failed for "+family+": "+str(found))
    assert equal(Fraction(1,3),"0.33") is True
    assert equal(Fraction(1,3),"0.32") is False
    assert rational("4 4/5")==Fraction(24,5)
    assert rational("-1 1/2")==Fraction(-3,2)

    assert solve("Find f′(-1) for f(x) = 3x⁴ - 4x.")==("polynomial-derivative",Fraction(-16))
    assert solve("Evaluate 7!/5!.")==("factorial-ratio",Fraction(42))
    assert solve("An arithmetic sequence has a₁ = 3 and common difference d = 4. Find a_20.")==("arithmetic-sequence",Fraction(79))
    assert solve("With F₁ = 1, F₂ = 1 and F_n = F_(n−1) + F_(n−2), find F_10.")==("fibonacci",Fraction(55))
    assert solve("Solve: 9x + 6 = 4x + 56")==("linear-equation",Fraction(10))
    assert solve("Write the first four terms of the sequence a_n = n² + 1, starting with n = 1. Separate terms with commas (fractions as a/b).")==("sequence-terms",[Fraction(2),Fraction(5),Fraction(10),Fraction(17)])
    assert check_sequence([Fraction(2),Fraction(5),Fraction(10),Fraction(17)],"2, 5, 10, 17") is True


self_test()

def normalized(x):
    import unicodedata
    return re.sub(r"\s+"," ",unicodedata.normalize("NFC",str(x)).strip().lower())

totals=Counter();checked=Counter();flags=[]
def flag(kind,bank,q,prompt,answer,computed,part=""):
    flags.append(dict(kind=kind,course=bank["courseId"],unit=bank["unitId"],id=q["id"],
        part=part,prompt=prompt,answer=str(answer),computed=str(computed)))
for entry in manifest["banks"]:
    bank=json.loads((root/entry["path"]).read_text())
    course=bank["courseId"]
    for q in bank["questions"]:
        totals[course]+=1
        candidates=[("main",q.get("prompt",""),q.get("answer",""))]
        if isinstance(q.get("parts"),list):
            candidates=[(str(i+1),p.get("prompt",""),p.get("answer","")) for i,p in enumerate(q["parts"]) if isinstance(p,dict)]
        for part,prompt,answer in candidates:
            result=solve(prompt)
            if result:
                family,expect=result
                verdict=check_sequence(expect,answer) if isinstance(expect,list) else equal(expect,answer)
                if verdict is not None:
                    checked[(course,family)]+=1
                    if verdict is False:flag("numeric-answer-mismatch",bank,q,prompt,answer,expect,part)
        opts=q.get("options",[])
        if q.get("format")=="multiple-choice":
            correct=[o for o in opts if o.get("correct")]
            if len(correct)==1 and isinstance(q.get("answer"),str):
                if normalized(correct[0].get("text"))!=normalized(q["answer"]):
                    flag("marked-answer-text-differs",bank,q,q.get("prompt",""),q["answer"],correct[0].get("text"))
            key=rational(q.get("answer"))
            if key is not None:
                for i,o in enumerate(opts):
                    v=rational(o.get("text"))
                    if v is not None and bool(o.get("correct"))!=(v==key):
                        flag("numeric-distractor-inconsistent",bank,q,q.get("prompt",""),q["answer"],o["text"],str(i+1))
        elif q.get("format")=="select-all" and isinstance(q.get("answer"),list):
            intended={normalized(x) for x in q["answer"]}
            selected={normalized(o.get("text")) for o in opts if o.get("correct")}
            if intended!=selected:flag("select-all-key-differs",bank,q,q.get("prompt",""),sorted(intended),sorted(selected))
            for i,o in enumerate(opts):
                if " → " not in str(o.get("text","")):continue
                stem,claim=o["text"].rsplit(" → ",1)
                result=solve(stem)
                if not result:continue
                family,expect=result
                verdict=equal(expect,claim)
                if verdict is None:continue
                checked[(course,"select-all/"+family)]+=1
                if verdict!=bool(o.get("correct")):flag("select-all-distractor-inconsistent",bank,q,stem,claim,expect,str(i+1))

summary=dict(banks=len(manifest["banks"]),questions=sum(totals.values()),courseQuestions=dict(totals),
  independentlyRecomputed=sum(checked.values()),
  verifiedFamilies=[dict(course=c,family=f,count=n) for (c,f),n in sorted(checked.items())],
  flagged=len(flags),flagTypes=dict(Counter(x["kind"] for x in flags)),
  limits=["Only recognized numeric templates are independently computed.",
          "Unrecognized questions remain unverified, not approved.",
          "Flags need manual review before questions are changed.",
          "Procedural Algebra 1 and Geometry use a separate generator."])
(dest/"report.json").write_text(json.dumps(dict(summary=summary,flags=flags),indent=2,ensure_ascii=False))
with (dest/"review-queue.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=["kind","course","unit","id","part","prompt","answer","computed"])
    w.writeheader();w.writerows(flags)
with (dest/"summary.md").open("w",encoding="utf-8") as f:
    f.write("# Independent mathematics verification\n\n")
    f.write("Read-only numeric checks. Warnings are candidates, not confirmed errors.\n\n")
    f.write("Questions: "+str(summary["questions"])+"; independently recomputed: "+str(summary["independentlyRecomputed"])+"; flags: "+str(len(flags))+"\n\n")
    f.write("| Course | Questions | Recomputed | \n|---|---:|---:|\n")
    for course,n in sorted(totals.items()):
        f.write("| "+course+" | "+str(n)+" | "+str(sum(v for (c,_),v in checked.items() if c==course))+" |\n")
    f.write("\n## Flag types\n\n")
    for kind,n in Counter(x["kind"] for x in flags).most_common():f.write("- "+kind+": "+str(n)+"\n")
    f.write("\nUnsupported problem types remain unverified; review all flagged rows before edits.\n")
print(json.dumps(summary,indent=2))
