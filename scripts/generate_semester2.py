#!/usr/bin/env python3
"""Generate generic Semester 2 daily slide fragments for 2026-27.

This runs only on the future-slides planning branch. It intentionally does not
change current/ or publish anything. Daily drafts are generated from the
school-calendar, Red Dot/Open Red Dot dates, and classroom observance rules
recorded below.
"""

from __future__ import annotations

import calendar
import shutil
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEM = ROOT / "2026-27" / "semester-2"
SHARED = SEM / "period-1" / "shared"

# The school calendar has Semester Turnaround Day on Feb. 3, 2027 and
# Semester 2 exams beginning June 21. The regular-class draft scaffold starts
# the next weekday, Feb. 4, and ends on the last weekday before exams, June 18.
START = date(2027, 2, 4)
END = date(2027, 6, 18)

NO_CLASS = {
    date(2027, 2, 12),  # PL Day
    date(2027, 2, 15),  # Family Day
    date(2027, 3, 26),  # Good Friday
    date(2027, 3, 29),  # Easter Monday
    date(2027, 5, 24),  # Victoria Day
    *{date(2027, 3, d) for d in range(15, 20)},  # Spring Break
}

# Student-facing school dates that should be announced 3, 2, and 1
# instructional days ahead.
SCHOOL_EVENTS = [
    (date(2027, 2, 10), "Final Report Card Distribution", "Semester 1 final report cards are distributed."),
    (date(2027, 2, 12), "PL Day", "No school for students."),
    (date(2027, 2, 15), "Family Day", "No school for students."),
    (date(2027, 2, 22), "Grad Photos", "Grad photos begin February 22 and run through March 5."),
    (date(2027, 3, 12), "Half Day", "11:05 AM dismissal."),
    (date(2027, 3, 15), "Spring Break", "Spring Break begins. No regular classes March 15-19."),
    (date(2027, 3, 26), "Good Friday", "School closed."),
    (date(2027, 3, 29), "Easter Monday", "School closed."),
    (date(2027, 4, 16), "Half Day", "11:05 AM dismissal."),
    (date(2027, 5, 20), "Spring Concert", "Spring Concert is scheduled for 7:00-9:00 PM."),
    (date(2027, 5, 24), "Victoria Day", "No school for students."),
    (date(2027, 6, 21), "Semester 2 Exams", "Semester 2 exam period begins June 21 and runs through June 25."),
]

# Red Dot/Open Red Dot observances. Every one gets a standalone notice on the
# previous instructional day. If the observance itself is an instructional
# day, it also gets a day-of notice.
RED_DOT_EVENTS = {
    date(2027, 2, 6): [
        ("Red Dot", "Lunar New Year", "Buddhism", ""),
    ],
    date(2027, 3, 10): [
        ("Red Dot", "Eid-ul-Fitr", "Islam", "Date may vary by one day due to the lunar calendar."),
    ],
    date(2027, 3, 26): [
        ("Red Dot + Open Red Dot", "Khordad Sal (FC)", "Zoroastrianism", ""),
        ("Red Dot", "Good Friday", "Christianity", "Gregorian calendar."),
    ],
    date(2027, 4, 13): [
        ("Red Dot", "Theravada New Year", "Buddhism", ""),
    ],
    date(2027, 4, 14): [
        ("Red Dot", "Vaisakhi", "Sikhism", ""),
    ],
    date(2027, 4, 21): [
        ("Red Dot + Open Red Dot", "First day of Ridvan", "Bahá'í", "Bahá'í observances begin at sunset on the evening prior."),
    ],
    date(2027, 4, 30): [
        ("Red Dot", "Good Friday", "Christianity", "Julian calendar."),
    ],
    date(2027, 5, 17): [
        ("Red Dot", "Eid-ul-Adha", "Islam", "Date may vary by one day due to the lunar calendar."),
    ],
    date(2027, 6, 21): [
        ("Red Dot + Open Red Dot", "Summer Solstice", "Wicca", ""),
        ("Red Dot", "National Indigenous Peoples Day", "Indigenous Worldview", ""),
    ],
}

# Major commemorative dates get 3, 2, and 1 instructional-day reminders, plus
# a same-day slide when the date itself is a regular instructional day.
MAJOR_OBSERVANCES = [
    (
        date(2027, 6, 21),
        "National Indigenous Peoples Day",
        "A day to recognize and celebrate the histories, cultures, and contributions of First Nations, Inuit, and Métis peoples.",
    ),
]

# Smaller classroom observances get one concise notice on the event day when
# there is school, otherwise on the most sensible nearby instructional day.
SMALL_OBSERVANCES = [
    (date(2027, 2, 1), "Black History Month", "February is Black History Month."),
    (date(2027, 3, 8), "International Women's Day", "International Women's Day is observed today."),
    (date(2027, 4, 22), "Earth Day", "Earth Day is observed today."),
    (date(2027, 5, 1), "Asian Heritage Month / South Asian Heritage Month", "May marks Asian Heritage Month and South Asian Heritage Month."),
    (date(2027, 6, 1), "Pride Month", "Pride Month begins today."),
]

SAME_DAY_SCHOOL_NOTICE = {
    date(2027, 2, 10): ("Final Report Card Distribution", "Semester 1 final report cards are distributed today."),
    date(2027, 2, 22): ("Grad Photos", "Grad photos begin today and continue through March 5."),
    date(2027, 3, 12): ("Half Day", "Dismissal is at 11:05 AM today."),
    date(2027, 4, 16): ("Half Day", "Dismissal is at 11:05 AM today."),
    date(2027, 5, 20): ("Spring Concert", "Spring Concert is tonight from 7:00-9:00 PM."),
}


def instructional_dates() -> list[date]:
    dates: list[date] = []
    d = START
    while d <= END:
        if d.weekday() < 5 and d not in NO_CLASS:
            dates.append(d)
        d += timedelta(days=1)
    return dates


def week_numbers(dates: list[date]) -> dict[date, int]:
    """Number teaching weeks consecutively, skipping the all-break week."""
    mondays: list[date] = []
    for d in dates:
        monday = d - timedelta(days=d.weekday())
        if monday not in mondays:
            mondays.append(monday)
    return {monday: i + 1 for i, monday in enumerate(mondays)}


def pretty(d: date) -> str:
    return f"{calendar.day_name[d.weekday()]}, {calendar.month_name[d.month]} {d.day}, {d.year}"


def previous_instructional_days(dates: list[date], event_date: date, count: int) -> list[date]:
    return [d for d in dates if d < event_date][-count:]


def countdown_notices(dates: list[date], events):
    notices = defaultdict(list)
    for event_date, name, detail in events:
        previous = previous_instructional_days(dates, event_date, 3)
        for index, d in enumerate(previous):
            notices[d].append((3 - index, event_date, name, detail))
        if event_date in dates:
            notices[event_date].append((0, event_date, name, detail))
    return notices


def red_dot_notices(dates: list[date]):
    notices = defaultdict(list)
    for event_date, events in RED_DOT_EVENTS.items():
        previous = previous_instructional_days(dates, event_date, 1)
        if previous:
            notices[previous[-1]].append(("upcoming", event_date, events))
        if event_date in dates:
            notices[event_date].append(("today", event_date, events))
    return notices


def small_observance_notices(dates: list[date]):
    notices = defaultdict(list)
    for event_date, name, detail in SMALL_OBSERVANCES:
        if event_date in dates:
            display_date = event_date
            timing = "today"
        elif event_date < dates[0] and event_date.year == dates[0].year and event_date.month == dates[0].month:
            display_date = dates[0]
            timing = "this-month"
        else:
            previous = previous_instructional_days(dates, event_date, 1)
            if not previous:
                continue
            display_date = previous[-1]
            timing = "upcoming"
        notices[display_date].append((timing, event_date, name, detail))
    return notices


def red_dot_slide(timing: str, event_date: date, events) -> str:
    title = "Today: Red Dot / Open Red Dot" if timing == "today" else "Upcoming Red Dot / Open Red Dot"
    lines = [f"# {title}\n\n"]
    when = "Today" if timing == "today" else pretty(event_date)
    lines.append(f"**{when}**\n\n")
    for kind, name, faith, note in events:
        lines.append(f"**{name} · {faith} · {kind}**  \n")
        if note:
            lines.append(f"{note}  \n")
    lines += [
        "\n**Red Dot:** do not schedule school events during the observance.  \n",
        "**Open Red Dot:** where shown, do not schedule events on the evening prior.\n\n",
        "Students observing may be unavailable for school activities or assessments.\n",
    ]
    return "".join(lines)


def countdown_slide(title: str, notices) -> str:
    lines = [f"# {title}\n\n"]
    for count, event_date, name, detail in notices:
        if count == 0:
            label = "Today"
        else:
            unit = "instructional day" if count == 1 else "instructional days"
            label = f"{count} {unit}"
        lines += [
            f"**{label}: {name}**  \n",
            f"{calendar.day_name[event_date.weekday()]}, {calendar.month_name[event_date.month]} {event_date.day}  \n",
            f"{detail}\n\n",
        ]
    return "".join(lines)


def small_observance_slide(notices) -> str:
    lines = ["# Recognition\n\n"]
    for timing, event_date, name, detail in notices:
        if timing == "today":
            prefix = "Today"
        elif timing == "this-month":
            prefix = "This month"
        else:
            prefix = f"Coming up: {calendar.month_name[event_date.month]} {event_date.day}"
        lines += [f"**{name}**  \n", f"{prefix}. {detail}\n\n"]
    return "".join(lines)


def same_day_school_slide(d: date) -> str:
    name, detail = SAME_DAY_SCHOOL_NOTICE[d]
    return f"# Today: {name}\n\n**{detail}**\n"


def write_daily_files() -> int:
    dates = instructional_dates()
    weeks = week_numbers(dates)
    school_notices = countdown_notices(dates, SCHOOL_EVENTS)
    major_notices = countdown_notices(dates, MAJOR_OBSERVANCES)
    red_notices = red_dot_notices(dates)
    small_notices = small_observance_notices(dates)

    for path in SHARED.glob("week-*"):
        if path.is_dir():
            shutil.rmtree(path)

    for day_number, d in enumerate(dates, 1):
        monday = d - timedelta(days=d.weekday())
        week = weeks[monday]
        folder = SHARED / f"week-{week:02d}"
        folder.mkdir(parents=True, exist_ok=True)
        out = folder / f"_{d.isoformat()}-day-{day_number:02d}.qmd"

        parts = [
            "<!--\n",
            f"lesson-day: {day_number}\n",
            f"date: {d.isoformat()}\n",
            f"week: {week}\n",
            "semester: 2\n",
            "-->\n\n",
            "# Quote of the Day\n\n",
            "::: {.small-note}\n",
            f"**Semester 2 · Day {day_number} · {pretty(d)} · Week {week}**\n",
            ":::\n\n",
            "> **PLACEHOLDER QUOTE**  \n",
            "> Replace this with a quote connected to today's lesson.\n\n",
        ]

        # Red/Open Red always takes the first announcement position after the quote.
        for timing, event_date, events in red_notices.get(d, []):
            parts.append(red_dot_slide(timing, event_date, events) + "\n")

        if d in major_notices:
            parts.append(countdown_slide("Important Date", major_notices[d]) + "\n")
        if d in small_notices:
            parts.append(small_observance_slide(small_notices[d]) + "\n")
        if d in SAME_DAY_SCHOOL_NOTICE:
            parts.append(same_day_school_slide(d) + "\n")
        if d in school_notices:
            parts.append(countdown_slide("Coming Up", school_notices[d]) + "\n")

        parts += [
            "# Today's Lesson\n\n",
            "::: {.big-prompt}\n",
            "**DRAFT PLACEHOLDER**\n\n",
            "Replace this section with the lesson content for this class and day.\n",
            ":::\n",
        ]
        out.write_text("".join(parts), encoding="utf-8")

    return len(dates)


def write_routine() -> None:
    routine = SHARED / "routines" / "_end-of-class.qmd"
    routine.parent.mkdir(parents=True, exist_ok=True)
    routine.write_text(
        """# End of Class

We finish together: **wrap up, clean up, save, submit, reflect.**

## 20 Minutes Remaining

- Warning: class is beginning to wrap up.
- Finish the **current task**.
- Begin winding down.

## 15 Minutes Remaining

- Put away tools and materials.
- Clean your workspace.
- Save your work.

## 10 Minutes Remaining

- Everyone returns to their **assigned desk**.
- Upload required evidence or photos.
- Complete the reflection.

When the required reflection/evidence is complete, you may use your phone for personal time until the bell.

## Reflection

Answer briefly:

- What did I do today?
- What did I learn or notice?
- What do I need to remember for next class?
""",
        encoding="utf-8",
    )


def write_manifest(total_days: int) -> None:
    (SEM / "SEMESTER-2-NOTICES.md").write_text(
        f"""# Semester 2 Draft Slide Calendar

This planning scaffold contains **{total_days} regular instructional-day drafts** beginning Thursday, February 4, 2027, the weekday after the February 3 semester turnaround day, and running through Friday, June 18, the final weekday before Semester 2 exams begin on June 21.

The school calendar identifies the turnaround day and exam window, but does not explicitly label June 18 as the last regular class day; June 18 is used here as the last weekday before the published exam period.

## Placement and timing rules

- Slide 1 is always the Quote of the Day placeholder.
- Every Red Dot/Open Red Dot observance gets a standalone slide on the previous instructional day and, when school is in session, on the day itself.
- Major commemorative dates get 3, 2, and 1 instructional-day reminders plus a day-of slide when school is in session.
- Smaller observances get one concise slide on the day itself, or on the nearest sensible instructional day when the date is not a school day.
- Student-facing school events continue to use 3, 2, and 1 instructional-day reminders.
- Red Dot/Open Red Dot notices take the first announcement position immediately after the quote.
- Finished lesson content replaces the `Today's Lesson` placeholder as each day is planned.

For Semester 1, Orange Shirt Day / National Day for Truth and Reconciliation and Remembrance Day are designated major commemorative dates and should use the same 3, 2, 1 instructional-day plus day-of rule.

## Smaller Semester 2 observances included

- Black History Month: acknowledged on the first Semester 2 instructional day
- March 8: International Women's Day
- April 22: Earth Day
- May 1: Asian Heritage Month / South Asian Heritage Month, shown on the previous instructional day because May 1 is a Saturday
- June 1: Pride Month begins

## Major Semester 2 commemorative date included

- June 21: National Indigenous Peoples Day, with 3, 2, and 1 instructional-day reminders before the exam period begins

## Student-facing school notices included

- February 10: Final Report Card Distribution
- February 12: PL Day, no school for students
- February 15: Family Day, no school for students
- February 22-March 5: Grad Photos
- March 12: Half Day, 11:05 AM dismissal
- March 15-19: Spring Break
- March 26: Good Friday, school closed
- March 29: Easter Monday, school closed
- April 16: Half Day, 11:05 AM dismissal
- May 20: Spring Concert, 7:00-9:00 PM
- May 24: Victoria Day, no school for students
- June 21-25: Semester 2 exams

Board/committee meetings and similar non-student-facing calendar items are intentionally not inserted into classroom slides.

## Semester 2 Red Dot/Open Red Dot observances included

- February 6: Lunar New Year, Buddhism, Red Dot
- March 10: Eid-ul-Fitr, Islam, Red Dot, date may vary +/- one day
- March 26: Khordad Sal (FC), Zoroastrianism, Red Dot + Open Red Dot; Good Friday, Christianity, Red Dot
- April 13: Theravada New Year, Buddhism, Red Dot
- April 14: Vaisakhi, Sikhism, Red Dot
- April 21: First day of Ridvan, Bahá'í, Red Dot + Open Red Dot
- April 30: Good Friday, Christianity, Julian calendar, Red Dot
- May 17: Eid-ul-Adha, Islam, Red Dot, date may vary +/- one day
- June 21: Summer Solstice, Wicca, Red Dot + Open Red Dot; National Indigenous Peoples Day, Indigenous Worldview, Red Dot

## Source basis

School schedule dates are transcribed from the uploaded Port Credit / Peel 2026-27 school calendar. Red Dot/Open Red Dot dates are transcribed from the Peel District School Board 2026-27 Red Dot and Open Red Dot Days sheet. Orange Shirt Day / National Day for Truth and Reconciliation and Remembrance Day are explicitly designated as major classroom dates in the planning instructions for this slide system.
""",
        encoding="utf-8",
    )


def main() -> None:
    total = write_daily_files()
    write_routine()
    write_manifest(total)
    print(f"Generated {total} Semester 2 daily draft slide files.")


if __name__ == "__main__":
    main()
