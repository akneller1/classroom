# Mr. K's Classroom

A static website: no server and no build step. Open `index.html` in a browser to preview it
(an internet connection is needed for the fonts).

## Add an activity
1. Make a folder under `artifacts/` (for example `artifacts/my-activity/`) and save the activity's HTML file inside it as `index.html`.
2. Optional: add a preview picture at `thumbs/my-activity.jpg`, about 720 x 450 pixels.
3. Open `data.js` and add an entry to the right unit's `artifacts` list. The comment at the top of `data.js` lists every field.

        {
          title: "My Activity",
          path: "artifacts/my-activity/index.html",
          thumb: "thumbs/my-activity.jpg",
          description: "One or two sentences about what students do.",
          type: "Game",
          level: ["CP", "Honors"],
          topics: ["Slope", "Graphing"],
          added: "2026-11-01"
        }

List each activity in **one** unit only, and give it a title no other activity in the course uses.
An activity that covers two units goes in the unit it is mainly about; an even mix goes in the later unit.
`python3 scripts/check_library.py` reports duplicates, repeated titles and missing files, and
`python3 scripts/check_library.py --fix` removes duplicate listings using the decisions in
`scripts/library-placement.json`. The same check runs on GitHub after every change to `data.js`
(the "Library check" action) and at the start of the menu generator tests.
A unit that has the Menu Assessment Generator does not also list a fixed assessment-menu PDF, and every
Algebra flashcard deck has an Easy / Medium / Hard level menu (`python3 scripts/flashcard_levels.py <deck>/index.html`
adds it to a hand-made deck); the check reports both.

Rename, reorder, add, or remove units in `data.js`, too. Units with no activities show as "Coming soon".
Course colors are "blue", "orange", "green", or "purple". Type and level filters appear on their own
once a unit has activities with different values.

## Put it online (free)
- **Netlify Drop:** drag this whole folder onto https://app.netlify.com/drop.
- **GitHub Pages:** create a repository, upload everything in this folder, then turn on Pages in the repository settings.

## Good to know
- Each activity is a copy. Changing the original in Claude does not change the copy in this folder.
- Saved activities (the Save button) are stored in each visitor's own browser.
