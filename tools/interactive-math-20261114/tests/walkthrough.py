"""Plays every "Try this" challenge of the 2026-11-14 tools the way a student would (sliders, buttons, tabs,
chips, arrow keys on draggable points) and checks that each list ends at 5 of 5, with no page errors.
Usage (repository root, static server on :8770): python3 tools/interactive-math-20261114/tests/walkthrough.py"""
import sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8770/artifacts/"


def run(pg, steps):
    for st in steps:
        k = st[0]
        if k == "slider":
            pg.evaluate("([id, v]) => { const e = document.getElementById('sl-' + id); e.value = v; e.dispatchEvent(new Event('input')); }", [st[1], st[2]])
        elif k == "click":
            pg.evaluate("t => [...document.querySelectorAll('button')].find(b => b.textContent.trim() === t).click()", st[1])
        elif k == "key":
            for _ in range(st[3]):
                pg.locator(f'[aria-label="{st[1]}"]').first.focus()
                pg.keyboard.press(st[2])
                pg.wait_for_timeout(40)
        pg.wait_for_timeout(60)


PLANS = {
    "math6-rational-number-line": [("key", "Point a", "ArrowLeft", 6), ("key", "Point a", "ArrowLeft", 3), ("key", "Point b", "ArrowRight", 4),
                                   ("key", "Point b", "ArrowLeft", 2), ("click", "Coordinate plane"), ("key", "Point P", "ArrowLeft", 6), ("key", "Point P", "ArrowDown", 4),
                                   ("key", "Point Q", "ArrowLeft", 6), ("key", "Point Q", "ArrowUp", 9)],
    "algebra2-rational-exponent-explorer": [("slider", "base-b", 8), ("slider", "numerator-m", 2), ("slider", "denominator-n", 3),
                                            ("slider", "base-b", 3), ("slider", "numerator-m", -2), ("slider", "denominator-n", 1),
                                            ("slider", "numerator-m", 1), ("slider", "denominator-n", 2), ("slider", "base-b", -8), ("slider", "denominator-n", 3),
                                            ("slider", "denominator-n", 2), ("slider", "base-b", 16), ("slider", "numerator-m", 2), ("slider", "denominator-n", 4),
                                            ("slider", "numerator-m", 1), ("slider", "denominator-n", 2)],
    "precalculus-ambiguous-case": [("slider", "side-a", 4), ("slider", "angle-A", 30), ("slider", "side-a", 5), ("slider", "side-a", 7),
                                   ("slider", "side-a", 12), ("slider", "angle-A", 120), ("slider", "side-a", 8)],
    "precalculus-matrix-transformations": [("slider", "entry-a", -1), ("slider", "entry-d", -1), ("slider", "entry-a", 2), ("slider", "entry-d", 3),
                                           ("slider", "entry-a", 1), ("slider", "entry-d", -1), ("slider", "entry-d", 0), ("slider", "entry-d", 1),
                                           ("slider", "entry-b", 2)],
    "calculus-optimization-box": [("slider", "cut-x", 2), ("click", "Show V′(x)"), ("slider", "cut-x", 5.75), ("slider", "sheet-width", 8),
                                  ("slider", "sheet-length", 15), ("slider", "cut-x", 1.75), ("slider", "sheet-width", 6), ("slider", "sheet-length", 6),
                                  ("slider", "cut-x", 1)],
    "calculus-area-volume-lab": [("slider", "slices-n", 12), ("click", "2x and x²"), ("click", "Volume: washers"), ("slider", "slices-n", 1),
                                 ("click", "√x and x/2"), ("click", "4 − x² and 0")],
    "calculus-slope-field": [("slider", "step-h", 0.25), ("slider", "step-h", 0.5), ("slider", "step-h", 0.05), ("click", "dy/dx = 0.5y(4 − y)"),
                             ("key", "Initial point", "ArrowDown", 2), ("key", "Initial point", "ArrowUp", 8), ("click", "dy/dx = −x/y"),
                             ("key", "Initial point", "ArrowRight", 6), ("key", "Initial point", "ArrowDown", 8), ("click", "dy/dx = x + y"),
                             ("key", "Initial point", "ArrowLeft", 6), ("key", "Initial point", "ArrowDown", 2)],
}

bad = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for slug, steps in PLANS.items():
        pg = b.new_page(viewport={"width": 1280, "height": 1000})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        pg.goto(BASE + slug + "/index.html", wait_until="load")
        pg.wait_for_timeout(400)
        run(pg, steps)
        pg.wait_for_timeout(300)
        found = pg.inner_text(".challenges-head span")
        ok = found.startswith("5 of 5") and not errs
        bad += not ok
        print(("PASS " if ok else "FAIL ") + slug, found, errs[:2])
        if not ok:
            print("   ", pg.eval_on_selector_all(".challenges li", "els => els.map(e => (e.classList.contains('done') ? '✓ ' : '· ') + e.innerText.slice(2, 70))"))
            print("   ", pg.inner_text(".readout")[:200].replace("\n", " / "))
        pg.close()
    b.close()
sys.exit(1 if bad else 0)
