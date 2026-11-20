#!/usr/bin/env node
// Whole-site audit 2 #1 (2026-11-20): writes worksheet-generator/planner/calendar.js into the assembled site, so the Lesson
// Planner numbers its days exactly as each course's pacing guide does (180 days, with the same practice, flex, review
// and exam days). Runs at deploy after the elementary courses are integrated. Usage: node scripts/build-planner-calendar.mjs [_site]
import fs from "node:fs";
import path from "node:path";
import { plannerCalendar, plannerCalendarCourses } from "./geo-planning.mjs";

const SITE = path.resolve(process.argv[2] || "_site");
const out = {}, report = [];
for (const course of plannerCalendarCourses) {
  const cal = plannerCalendar(course, SITE);
  if (!cal) { report.push(course + ": no calendar"); continue; }
  out[course] = cal;
  report.push(`${course} ${cal.days.length}`);
}
const file = path.join(SITE, "worksheet-generator/planner/calendar.js");
fs.writeFileSync(file, "/* Built at deploy from the pacing guides (whole-site audit 2 #1). */\nwindow.MKPLAN_CALENDAR = " + JSON.stringify(out) + ";\n");
console.log("Planner calendar: " + report.join(", "));
const short = Object.entries(out).filter(([, c]) => c.days.length < 170);
if (short.length) { console.error("Calendars shorter than a school year: " + short.map(([k, c]) => k + " " + c.days.length).join(", ")); process.exit(1); }
