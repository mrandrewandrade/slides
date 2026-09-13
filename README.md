# Technology Class Slides

Quarto RevealJS slides for the 2026-27 school year.

The classroom slides are designed to be used with the course notes and resources at https://andrewandrade.ca/commons.

## Local workflow

Use the `master` branch in `~/Documents/slides`.

```bash
cd ~/Documents/slides
git switch master
git pull --ff-only
```

### Preview one current class

```bash
bash run.sh tej
```

Use `tej`, `tts`, or `tas`.

This previews only the current classroom deck for that course.

### Check the semester state

```bash
bash run.sh status
```

For each course this shows:

- **Current**: the one live classroom day
- **Full**: published days through Current, newest first
- **Future**: staged days after Current

### Build the complete local site

```bash
bash run.sh all
```

This regenerates the Full decks, builds Current and Full, builds the Future decks, and starts a local server at:

```text
http://localhost:4200/
```

The local site includes Current, archived days, Full slides, and Future slides.

### Publish the site

Publishing is local-first. From `master`, run:

```bash
bash publish.sh
```

This does the following:

1. pulls the latest `master`
2. builds the complete site locally into `_site`
3. commits any source or regenerated cumulative deck changes
4. pushes `master`
5. copies the exact local `_site` build to the `gh-pages` branch and pushes it

GitHub Actions builds `master` as a verification check, but it does not publish the site. The `gh-pages` branch is generated output.

For GitHub Pages, configure the repository once with:

- source: **Deploy from a branch**
- branch: **gh-pages**
- folder: **/(root)**

### Move to the next class day

When the next staged day is ready:

```bash
bash run.sh advance tej
```

Use `tej`, `tts`, `tas`, or `all`.

Advance performs the lifecycle in this order:

1. confirms that the next staged day exists
2. renders the current deck as a self-contained permanent archive HTML file
3. changes `current/<course>.qmd` to the next staged day
4. regenerates the course Full deck through the new Current day

Then inspect the result:

```bash
bash run.sh status
bash run.sh all
```

Example:

```text
Before advance
Current: Day 1
Full:    Day 1
Future:  Day 2, Day 3, ...

After advance
Archive: Day 1
Current: Day 2
Full:    Day 2, Day 1
Future:  Day 3, ...
```

`advance` archives Current before changing the pointer. If the next staged day cannot be found, promotion does not start.

## Source layout

```text
current/                         one live wrapper per course
2026-27/semester-1/period-1/
  shared/week-*/                 shared staged day sources
  tej/week-*/                    TEJ-specific staged day sources
  tts/week-*/                    TTS-specific staged day sources
  tas/week-*/                    TAS-specific staged day sources
  tej/full.qmd                   generated cumulative TEJ deck
  tts/full.qmd                   generated cumulative TTS deck
  tas/full.qmd                   generated cumulative TAS deck
archive/                         completed self-contained classroom decks
```

The day source files remain the staging pool. A day is Current, published in Full, or shown in Future according to the day referenced by `current/<course>.qmd`.

## RevealJS navigation

Slide decks use `navigation-mode: vertical`:

- `#` headings are major horizontal lesson parts.
- `##` headings are supporting vertical slides.
- Left/right moves between major parts.
- Up/down opens supporting slides.
- Space advances through the full sequence.

## License

This repository uses two licenses:

- Code, configuration, scripts, and styles are licensed under **GNU GPL v3 or later** (`GPL-3.0-or-later`).
- Slide text, lesson content, documentation, and other educational content are licensed under **Creative Commons Attribution 4.0 International** (`CC BY 4.0`).

See `LICENSE` and the files in `LICENSES/` for details.
