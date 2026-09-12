# Technology Class Slides

Quarto RevealJS slides for the 2026-27 school year.

The classroom slides are designed to be used in conjunction with the course notes and resources at https://andrewandrade.ca/commons.

## Normal use

There are only two commands you should normally need.

### Run one class locally

```bash
bash run.sh tej
```

Use exactly one course code: `tej`, `tts`, or `tas`.

`run.sh` previews only that course's current deck, so last-minute classroom edits do not trigger a project-wide rebuild.

### Publish changes

```bash
bash publish.sh
```

This safely pulls, commits local changes if needed, and pushes them to GitHub. On `main`, GitHub Actions handles the heavier publishing work in the background.

## Future slide planning

Upcoming lessons are staged on the dedicated branch:

```text
future-slides
```

Future lessons use their final canonical paths, for example:

```text
2026-27/semester-1/period-1/shared/week-01/_2026-09-09-day-02.qmd
```

They are not active render targets, so planning ahead does not slow classroom preview or normal builds.

When a planned day is ready, ChatGPT promotes it to `main` by bringing over that lesson source and updating:

```text
current/tej.qmd
current/tts.qmd
current/tas.qmd
```

There is no local promotion script to remember.

## What gets built

The active Quarto project renders only:

```text
index.qmd
current/tej.qmd
current/tts.qmd
current/tas.qmd
```

Old lesson source and future lesson source do not increase normal render time.

## Background publish and archive

When `main` is pushed, GitHub Actions does the slower housekeeping:

1. restores the previously published archive from `gh-pages`
2. rebuilds the student index
3. renders the three current course decks
4. makes a self-contained dated snapshot of each current deck
5. preserves every older snapshot
6. publishes the complete site to `gh-pages`

Publishing the same instructional day again replaces that day's snapshot with the newest version. When a new day is promoted to `main`, the previous day's published snapshot remains as the permanent historical copy.

## Student navigation

There is one student-facing `/slides/` index page.

Each class is collapsible. The newest week appears first, with older weeks underneath it. The current day links to the current deck; previous days link to their dated archive URLs.

Conceptually:

```text
/slides/
  TEJ
    Week 2
      Day 8 - current
      Day 7
    Week 1
      Day 6
      Day 5
      ...
  TTS
    ...
  TAS
    ...
```

## RevealJS navigation

Slide decks use `navigation-mode: vertical`:

- `#` headings are major horizontal lesson parts.
- `##` headings are supporting vertical slides.
- Left/right moves between major parts.
- Up/down opens supporting slides.
- Space advances through the full sequence.

## GitHub Pages

After the setup PR is merged, configure **Repository Settings > Pages** to deploy from the `gh-pages` branch at `/ (root)`.

## Links

- Slides repository: https://github.com/mrandrewandrade/slides
- GitHub: https://github.com/mrandrewandrade
- Commons course notes: https://andrewandrade.ca/commons

## License

This repository uses two licenses:

- Code, configuration, scripts, and styles are licensed under **GNU GPL v3 or later** (`GPL-3.0-or-later`).
- Slide text, lesson content, documentation, and other educational content are licensed under **Creative Commons Attribution 4.0 International** (`CC BY 4.0`).

See `LICENSE` and the files in `LICENSES/` for details.
