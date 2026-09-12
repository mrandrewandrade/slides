# Future Slides Branch

This branch is the planning workspace for upcoming classroom slide days.

## Rules

- Keep `main` focused on the current classroom day and published history.
- Stage future lesson source here using its final canonical path under the appropriate school year / semester / period / shared / week folder.
- Future files are not part of the normal classroom render targets, so they do not affect last-minute preview speed.
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

## Announcement timing rules

The Quote of the Day remains the first slide.

- Red Dot/Open Red Dot observances get a standalone **Upcoming Celebration / Observance** slide on the previous instructional day and a **Today's Celebration / Observance** slide on the day itself when school is in session.
- Red Dot/Open Red Dot remains visible as the Peel scheduling designation in the slide detail, but it is not presented to students as a warning.
- Major commemorative dates get 3, 2, and 1 instructional-day reminders, plus the day-of slide when school is in session.
- Orange Shirt Day / National Day for Truth and Reconciliation and Remembrance Day are major Semester 1 dates.
- Smaller observances get one concise notice on the day itself, or on the nearest sensible instructional day when the date falls outside a regular school day.
- Student-facing operational dates such as half days, PL days, breaks, closures, and exams continue to use 3, 2, and 1 instructional-day reminders.

Instructional-day counting skips weekends, holidays, PL/PA days, breaks, and other non-school days. For a Wednesday event, the 3/2/1 reminders normally fall on Friday, Monday, and Tuesday.

## Student-facing tentative plan

Future slides are rendered in the background to a separate `/tentative/` area for students who want to anticipate what may be coming.

The tentative area is intentionally secondary to the current class slides and carries this message:

> **Tentative and subject to change.** Topics, timing, activities, assessments, and due dates may change based on class progress, school events, and student needs.

The live landing page links to this area from a collapsed **Upcoming / Tentative** section rather than mixing drafts into the confirmed current-week list.

## Semester 2 generic drafts

Semester 2 has a generated scaffold under:

```text
2026-27/semester-2/period-1/shared/week-XX/
```

The generators are:

```text
scripts/generate_semester2.py
scripts/build_tentative.py
```

It stages every regular instructional day with:

1. Quote of the Day placeholder
2. Upcoming Celebration / Observance or Today's Celebration / Observance when applicable
3. major or smaller recognition slide when applicable
4. school announcement slide(s), including 3/2/1 instructional-day countdowns and same-day notices where useful
5. Today's Lesson placeholder

The generated schedule and notice list are documented in:

```text
2026-27/semester-2/SEMESTER-2-NOTICES.md
```

When one of these days is promoted to `main`, keep its prebuilt announcement slides with the day's lesson source rather than recreating them manually.

ChatGPT can maintain this branch and promote days when requested.
