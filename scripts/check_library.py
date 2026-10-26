#!/usr/bin/env python3
"""Check (and optionally fix) the activity library in data.js.

Problems reported:
  * the same activity (same path) listed in more than one unit of a course
  * the same activity listed twice in one unit
  * two different activities with the same title in one course (teachers cannot tell them apart)
  * an activity or thumbnail file that does not exist
  * an Algebra flashcard deck without the Easy / Medium / Hard level menu
  * a fixed assessment-menu PDF in a unit that has the Assessment Generator
  * an old template worksheet generator in a unit that has the verified Worksheet Generator (worksheet.html)
  * an Algebra 1 unit without the Worksheet Generator or the Assessment Generator, or a generator link to a
    unit the generators do not know (#unit=<id> must be a registered skill set)
  * an Algebra 1 unit without exactly one of each generated game (Flashcards, Showdown, Connect Four,
    Tic-Tac-Toe, Picture Reveal), or with an older hand-made copy of one of those games
  * an Algebra 1 unit without the printable generators (Maze, Color by Number, Tarsia, Error Analysis,
    Partner Check; worksheet-generator/printables.html#unit=<set>&kind=<kind>), or with an older fixed PDF of one

Usage:
  python3 scripts/check_library.py          # report; exit code 1 if anything is wrong
  python3 scripts/check_library.py --fix    # remove duplicate listings, keeping each activity in one unit

Where a shared activity is kept is decided by scripts/library-placement.json (path -> unit).
An activity that covers two units goes to the unit its content is mainly about; an even mix goes to the
later unit (by then students have learned all of it). New duplicates without a decision are kept in the
later unit and the decision is added to library-placement.json, so the same choice is made every time.
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data.js')
PLACE = os.path.join(ROOT, 'scripts', 'library-placement.json')


def load():
    s = open(DATA, encoding='utf-8').read()
    i = s.index('=')
    return s[:i + 1], json.loads(s[i + 1:].strip().rstrip(';'))


def save(head, d):
    open(DATA, 'w', encoding='utf-8').write(head + ' ' + json.dumps(d, indent=2, ensure_ascii=False) + ';\n')


_SETS = None
def skill_sets():
    """Ids of the skill sets registered in worksheet-generator/menu/skills/*.js."""
    global _SETS
    if _SETS is None:
        _SETS = set()
        d = os.path.join(ROOT, 'worksheet-generator', 'menu', 'skills')
        for f in os.listdir(d) if os.path.isdir(d) else []:
            if f.endswith('.js'):
                txt = open(os.path.join(d, f), encoding='utf-8').read()
                _SETS.update(re.findall(r"registerSkillSet\(\{\s*id:\s*'([a-z0-9-]+)'", txt))
    return _SETS


def main():
    fix = '--fix' in sys.argv
    head, d = load()
    place = json.load(open(PLACE, encoding='utf-8')) if os.path.exists(PLACE) else {}
    problems, changed, new_decisions = [], 0, 0
    for c in d['courses']:
        order = [u['id'] for u in c['units']]
        where = collections.defaultdict(list)
        for u in c['units']:
            for a in u['artifacts']:
                where[a['path']].append(u['id'])
        for path, units in where.items():
            if len(units) == 1:
                continue
            distinct = sorted(set(units), key=order.index)
            keep = place.get(path, {}).get('unit')
            if keep not in distinct:
                keep = distinct[-1]
                if len(distinct) > 1:
                    place[path] = {'course': c['id'], 'unit': keep}
                    new_decisions += 1
            if len(distinct) > 1:
                problems.append('%s: "%s" is listed in %s (belongs in %s)' % (c['id'], path, ', '.join(distinct), keep))
            else:
                problems.append('%s: "%s" is listed %d times in %s' % (c['id'], path, len(units), keep))
            if fix:
                for u in c['units']:
                    kept = False
                    new = []
                    for a in u['artifacts']:
                        if a['path'] != path:
                            new.append(a)
                        elif u['id'] == keep and not kept:
                            new.append(a)
                            kept = True
                        else:
                            changed += 1
                    u['artifacts'] = new
        for u in c['units']:   # a unit with the menu generator does not also list a fixed assessment-menu PDF
            if any('menu-assessment.html' in a['path'] for a in u['artifacts']):
                for a in u['artifacts']:
                    if a['path'].endswith('-assessment-menu/worksheet.pdf'):
                        problems.append('%s/%s: fixed assessment menu "%s" listed next to the Assessment Generator (remove it)' % (c['id'], u['id'], a['title']))
        for u in c['units']:   # the verified Worksheet Generator replaces the old template generators
            if any(a['path'].startswith('worksheet-generator/worksheet.html') for a in u['artifacts']):
                for a in u['artifacts']:
                    p = a['path'].split('#')[0]
                    if (p.startswith('worksheet-generator/algebra1-') and p.endswith('.html')) or p == 'artifacts/worksheet-generator/index.html':
                        problems.append('%s/%s: old worksheet generator "%s" listed next to the Worksheet Generator (remove it)' % (c['id'], u['id'], a['title']))
        if c['id'] == 'algebra':   # every Algebra 1 unit has both generators, pointing at a real skill set
            for u in c['units']:
                for page, name in (('worksheet.html', 'Worksheet Generator'), ('menu-assessment.html', 'Assessment Generator')):
                    links = [a['path'] for a in u['artifacts'] if a['path'].startswith('worksheet-generator/' + page + '#unit=')]
                    if not links:
                        problems.append('%s/%s: no %s (add worksheet-generator/%s#unit=<skill set>)' % (c['id'], u['id'], name, page))
                    for l in links:
                        sid = l.split('#unit=')[1].split('&')[0]
                        if sid not in skill_sets():
                            problems.append('%s/%s: %s points at unknown skill set "%s"' % (c['id'], u['id'], name, sid))
        if c['id'] == 'algebra':   # the same five generated games in every Algebra 1 unit, and no older copies
            KINDS = [('Flashcards', r'flashcards'), ('Showdown', r'showdown|jeopardy'), ('Connect Four', r'connect-four|-four/'),
                     ('Tic-Tac-Toe', r'tic-tac-toe'), ('Picture Reveal', r'picture-reveal')]
            for u in c['units']:
                for kind, rx in KINDS:
                    found = [a['path'] for a in u['artifacts'] if a['path'].startswith('artifacts/') and re.search(rx, a['path'])]
                    gen = [p for p in found if os.path.exists(os.path.join(ROOT, p)) and 'data-game=' in open(os.path.join(ROOT, p), encoding='utf-8', errors='ignore').read()]
                    if len(gen) != 1:
                        problems.append('%s/%s: needs exactly one generated %s (found %d; make it with worksheet-generator/games/mkgames.py)' % (c['id'], u['id'], kind, len(gen)))
                    for p in found:
                        if p not in gen:
                            problems.append('%s/%s: older hand-made %s "%s" duplicates the generated one (remove it)' % (c['id'], u['id'], kind, p))
        if c['id'] == 'algebra':   # the printable generators replace the fixed maze / Tarsia / color / error / partner / whodunnit / stations PDFs
            PKINDS = [('maze', 'Maze', r'maze'), ('color', 'Color by Number', r'color-by-number'), ('tarsia', 'Tarsia', r'tarsia'),
                      ('error', 'Error Analysis', r'error-analysis'), ('partner', 'Partner Check', r'partner-check'),
                      ('who', 'Whodunnit', r'-whodunnit/'), ('stations', 'Stations', r'-stations/')]
            GAPS = {'statistics-data-modeling': ['tarsia']}   # too few short problems for a Tarsia (see menu/tests/printables-tests.cjs)
            for u in c['units']:
                for kind, name, rx in PKINDS:
                    gens = [a['path'] for a in u['artifacts'] if re.match(r'worksheet-generator/printables\.html#unit=[a-z0-9-]+&kind=' + kind + '$', a['path'])]
                    if kind in GAPS.get(u['id'], []):
                        if gens: problems.append('%s/%s: lists a %s generator, but this unit cannot make one' % (c['id'], u['id'], name))
                    elif len(gens) != 1:
                        problems.append('%s/%s: needs exactly one %s generator (found %d)' % (c['id'], u['id'], name, len(gens)))
                    for g in gens:
                        sid = g.split('#unit=')[1].split('&')[0]
                        if sid not in skill_sets(): problems.append('%s/%s: %s generator points at unknown skill set "%s"' % (c['id'], u['id'], name, sid))
                    for a in u['artifacts']:
                        if a['path'].startswith('artifacts/') and a['path'].endswith('.pdf') and re.search(rx, a['path']):
                            problems.append('%s/%s: older fixed %s "%s" duplicates the %s generator (remove it)' % (c['id'], u['id'], name, a['title'], name))
            # every Algebra 1 unit has the hand-made unit pack: a cheat sheet, an escape room and an online detective game
            for u in c['units']:
                arts = u['artifacts']
                if not any(re.search(r'-cheat-sheet/worksheet\.pdf$', a['path']) for a in arts): problems.append('%s/%s: no cheat sheet' % (c['id'], u['id']))
                if not any(re.search(r'-escape-room/index\.html$', a['path']) for a in arts): problems.append('%s/%s: no escape room' % (c['id'], u['id']))
                if not any('Detective game' in (a.get('topics') or []) for a in arts): problems.append('%s/%s: no detective game' % (c['id'], u['id']))
        if c['id'] == 'algebra':   # every Algebra 1 unit opens the Daily Lesson Planner on that unit
            for u in c['units']:
                links = [a['path'] for a in u['artifacts'] if a['path'].startswith('worksheet-generator/lesson-planner.html')]
                if len(links) != 1:
                    problems.append('%s/%s: needs exactly one Daily Lesson Planner (found %d)' % (c['id'], u['id'], len(links)))
                elif links[0].split('#unit=')[-1] not in skill_sets():
                    problems.append('%s/%s: Daily Lesson Planner points at unknown skill set "%s"' % (c['id'], u['id'], links[0].split('#unit=')[-1]))
        for u in c['units']:   # every cheat sheet is built by scripts/cheat-sheets (one style; Andrey 2026-10-25)
            for a in u['artifacts']:
                m = re.match(r'artifacts/(.+)-cheat-sheet/worksheet\.pdf$', a['path'])
                if m and not os.path.exists(os.path.join(ROOT, 'scripts', 'cheat-sheets', 'content', m.group(1) + '.cjs')):
                    problems.append('%s/%s: cheat sheet "%s" has no content file scripts/cheat-sheets/content/%s.cjs (build it in the shared style)' % (c['id'], u['id'], a['title'], m.group(1)))
        titles = collections.defaultdict(set)
        for u in c['units']:
            for a in u['artifacts']:
                titles[a['title'].strip().lower()].add(a['path'])
        for t, paths in titles.items():
            if len(paths) > 1 and t not in ('menu assessment generator', 'assessment generator', 'worksheet generator', 'maze generator', 'color by number generator', 'tarsia generator', 'error analysis generator', 'partner check generator', 'whodunnit generator', 'stations generator', 'daily lesson planner'):
                problems.append('%s: %d different activities share the title "%s": %s' % (c['id'], len(paths), t, ', '.join(sorted(paths))))
        for u in c['units']:
            for a in u['artifacts']:
                f = a['path'].split('#')[0]
                if not os.path.exists(os.path.join(ROOT, f)):
                    problems.append('%s/%s: missing file %s' % (c['id'], u['id'], f))
                if c['id'] in ('algebra', 'algebra2') and f.endswith('-flashcards/index.html') and os.path.exists(os.path.join(ROOT, f)):
                    page = open(os.path.join(ROOT, f), encoding='utf-8', errors='ignore').read()
                    if 'id="level"' not in page and 'data-game="flashcards"' not in page:
                        problems.append('%s/%s: flashcards without an Easy/Medium/Hard level menu: %s (run scripts/flashcard_levels.py on it)' % (c['id'], u['id'], f))
                if a.get('thumb') and not os.path.exists(os.path.join(ROOT, a['thumb'])):
                    problems.append('%s/%s: missing thumbnail %s' % (c['id'], u['id'], a['thumb']))
    if fix and changed:
        save(head, d)
    if fix and new_decisions:
        json.dump(place, open(PLACE, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    if fix:
        print('Removed %d duplicate listing(s); %d new placement decision(s) recorded.' % (changed, new_decisions))
        _, d2 = load()   # report what is left after fixing
        sys.argv = [a for a in sys.argv if a != '--fix']
        return main()
    for p in problems:
        print('PROBLEM ' + p)
    print('%d problem(s) in the library.' % len(problems))
    if problems:
        print('Duplicate listings can be fixed with: python3 scripts/check_library.py --fix')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
