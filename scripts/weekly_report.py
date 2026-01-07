from __future__ import annotations

import argparse
import sqlite3 as sql
from datetime import date, timedelta


def week_bounds(d: date) -> tuple[date, date]:
    monday = d - timedelta(days=d.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    args = parser.parse_args()

    with sql.connect(args.db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(date) FROM sessions")
        row = cursor.fetchone()
        if row[0] is None:
            print("No sessions found")
            return 0
        max_date_str = row[0]

        max_date = date.fromisoformat(max_date_str)
        week_start, week_end = week_bounds(max_date)

        query_totals = """
        SELECT SUM(duration_min), COUNT(*)
        FROM sessions
        WHERE date >= ? AND date <= ?"""

        start_s = week_start.isoformat()
        end_s = week_end.isoformat()
        cur = cursor.execute(query_totals, (start_s, end_s))
        total_minutes, total_sessions = cur.fetchone()

        if total_minutes is None:
            total_minutes = 0

        print(f"Week: {start_s} - {end_s}"
              f", total minutes: {total_minutes}, total sessions: {total_sessions}")

        query_per_activity = """
        SELECT activity, SUM(duration_min), COUNT(*)
        FROM sessions
        WHERE date >= ? AND date <= ?
        GROUP BY activity
        ORDER BY activity"""

        cur = cursor.execute(query_per_activity, (start_s, end_s))
        rows = cur.fetchall()

        print("By activity:")
        for activity, minutes, sessions in rows:
            print(f" - {activity}: {minutes} minutes, {sessions} sessions")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
