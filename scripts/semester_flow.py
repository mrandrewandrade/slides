#!/usr/bin/env python3
"""Manage the classroom slide lifecycle for Semester 1.

The source-of-truth is deliberately small:
- staged day fragments live under shared/week-* or <course>/week-*
- current/<course>.qmd points at the one live day
- archive/ stores immutable self-contained HTML for completed days
- <course>/full.qmd is generated from all days up to Current, newest first
- Future is generated at build time from all staged days after Current

Advance is fail-safe: it resolves the next staged day and archives Current before
changing the current pointer.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEM = ROOT / "2026-27" / "semester-1" / "period-1"
SHARED = SEM / "shared"
ROUTINE = SHARED / "routines" / "_end-of-class.qmd"
COURSES = ("tej", "tts", "tas")
DAY_RE = re.compile(r"^_?(\d{4}-\d{2}-\d{2})-day-(\d{2})\.qmd$")
INCLUDE_RE = re.compile(
    r"\{\{<\s*include\s+([^>]*week-(\d{2})/_?(\d{4}-\d{2}-\d{2})-day-(\d{2})\.qmd)\s*>\}\}"
)


@dataclass(frozen=True)
class Day:
    date: str
    day: int
    week: int
    source: Path

    @property
    def key(self) -> tuple[str, int]:
        return (self.date, self.day)


def pretty_date(iso_date: str) -> str:
    value = datetime.strptime(iso_date, "%Y-%m-%d")
    return f"{value.strftime('%A, %B')} {value.day}, {value.year}"


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def split_frontmatter(text: str) -> tuple[list[str], str]:
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise RuntimeError("Expected YAML front matter")
    marker = text.find("\n---\n", 4)
    if marker < 0:
        raise RuntimeError("Could not find closing YAML front matter marker")
    header = text[4:marker].splitlines()
    body = text[marker + 5 :]
    return header, body


def header_without_day(header: list[str]) -> list[str]:
    return [line for line in header if not re.match(r"^(day|class-date):", line)]


def current_path(course: str) -> Path:
    return ROOT / "current" / f"{course}.qmd"


def full_path(course: str) -> Path:
    return SEM / course / "full.qmd"


def current_day(course: str) -> Day:
    path = current_path(course)
    text = path.read_text(encoding="utf-8")
    match = INCLUDE_RE.search(text)
    if not match:
        raise RuntimeError(f"Could not resolve the current day from {path.relative_to(ROOT)}")

    include_path = match.group(1).strip()
    source = (path.parent / include_path).resolve()
    if not source.exists():
        raise RuntimeError(f"Current source does not exist: {source}")

    return Day(
        date=match.group(3),
        day=int(match.group(4)),
        week=int(match.group(2)),
        source=source,
    )


def collect_days(course: str) -> list[Day]:
    """Collect staged days. Course-specific content wins over shared content."""
    found: dict[tuple[str, int], Day] = {}

    for base in (SHARED, SEM / course):
        if not base.exists():
            continue
        for path in sorted(base.glob("week-*/*.qmd")):
            match = DAY_RE.match(path.name)
            week_match = re.fullmatch(r"week-(\d{2})", path.parent.name)
            if not match or not week_match:
                continue
            day = Day(
                date=match.group(1),
                day=int(match.group(2)),
                week=int(week_match.group(1)),
                source=path.resolve(),
            )
            found[day.key] = day

    return sorted(found.values(), key=lambda item: item.key)


def published_days(course: str) -> list[Day]:
    current = current_day(course)
    days = [day for day in collect_days(course) if day.key <= current.key]
    if not any(day.key == current.key for day in days):
        raise RuntimeError(f"Current {course.upper()} day is missing from the staging pool")
    return days


def future_days(course: str) -> list[Day]:
    current = current_day(course)
    return [day for day in collect_days(course) if day.key > current.key]


def next_day(course: str) -> Day:
    days = future_days(course)
    if not days:
        current = current_day(course)
        raise RuntimeError(
            f"No staged day exists after {course.upper()} Day {current.day} ({current.date})."
        )
    return days[0]


def rel_include(from_dir: Path, source: Path) -> str:
    return os.path.relpath(source, from_dir).replace(os.sep, "/")


def write_current(course: str, day: Day) -> None:
    path = current_path(course)
    header, _ = split_frontmatter(path.read_text(encoding="utf-8"))

    updated: list[str] = []
    saw_day = False
    saw_date = False
    for line in header:
        if re.match(r"^day:", line):
            updated.append(f"day: {day.day}")
            saw_day = True
        elif re.match(r"^class-date:", line):
            updated.append(f'class-date: "{pretty_date(day.date)}"')
            saw_date = True
        else:
            updated.append(line)

    if not saw_day:
        updated.insert(1, f"day: {day.day}")
    if not saw_date:
        updated.insert(2, f'class-date: "{pretty_date(day.date)}"')

    source_rel = rel_include(path.parent, day.source)
    routine_rel = rel_include(path.parent, ROUTINE)
    body = (
        f"{{{{< include {source_rel} >}}}}\n\n"
        f"{{{{< include {routine_rel} >}}}}\n"
    )
    atomic_write(path, "---\n" + "\n".join(updated) + "\n---\n\n" + body)


def write_full(course: str) -> None:
    current = current_path(course)
    header, _ = split_frontmatter(current.read_text(encoding="utf-8"))
    header = header_without_day(header)
    target = full_path(course)

    pieces = ["---\n", "\n".join(header), "\n---\n\n"]
    for day in reversed(published_days(course)):
        pieces.append(f"{{{{< include {rel_include(target.parent, day.source)} >}}}}\n\n")
        pieces.append(f"{{{{< include {rel_include(target.parent, ROUTINE)} >}}}}\n\n")

    atomic_write(target, "".join(pieces).rstrip() + "\n")


def archive_path(course: str, day: Day) -> Path:
    return (
        ROOT
        / "archive"
        / "2026-27"
        / "semester-1"
        / course
        / f"week-{day.week:02d}"
        / f"{day.date}-day-{day.day:02d}.html"
    )


def find_quarto() -> str:
    quarto = shutil.which("quarto")
    if not quarto:
        raise RuntimeError("Quarto was not found on PATH. Archive/promotion was not started.")
    return quarto


def render_self_contained(source: Path) -> Path:
    """Render one project document to its normal _site location as standalone HTML."""
    quarto = find_quarto()
    source = source.resolve()
    try:
        relative = source.relative_to(ROOT)
    except ValueError as exc:
        raise RuntimeError(f"Render source must be inside the repository: {source}") from exc

    subprocess.run(
        [
            quarto,
            "render",
            relative.as_posix(),
            "-M",
            "embed-resources:true",
        ],
        cwd=ROOT,
        check=True,
    )

    rendered = ROOT / "_site" / relative.with_suffix(".html")
    if not rendered.exists():
        raise RuntimeError(f"Quarto rendered without producing {rendered.relative_to(ROOT)}")
    return rendered


def archive_current(course: str) -> Path:
    day = current_day(course)
    destination = archive_path(course, day)
    if destination.exists():
        print(f"Archive already exists: {destination.relative_to(ROOT)}")
        return destination

    rendered = render_self_contained(current_path(course))
    html = rendered.read_text(encoding="utf-8")
    html = html.replace('href="../index.html"', 'href="../../../../../index.html"')
    atomic_write(destination, html)

    print(f"Archived {course.upper()} Day {day.day}: {destination.relative_to(ROOT)}")
    return destination


def advance(courses: list[str]) -> None:
    # Resolve every next day first. No archives or pointers change if any course is missing staging.
    planned = {course: next_day(course) for course in courses}

    # Archive every current deck before changing any current pointer.
    for course in courses:
        archive_current(course)

    # Only after all archives succeed do we promote and regenerate Full.
    for course in courses:
        day = planned[course]
        write_current(course, day)
        write_full(course)
        print(
            f"Promoted {course.upper()} to Day {day.day} ({day.date}); "
            f"Full now contains {len(published_days(course))} published day(s)."
        )


def future_document(course: str) -> str | None:
    days = future_days(course)
    if not days:
        return None

    header, _ = split_frontmatter(current_path(course).read_text(encoding="utf-8"))
    header = header_without_day(header)
    pieces = ["---\n", "\n".join(header), "\n---\n\n"]
    current = current_day(course)
    pieces.append("# Future Slide Deck {.course-day-slide}\n\n")
    pieces.append(
        f"Staged slides after **Day {current.day}**. These are work in progress and may change.\n\n"
    )
    for day in days:
        pieces.append(f"{{{{< include {day.source.relative_to(ROOT).as_posix()} >}}}}\n\n")
        pieces.append(f"{{{{< include {ROUTINE.relative_to(ROOT).as_posix()} >}}}}\n\n")
    return "".join(pieces).rstrip() + "\n"


def render_future(course: str, output_dir: Path) -> None:
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    document = future_document(course)
    output = output_dir / "index.html"

    if document is None:
        current = current_day(course)
        output.write_text(
            "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<title>{course.upper()} Future Slide Deck</title>"
            "<style>body{font-family:system-ui,sans-serif;max-width:900px;margin:3rem auto;padding:0 1rem;line-height:1.5;color:#2f3439}a{color:#234a73}</style>"
            "</head><body>"
            f"<h1>{course.upper()} Future Slide Deck</h1>"
            f"<p>No staged slides exist after Day {current.day} yet.</p>"
            '<p><a href="../../index.html">Back to Slides Home</a></p>'
            "</body></html>\n",
            encoding="utf-8",
        )
        return

    temp_qmd = ROOT / f"future-{course}.generated.qmd"
    rendered: Path | None = None
    try:
        atomic_write(temp_qmd, document)
        rendered = render_self_contained(temp_qmd)
        shutil.copy2(rendered, output)
    finally:
        temp_qmd.unlink(missing_ok=True)
        if rendered is not None:
            rendered.unlink(missing_ok=True)


def print_status(course: str) -> None:
    current = current_day(course)
    published = published_days(course)
    future = future_days(course)
    print(f"{course.upper()}: Current = Day {current.day} ({current.date}), Week {current.week}")
    print("  Full:   " + ", ".join(f"Day {d.day}" for d in reversed(published)))
    if future:
        print("  Future: " + ", ".join(f"Day {d.day} ({d.date})" for d in future))
    else:
        print("  Future: no staged days")


def parse_courses(value: str) -> list[str]:
    value = value.lower()
    if value == "all":
        return list(COURSES)
    if value not in COURSES:
        raise argparse.ArgumentTypeError("course must be tej, tts, tas, or all")
    return [value]


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage current, archived, full, and future slides")
    sub = parser.add_subparsers(dest="command", required=True)

    advance_parser = sub.add_parser("advance", help="archive Current, then promote the next staged day")
    advance_parser.add_argument("course")

    sync_parser = sub.add_parser("sync", help="regenerate Full from the current pointer")
    sync_parser.add_argument("course")

    status_parser = sub.add_parser("status", help="show Current, Full, and Future state")
    status_parser.add_argument("course")

    future_parser = sub.add_parser("render-future", help="render staged days after Current")
    future_parser.add_argument("course")
    future_parser.add_argument("output_dir")

    args = parser.parse_args()

    try:
        if args.command == "advance":
            advance(parse_courses(args.course))
        elif args.command == "sync":
            for course in parse_courses(args.course):
                write_full(course)
                print(f"Synced {course.upper()} Full deck.")
        elif args.command == "status":
            for course in parse_courses(args.course):
                print_status(course)
        elif args.command == "render-future":
            courses = parse_courses(args.course)
            if len(courses) != 1:
                raise RuntimeError("render-future accepts one course at a time")
            render_future(courses[0], Path(args.output_dir))
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
