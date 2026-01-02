from __future__ import annotations

import sys
from datetime import date

REQUIRED_COLUMNS = ["date", "duration_min", "activity", "notes"]
CANONICAL_ACTIVITIES = {"audio", "vocab_app", "new_lesson_app", "grammar_gpt"}


def die(message: str, code: int = 2) -> int:
    print(message, file=sys.stderr)
    return code


def normalize_activity(activity_raw: str) -> str:
    activity = activity_raw.strip().lower()
    aliases = {
        "vocab": "vocab_app",
        "grammar": "grammar_gpt",
        "new_lesson": "new_lesson_app"
    }
    activity = aliases.get(activity, activity)

    if activity not in CANONICAL_ACTIVITIES:
        raise ValueError(
            f"Invalid activity '{activity_raw}'.\n"
            f"Must be one of {sorted(list(CANONICAL_ACTIVITIES))}"
        )

    return activity


def parse_duration(value: str) -> int:
    try:
        duration = int(value.strip())
    except (ValueError, TypeError):
        raise ValueError(
            f"Invalid duration_min '{value}'.\n"
            f"Expected integer minutes."
        )

    if duration <= 0:
        raise ValueError(
            f"duration_min must be > 0, got {duration}.\n"
            f"Zero or negative duration are rejected as invalid data."
        )

    return duration


def parse_date(value: str) -> str:
    try:
        parsed_date = date.fromisoformat(value.strip())
        return parsed_date.isoformat()
    except ValueError:
        raise ValueError(f"Invalid date format: '{value}'. Expected ISO format YYYY-MM-DD.")


def normalize_row(row: dict) -> dict:
    return {
        "date": parse_date(row["date"]),
        "duration_min": parse_duration(row["duration_min"]),
        "activity": normalize_activity(row["activity"]),
        "notes": row["notes"].strip() or None
    }
