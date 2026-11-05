"""Helpers to write cheat-sheet content files (scripts/cheat-sheets/content/<name>.cjs) from Python data."""
import json, os
COLORS = ['purple', 'blue', 'green', 'orange', 'pink', 'teal']
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts', 'cheat-sheets', 'content')
SHEETS = []


def V(title, rows): return dict(title=title, kind='vocab', rows=rows)
def TB(title, head, rows, after=None, check=None):
    d = dict(title=title, kind='table', plain=True, head=head, rows=rows)
    if after: d['after'] = after
    if check: d['check'] = check
    return d
def EX(title, text, example, steps, answer, check):
    return dict(title=title, kind='example', text=text, example=example, steps=steps, answer=answer, check=check)
def MS(title, good, bad): return dict(title=title, kind='mistakes', good=good, bad=bad)
def L(title, items, check=None):
    d = dict(title=title, kind='list', items=items)
    if check: d['check'] = check
    return d
def W(title, rows, check=None):
    d = dict(title=title, kind='words', rows=rows)
    if check: d['check'] = check
    return d
def N(e, v): return dict(num=e, **{'is': v})
def TRUE(e): return {'true': e}


def sheet(name, course, unitNo, unitName, focus, morefocus, front, back):
    assert len(front) == 6 and len(back) == 6, name
    for i, s in enumerate(front): s['color'] = COLORS[i]
    for i, s in enumerate(back): s['color'] = COLORS[i]
    SHEETS.append(name)
    body = dict(name=name, course=course, unitNo=unitNo, unitName=unitName, focus=focus, morefocus=morefocus, front=front, back=back)
    js = ('/* ' + course + ' Unit ' + str(unitNo) + ' cheat sheet (' + unitName + '). Every worked example is checked by build.cjs. */\n'
          'module.exports = ' + json.dumps(body, ensure_ascii=False, indent=1) + ';\n')
    open(os.path.join(OUT, name + '.cjs'), 'w', encoding='utf-8').write(js)
