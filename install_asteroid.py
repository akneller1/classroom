from pathlib import Path
import re
root=Path(__file__).resolve().parent
site=Path.cwd()
source=root/'data.js'
txt=source.read_text()
a=txt.index('/* Asteroid Blaster:')
b=txt.index('/* Interactive Math:',a)
block=txt[a:b]
target=site/'data.js'
if not target.exists(): raise SystemExit('Run from the root of your classroom repository (data.js not found).')
existing=target.read_text()
if '/* Asteroid Blaster:' not in existing:
    marker='/* Interactive Math:'
    if marker not in existing: raise SystemExit('Insertion marker missing; no changes made.')
    existing=existing.replace(marker,block+marker,1)
    target.write_text(existing)
    print('Added Asteroid Blaster cards without replacing existing library data.')
else: print('Asteroid Blaster already registered; no duplicate added.')
for name in ['worksheet-generator/asteroid-blaster.html','thumbs/asteroid-blaster.jpg']:
    f=site/name; f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((root/name).read_bytes());print('Installed',name)
