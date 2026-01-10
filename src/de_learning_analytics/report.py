from __future__ import annotations

import sqlite3 as sql
from datetime import date, timedelta


def week_bounds(d: date) -> tuple[date, date]:
    monday = d - timedelta(days=d.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def get_max_date(conn: sql.Connection) -> date | None:
    cur = conn.cursor()
    cur.execute("SELECT MAX(date) FROM sessions")
    row = cur.fetchone()
    if row[0] is None:
        return None
    max_date_str = row[0]
    max_date = date.fromisoformat(max_date_str)
    return max_date


def date_range(end_date: date, mode: str) -> tuple[date, date]:
    if mode not in ("week", "last7"):
        raise ValueError(f"Invalid mode: {mode}")
    elif mode == "last7":
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


def build_report(db_path: str, mode: str) -> str:
    with sql.connect(db_path) as conn:
        cursor = conn.cursor()
        max_date = get_max_date(conn)
        if max_date is None:
            return "No sessions found.\n"
        start_date, end_date = date_range(max_date, mode)

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
        return report_text
