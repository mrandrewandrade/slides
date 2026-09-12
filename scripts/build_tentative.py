#!/usr/bin/env python3
"""Prepare student-facing tentative future slides.

This runs on the future-slides branch after the Semester 2 draft generator.
It keeps observance language positive and creates a separate Quarto subproject
that can be rendered in the background without affecting the fast live build.
"""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEM = ROOT / "2026-27" / "semester-2"
SHARED = SEM / "period-1" / "shared"
TENTATIVE = ROOT / "tentative"


def student_friendly_observance_language(text: str) -> str:
    text = text.replace(
        "# Upcoming Red Dot / Open Red Dot",
        "# Upcoming Celebration / Observance",
    )
    text = text.replace(
        "# Today: Red Dot / Open Red Dot",
        "# Today's Celebration / Observance",
    )
    text = text.replace(
        "**Red Dot:** do not schedule school events during the observance.  \n"
        "**Open Red Dot:** where shown, do not schedule events on the evening prior.\n\n"
        "Students observing may be unavailable for school activities or assessments.\n",
        "**Red Dot / Open Red Dot** are Peel scheduling designations that help the school respect important observances.  \n"
        "Open Red Dot observances may include the evening before.\n\n"
        "Some students may be celebrating or observing and may be away from regular school activities.\n",
    )
    return text


def refine_daily_files() -> list[tuple[int, int, str, Path]]:
    days: list[tuple[int, int, str, Path]] = []
    pattern = re.compile(r"_(\d{4}-\d{2}-\d{2})-day-(\d{2})\.qmd$")

    for path in sorted(SHARED.glob("week-*/*.qmd")):
        match = pattern.search(path.name)
        if not match:
            continue
        week_match = re.search(r"week-(\d{2})", path.parent.name)
        if not week_match:
            continue

        text = path.read_text(encoding="utf-8")
        refined = student_friendly_observance_language(text)
        if refined != text:
            path.write_text(refined, encoding="utf-8")

        week = int(week_match.group(1))
        day = int(match.group(2))
        date_text = match.group(1)
        days.append((week, day, date_text, path))

    return days


def write_tentative_project(days: list[tuple[int, int, str, Path]]) -> None:
    if TENTATIVE.exists():
        shutil.rmtree(TENTATIVE)
    TENTATIVE.mkdir(parents=True)

    (TENTATIVE / "_quarto.yml").write_text(
        """project:
  type: default
  output-dir: ../_tentative-site

format:
  html:
    toc: false

execute:
  freeze: auto
""",
        encoding="utf-8",
    )

    index = [
        "---\n",
        'title: "Upcoming / Tentative Slides"\n',
        "---\n\n",
        "# Semester 2 Tentative Plan\n\n",
        "**Tentative and subject to change.** These drafts are here to help you anticipate what may be coming. "
        "Topics, timing, activities, assessments, and due dates may change based on class progress, school events, and student needs.\n\n",
        "For confirmed course notes and resources, use [andrewandrade.ca/commons](https://andrewandrade.ca/commons).\n\n",
    ]

    current_week = None
    for week, day, date_text, source in days:
        if week != current_week:
            if current_week is not None:
                index.append("\n")
            index.append(f"## Week {week}\n\n")
            current_week = week

        pretty_date = datetime.strptime(date_text, "%Y-%m-%d").strftime("%A, %B %-d, %Y")
        # Windows does not use %-d, but this generator runs in Linux CI.
        relative = f"week-{week:02d}/day-{day:02d}.html"
        index.append(f"- [Day {day}: {pretty_date}]({relative})\n")

        wrapper_dir = TENTATIVE / f"week-{week:02d}"
        wrapper_dir.mkdir(parents=True, exist_ok=True)
        include_path = source.relative_to(ROOT).as_posix()
        wrapper = wrapper_dir / f"day-{day:02d}.qmd"
        wrapper.write_text(
            f"""---
title: "Tentative Semester 2 - Day {day}"
subtitle: "Week {week} · {date_text} · Subject to change"
format:
  revealjs:
    theme: default
    slide-number: true
    progress: true
    transition: none
    navigation-mode: vertical
---

# Tentative Plan

**This is a draft and is subject to change.**

Use it to anticipate what may be coming, not as a final assessment or due-date commitment.

{{{{< include ../../{include_path} >}}}}

# Back to Tentative Plan

[← Upcoming / Tentative Slides](../index.html)
""",
            encoding="utf-8",
        )

    (TENTATIVE / "index.qmd").write_text("".join(index), encoding="utf-8")


def main() -> None:
    days = refine_daily_files()
    write_tentative_project(days)
    print(f"Prepared {len(days)} student-facing tentative slide decks.")


if __name__ == "__main__":
    main()
