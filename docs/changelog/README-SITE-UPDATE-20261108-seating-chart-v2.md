# Site update 2026-11-08: Seating Chart Maker, version 2

Smarter seating, faster room setup, projector mode, substitute plans and backups.

## Files in this update (7)

| File | Status |
|------|--------|
| `worksheet-generator/seating-chart.html` | Replaced (now just the page; code moved into `seating/`) |
| `worksheet-generator/seating/seating.css` | New |
| `worksheet-generator/seating/seating-core.js` | New: furniture, drawing, auto-seat solver, rule checks, roster import, PDF |
| `worksheet-generator/seating/seating-app.js` | New: everything the teacher clicks |
| `worksheet-generator/seating/tests/solver-tests.cjs` | New: `node worksheet-generator/seating/tests/solver-tests.cjs [rounds]` |
| `thumbs/seating-chart.svg` | Same as version 1 (included in case version 1 was not uploaded yet) |
| `README-SITE-UPDATE-20261108-seating-chart-v2.md` | This guide |

No shared site file (`data.js`, `index.html`, `app.js`) is touched.

## How to upload

1. Unzip first. Do not upload the ZIP itself.
2. GitHub → Add file → Upload files → drag in the `worksheet-generator` and `thumbs` folders → commit to `main`.
3. If the version 1 install guide (`README-SITE-UPDATE-20261108-seating-chart.md`) is in the repo, it can be deleted; this guide replaces it.
4. If the "Seating Chart" link next to the Daily Lesson Planner was not added yet, add it now (label `Seating Chart`, href `worksheet-generator/seating-chart.html`; copy the markup of the planner link on the current `main`).

Teachers keep their saved charts: the storage key (`mkseating:v1`) is unchanged and version 1 charts are converted automatically on first load (tested).

## What's new

**Step 1, Room**
- Room size in feet (12–90 ft each way); grid squares are 1 foot.
- New furniture: lab table of 4, groups of 3, 5 and 8, round tables of 4, 6 and 8. Any desk or table: Seats −/+, One row/Two rows, Narrower/Wider. Teacher's desk resizes too.
- Several at once: drag a box around items, Shift-click, or Ctrl+A. Move them together, Turn 90° as a group, Line up (left/right/top/bottom edges, centers, middles, space evenly across or down), Copy, Delete.

**Step 2, Class**
- Import a roster file (CSV or text from a gradebook, Google Classroom or a spreadsheet). Names land in the box to check before adding. Duplicates are skipped.
- Copy the class list from another chart (with needs, tags, rules, notes).
- Select a student to set: seat needs (near the front, near the teacher's desk, near the door, near the back, away from the windows), "keep in this seat when reseating", keep apart from, works well with, tags, and a note for a substitute.
- Seating rules list with a quick "A keep apart from / works well with B" form.
- Tags (ELL, Strong in math, …) with colors.

**Step 3, Seats**
- Reseat everyone / Seat only students without a seat. Options: which seats to use when there are extra (any seat at random, front seats first, spread evenly across groups), follow rules, give seat needs, new neighbors (uses past seatings), spread tags evenly across groups. Pinned students stay put.
- "Any seat at random" picks from every seat in the room, not front to back.
- Rules check: lists any rule or need that is not met and outlines those seats in red; works for hand-placed seats too.
- Past seatings: Reseat and Clear save the current seats first (last 12 kept); Restore or delete them.
- Keyboard seating: Tab to a name or seat, Enter to pick up and place, arrow keys move between seats, Delete unseats.

**Everywhere**
- Pick a student: highlights a seat and shows the name; nobody repeats until everyone has had a turn.
- Projector: full-screen chart with larger names and the picker.
- Print and export dialog: US Letter or A4, larger names, desk numbers, tag colors, optional substitute page (teacher's notes, students to know about with seat and note, keep-apart pairs, class list with attendance check boxes). PDF is multi-page when the substitute page is on.
- All browser pop-ups replaced with built-in dialogs.
- Backup: "Back up all charts" and "Open a chart or backup file" in the Charts menu, and a reminder bar when charts have changed and no recent backup exists (first after 30 minutes of use, then every 14 days; "Remind me next week" snoozes).

## How the auto-seat works (for maintenance)

`SEAT.solve` in `seating-core.js` runs simulated annealing over seat assignments (3 restarts, about 40 ms for 30 students). Two seats are neighbors when they are at the same desk/table or their centers are under 150 units (about 4.7 ft) apart. Costs: keep apart 40 (same desk) / 25 (nearby); works well with 14 if not near, 5 if nearby but not at the same desk; seat needs by percentile rank of distance to the matching label (front/board, back, door, windows, teacher's desk), met when in the best third; repeat tablemates from past seatings (newer weigh more); tag counts per group against the even share. With no rules or options it is a plain random shuffle across all usable seats.

## Tested

- `solver-tests.cjs`: 90 checks (everyone seated once, random seats reach the back, front-first fills front rows, rules and needs met in 30/30 random classes, pins kept, fill-empty keeps seats, new neighbors under 5% repeat tablemates, balanced tags, even spread, more students than seats, roster formats, two-page PDF).
- Headless Chromium, desktop and phone: box select, line up, space evenly, seats ±, room size, roster import, rules, tags, student dialog, auto-seat, keyboard and touch seating, picker, projector, every export (PDF on A4 with the substitute page), backup and reopen, copy class list, version 1 migration. No console errors.
