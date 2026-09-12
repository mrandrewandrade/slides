#!/usr/bin/env python3
from pathlib import Path
import html
import re
import sys

site_root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
base = site_root / "archive" / "2026-27" / "semester-1"

courses = ("tej", "tts", "tas")
pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})-day-(\d{2})\.html$")

for course in courses:
    course_dir = base / course
    course_dir.mkdir(parents=True, exist_ok=True)
    weeks = sorted(
        [p for p in course_dir.glob("week-*") if p.is_dir()],
        key=lambda p: p.name,
        reverse=True,
    )

    parts = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        f"<title>{course.upper()} All Published Slides</title>",
        "<style>body{font-family:system-ui,sans-serif;max-width:900px;margin:3rem auto;padding:0 1rem;line-height:1.5}h1{margin-bottom:.25rem}.week{border:1px solid #ddd;border-radius:.5rem;margin:1rem 0;padding:.5rem 1rem}li{margin:.45rem 0}.muted{opacity:.65}</style>",
        "</head>",
        "<body>",
        f"<h1>{course.upper()} All Published Slides</h1>",
        '<p class="muted">Completed classroom slide decks, grouped by instructional week.</p>',
        '<p><a href="../../../../index.html">Back to Slides Home</a></p>',
    ]

    if not weeks:
        parts.append("<p>No published slides yet.</p>")
    else:
        for week_dir in weeks:
            week_num = int(week_dir.name.split("-")[-1])
            files = sorted(week_dir.glob("*.html"), reverse=True)
            entries = []
            for file in files:
                match = pattern.match(file.name)
                if not match:
                    continue
                date, day = match.groups()
                entries.append(
                    f'<li><a href="{html.escape(week_dir.name)}/{html.escape(file.name)}">Day {int(day)} · {html.escape(date)}</a></li>'
                )
            if entries:
                parts.extend([
                    '<section class="week">',
                    f"<h2>Week {week_num}</h2>",
                    "<ul>",
                    *entries,
                    "</ul>",
                    "</section>",
                ])

    parts.extend(["</body>", "</html>"])
    (course_dir / "index.html").write_text("\n".join(parts) + "\n", encoding="utf-8")
