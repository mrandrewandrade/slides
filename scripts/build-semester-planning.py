#!/usr/bin/env python3
"""Build calendar-driven semester planning decks for the WIP site."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEM1 = ROOT / "2026-27" / "semester-1" / "period-1"
SHARED = SEM1 / "shared"
ROUTINE = SHARED / "routines" / "_end-of-class.qmd"
PLAN = ROOT / "planning" / "2026-27-student-slide-calendar.tsv"
EXAMS = ROOT / "planning" / "2026-27-exam-days.tsv"
COURSES = ("tej", "tts", "tas")
DAY_RE = re.compile(r"^_?(\d{4}-\d{2}-\d{2})-day-(\d{2})\.qmd$")
CURRENT_RE = re.compile(r"_([0-9]{4}-[0-9]{2}-[0-9]{2})-day-[0-9]{2}\.qmd")


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


def load_plan() -> list[PlanDay]:
    days: list[PlanDay] = []
    for raw in PLAN.read_text(encoding="utf-8").splitlines():
        if not raw or raw.startswith("#"):
            continue
        date, semester, raw_announcements = raw.split("\t", 2)
        announcements = tuple(
            item.strip() for item in raw_announcements.split(" || ") if item.strip()
        )
        days.append(PlanDay(date, semester, announcements))
    return days


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


def placeholder_day(day: PlanDay, lesson_label: str) -> str:
    date_label = pretty_date(day.date)
    announcement_text = (
        "\n".join(f"- {item}" for item in day.announcements)
        if day.announcements
        else "[No calendar announcements.]"
    )
    return f'''# Quote

{date_label}

[QUOTE]

# Announcements {{.announcements-slide}}

{date_label}

{announcement_text}

# {lesson_label} - Lesson

{date_label}

[{lesson_label.upper()} LESSON]

'''


def exam_day(day: ExamDay) -> str:
    date_label = pretty_date(day.date)
    return f'''# Quote

{date_label}

[QUOTE]

# Announcements {{.announcements-slide}}

{date_label}

- **Exam day:** {day.label}.

# Exam Day

{date_label}

[EXAM SCHEDULE / COURSE-SPECIFIC DETAILS]

'''


def semester1_document(course: str, plan: list[PlanDay], exams: list[ExamDay]) -> str:
    label = course.upper()
    now = current_date(course)
    staged = staged_days(course)
    planned = {
        day.date: day
        for day in plan
        if day.semester == "semester-1" and day.date > now
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
            pieces.append(exam_day(exam_map[date]))
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


def semester2_document(plan: list[PlanDay], exams: list[ExamDay]) -> str:
    pieces = [reveal_header("Semester 2")]
    pieces.append("# Semester 2 Planning {.course-day-slide}\n\n")
    pieces.append(
        "Generic course deck. Semester 2 timetable periods are intentionally not assumed.\n\n"
    )

    planned = {day.date: day for day in plan if day.semester == "semester-2"}
    exam_map = {day.date: day for day in exams if day.semester == "semester-2"}

    for date in sorted(set(planned) | set(exam_map)):
        if date in exam_map:
            pieces.append(exam_day(exam_map[date]))
        else:
            pieces.append(placeholder_day(planned[date], "Course"))

    return "".join(pieces).rstrip() + "\n"


def render_document(name: str, document: str, output_dir: Path) -> None:
    quarto = shutil.which("quarto")
    if not quarto:
        raise RuntimeError("Quarto was not found on PATH.")

    output_dir.mkdir(parents=True, exist_ok=True)
    temp = ROOT / f"future-{name}.generated.qmd"
    project_rendered = ROOT / "_site" / f"future-{name}.generated.html"
    adjacent_rendered = ROOT / f"future-{name}.generated.html"
    temp.write_text(document, encoding="utf-8")
    try:
        subprocess.run(
            [quarto, "render", temp.name, "-M", "embed-resources:true"],
            cwd=ROOT,
            check=True,
        )
        rendered = project_rendered if project_rendered.exists() else adjacent_rendered
        if not rendered.exists():
            raise RuntimeError(f"Quarto did not produce HTML for {temp.name}.")
        shutil.copy2(rendered, output_dir / "index.html")
    finally:
        temp.unlink(missing_ok=True)
        project_rendered.unlink(missing_ok=True)
        adjacent_rendered.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the four semester planning decks")
    parser.add_argument("output_root", nargs="?", default="_site/wip")
    args = parser.parse_args()

    output_root = Path(args.output_root)
    if not output_root.is_absolute():
        output_root = ROOT / output_root

    plan = load_plan()
    exams = load_exams()
    for course in COURSES:
        render_document(
            course,
            semester1_document(course, plan, exams),
            output_root / course,
        )
    render_document(
        "semester2",
        semester2_document(plan, exams),
        output_root / "semester2",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
