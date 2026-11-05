import sys, importlib, pjlib
mods = sys.argv[1].split(',')
for m in mods: importlib.import_module(m)
only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
ps = [p for p in pjlib.PROJECTS if not only or p['slug'] in only]
pjlib.build(ps)
print('built', len(ps), [p['folder'] for p in ps])
