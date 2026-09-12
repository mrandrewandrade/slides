# Technology Class Slides

Quarto RevealJS slide decks for the 2026-27 school year.

## Structure

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
      tts/
        index.qmd
      tas/
        index.qmd
```

The hierarchy is always **school year / semester / period / course**. Each course has its own growing semester deck, while reusable lesson material lives in `shared/`.

Within `shared/`, daily lesson fragments are grouped by instructional week. Each daily filename contains both the calendar date and instructional day number:

```text
_YYYY-MM-DD-day-XX.qmd
```

For example:

```text
week-01/_2026-09-08-day-01.qmd
week-01/_2026-09-09-day-02.qmd
week-02/_2026-09-14-day-05.qmd
```

The date makes it easy to find what was taught on a particular day. The instructional day number preserves the lesson sequence when holidays, PD days, closures, or schedule changes interrupt the calendar.

Files beginning with `_` are source fragments. Quarto ignores them as standalone render targets.

## Daily metadata

Each shared daily fragment begins with a small machine-readable HTML comment:

```html
<!--
lesson-day: 1
date: 2026-09-08
week: 1
-->
```

This keeps the metadata easy for ChatGPT or scripts to parse without placing YAML front matter inside an included document fragment.

Day 1 also displays its date on the opening slide.

## Shared daily slides

Day 1 exists once at:

```text
2026-27/semester-1/period-1/shared/week-01/_2026-09-08-day-01.qmd
```

Each course deck includes that same Day 1 file, then includes the reusable end-of-class routine from:

```text
2026-27/semester-1/period-1/shared/routines/_end-of-class.qmd
```

A course can insert its own slides between those two includes without changing the shared source.

## Add Day 2

For a shared Day 2 on September 9, 2026, create:

```text
2026-27/semester-1/period-1/shared/week-01/_2026-09-09-day-02.qmd
```

Then append these includes below Day 1 in each course `index.qmd`:

```qmd
{{< include ../shared/week-01/_2026-09-09-day-02.qmd >}}

{{< include ../shared/routines/_end-of-class.qmd >}}
```

When a new instructional week begins, create the next `week-XX/` folder and continue the instructional day numbering.

If a lesson differs by course, place the dated `_YYYY-MM-DD-day-XX.qmd` file inside that course folder, or a week subfolder within it, and include it only from that course deck.

## Add Semester 2

Create a sibling folder:

```text
2026-27/semester-2/period-1/
```

Reuse the same `shared/`, `routines/`, weekly folders, and per-course pattern. No existing paths need to move.

## Add another period

Create another period beside `period-1`, for example:

```text
2026-27/semester-1/period-2/
```

Then add its `shared/` and course folders as needed.

## RevealJS navigation

The root `_quarto.yml` uses `navigation-mode: vertical`.

- `#` headings are major horizontal lesson parts.
- `##` headings are supporting slides below that major part.
- Left/right moves between major parts.
- Up/down opens supporting/detail slides.
- Space moves through the full sequence.

Use vertical stacks only when a supporting slide naturally belongs under a main slide.

## Preview locally

Install Quarto, then from the repository root run:

```bash
quarto preview 2026-27/semester-1/period-1/tej/index.qmd
```

Render all course decks with:

```bash
quarto render
```

Rendered output is written to `_site/`.

GitHub Actions also runs `quarto render` on pushes and pull requests.

## Links

- Slides repository: https://github.com/mrandrewandrade/slides
- GitHub: https://github.com/mrandrewandrade
- Commons: https://andrewandrade.ca/commons

## License

This repository uses two licenses:

- Code, configuration, scripts, and styles are licensed under **GNU GPL v3 or later** (`GPL-3.0-or-later`).
- Slide text, lesson content, documentation, and other educational content are licensed under **Creative Commons Attribution 4.0 International** (`CC BY 4.0`).

See `LICENSE` and the files in `LICENSES/` for details.
