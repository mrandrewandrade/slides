# Static slide archive

Finished daily slide decks are stored here as self-contained HTML files so they keep permanent URLs without being rebuilt by Quarto.

Expected structure:

```text
archive/
  2026-27/
    semester-1/
      tej/
        week-01/
          2026-09-08-day-01.html
      tts/
      tas/
```

Use `scripts/archive-current.sh` after a daily deck is finished, then update `index.qmd` so that day links to its archived HTML file.
