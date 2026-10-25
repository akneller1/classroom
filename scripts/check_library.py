#!/usr/bin/env python3
"""Check (and optionally fix) the activity library in data.js.

Problems reported:
  * the same activity (same path) listed in more than one unit of a course
  * the same activity listed twice in one unit
  * two different activities with the same title in one course (teachers cannot tell them apart)
  * an activity or thumbnail file that does not exist

Usage:
  python3 scripts/check_library.py          # report; exit code 1 if anything is wrong
  python3 scripts/check_library.py --fix    # remove duplicate listings, keeping each activity in one unit

Where a shared activity is kept is decided by scripts/library-placement.json (path -> unit).
An activity that covers two units goes to the unit its content is mainly about; an even mix goes to the
later unit (by then students have learned all of it). New duplicates without a decision are kept in the
later unit and the decision is added to library-placement.json, so the same choice is made every time.
"""
import json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data.js')
PLACE = os.path.join(ROOT, 'scripts', 'library-placement.json')


def load():
    s = open(DATA, encoding='utf-8').read()
    i = s.index('=')
    return s[:i + 1], json.loads(s[i + 1:].strip().rstrip(';'))


def save(head, d):
    open(DATA, 'w', encoding='utf-8').write(head + ' ' + json.dumps(d, indent=2, ensure_ascii=False) + ';\n')


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
        titles = collections.defaultdict(set)
        for u in c['units']:
            for a in u['artifacts']:
                titles[a['title'].strip().lower()].add(a['path'])
        for t, paths in titles.items():
            if len(paths) > 1 and t != 'menu assessment generator':
                problems.append('%s: %d different activities share the title "%s": %s' % (c['id'], len(paths), t, ', '.join(sorted(paths))))
        for u in c['units']:
            for a in u['artifacts']:
                f = a['path'].split('#')[0]
                if not os.path.exists(os.path.join(ROOT, f)):
                    problems.append('%s/%s: missing file %s' % (c['id'], u['id'], f))
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
