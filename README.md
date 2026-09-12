# Technology Class Slides

Quarto RevealJS slides for the 2026-27 school year.

The classroom slides are designed to be used in conjunction with the course notes and resources at https://andrewandrade.ca/commons.

## Normal use

There are only two commands you should normally need.

### Run one class quickly

```bash
bash run.sh tej
```

Use `tej`, `tts`, or `tas`.

If you run `bash run.sh` with no argument, it gives you a simple 1/2/3 class menu.

This previews only the latest deck for that class, so it is the fastest path for last-minute classroom edits.

### Publish

```bash
bash publish.sh
```

This only handles Git locally: it safely pulls, commits any small edits, and pushes.

The heavier work happens in GitHub Actions after a push to `main`:

1. restore the previously published slide archive from `gh-pages`
2. rebuild the index from the archive plus the current decks
3. render only the current site
4. snapshot the latest TEJ, TTS, and TAS decks into permanent dated archive URLs
5. publish the complete site back to the `gh-pages` branch

Publishing during the same day simply replaces that day's archive snapshot with the newest version. When the current deck advances to the next day, the previous day's published snapshot remains in the archive automatically.

## What stays fast

The active Quarto project renders only:

```text
index.qmd
current/tej.qmd
current/tts.qmd
current/tas.qmd
```

Historical decks are already-built HTML on the `gh-pages` branch. They are copied forward during deployment, not recompiled.

The most important classroom path is therefore:

```bash
bash run.sh tej
```

That watches only `current/tej.qmd` and the files it includes.

## Student navigation

There is one student-facing `/slides/` index page.

Each class is collapsible. The latest week appears first and expanded. Older weeks remain underneath it. The latest day links to the current deck; previous days link to their permanent archived presentations.

Conceptually:

```text
/slides/
  TEJ
    Week 2 - latest
      Day 8 - latest
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

## Editing

The live class decks are:

```text
current/tej.qmd
current/tts.qmd
current/tas.qmd
```

Shared lesson material and reusable routines remain under:

```text
2026-27/semester-1/period-1/shared/
```

Andrew can make small local edits to the current files. Larger operations such as advancing the instructional day or week are intended to be handled through ChatGPT/GitHub, not additional user-facing scripts.

## RevealJS navigation

Slide decks use `navigation-mode: vertical`:

- `#` headings are major horizontal lesson parts.
- `##` headings are supporting vertical slides.
- Left/right moves between major parts.
- Up/down opens supporting slides.
- Space advances through the full sequence.

## GitHub Pages

Pull requests run a fast Quarto validation build.

Pushes to `main` publish the complete site to the `gh-pages` branch while preserving the historical HTML archive.

GitHub Pages must be configured once under **Repository Settings > Pages** to deploy from the **`gh-pages` branch, root (`/`)**.

## Links

- Slides repository: https://github.com/mrandrewandrade/slides
- GitHub: https://github.com/mrandrewandrade
- Commons course notes: https://andrewandrade.ca/commons

## License

This repository uses two licenses:

- Code, configuration, scripts, and styles are licensed under **GNU GPL v3 or later** (`GPL-3.0-or-later`).
- Slide text, lesson content, documentation, and other educational content are licensed under **Creative Commons Attribution 4.0 International** (`CC BY 4.0`).

See `LICENSE` and the files in `LICENSES/` for details.
