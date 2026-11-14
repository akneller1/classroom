# Site update f — Teacher Guide

This update adds two files. Unzip it at the repository root.

| File | Change |
| --- | --- |
| `guide.html` | **New.** The Teacher Guide page. |
| `feedback.js` | One block added at the end. The existing feedback code is unchanged. |

`index.html`, `app.js` and `styles.css` are not touched, so your earlier changes (such as the hidden games) stay as they are.

## What the guide covers

It's a short page with collapsible questions:

- **Quick start:** course → unit → create or play.
- **Sharing with students:**
  - how Copy student link works, including the skill picker and the Assessment Readiness Check setup
  - which activities have a student link
  - a clear note that a student link is a focused view, not a password
- **Which game when:** a table of whole-class projected games, small-group games and individual review games, and which ones have student links.
- **Making resources:** the options all generators share (level, skills, versions, student copy and key), plus the Lesson Plan, Worksheet, Activity and Assessment options.
- **Finding things:** search, unit navigation, Browse Activities filters, Saved.
- **FAQ:** no accounts, what's saved in the browser, printing, reporting mistakes, browsers.

It has a "Print this guide" button that prints every section. It follows light and dark mode and fits phones.

## Where teachers find it

The header is unchanged. The links are added by the new block in `feedback.js`:

- **Footer:** a "Teacher guide" link next to "Feedback or report an issue".
- **Home page:** "New here? Read the teacher guide." is added to the end of the line under "More learning. Less planning."

Browsers may keep the old `feedback.js` for a few minutes after you upload (GitHub Pages caches for about 10 minutes).
