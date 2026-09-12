# Technology Class Slides

Quarto RevealJS slides for the 2026-27 school year.

The slides are designed to be used in conjunction with the course notes and resources at https://andrewandrade.ca/commons.

## Fast classroom workflow

The repository is optimized for last-minute classroom edits.

A normal `quarto render` builds only:

```text
index.qmd
current/tej.qmd
current/tts.qmd
current/tas.qmd
```

Finished days are archived as static, self-contained HTML files. Archived presentations keep permanent URLs but are not re-rendered every time you change today's slides.

The root page is the only student navigation page. It uses collapsible sections:

```text
/slides/
  TEJ
    Week 2 - latest
      Day 8
      Day 7
    Week 1
      Day 4
      Day 3
      Day 2
      Day 1
  TTS
    ...
  TAS
    ...
```

Inside each class, the latest week appears first and is expanded. Older weeks stay collapsed below it.

## Source structure

```text
index.qmd
current/
  tej.qmd
  tts.qmd
  tas.qmd
archive/
  2026-27/
    semester-1/
      tej/
      tts/
      tas/
2026-27/
  semester-1/
    period-1/
      shared/
        routines/
          _end-of-class.qmd
        week-01/
          _2026-09-08-day-01.qmd
```

Reusable lesson content can still live under `shared/`. The three current course decks can include the same shared fragment and then add course-specific slides when needed.

## Preview before class

For TEJ:

```bash
quarto preview current/tej.qmd
```

For TTS:

```bash
quarto preview current/tts.qmd
```

For TAS:

```bash
quarto preview current/tas.qmd
```

This previews only the deck you are editing.

## Fast build

Render one deck:

```bash
quarto render current/tej.qmd
```

Render the student index plus all three current decks:

```bash
quarto render
```

Because `_quarto.yml` has an explicit `project.render` list, archived source files and older scaffolding are not render targets.

Output is written to `_site/`.

## Archive a finished day

When a day is finished, archive that course deck once:

```bash
bash scripts/archive-current.sh tej 01 01 2026-09-08
```

Arguments are:

```text
course  week-number  day-number  YYYY-MM-DD
```

The script creates a self-contained file such as:

```text
archive/2026-27/semester-1/tej/week-01/2026-09-08-day-01.html
```

Then change that day's link in `index.qmd` from the current URL:

```text
current/tej.html
```

to its permanent archive URL:

```text
archive/2026-27/semester-1/tej/week-01/2026-09-08-day-01.html
```

After that, replace the contents of `current/tej.qmd` with the next TEJ lesson. Repeat independently for TTS and TAS.

Archived HTML is included in `_site/` as a project resource, but Quarto does not compile it again.

## Adding a new week to the index

Each class is a collapsible `<details>` section in `index.qmd`. Put the newest week first and mark it `open`. Older weeks remain collapsed.

Each day should link directly to the beginning of that day's deck. RevealJS also provides hash URLs for individual slides within a deck, so a specific slide can be linked directly when useful.

There are no separate student course pages, weekly landing pages, or cumulative semester decks in the active workflow. The root index is the navigation system.

## RevealJS navigation

Slide decks use `navigation-mode: vertical`:

- `#` headings are major horizontal lesson parts.
- `##` headings are supporting vertical slides.
- Left/right moves between major parts.
- Up/down opens supporting slides.
- Space advances through the full sequence.

## CI

GitHub Actions runs:

```bash
quarto render
```

Because the project render targets are restricted, CI tests the index and current decks rather than rebuilding the archive.

## Links

- Slides repository: https://github.com/mrandrewandrade/slides
- GitHub: https://github.com/mrandrewandrade
- Commons course notes: https://andrewandrade.ca/commons

## License

This repository uses two licenses:

- Code, configuration, scripts, and styles are licensed under **GNU GPL v3 or later** (`GPL-3.0-or-later`).
- Slide text, lesson content, documentation, and other educational content are licensed under **Creative Commons Attribution 4.0 International** (`CC BY 4.0`).

See `LICENSE` and the files in `LICENSES/` for details.
