# Technology Class Slides

Quarto RevealJS slide decks for the 2026-27 school year.

The slides are designed to be used in conjunction with the course notes and resources at https://andrewandrade.ca/commons.

## Student navigation

The published site follows this hierarchy:

```text
/slides/
  course/
    week/
      day
```

The root `index.qmd` is the slide-site home page. Students can choose a course and week, then open a standalone daily deck.

Each course also keeps a cumulative semester deck for teacher use, review, and searching.

Example:

```text
2026-27/
  semester-1/
    period-1/
      shared/
        routines/
          _end-of-class.qmd
        week-01/
          _2026-09-08-day-01.qmd
      tej/
        index.qmd
        semester.qmd
        week-01/
          index.qmd
          day-01.qmd
      tts/
        index.qmd
        semester.qmd
        week-01/
          index.qmd
          day-01.qmd
      tas/
        index.qmd
        semester.qmd
        week-01/
          index.qmd
          day-01.qmd
```

## Shared lesson content

Reusable lesson content is written once under `shared/`.

Daily fragments are grouped by instructional week and use both the date and instructional day number:

```text
_YYYY-MM-DD-day-XX.qmd
```

Examples:

```text
week-01/_2026-09-08-day-01.qmd
week-01/_2026-09-09-day-02.qmd
week-02/_2026-09-14-day-05.qmd
```

The date makes it easy to find what was taught on a particular calendar day. The instructional day number keeps the lesson sequence stable when holidays, PD days, closures, or schedule changes create gaps.

Files beginning with `_` are source fragments, so Quarto does not render them as standalone pages.

## Daily metadata

Each shared daily fragment starts with a machine-readable HTML comment:

```html
<!--
lesson-day: 1
date: 2026-09-08
week: 1
-->
```

This keeps the metadata easy for scripts or ChatGPT to parse without putting YAML front matter inside an included fragment.

## Daily decks

Each course gets a standalone wrapper for each day. For example, TEJ Day 1 is:

```text
2026-27/semester-1/period-1/tej/week-01/day-01.qmd
```

It includes the shared daily lesson, allows course-specific slides to be inserted, then includes the reusable end-of-class routine.

Daily decks end with navigation back to the week and course. As additional days are added, include previous and next day links as well:

```text
← Day 1 | Week 1 | Day 3 →
```

Do not duplicate the shared lesson content in the course wrappers.

## Weekly pages

Each course has a `week-XX/index.qmd` page listing the daily decks for that week.

This is the normal student entry point for reviewing what happened during a particular week.

## Semester decks

Each course has `semester.qmd`, which grows through the semester by including the same daily fragments used by the standalone daily decks.

The semester deck is secondary navigation. Students normally use Home → Course → Week → Day.

## Add Day 2

For a shared Day 2 on September 9, 2026:

1. Create `shared/week-01/_2026-09-09-day-02.qmd`.
2. Create `tej/week-01/day-02.qmd`, `tts/week-01/day-02.qmd`, and `tas/week-01/day-02.qmd` wrappers as needed.
3. Add Day 2 to each course Week 1 page.
4. Append the Day 2 include and end-of-class routine to each relevant `semester.qmd`.
5. Add previous/week/next navigation to the daily wrappers.

If a lesson diverges by course, put the course-specific material in that course's daily wrapper or in a course-specific fragment rather than changing the shared lesson for everyone.

## RevealJS navigation

The root `_quarto.yml` uses `navigation-mode: vertical` for slide decks.

- `#` headings are major horizontal lesson parts.
- `##` headings are supporting slides below that major part.
- Left/right moves between major parts.
- Up/down opens supporting/detail slides.
- Space moves through the full sequence.

Course, week, and site home pages explicitly render as normal HTML pages rather than RevealJS decks.

## Preview locally

Preview the slide-site home page:

```bash
quarto preview index.qmd
```

Preview a daily deck:

```bash
quarto preview 2026-27/semester-1/period-1/tej/week-01/day-01.qmd
```

Preview the cumulative TEJ semester deck:

```bash
quarto preview 2026-27/semester-1/period-1/tej/semester.qmd
```

Render everything:

```bash
quarto render
```

Rendered output is written to `_site/`. GitHub Actions also runs `quarto render` on pushes and pull requests.

## Links

- Slides repository: https://github.com/mrandrewandrade/slides
- GitHub: https://github.com/mrandrewandrade
- Commons course notes: https://andrewandrade.ca/commons

## License

This repository uses two licenses:

- Code, configuration, scripts, and styles are licensed under **GNU GPL v3 or later** (`GPL-3.0-or-later`).
- Slide text, lesson content, documentation, and other educational content are licensed under **Creative Commons Attribution 4.0 International** (`CC BY 4.0`).

See `LICENSE` and the files in `LICENSES/` for details.
