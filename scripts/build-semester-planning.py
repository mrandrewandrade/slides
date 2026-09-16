#!/usr/bin/env python3
"""Build calendar-driven semester planning decks for the WIP site."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEM1 = ROOT / "2026-27" / "semester-1" / "period-1"
SHARED = SEM1 / "shared"
ROUTINE = SHARED / "routines" / "_end-of-class.qmd"
PLAN = ROOT / "planning" / "2026-27-student-slide-calendar.tsv"
REQUIRED_ANNOUNCEMENTS = ROOT / "planning" / "2026-27-required-announcements.tsv"
EXAMS = ROOT / "planning" / "2026-27-exam-days.tsv"
COURSES = ("tej", "tts", "tas")
DAY_RE = re.compile(r"^_?(\d{4}-\d{2}-\d{2})-day-(\d{2})\.qmd$")
CURRENT_RE = re.compile(r"_([0-9]{4}-[0-9]{2}-[0-9]{2})-day-[0-9]{2}\.qmd")
SUPERSEDED_ANNOUNCEMENT_MARKERS = (
    "Fire Drill",
    "Lockdown",
    "Bomb Threat",
    "**Reporting cycle:**",
    "**Submission cutoff for this reporting cycle:**",
    "**Reporting deadline today:**",
)


@dataclass(frozen=True)
class PlanDay:
    date: str
    semester: str
    announcements: tuple[str, ...]


@dataclass(frozen=True)
class ExamDay:
    date: str
    semester: str
    label: str


def pretty_date(iso_date: str) -> str:
    value = datetime.strptime(iso_date, "%Y-%m-%d")
    return f"{value.strftime('%A, %B')} {value.day}, {value.year}"


def parse_announcement_file(path: Path) -> list[PlanDay]:
    days: list[PlanDay] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw or raw.startswith("#"):
            continue
        fields = raw.split("\t", 2)
        if len(fields) == 2:
            date, semester = fields
            raw_announcements = ""
        elif len(fields) == 3:
            date, semester, raw_announcements = fields
        else:
            raise RuntimeError(f"Invalid planning row in {path}: {raw}")
        announcements = tuple(
            item.strip() for item in raw_announcements.split(" || ") if item.strip()
        )
        days.append(PlanDay(date, semester, announcements))
    return days


def load_plan() -> list[PlanDay]:
    return parse_announcement_file(PLAN)


def load_required_announcements() -> dict[tuple[str, str], tuple[str, ...]]:
    required: dict[tuple[str, str], tuple[str, ...]] = {}
    for day in parse_announcement_file(REQUIRED_ANNOUNCEMENTS):
        key = (day.semester, day.date)
        required[key] = required.get(key, ()) + day.announcements
    return required


def load_exams() -> list[ExamDay]:
    days: list[ExamDay] = []
    for raw in EXAMS.read_text(encoding="utf-8").splitlines():
        if not raw or raw.startswith("#"):
            continue
        date, semester, label = raw.split("\t", 2)
        days.append(ExamDay(date, semester, label))
    return days


def current_date(course: str) -> str:
    text = (ROOT / "current" / f"{course}.qmd").read_text(encoding="utf-8")
    match = CURRENT_RE.search(text)
    if not match:
        raise RuntimeError(f"Could not determine the current date for {course.upper()}.")
    return match.group(1)


def staged_days(course: str) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for base in (SHARED, SEM1 / course):
        if not base.exists():
            continue
        for path in sorted(base.glob("week-*/*.qmd")):
            match = DAY_RE.match(path.name)
            if match:
                found[match.group(1)] = path
    return found


def reveal_header(course_label: str) -> str:
    return f'''---
course: "{course_label}"
format:
  revealjs:
    theme: default
    css: styles.css
    slide-number: true
    progress: true
    transition: none
    navigation-mode: vertical
    controls: auto
---

'''


def remove_superseded_announcements(
    announcements: tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(
        item
        for item in announcements
        if not any(marker in item for marker in SUPERSEDED_ANNOUNCEMENT_MARKERS)
    )


def merged_plan(
    plan: list[PlanDay],
    required: dict[tuple[str, str], tuple[str, ...]],
    semester: str,
) -> dict[str, PlanDay]:
    merged: dict[str, PlanDay] = {}

    for day in plan:
        if day.semester != semester:
            continue
        cleaned = remove_superseded_announcements(day.announcements)
        additions = required.get((semester, day.date), ())
        merged[day.date] = PlanDay(day.date, semester, cleaned + additions)

    for (required_semester, date), announcements in required.items():
        if required_semester != semester or date in merged:
            continue
        merged[date] = PlanDay(date, semester, announcements)

    return merged


def announcement_text(announcements: tuple[str, ...]) -> str:
    if not announcements:
        return "[No calendar announcements.]"
    return "\n".join(f"- {item}" for item in announcements)


def placeholder_day(day: PlanDay, lesson_label: str) -> str:
    date_label = pretty_date(day.date)
    return f'''# Quote

{date_label}

[QUOTE]

# Announcements {{.announcements-slide}}

{date_label}

{announcement_text(day.announcements)}

# {lesson_label} - Lesson

{date_label}

[{lesson_label.upper()} LESSON]

'''


def exam_day(day: ExamDay, planned_day: PlanDay | None = None) -> str:
    date_label = pretty_date(day.date)
    announcements = (f"**Exam day:** {day.label}.",)
    if planned_day is not None:
        announcements += planned_day.announcements
    return f'''# Quote

{date_label}

[QUOTE]

# Announcements {{.announcements-slide}}

{date_label}

{announcement_text(announcements)}

# Exam Day

{date_label}

[EXAM SCHEDULE / COURSE-SPECIFIC DETAILS]

'''


def semester1_document(
    course: str,
    plan: list[PlanDay],
    required: dict[tuple[str, str], tuple[str, ...]],
    exams: list[ExamDay],
) -> str:
    label = course.upper()
    now = current_date(course)
    staged = staged_days(course)
    planned = {
        date: day
        for date, day in merged_plan(plan, required, "semester-1").items()
        if date > now
    }
    exam_map = {
        day.date: day
        for day in exams
        if day.semester == "semester-1" and day.date > now
    }
    dates = sorted(
        set(planned)
        | set(exam_map)
        | {date for date in staged if date > now}
    )

    pieces = [reveal_header(label)]
    pieces.append("# Future Slide Deck {.course-day-slide}\n\n")
    pieces.append(
        f"Semester 1 planning after **{pretty_date(now)}**. "
        "Calendar placeholders remain work in progress until replaced by lesson slides.\n\n"
    )

    for date in dates:
        if date in exam_map:
            pieces.append(exam_day(exam_map[date], planned.get(date)))
            continue

        staged_path = staged.get(date)
        if staged_path is not None:
            relative = staged_path.relative_to(ROOT).as_posix()
            pieces.append(f"{{{{< include {relative} >}}}}\n\n")
            pieces.append(
                f"{{{{< include {ROUTINE.relative_to(ROOT).as_posix()} >}}}}\n\n"
            )
        else:
            pieces.append(placeholder_day(planned[date], label))

    return "".join(pieces).rstrip() + "\n"


def semester2_document(
    plan: list[PlanDay],
    required: dict[tuple[str, str], tuple[str, ...]],
    exams: list[ExamDay],
) -> str:
    pieces = [reveal_header("Semester 2")]
    pieces.append("# Semester 2 Planning {.course-day-slide}\n\n")
    pieces.append(
        "Generic course deck. Semester 2 timetable periods are intentionally not assumed.\n\n"
    )

    planned = merged_plan(plan, required, "semester-2")
    exam_map = {day.date: day for day in exams if day.semester == "semester-2"}

    for date in sorted(set(planned) | set(exam_map)):
        if date in exam_map:
            pieces.append(exam_day(exam_map[date], planned.get(date)))
        else:
            pieces.append(placeholder_day(planned[date], "Course"))

    return "".join(pieces).rstrip() + "\n"


def write_document(name: str, document: str) -> None:
    path = ROOT / f"future-{name}.generated.qmd"
    path.write_text(document, encoding="utf-8")
    print(f"Generated {path.name}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the four temporary semester planning sources"
    )
    parser.parse_args()

    plan = load_plan()
    required = load_required_announcements()
    exams = load_exams()
    for course in COURSES:
        write_document(
            course,
            semester1_document(course, plan, required, exams),
        )
    write_document(
        "semester2",
        semester2_document(plan, required, exams),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
