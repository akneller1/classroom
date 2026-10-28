"""Keep the Geometry units in data.js complete: tools, cheat sheet, flashcards and the four generated games.
Run from the repo root: python3 scripts/sync_geometry_listings.py   (idempotent; rewrites data.js with the same formatting)."""
import json, os
TODAY = '2026-10-28'
# unit id -> (menu set id, game folder prefix, label, cheat sheet name)
U = {
  'foundations-geometry': ('geometry-basics-reasoning', 'basics-reasoning', 'Basics & Reasoning', 'geometry-basics'),
  'angles-parallel-lines': ('geometry-angles-parallel-lines', 'angles-parallel-lines', 'Angles & Parallel Lines', 'geometry-angles-parallel-lines'),
  'triangle-congruence': ('geometry-triangles-congruence', 'triangles-congruence', 'Triangles & Congruence', 'geometry-triangles-congruence'),
  'triangle-relationships': ('geometry-triangle-relationships', 'triangle-relationships', 'Triangle Relationships', 'geometry-triangle-relationships'),
  'similarity': ('geometry-similarity', 'similarity', 'Similarity', 'geometry-similarity'),
  'right-triangles-trigonometry': ('geometry-right-triangles-trigonometry', 'right-triangles-trigonometry', 'Right Triangles & Trigonometry', 'geometry-right-triangles-trigonometry'),
  'quadrilaterals-polygons': ('geometry-quadrilaterals-polygons', 'quadrilaterals-polygons', 'Quadrilaterals & Polygons', 'geometry-quadrilaterals-polygons'),
  'transformations': ('geometry-transformations', 'coordinate-geometry-transformations', 'Transformations', 'geometry-coordinate-transformations'),
  'circles': ('geometry-circles', 'circles', 'Circles', 'geometry-circles'),
  'area-surface-area-volume': ('geometry-area-surface-area-volume', 'area-surface-area-volume', 'Area, Surface Area & Volume', 'geometry-area-surface-area-volume'),
}
# printables that can carry Geometry diagrams (Maze and Tarsia need short problems without a picture; the proof-based Congruence unit only fills stations)
PRINT = [
  ('color', 'Color by Number Generator', 'Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.'),
  ('error', 'Error Analysis Generator', 'Make an error-analysis worksheet for this unit: each student\u2019s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.'),
  ('partner', 'Partner Check Generator', 'Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners\u2019 solutions.'),
  ('who', 'Whodunnit Generator', 'Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.'),
  ('stations', 'Stations Generator', 'Make station pages for this unit: choose 2\u20136 stations and 6\u201310 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.'),
]
CHEAT = json.load(open(os.environ.get('CHEATJSON', 'scripts/cheat-sheets/geometry-meta.json')))
s = open('data.js').read(); i = s.index('{'); j = s.rindex('}') + 1
pre, post = s[:i], s[j:]; d = json.loads(s[i:j])
geo = [c for c in d['courses'] if c['id'] == 'geometry'][0]

def upsert(arts, match, entry, keep=('added',)):
    for a in arts:
        if match(a):
            for k in keep:
                if k in a: entry[k] = a[k]
            a.clear(); a.update(entry); return
    arts.append(entry)

for u in geo['units']:
    if u['id'] not in U: continue
    sid, pre_, label, cname = U[u['id']]
    A = u['artifacts']; meta = CHEAT[cname]
    fc = next((a for a in A if a['path'] == 'artifacts/%s-flashcards/index.html' % pre_), None)
    topics = (fc or {}).get('topics') or [meta['focus']]
    base = 'worksheet-generator/%s#unit=' + sid
    tools = [
      ('Assessment Readiness Check', 'practice-test.html', 'Study Guide', 'A %s readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.' % label),
      ('Daily Lesson Planner', 'lesson-planner.html', 'Planning', 'Day-by-day lesson plans for Geometry, including %s: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.' % label),
      ('Worksheet Generator', 'worksheet.html', 'Practice', 'Differentiated %s worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.' % label),
      ('Assessment Generator', 'menu-assessment.html', 'Printable', 'Build %s quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.' % label),
    ]
    for title, page, typ, desc in tools:
        e = {'title': title, 'path': base % page, 'description': desc, 'type': typ, 'added': TODAY}
        upsert(A, lambda a, p=base % page: a['path'] == p, e)
    # tools first, in this order
    order = [base % t[1] for t in tools]
    A.sort(key=lambda a: order.index(a['path']) if a['path'] in order else len(order))
    for kind, ptitle, pdesc in PRINT:
        if sid == 'geometry-triangles-congruence' and kind != 'stations': continue
        pp = 'worksheet-generator/printables.html#unit=%s&kind=%s' % (sid, kind)
        upsert(A, lambda a, q=pp: a['path'] == q, {'title': ptitle, 'path': pp, 'description': pdesc, 'type': 'Printable', 'topics': ['Printable generator', label], 'added': TODAY})
    # flashcards keep their entry; games
    gdesc = {
      'showdown': ('%s Showdown', 'A game board for %s: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.'),
      'connect-four': ('%s Four', 'Connect Four for two teams on %s. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.'),
      'tic-tac-toe': ('%s Tic-Tac-Toe', 'Tic-Tac-Toe for two teams on %s. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.'),
      'picture-reveal': ('%s Picture Reveal', 'Ten typed problems on %s. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.'),
    }
    for g, (tt, dd) in gdesc.items():
        path = 'artifacts/%s-%s/index.html' % (pre_, g)
        old = [a for a in A if a['path'] in (path, 'artifacts/%s-jeopardy/index.html' % pre_)] if g == 'showdown' else [a for a in A if a['path'] == path]
        title = old[0]['title'] if old else (tt % label if g != 'picture-reveal' else label + ' Picture Reveal')
        e = {'title': title, 'path': path, 'description': dd % label, 'type': 'Game', 'topics': topics + ['Team game'] if g != 'picture-reveal' else topics, 'added': old[0]['added'] if old else TODAY}
        if old: old[0].clear(); old[0].update(e)
        else: A.append(e)
    # cheat sheet
    cpath = 'artifacts/%s-cheat-sheet/worksheet.pdf' % cname
    e = {'title': label + ' Cheat Sheet', 'path': cpath, 'thumb': 'thumbs/%s-cheat-sheet.jpg' % cname,
         'description': 'Two-page printable cheat sheet for %s. Front: %s. Back: %s. Key vocabulary, worked examples with every answer checked, and common mistakes.' % (label, meta['focus'], meta['morefocus']),
         'type': 'Printable', 'topics': ['Cheat sheet', 'Reference', label, 'Unit %s' % meta['unitNo']], 'added': TODAY}
    upsert(A, lambda a: a['path'] == cpath, e)
    for a in A:   # thumbs for generated games
        if a['path'].startswith('artifacts/%s-' % pre_) and a['path'].endswith('/index.html') and 'thumb' not in a:
            a['thumb'] = 'thumbs/' + a['path'].split('/')[1] + '.jpg'
        if a['path'].startswith('artifacts/%s-' % pre_) and a['path'].endswith('/index.html') and a['type'] == 'Game' and any(x in a['path'] for x in ('showdown', 'jeopardy')):
            a['thumb'] = 'thumbs/%s-showdown.jpg' % pre_
open('data.js', 'w').write(pre + json.dumps(d, indent=2, ensure_ascii=False) + post)
print('ok')
