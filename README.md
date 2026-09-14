# Technology Class Slides

Quarto RevealJS slides for the 2026-27 school year.

The classroom slides are designed to be used with the course notes and resources at https://andrewandrade.ca/commons.

## Operating model

The site has three states for each course:

- **Current** is the lesson being taught next or now.
- **Full** contains completed lessons only, newest completed day first.
- **Future** contains staged material after Current.

The homepage lists days in normal chronological order. Completed days link to their exact day anchor inside the Full deck. The Current day appears underneath the completed days and links to `current/<course>.html`.

Example during Day 2:

```text
Homepage
Day 1 -> Full deck at #/day-01
Day 2 -> Current

Full
Day 1 only

Current
Day 2
```

After Day 2 is finished and the course is advanced to Day 3:

```text
Homepage
Day 1 -> Full deck at #/day-01
Day 2 -> Full deck at #/day-02
Day 3 -> Current

Full
Day 2
Day 1

Current
Day 3
```

This is the intended lifecycle for TEJ, TTS, and TAS.

## Standard operating procedure

### 1. Start from `master`

```bash
cd ~/Documents/slides
git switch master
git pull --ff-only
```

`master` is the source branch used for classroom publishing. Do not prepare or publish classroom changes from `main`.

### 2. Check the current state

```bash
bash run.sh status
```

Confirm that each course shows the expected Current day before editing or publishing.

### 3. Preview a course locally

```bash
bash run.sh tej
```

Use `tej`, `tts`, or `tas`.

This previews only the Current deck for that course.

To build the complete site locally:

```bash
bash run.sh all
```

The complete local site is served at:

```text
http://localhost:4200/
```

### 4. Prepare the next day

Future lesson content remains staged in the semester source folders until it is promoted to Current.

Before advancing, confirm that the next staged day exists and renders correctly.

### 5. Advance at the end of a completed day

For one course:

```bash
bash run.sh advance tej
```

For all courses together:

```bash
bash run.sh advance all
```

Advance must follow this sequence:

1. identify the next staged day
2. archive the Current day
3. move the completed Current day into Full
4. place the completed day at the front of Full
5. promote the next staged day to Current
6. regenerate Full and homepage links

The newly promoted Current day must **not** appear in Full until that day is completed and the course is advanced again.

After advancing, check:

```bash
bash run.sh status
bash run.sh all
```

Verify the homepage locally before publishing:

- completed days link to `full.html#/day-XX`
- the newest Current day links to `current/<course>.html`
- Full contains completed days only
- Current contains only the live day

### 6. Publish

From `master`:

```bash
bash publish.sh
```

`publish.sh`:

1. rebases onto the latest `master`
2. builds the complete site locally
3. commits regenerated tracked files when needed
4. pushes `master`
5. relies on the GitHub Pages workflow to deploy the site

The deployment workflow is `.github/workflows/render.yml`. It renders the site from `master` and deploys the resulting `_site` directory with GitHub Pages.

The public site is:

```text
https://andrewandrade.ca/slides/
```

### 7. Verify the public site

Do not treat a successful source push as proof that the public site is correct.

After deployment completes, check at least:

```text
https://andrewandrade.ca/slides/
https://andrewandrade.ca/slides/current/tej.html
https://andrewandrade.ca/slides/current/tts.html
https://andrewandrade.ca/slides/current/tas.html
```

Confirm that the Current decks show the expected day and that completed homepage links open the correct day inside each Full deck.

## Deployment rules

- `master` is the only branch that should deploy the classroom site.
- `main` is legacy and must not deploy GitHub Pages.
- `_site/` is generated output and is not the source of truth.
- The public site is deployed by GitHub Pages Actions, not by copying files to `gh-pages`.
- A successful build and a successful deployment are separate checks.
- When debugging a mismatch, compare the Current source on `master`, the rendered Pages deployment, and the public URL before changing lesson content.

## Source layout

```text
current/                         one live wrapper per course
2026-27/semester-1/period-1/
  shared/week-*/                 shared staged day sources
  tej/week-*/                    TEJ-specific staged day sources
  tts/week-*/                    TTS-specific staged day sources
  tas/week-*/                    TAS-specific staged day sources
  tej/full.qmd                   generated completed TEJ deck
  tts/full.qmd                   generated completed TTS deck
  tas/full.qmd                   generated completed TAS deck
archive/                         completed self-contained classroom decks
```

The day source files remain the staging pool. A day is Current, completed in Full, or shown in Future according to the Current pointer and the publishing lifecycle above.

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
