"""Statistics audit #3: writes the AP Statistics (fall 2026 framework) objective descriptions into
worksheet-generator/menu/standards.js, between marker comments. Idempotent."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib
from ap2026 import LO, BEYOND, describe

P = os.path.join(lib.ROOT, 'worksheet-generator', 'menu', 'standards.js')
START, END = '  /* AP Statistics, framework effective fall 2026 (Statistics audit 2026-11-18) */', '  /* end AP Statistics 2026 */'


def main():
    s = open(P, encoding='utf-8').read()
    entries = {('APSTATS.' + k): describe('APSTATS.' + k) for k in LO}
    entries.update({('APSTATS.BEYOND.' + k): describe('APSTATS.BEYOND.' + k) for k in BEYOND})
    block = START + '\n  Object.assign(D, ' + json.dumps(entries, ensure_ascii=False, indent=4).replace('\n}', '\n  }') + ');\n' + END
    if START in s:
        s = re.sub(re.escape(START) + r'.*?' + re.escape(END), lambda m: block, s, flags=re.S)
    else:
        anchor = '  /* AP framework codes (Calculus, Statistics banks): summarize by big idea / topic outline area. */'
        assert anchor in s
        s = s.replace(anchor, block + '\n' + anchor)
    open(P, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    main()
