# Future Slides Branch

This branch is the planning workspace for upcoming classroom slide days.

## Rules

- Keep `main` focused on the current classroom day and published history.
- Stage future lesson source here using its final canonical path under `2026-27/semester-1/period-1/shared/week-XX/`.
- Future files are not Quarto render targets, so they do not affect classroom preview speed.
- When a day is ready, promote that lesson source to `main` and update `current/tej.qmd`, `current/tts.qmd`, and `current/tas.qmd` to include it.
- Publishing `main` snapshots the newly current day and preserves the previously published day in the `gh-pages` archive.

## Naming

Use:

```text
_YYYY-MM-DD-day-XX.qmd
```

Example:

```text
2026-27/semester-1/period-1/shared/week-01/_2026-09-09-day-02.qmd
```

ChatGPT can maintain this branch and promote days when requested.
