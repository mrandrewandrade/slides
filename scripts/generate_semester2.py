#!/usr/bin/env python3
"""Generate generic Semester 2 daily slide fragments for 2026-27.

This runs only on the future-slides planning branch. It intentionally does not
change current/ or publish anything. Daily drafts are generated from the
school-calendar and Red Dot/Open Red Dot dates recorded below.
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

# Schedule-changing dates from the 2026-27 school calendar.
NO_CLASS = {
    date(2027, 2, 12),  # PL Day
    date(2027, 2, 15),  # Family Day
    date(2027, 3, 26),  # Good Friday
    date(2027, 3, 29),  # Easter Monday
    date(2027, 5, 24),  # Victoria Day
    *{date(2027, 3, d) for d in range(15, 20)},  # Spring Break
}

SCHOOL_EVENTS = [
    (date(2027, 2, 12), "PL Day", "No school for students."),
    (date(2027, 2, 15), "Family Day", "No school for students."),
    (date(2027, 3, 12), "Half Day", "11:05 AM dismissal."),
    (date(2027, 3, 15), "Spring Break", "Spring Break begins. No regular classes March 15-19."),
    (date(2027, 3, 26), "Good Friday", "School closed."),
    (date(2027, 3, 29), "Easter Monday", "School closed."),
    (date(2027, 4, 16), "Half Day", "11:05 AM dismissal."),
    (date(2027, 5, 24), "Victoria Day", "No school for students."),
    (date(2027, 6, 21), "Semester 2 Exams", "Semester 2 exam period begins June 21 and runs through June 25."),
]

# Red Dot/Open Red Dot dates that occur on regular instructional days.
# Non-instructional Red Dot dates are documented in the generated manifest.
RED_DOT = {
    date(2027, 3, 10): ("Red Dot", "Eid-ul-Fitr", "Islam", "Date may vary by one day due to the lunar calendar."),
    date(2027, 4, 13): ("Red Dot", "Theravada New Year", "Buddhism", ""),
    date(2027, 4, 14): ("Red Dot", "Vaisakhi", "Sikhism", ""),
    date(2027, 4, 21): ("Red Dot + Open Red Dot", "First day of Ridvan", "Bahá'í", "Bahá'í observances begin at sunset on the evening prior."),
    date(2027, 4, 30): ("Red Dot", "Good Friday (Julian calendar)", "Christianity", ""),
    date(2027, 5, 17): ("Red Dot", "Eid-ul-Adha", "Islam", "Date may vary by one day due to the lunar calendar."),
}

SAME_DAY_SCHOOL_NOTICE = {
    date(2027, 3, 12): ("Half Day", "Dismissal is at 11:05 AM today."),
    date(2027, 4, 16): ("Half Day", "Dismissal is at 11:05 AM today."),
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


def countdowns(dates: list[date]):
    notices = defaultdict(list)
    for event_date, name, detail in SCHOOL_EVENTS:
        previous = [d for d in dates if d < event_date][-3:]
        for index, d in enumerate(previous):
            notices[d].append((3 - index, event_date, name, detail))
    return notices


def red_dot_slide(d: date) -> str:
    kind, name, faith, note = RED_DOT[d]
    lines = [
        f"# {kind}\n\n",
        f"**{name} · {faith}**\n\n",
        f"Today is identified by the Peel District School Board as a **{kind}** day.\n\n",
    ]
    if "Open" in kind:
        lines += [
            "- **Red Dot:** do not schedule school events during the day.\n",
            "- **Open Red Dot:** do not schedule school events on the evening prior.\n",
        ]
    else:
        lines += [
            "- Do not schedule school events on this day.\n",
            "- Be mindful that students observing may be unavailable for school activities or assessments.\n",
        ]
    if note:
        lines.append(f"\n*{note}*\n")
    return "".join(lines)


def school_notice_slide(d: date, notices) -> str:
    lines = ["# Coming Up\n\n"]
    for count, event_date, name, detail in notices:
        unit = "instructional day" if count == 1 else "instructional days"
        lines += [
            f"**{count} {unit}: {name}**  \n",
            f"{calendar.day_name[event_date.weekday()]}, {calendar.month_name[event_date.month]} {event_date.day}  \n",
            f"{detail}\n\n",
        ]
    return "".join(lines)


def same_day_school_slide(d: date) -> str:
    name, detail = SAME_DAY_SCHOOL_NOTICE[d]
    return f"# Today: {name}\n\n**{detail}**\n"


def write_daily_files() -> int:
    dates = instructional_dates()
    weeks = week_numbers(dates)
    notices = countdowns(dates)

    # Regenerate only Semester 2 weekly draft folders.
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

        # Red/Open Red notices take precedence as the immediate slide after
        # the opening quote. School notices follow when both occur.
        if d in RED_DOT:
            parts.append(red_dot_slide(d) + "\n")
        if d in SAME_DAY_SCHOOL_NOTICE:
            parts.append(same_day_school_slide(d) + "\n")
        if d in notices:
            parts.append(school_notice_slide(d, notices[d]) + "\n")

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

## Placement rules

- Slide 1 is always the Quote of the Day placeholder.
- On a Red Dot/Open Red Dot instructional day, that notice is a standalone slide immediately after the quote.
- School schedule notices follow the quote, or follow the Red Dot/Open Red Dot notice when both occur.
- Schedule-changing school events are announced 3, 2, and 1 **instructional days** in advance.
- Half days also get a same-day notice.
- Finished lesson content replaces the `Today's Lesson` placeholder as each day is planned.

## School schedule notices included

- February 12: PL Day, no school for students
- February 15: Family Day, no school for students
- March 12: Half Day, 11:05 AM dismissal
- March 15-19: Spring Break
- March 26: Good Friday, school closed
- March 29: Easter Monday, school closed
- April 16: Half Day, 11:05 AM dismissal
- May 24: Victoria Day, no school for students
- June 21-25: Semester 2 exams

## Red Dot / Open Red Dot regular-class dates included

- March 10: Eid-ul-Fitr, Islam, Red Dot, date may vary +/- one day
- April 13: Theravada New Year, Buddhism, Red Dot
- April 14: Vaisakhi, Sikhism, Red Dot
- April 21: First day of Ridvan, Bahá'í, Red Dot + Open Red Dot
- April 30: Good Friday (Julian calendar), Christianity, Red Dot
- May 17: Eid-ul-Adha, Islam, Red Dot, date may vary +/- one day

## Other Semester 2 Red Dot/Open Red Dot dates

These do not get a regular-class draft slide because they fall on a weekend, school closure, or the exam period:

- February 6: Lunar New Year, Buddhism, Red Dot
- March 26: Khordad Sal (FC), Zoroastrianism, Red Dot + Open Red Dot; Good Friday, Christianity, Red Dot; school is closed
- June 21: Summer Solstice, Wicca, Red Dot + Open Red Dot; National Indigenous Peoples Day, Indigenous Worldview, Red Dot; exam period begins

## Source basis

Dates are transcribed from the uploaded Port Credit / Peel 2026-27 school calendar ICS and the Peel District School Board 2026-27 Red Dot and Open Red Dot Days sheet. Future changes to official dates should be reflected here and the generator rerun.
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
