# Technology Class Slides

Quarto RevealJS slides for the 2026-27 school year.

The classroom slides are designed to be used in conjunction with the course notes and resources at https://andrewandrade.ca/commons.

## Normal use

There are only two commands you should normally need.

### Run one class locally

```bash
bash run.sh tej
```

Use `tej`, `tts`, or `tas`.

This previews only that course's latest deck, so last-minute classroom edits stay fast.

To inspect the complete site, including Work in Progress views:

```bash
bash run.sh all
```

That intentionally performs a full render and is slower. It is for checking the whole slide system, not normal classroom use.

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

Future lessons use their final canonical paths and are not active classroom render targets. When a planned day is ready, ChatGPT can promote it to `main` and update the three `current/*.qmd` wrappers. There is no local promotion command to remember.

## Fast classroom build

The normal Quarto project renders only:

```text
index.qmd
current/tej.qmd
current/tts.qmd
current/tas.qmd
```

Old lesson source and future lesson source do not increase normal classroom preview time.

## Full background build

The full build uses `_quarto-full.yml` and includes the current decks plus the alternate course, week, day, and semester views listed under **Work in Progress** on the first page.

The full build runs in GitHub Actions for validation and publication. It can also be viewed locally with:

```bash
bash run.sh all
```

## Background publish and archive

When `main` is pushed, GitHub Actions:

1. restores the previously published archive from `gh-pages`
2. rebuilds the student index
3. performs the full site build
4. makes a self-contained dated snapshot of each current deck
5. preserves every older snapshot
6. publishes the complete site to `gh-pages`

Publishing the same instructional day again replaces that day's snapshot with the newest version. When a new day is promoted to `main`, the previous day's published snapshot remains as the permanent historical copy.

## Student navigation

There is one student-facing `/slides/` index page.

Each class is collapsible. The newest week appears first, with older weeks underneath it. The current day links to the current deck; previous days link to their dated archive URLs.

A separate collapsed **Work in Progress** section links directly to the alternate and cumulative slide views. Those links are clearly marked as draft material and may change before class.

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
