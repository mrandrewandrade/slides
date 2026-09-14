# Technology Class Slides

Quarto RevealJS slides for the 2026-27 school year.

The classroom slides are designed to be used with the course notes and resources at https://andrewandrade.ca/commons.

## Operating model

Each course has three states:

- **Current** is the lesson being taught next or now.
- **Full** contains completed lessons only, newest completed day first.
- **Future** contains staged material after Current.

The homepage is also newest first. The Current day appears at the top of the latest week, followed by completed days in descending order. Completed days link to their exact anchor inside the Full deck.

Example during Day 2:

```text
Week 1
Day 2 -> Current
Day 1 -> Full deck at #/day-01
```

After Day 2 is finished and the course is advanced to Day 3:

```text
Week 1
Day 3 -> Current
Day 2 -> Full deck at #/day-02
Day 1 -> Full deck at #/day-01
```

As the semester grows, the newest week appears first. Within each week, the newest day appears first.

Example later in the semester:

```text
Week 2
Day 5
Day 4
Day 3

Week 1
Day 2
Day 1
```

This is the intended lifecycle for TEJ, TTS, and TAS.

## Standard operating procedure

### 1. Work from `master`

```bash
cd ~/Documents/slides
git switch master
git pull --ff-only
```

`master` is the source branch for classroom publishing.

Do not prepare or publish classroom changes from `main`. The `main` branch is legacy and should be removed once GitHub's default branch is set to `master`.

### 2. Check the current state

```bash
bash run.sh status
```

Confirm that TEJ, TTS, and TAS show the expected Current day before editing, advancing, or publishing.

### 3. Preview locally

Preview one Current deck:

```bash
bash run.sh tej
```

Use `tej`, `tts`, or `tas`.

To build the complete local site exactly as students will navigate it:

```bash
bash run.sh all
```

Open:

```text
http://localhost:4200/
http://localhost:4200/current/tej.html
http://localhost:4200/current/tts.html
http://localhost:4200/current/tas.html
```

Before publishing, verify:

- the homepage is newest first
- Current is the top day in the latest week
- completed days point to `full.html#/day-XX`
- Full contains completed days only
- Current contains only the live day

### 4. Prepare the next day

Future lesson content stays staged in the semester source folders until it is promoted to Current.

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
6. regenerate the homepage links

The newly promoted Current day must **not** appear in Full until that day is completed and the course is advanced again.

After advancing:

```bash
bash run.sh status
bash run.sh all
```

Check the homepage and all three Current decks before publishing.

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
5. triggers `.github/workflows/render.yml`

The workflow then:

1. rebuilds the complete site from `master`
2. mirrors the exact generated `_site` output to `gh-pages`
3. uploads the same `_site` output as the GitHub Pages artifact
4. deploys that artifact to the public site

This means `master` is the source of truth and `gh-pages` is a generated mirror of the published site.

Public site:

```text
https://andrewandrade.ca/slides/
```

### 7. Verify the public site

A successful source push is not proof that the public site is correct.

After the deployment finishes, check:

```text
https://andrewandrade.ca/slides/
https://andrewandrade.ca/slides/current/tej.html
https://andrewandrade.ca/slides/current/tts.html
https://andrewandrade.ca/slides/current/tas.html
```

Confirm that:

- Current shows the expected day for each course
- the homepage lists newest days first
- completed day links open the exact day inside Full
- Full does not contain the Current day

If the source and public site disagree, check the workflow run and the generated `gh-pages` output before changing lesson content.

## Deployment rules

- `master` is the only source branch used for classroom publishing.
- `gh-pages` is generated output and should not be edited by hand.
- `main` is legacy and should not be used for classroom publishing.
- `_site/` is generated output and is not the source of truth.
- The workflow mirrors `_site` to `gh-pages` and deploys the same build through GitHub Pages.
- A successful build and a successful deployment are separate checks.
- When debugging, compare `master`, `gh-pages`, the workflow result, and the public URL.

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
