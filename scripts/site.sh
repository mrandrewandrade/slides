#!/usr/bin/env bash
set -euo pipefail

COURSES=(tej tts tas)

current_metadata() {
  local course="$1"
  local include_line
  include_line="$(grep -m1 'shared/week-' "current/${course}.qmd" || true)"

  if [[ "$include_line" =~ week-([0-9]{2})/_([0-9]{4}-[0-9]{2}-[0-9]{2})-day-([0-9]{2})\.qmd ]]; then
    printf '%s %s %s\n' "${BASH_REMATCH[1]}" "${BASH_REMATCH[3]}" "${BASH_REMATCH[2]}"
    return 0
  fi

  echo "Could not read week/day/date metadata from current/${course}.qmd" >&2
  return 1
}

generate_index() {
  local archive_root="${1:-archive}"

  cat > index.qmd <<'EOF'
---
title: "Technology Class Slides"
format:
  html:
    toc: false
    css: site.css
---

# 2026-27 Classroom Slides

Choose a course. The latest week opens first, with earlier weeks kept out of the way.

EOF

  for course in "${COURSES[@]}"; do
    local label="${course^^}"
    local metadata current_week current_day current_date
    metadata="$(current_metadata "$course")"
    read -r current_week current_day current_date <<< "$metadata"

    local archive_base="${archive_root}/2026-27/semester-1/${course}"
    local weeks=("$current_week")

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

    local first_week=1
    local week
    for week in "${weeks[@]}"; do
      local week_num=$((10#$week))
      local open_attr=""
      local archive_dir="${archive_base}/week-${week}"

      [[ $first_week -eq 1 ]] && open_attr=" open"

      {
        echo "<details class=\"week-block\"${open_attr}>"
        if [[ $first_week -eq 1 ]]; then
          echo "<summary><strong>Week ${week_num}</strong> <span class=\"current-label\">Latest</span></summary>"
        else
          echo "<summary><strong>Week ${week_num}</strong></summary>"
        fi
        echo '<ul>'
      } >> index.qmd

      if [[ "$current_week" == "$week" ]]; then
        local current_day_num=$((10#$current_day))
        echo "<li><a href=\"current/${course}.html\">Day ${current_day_num} · ${current_date}</a></li>" >> index.qmd
      fi

      if [[ -d "$archive_dir" ]]; then
        local archived
        while IFS= read -r archived; do
          [[ -z "$archived" ]] && continue
          local base="${archived##*/}"

          if [[ "$base" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})-day-([0-9]{2})\.html$ ]]; then
            local archive_date="${BASH_REMATCH[1]}"
            local archive_day="${BASH_REMATCH[2]}"

            if [[ "$current_week" == "$week" && "$current_date" == "$archive_date" && "$current_day" == "$archive_day" ]]; then
              continue
            fi

            local archive_day_num=$((10#$archive_day))
            local relative="archive/2026-27/semester-1/${course}/week-${week}/${base}"
            echo "<li><a href=\"${relative}\">Day ${archive_day_num} · ${archive_date}</a></li>" >> index.qmd
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

    {
      echo '<div class="course-deck-links">'
      echo "<p><a href=\"2026-27/semester-1/period-1/${course}/full.html\"><strong>Full slides</strong></a> · all published days in one deck, newest first</p>"
      echo "<p><a href=\"wip/${course}/index.html\"><strong>Future slide deck</strong></a> · staged slides for the rest of the semester</p>"
      echo '</div>'
      echo
      echo '</details>'
      echo
    } >> index.qmd
  done

  cat >> index.qmd <<'EOF'
## Course Notes

Notes, references, assignments, and course resources live at [andrewandrade.ca/commons](https://andrewandrade.ca/commons).
EOF
}

snapshot_current() {
  local archive_root="$1"
  local course

  for course in "${COURSES[@]}"; do
    local metadata week day date
    metadata="$(current_metadata "$course")"
    read -r week day date <<< "$metadata"

    local archive_dir="${archive_root}/2026-27/semester-1/${course}/week-${week}"
    local archive_file="${archive_dir}/${date}-day-${day}.html"
    local tmp_dir
    tmp_dir="$(mktemp -d)"

    mkdir -p "$archive_dir"

    quarto render "current/${course}.qmd" \
      --output-dir "$tmp_dir" \
      -M embed-resources:true

    local rendered_file
    rendered_file="$(find "$tmp_dir" -type f -name "${course}.html" -print -quit)"

    if [[ -z "$rendered_file" ]]; then
      echo "Could not find rendered ${course}.html" >&2
      rm -rf "$tmp_dir"
      exit 1
    fi

    cp "$rendered_file" "$archive_file"

    # Archived decks live five levels below the site root.
    sed -i 's#href="../index.html"#href="../../../../../index.html"#g' "$archive_file"

    rm -rf "$tmp_dir"
    echo "Archived ${course^^}: ${archive_file}"
  done
}

case "${1:-}" in
  index)
    generate_index "${2:-archive}"
    ;;
  snapshot)
    snapshot_current "${2:-_site/archive}"
    ;;
  *)
    echo "This is an internal helper used by run/publish and GitHub Actions." >&2
    exit 1
    ;;
esac
