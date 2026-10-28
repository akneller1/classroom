"""Geometry games: Showdown, Connect Four, Tic-Tac-Toe and Picture Reveal pages for the ten Geometry units.
Usage: python3 worksheet-generator/games/mkgeometrygames.py <repo>
Each page is a thin wrapper around MKMENU (same verified problems and figures as the flashcards).
An older hand-built page at the same path is kept as legacy.html and linked at the bottom of the new page."""
import sys, os, re
repo = sys.argv[1]
V = 'games-15'
# unit: (folder prefix, menu skill set, label, folder suffix used for the Showdown)
UNITS = [
  ('basics-reasoning', 'geometry-basics-reasoning', 'Basics & Reasoning', 'showdown'),
  ('angles-parallel-lines', 'geometry-angles-parallel-lines', 'Angles & Parallel Lines', 'showdown'),
  ('triangles-congruence', 'geometry-triangles-congruence', 'Triangles & Congruence', 'showdown'),
  ('triangle-relationships', 'geometry-triangle-relationships', 'Triangle Relationships', 'showdown'),
  ('similarity', 'geometry-similarity', 'Similarity', 'showdown'),
  ('right-triangles-trigonometry', 'geometry-right-triangles-trigonometry', 'Right Triangles & Trigonometry', 'showdown'),
  ('quadrilaterals-polygons', 'geometry-quadrilaterals-polygons', 'Quadrilaterals & Polygons', 'showdown'),
  ('coordinate-geometry-transformations', 'geometry-transformations', 'Transformations', 'showdown'),
  ('circles', 'geometry-circles', 'Circles', 'showdown'),
  ('area-surface-area-volume', 'geometry-area-surface-area-volume', 'Area, Surface Area & Volume', 'showdown'),
]
GAMES = [('showdown', 'Showdown'), ('connect-four', 'Connect Four'), ('tic-tac-toe', 'Tic-Tac-Toe'), ('picture-reveal', 'Picture Reveal')]
tpl = open(os.path.join(repo, 'artifacts/circles-flashcards/index.html')).read()
tpl = tpl.split('<p style="text-align:center;margin:20px">')[0]   # drop the flashcards-only legacy link
for prefix, set_id, label, sd in UNITS:
    page = tpl.replace('geometry-circles', set_id).replace('skills/' + set_id + '.js', 'skills/' + set_id + '.js')
    assert 'skills/' + set_id + '.js' in page
    for g, name in GAMES:
        folder = prefix + '-' + g
        title = label + ': Picture Reveal' if g == 'picture-reveal' else label + ' ' + name
        d = os.path.join(repo, 'artifacts', folder); os.makedirs(d, exist_ok=True)
        f = os.path.join(d, 'index.html'); legacy = os.path.join(d, 'legacy.html')
        old = open(f).read() if os.path.exists(f) else ''
        if old and 'games/bank.js' not in old and not os.path.exists(legacy):
            open(legacy, 'w').write(old)
        html = re.sub(r'<title>[^<]*</title>', '<title>' + title.replace('&', '&amp;') + '</title>', page)
        html = re.sub(r'data-game="[^"]*" data-title="[^"]*"', 'data-game="' + g + '" data-title="' + title.replace('&', '&amp;') + '"', html)
        if os.path.exists(legacy):
            html += '<p style="text-align:center;margin:20px"><a href="legacy.html">Open the original hand-built ' + name.lower() + ' (archived)</a></p>\n'
        open(f, 'w').write(html + '</body></html>\n')
        print(folder)
