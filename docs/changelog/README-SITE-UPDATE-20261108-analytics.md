# Site update 2026-11-08: private visitor statistics (Umami)

A visitor counter only you can see. The numbers are in your Umami dashboard behind your login; nothing is shown on the site.

## What you will see in Umami

- **Overview:** visitors, visits, page views, bounce rate and **visit duration**
- **Pages:** which pages were viewed (home, course and unit pages, each generator, each activity opened through `activity.html?path=…`)
- **Referrers:** where visitors came from (Google, a district site, an email link, …)
- **Countries / regions, browsers, operating systems, devices**
- **Events** (click an event name to see its details):

| Event | Details | When |
|-------|---------|------|
| Open resource | title, from (the course or unit page) | A resource card, generator shortcut or task card is clicked on the home / course / unit pages |
| Browse | page (e.g. "Unit 11: Quadratic Functions and Equations, Algebra 1") | A course or unit is viewed on the home page |
| Generator action | action, tool (e.g. "Print teacher key", "Worksheet Generator · algebra1-quadratics") | Build, Rebuild, Print student copy, Print teacher key, Student/Teacher PowerPoint, Download file, Save, New problems, Play online |
| Outbound link | url | A link that leaves the site (Buy Me a Coffee, Gmail, Outlook) |
| Report a problem | item | The "Report a problem" email link on a resource card |
| Time on page | minutes (1, 5, 15, 30), page | A page has been open and visible that long |

Umami uses no cookies and collects no names or other personal information, so no cookie banner is needed. Students who open a shared game are counted as visitors too, anonymously.

## Setup (about 5 minutes)

1. Go to **https://umami.is**, choose **Umami Cloud**, and sign up. The free **Hobby** plan includes 1 website, 100,000 events a month and 6 months of history. (Each page view counts as 1 event, and so does each custom event and each detail on it. A typical teacher visit uses about 10–40, so the free plan covers a few thousand visits a month.)
2. **Add a website:** name `Mr. K's Classroom`, domain `akneller1.github.io`.
3. Open the website's **Edit → Tracking code**. Copy the `data-website-id` value (a long code like `a1b2c3d4-…`). Also check that its `src` is `https://cloud.umami.is/script.js`; if it is different, use that address in step 4 too.
4. Upload this update (below). Then on GitHub open `analytics.js`, click the pencil (Edit), paste the ID between the quotes on the line `var WEBSITE_ID = '';`, and commit. (Or send me the ID and I'll fill it in.)
5. **Stop counting yourself:** open `https://akneller1.github.io/classroom/?analytics=off` once in every browser you use (school laptop, home computer, phone). `?analytics=on` turns it back on.

Visits appear in the dashboard within a minute.

## Files in this update

- `analytics.js` (new, site root): loads Umami and records the events above. Until the Website ID is filled in, it does nothing.
- One line added before `</head>` in 31 pages: `index.html`, `activity.html`, `guide.html`, `coverage.html` and every page in `worksheet-generator/`. Example: `<script src="analytics.js?v=analytics-20261108" defer></script>` (`../analytics.js` in `worksheet-generator/`).
- `README-SITE-UPDATE-20261108-analytics.md`: this guide.

Built on `main` as of today. `index.html` and `activity.html` change often, so upload soon; if either changed on GitHub in the meantime, just add the one `analytics.js` line to the current file instead of uploading mine.

## How to upload

1. Unzip first. Do **not** upload the ZIP itself.
2. GitHub: Add file → Upload files. Drag in `analytics.js`, `index.html`, `activity.html`, `guide.html`, `coverage.html`, this README, and the `worksheet-generator` folder.
3. Commit to `main`.

## Notes

- Only the live site (`akneller1.github.io`) is counted: local copies, previews and test servers are ignored.
- Pages inside an iframe (the Vocabulary Builder embedded in the Printable Generator) are not counted twice.
- Clicks that open another page in the same tab are saved for a moment in that tab and sent from the next page, so they are not lost when the page changes.
- The individual activity pages under `artifacts/` don't load the counter themselves; opening one through the site is still counted (as a page view of `activity.html?path=…` and an "Open resource" event).
- Checked in a browser: every event above fires once with the right details, nothing loads when the ID is empty or `?analytics=off` is set, the embedded Vocabulary Builder doesn't load it twice, and none of the 31 pages shows an error.
