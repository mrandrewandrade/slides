#!/usr/bin/env bash
set -euo pipefail

COURSES=(tej tts tas)

usage() {
  cat <<'EOF'
Usage:
  bash scripts/slides.sh preview <tej|tts|tas>
  bash scripts/slides.sh build <tej|tts|tas|all>
  bash scripts/slides.sh archive
  bash scripts/slides.sh new <day> <YYYY-MM-DD> <week>
  bash scripts/slides.sh index

Examples:
  bash scripts/slides.sh preview tej
  bash scripts/slides.sh build tej
  bash scripts/slides.sh build all
  bash scripts/slides.sh archive
  bash scripts/slides.sh new 2 2026-09-09 1
EOF
}

validate_course() {
  case "$1" in
    tej|tts|tas) ;;
    *)
      echo "Course must be tej, tts, or tas." >&2
      exit 1
      ;;
  esac
}

current_metadata() {
  local course="$1"
  local include_line

  include_line="$(grep -m1 'shared/week-' "current/${course}.qmd" || true)"

  if [[ "$include_line" =~ week-([0-9]{2})/_([0-9]{4}-[0-9]{2}-[0-9]{2})-day-([0-9]{2})\.qmd ]]; then
    printf '%s %s %s\n' "${BASH_REMATCH[1]}" "${BASH_REMATCH[3]}" "${BASH_REMATCH[2]}"
    return 0
  fi

  return 1
}

make_index() {
  cat > index.qmd <<'EOF'
---
title: "Technology Class Slides"
format:
  html:
    toc: false
    css: site.css
---

# 2026-27 Classroom Slides

These classroom slides are designed to be used **in conjunction with the course notes and resources at [andrewandrade.ca/commons](https://andrewandrade.ca/commons)**.

Open a class below. The newest instructional week appears first. Older weeks remain available underneath it.

EOF

  for course in "${COURSES[@]}"; do
    local label="${course^^}"
    local metadata=""
    local current_week=""
    local current_day=""
    local current_date=""
    local archive_base="archive/2026-27/semester-1/${course}"
    local weeks=()

    metadata="$(current_metadata "$course" || true)"
    if [[ -n "$metadata" ]]; then
      read -r current_week current_day current_date <<< "$metadata"
      weeks+=("$current_week")
    fi

    if [[ -d "$archive_base" ]]; then
      while IFS= read -r dir; do
        [[ -n "$dir" ]] && weeks+=("${dir##*/week-}")
      done < <(find "$archive_base" -mindepth 1 -maxdepth 1 -type d -name 'week-*' -print 2>/dev/null | sort -r)
    fi

    mapfile -t weeks < <(printf '%s\n' "${weeks[@]}" | sed '/^$/d' | sort -u -r)

    {
      echo '<details class="course-block">'
      echo "<summary><strong>${label}</strong></summary>"
      echo
    } >> index.qmd

    if [[ ${#weeks[@]} -eq 0 ]]; then
      echo '<p>No slides yet.</p>' >> index.qmd
    else
      local first_week=1
      local week
      for week in "${weeks[@]}"; do
        local week_num=$((10#$week))
        local open_attr=""
        local archive_dir="${archive_base}/week-${week}"

        if [[ $first_week -eq 1 ]]; then
          open_attr=" open"
        fi

        {
          echo "<details class=\"week-block\"${open_attr}>"
          if [[ $first_week -eq 1 ]]; then
            echo "<summary><strong>Week ${week_num}</strong> <span class=\"current-label\">Latest week</span></summary>"
          else
            echo "<summary><strong>Week ${week_num}</strong></summary>"
          fi
          echo '<ul>'
        } >> index.qmd

        if [[ "$current_week" == "$week" ]]; then
          local current_day_num=$((10#$current_day))
          echo "<li><a href=\"current/${course}.html\">Day ${current_day_num} · ${current_date}</a> <span class=\"current-label\">Current deck</span></li>" >> index.qmd
        fi

        if [[ -d "$archive_dir" ]]; then
          local archived
          while IFS= read -r archived; do
            [[ -z "$archived" ]] && continue
            local base="${archived##*/}"
            if [[ "$base" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})-day-([0-9]{2})\.html$ ]]; then
              local archive_date="${BASH_REMATCH[1]}"
              local archive_day="${BASH_REMATCH[2]}"

              # If the current deck has already been archived but not advanced yet,
              # show only the current link until a new day is started.
              if [[ "$current_week" == "$week" && "$current_date" == "$archive_date" && "$current_day" == "$archive_day" ]]; then
                continue
              fi

              local archive_day_num=$((10#$archive_day))
              echo "<li><a href=\"${archived}\">Day ${archive_day_num} · ${archive_date}</a></li>" >> index.qmd
            fi
          done < <(find "$archive_dir" -maxdepth 1 -type f -name '*.html' -print 2>/dev/null | sort -r)
        fi

        {
          echo '</ul>'
          echo '</details>'
          echo
        } >> index.qmd

        first_week=0
      done
    fi

    {
      echo '</details>'
      echo
    } >> index.qmd
  done

  cat >> index.qmd <<'EOF'
## Course Notes

The companion notes, references, assignments, and course resources live at [andrewandrade.ca/commons](https://andrewandrade.ca/commons).
EOF
}

command="${1:-help}"

case "$command" in
  preview)
    course="${2:-}"
    validate_course "$course"
    make_index
    exec quarto preview "current/${course}.qmd"
    ;;

  build)
    target="${2:-all}"
    make_index
    if [[ "$target" == "all" ]]; then
      quarto render
    else
      validate_course "$target"
      quarto render "current/${target}.qmd"
    fi
    ;;

  archive)
    for course in "${COURSES[@]}"; do
      metadata="$(current_metadata "$course" || true)"
      if [[ -z "$metadata" ]]; then
        echo "Could not determine the current day for ${course}." >&2
        exit 1
      fi
      read -r week day date <<< "$metadata"
      bash scripts/archive-current.sh "$course" "$week" "$day" "$date"
    done
    make_index
    echo "Archived all current decks and refreshed index.qmd."
    ;;

  new)
    raw_day="${2:-}"
    date="${3:-}"
    raw_week="${4:-}"

    if [[ -z "$raw_day" || -z "$date" || -z "$raw_week" ]]; then
      usage
      exit 1
    fi

    printf -v day '%02d' "$((10#$raw_day))"
    printf -v week '%02d' "$((10#$raw_week))"
    day_num=$((10#$day))
    week_num=$((10#$week))

    if [[ ! "$date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
      echo "Date must be YYYY-MM-DD." >&2
      exit 1
    fi

    # Protect unfinished current work from being overwritten.
    for course in "${COURSES[@]}"; do
      metadata="$(current_metadata "$course" || true)"
      if [[ -n "$metadata" ]]; then
        read -r old_week old_day old_date <<< "$metadata"
        old_archive="archive/2026-27/semester-1/${course}/week-${old_week}/${old_date}-day-${old_day}.html"
        if [[ ! -f "$old_archive" ]]; then
          echo "Current ${course^^} deck is not archived yet." >&2
          echo "Run: bash scripts/slides.sh archive" >&2
          exit 1
        fi
      fi
    done

    shared_dir="2026-27/semester-1/period-1/shared/week-${week}"
    shared_file="${shared_dir}/_${date}-day-${day}.qmd"

    if [[ -e "$shared_file" ]]; then
      echo "Lesson already exists: $shared_file" >&2
      exit 1
    fi

    mkdir -p "$shared_dir"

    cat > "$shared_file" <<EOF
<!--
lesson-day: ${day_num}
date: ${date}
week: ${week_num}
-->

# Quote of the Day

> **PLACEHOLDER QUOTE**

# Arrival

Take a moment to arrive and focus.

# Today's Plan

- Add today's agenda.

# Lesson

Add today's lesson slides here.
EOF

    for course in "${COURSES[@]}"; do
      label="${course^^}"
      cat > "current/${course}.qmd" <<EOF
---
title: "${label} · Day ${day_num}"
subtitle: "2026-27 · Semester 1 · Period 1"
author: "Andrew Andrade"
---

{{< include ../${shared_file} >}}

<!-- Insert ${label}-specific slides for the current day here. -->

{{< include ../2026-27/semester-1/period-1/shared/routines/_end-of-class.qmd >}}

# Navigation

[Slides home](../index.html)
EOF
    done

    make_index
    echo "Started Day ${day_num}, Week ${week_num}, ${date}."
    echo "Edit: $shared_file"
    ;;

  index)
    make_index
    echo "Rebuilt index.qmd from current decks and archive files."
    ;;

  help|-h|--help)
    usage
    ;;

  *)
    usage
    exit 1
    ;;
esac
