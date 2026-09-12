# Technology Class Slides

Quarto RevealJS slide decks for the 2026-27 school year.

## Structure

```text
2026-27/
  semester-1/
    period-1/
      shared/
        _day-01.qmd
        _end-of-class.qmd
      tej/
        index.qmd
      tts/
        index.qmd
      tas/
        index.qmd
```

The hierarchy is always **school year / semester / period / course**. Each course has its own growing semester deck, while reusable material lives in `shared/`.

Files beginning with `_` are source fragments. Quarto ignores them as standalone render targets.

## Shared daily slides

Day 1 exists once at:

```text
2026-27/semester-1/period-1/shared/_day-01.qmd
```

Each course deck includes that same Day 1 file, then includes the reusable `_end-of-class.qmd` routine. A course can insert its own Day 1 slides between those two includes without changing the shared source.

## Add Day 2

If Day 2 is shared by all courses, create:

```text
2026-27/semester-1/period-1/shared/_day-02.qmd
```

Then append these includes below the existing Day 1 material in each course `index.qmd`:

```qmd
{{< include ../shared/_day-02.qmd >}}

{{< include ../shared/_end-of-class.qmd >}}
```

If Day 2 differs by course, put `_day-02.qmd` inside the course folder, include it from that course deck, then include the shared end-of-class routine after it.

## Add Semester 2

Create a sibling folder:

```text
2026-27/semester-2/period-1/
```

Reuse the same `shared/` plus per-course pattern. No existing paths need to move.

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
