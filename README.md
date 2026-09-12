# Technology Class Slides

Quarto RevealJS slides for the 2026-27 school year.

The classroom slides are designed to be used in conjunction with the course notes and resources at https://andrewandrade.ca/commons.

## Normal use

There are only two commands you should normally need.

### Run the slides locally

```bash
bash run.sh
```

This starts Quarto preview for the current slide site. Open the class from the main index page and leave it running while you make small edits. Quarto watches the current files and refreshes the preview.

### Publish changes

```bash
bash publish.sh
```

This:

1. pulls current Git changes while preserving small local edits
2. runs the fast Quarto build
3. commits changed slide/source files if needed
4. pushes the current branch to GitHub

Once the normal working branch is `main`, the push automatically triggers GitHub Pages deployment.

If you are on another branch, the script pushes that branch for review but does not deploy it publicly until the changes reach `main`.

## What gets built

The active Quarto project intentionally renders only:

```text
index.qmd
current/tej.qmd
current/tts.qmd
current/tas.qmd
```

Older finished presentations live as static archived HTML, so historical slides do not make the normal build slower as the semester grows.

## Student navigation

There is one student-facing `/slides/` index page.

Each class is collapsible. The newest week appears first, with older weeks underneath it. Each day links directly to that day's RevealJS presentation.

Conceptually:

```text
/slides/
  TEJ
    Week 2
      Day 8
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

The current class decks are:

```text
current/tej.qmd
current/tts.qmd
current/tas.qmd
```

Shared lesson material and reusable routines remain under:

```text
2026-27/semester-1/period-1/shared/
```

In normal use, Andrew only needs to make small edits to the current material. Larger changes such as advancing to a new instructional day, changing weeks, archiving completed slides, or restructuring navigation can be handled through ChatGPT/GitHub rather than through local scripts.

## RevealJS navigation

Slide decks use `navigation-mode: vertical`:

- `#` headings are major horizontal lesson parts.
- `##` headings are supporting vertical slides.
- Left/right moves between major parts.
- Up/down opens supporting slides.
- Space advances through the full sequence.

## GitHub Pages

The GitHub Actions workflow validates pull requests with `quarto render`.

On pushes to `main`, it also uploads `_site/` and deploys it using GitHub Pages.

GitHub Pages must be enabled once under **Repository Settings > Pages > Source > GitHub Actions**.

## Links

- Slides repository: https://github.com/mrandrewandrade/slides
- GitHub: https://github.com/mrandrewandrade
- Commons course notes: https://andrewandrade.ca/commons

## License

This repository uses two licenses:

- Code, configuration, scripts, and styles are licensed under **GNU GPL v3 or later** (`GPL-3.0-or-later`).
- Slide text, lesson content, documentation, and other educational content are licensed under **Creative Commons Attribution 4.0 International** (`CC BY 4.0`).

See `LICENSE` and the files in `LICENSES/` for details.
