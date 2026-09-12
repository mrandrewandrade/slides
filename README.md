# Technology Class Slides

Quarto RevealJS slides for the 2026-27 school year.

The slides are designed to be used in conjunction with the course notes and resources at https://andrewandrade.ca/commons.

## The normal commands

You should only need these four scripts during normal use.

### 1. Preview one class while editing

```bash
bash scripts/preview.sh tej
```

Use `tej`, `tts`, or `tas`.

This is the normal before-class workflow. It previews only that current deck and refreshes as you edit.

### 2. Build

Build one class:

```bash
bash scripts/build.sh tej
```

Build the student index and all three current decks:

```bash
bash scripts/build.sh
```

The full current-site build does not rebuild historical archived slides.

### 3. Archive the finished day

```bash
bash scripts/archive.sh
```

This archives the current TEJ, TTS, and TAS decks as self-contained HTML files with permanent URLs. It automatically reads the week, instructional day, and date from the current decks and refreshes `index.qmd`.

Example archive path:

```text
archive/2026-27/semester-1/tej/week-01/2026-09-08-day-01.html
```

Archived decks are copied into the published site but are not recompiled during normal builds.

### 4. Start the next day

After archiving the current day:

```bash
bash scripts/new-day.sh 2 2026-09-09 1
```

Arguments are:

```text
day-number  YYYY-MM-DD  week-number
```

The script:

- checks that the current decks were archived first
- creates the next shared lesson file
- points TEJ, TTS, and TAS at the new lesson
- leaves a place for course-specific slides
- refreshes the collapsible student index

Then edit the new shared lesson file printed by the script.

## Typical daily workflow

```bash
# Before class
bash scripts/preview.sh tej

# Optional final check
bash scripts/build.sh tej

# At the end of the instructional day
bash scripts/archive.sh

# Prepare tomorrow
bash scripts/new-day.sh 2 2026-09-09 1
```

If the three courses later diverge, the current course wrappers can still contain course-specific slides while sharing common material where appropriate.

## Student navigation

There is one student-facing `index.qmd` page. Each class is collapsible. Within each class, the latest week appears first and expanded, while older weeks remain collapsed underneath it.

The index is generated from the current decks and files under `archive/`, so archived days automatically remain available.

Conceptually:

```text
/slides/
  TEJ
    Week 2 - latest
      Day 8 - current
      Day 7
      Day 6
    Week 1
      Day 5
      Day 4
      Day 3
      Day 2
      Day 1
  TTS
    ...
  TAS
    ...
```

Each day links directly to the beginning of that day's RevealJS deck.

## Fast render model

A normal full build renders only:

```text
index.qmd
current/tej.qmd
current/tts.qmd
current/tas.qmd
```

The historical archive is static HTML, so the build should stay roughly the same size as the semester grows.

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
scripts/
  preview.sh
  build.sh
  archive.sh
  new-day.sh
  slides.sh
  archive-current.sh
```

`slides.sh` and `archive-current.sh` contain the underlying logic. In normal use, use the four short wrapper scripts above.

## RevealJS navigation

Slide decks use `navigation-mode: vertical`:

- `#` headings are major horizontal lesson parts.
- `##` headings are supporting vertical slides.
- Left/right moves between major parts.
- Up/down opens supporting slides.
- Space advances through the full sequence.

## CI

GitHub Actions tests the same fast current-site build instead of recompiling the historical archive.

## Links

- Slides repository: https://github.com/mrandrewandrade/slides
- GitHub: https://github.com/mrandrewandrade
- Commons course notes: https://andrewandrade.ca/commons

## License

This repository uses two licenses:

- Code, configuration, scripts, and styles are licensed under **GNU GPL v3 or later** (`GPL-3.0-or-later`).
- Slide text, lesson content, documentation, and other educational content are licensed under **Creative Commons Attribution 4.0 International** (`CC BY 4.0`).

See `LICENSE` and the files in `LICENSES/` for details.
