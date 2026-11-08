# Site update 2026-11-08: Seating Chart Maker

A teacher tool for building classroom seating charts. One self-contained page, no build step, no outside scripts.

## Files in this update (3, all new)

| File | What it is |
|------|------------|
| `worksheet-generator/seating-chart.html` | The tool (HTML, CSS and JavaScript in one file) |
| `thumbs/seating-chart.svg` | 720×450 thumbnail, same style as the other generator thumbs |
| `README-SITE-UPDATE-20261108-seating-chart.md` | This guide |

No existing file is replaced, so this ZIP cannot overwrite anyone's work.

## How to upload

1. Unzip first. Do **not** upload the ZIP itself to the repo root.
2. On GitHub, Add file → Upload files, and drag in the `worksheet-generator` and `thumbs` folders (not their contents loose at the root).
3. Commit to `main`.

The page then works at `https://akneller1.github.io/classroom/worksheet-generator/seating-chart.html`.

## One small manual edit: link it from the site

This update deliberately does **not** include `data.js`, `index.html` or `app.js`, because those change often and shipping a stale copy would overwrite other edits (see the 2026-10-24 incident). Make this edit on the current `main`:

- Find where the **Daily Lesson Planner** (`worksheet-generator/lesson-planner.html`) is linked in the top menu of `index.html` (or wherever `app.js` builds that menu) and add a sibling link with the same markup:
  - label: `Seating Chart`
  - href: `worksheet-generator/seating-chart.html`
- Because the path is under `worksheet-generator/`, `app.js` already opens it directly (not in the activity.html iframe), in the same tab, so Back works.
- No `data.js` entry is needed. It is a teacher tool, not a unit activity, so it should not be listed in any unit (that would also trip the "listed in exactly one unit" rule in `scripts/check_library.py`).
- If you also bump cache strings, never run a `sed` over every `.html`; only touch the file you edited.

## What the tool does

- **Step 1, Arrange the room:** 8 starting layouts (rows, pairs, groups of 4, groups of 6, double U, round tables, testing rows, empty room). Add single desks, pair desks, groups of 4 or 6, round tables and a teacher's desk. Add labels: front of room, back of room, whiteboard, projector screen, door, windows and custom text. Drag to move, drag the round handle to rotate (15° steps), Turn 90°, Copy, Delete, Edit text, Longer/Shorter. Arrow keys nudge, R rotates, Delete removes, Ctrl+D copies, Ctrl+Z / Ctrl+Y undo and redo.
- **Step 2, Seat students:** paste a class list (one per line; "Smith, Maya" becomes Maya Smith; one comma-separated line also works). Drag a name onto a seat, or click a name and then a seat (works on tablets). Dropping on a taken seat swaps the two students; dragging a seated name back to the list unseats it. Fill empty seats randomly, shuffle everyone, seat A–Z by last name, clear all seats. Names can show as full name, first name and last initial, or first name only.
- Switching layouts keeps seated students in the same reading order on the new desks.
- **Front of the room at Top/Bottom:** flips the whole chart for the teacher's view from the front; names stay upright.
- **Output:** Print (landscape, one page), PDF (US Letter landscape), PNG, SVG, a CSV class list with desk and seat, and a chart file (.json) to back up or move a chart to another computer. Show desk numbers puts the same numbers on the chart and in the CSV.
- **Several classes:** the Charts menu makes a new chart, a new class in the same room (copies desks, empty list), a duplicate, rename and delete. Everything saves automatically in the browser (`localStorage` key `mkseating:v1`); nothing is uploaded anywhere, so student names stay on the teacher's computer.

## Tested

Headless Chromium (desktop 1400×900 and phone 390×844): layouts, adding and moving items, rotation, label editing, drag-and-drop and tap seating, swap, fill buttons, undo, flip view, reload persistence, and all five downloads (PDF opens as a 792×612 page, CSV opens in Excel with UTF-8 names). No console errors.
