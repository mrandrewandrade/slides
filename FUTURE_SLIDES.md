# Future Slides Branch

This branch is the planning workspace for upcoming classroom slide days.

## Rules

- Keep `main` focused on the current classroom day and published history.
- Stage future lesson source here using its final canonical path under the appropriate school year / semester / period / shared / week folder.
- Future files are not Quarto render targets, so they do not affect classroom preview speed.
- When a day is ready, promote that lesson source to `main` and update `current/tej.qmd`, `current/tts.qmd`, and `current/tas.qmd` to include it.
- Publishing `main` preserves the previously published day in the `gh-pages` archive and publishes the new current day.

## Naming

Use:

```text
_YYYY-MM-DD-day-XX.qmd
```

Example:

```text
2026-27/semester-1/period-1/shared/week-01/_2026-09-09-day-02.qmd
```

## Semester 2 generic drafts

Semester 2 has a generated scaffold under:

```text
2026-27/semester-2/period-1/shared/week-XX/
```

The generator is:

```text
scripts/generate_semester2.py
```

It stages every regular instructional day with:

1. Quote of the Day placeholder
2. Red Dot/Open Red Dot slide when applicable
3. school announcement slide(s), including 3/2/1 instructional-day countdowns and same-day notices where useful
4. Today's Lesson placeholder

The generated schedule and notice list are documented in:

```text
2026-27/semester-2/SEMESTER-2-NOTICES.md
```

When one of these days is promoted to `main`, keep its prebuilt announcement slides with the day's lesson source rather than recreating them manually.

ChatGPT can maintain this branch and promote days when requested.
