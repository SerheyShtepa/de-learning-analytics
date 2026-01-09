from __future__ import annotations

import argparse
import sqlite3 as sql
from datetime import date, timedelta
from pathlib import Path


def week_bounds(d: date) -> tuple[date, date]:
    monday = d - timedelta(days=d.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def get_max_date(conn: sql.Connection) -> date | None:
    cur = conn.cursor()
    cur.execute("SELECT MAX(date) FROM sessions")
    row = cur.fetchone()
    if row[0] is None:
        print("No sessions found")
        return None
    max_date_str = row[0]
    max_date = date.fromisoformat(max_date_str)
    return max_date


def date_range(end_date: date, mode: str) -> tuple[date, date]:
    if mode == "last7":
        start_date = end_date - timedelta(days=6)
    else:
        start_date, end_date = week_bounds(end_date)
    return start_date, end_date


def get_totals(cursor: sql.Cursor, start_s: str, end_s: str) -> tuple[int, int]:
    query_totals = """
    SELECT SUM(duration_min), COUNT(*)
    FROM sessions
    WHERE date >= ? AND date <= ?"""
    cur = cursor.execute(query_totals, (start_s, end_s))
    total_minutes, total_sessions = cur.fetchone()
    if total_minutes is None:
        total_minutes = 0
    return total_minutes, total_sessions


def get_activity_rows(cursor: sql.Cursor, start_s: str, end_s: str) -> list[tuple[str, int, int]]:
    query_per_activity = """
        SELECT activity, SUM(duration_min), COUNT(*)
        FROM sessions
        WHERE date >= ? AND date <= ?
        GROUP BY activity
        ORDER BY activity"""

    cur = cursor.execute(query_per_activity, (start_s, end_s))
    rows = cur.fetchall()
    rows = sorted(rows, key=lambda x: (-x[1], x[0]))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--mode", "-m", default="week", choices=["week", "last7"])
    parser.add_argument("--output", type=str, default=None, help="Write report to file instead of stdout")
    args = parser.parse_args()

    with sql.connect(args.db) as conn:
        cursor = conn.cursor()
        max_date = get_max_date(conn)
        if max_date is None:
            return 0
        start_date, end_date = date_range(max_date, args.mode)

        start_s = start_date.isoformat()
        end_s = end_date.isoformat()
        total_minutes, total_sessions = get_totals(cursor, start_s, end_s)

        rows = get_activity_rows(cursor, start_s, end_s)
        lines = [
            f"Week: {start_s} - {end_s}",
            f"total minutes: {total_minutes}, total sessions: {total_sessions}",
            "By activity:",
        ]
        for activity, minutes, n_sessions in rows:
            session_word = "session" if n_sessions == 1 else "sessions"
            lines.append(f" - {activity}: {minutes} minutes, {n_sessions} {session_word}")
        report_text = "\n".join(lines)
        if args.output is None:
            print(report_text)
        else:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(report_text, encoding="utf-8")


    return 0


if __name__ == "__main__":
    raise SystemExit(main())
