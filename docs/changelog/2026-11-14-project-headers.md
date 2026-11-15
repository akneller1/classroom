# 2026-11-14 — Project files use the new course names

The 21 projects for Pre-Algebra, 8th Grade Math and Precalculus Unit 7 were rebuilt from `tools/course-projects-20261105` with the updated `COURSE_NAME` and unit names in `pjlib.py`. For each project this rebuilt:
- the CP2/CP1/Honors Word, PowerPoint and PDF files;
- the teacher guide (Word and PDF);
- the hero picture;
- the thumbnail.

Headers and footers now read "Pre-Algebra", "8th Grade Math" and "Precalculus · Unit 7: Vectors, Complex Numbers & Polar Coordinates". The project content is unchanged.

Rebuild only these projects (from `tools/course-projects-20261105`):

    python3 -c "import pjlib,p_g6,p_g7,p_g8,p_pc,p_ca; pjlib.build([p for p in pjlib.PROJECTS if p['course'] in ('prealgebra7','prealgebra') or (p['course']=='precalculus' and p['unit']=='vectors')])"

Check: no Word, PowerPoint or PDF file under `artifacts/*project*` contains "Pre-Algebra (7th)" or "Pre-Algebra (8th)".
