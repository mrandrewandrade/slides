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

Do not move daily slides here by hand. Use the semester flow command:

```bash
bash run.sh advance tej
```

That command first renders and stores the current deck in this archive, then promotes the next staged day to `current/` and regenerates the course's `full.qmd` deck. Use `bash run.sh status` to inspect Current, Full, and Future before or after a promotion.
