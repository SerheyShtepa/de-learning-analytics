import sqlite3 as sql


def init_db(db_path: str) -> None:
    with sql.connect(db_path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            duration_min INTEGER NOT NULL,
            activity TEXT NOT NULL,
            notes TEXT NOT NULL DEFAULT '',
            UNIQUE (date, activity, duration_min, notes)
        );
        """)


def insert_sessions(db_path: str, sessions: list[dict]) -> int:
    with sql.connect(db_path) as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM sessions")
        count_value_before = int(cursor.fetchone()[0])
        rows = [
            (s["date"], s["duration_min"], s["activity"], s["notes"] or "")
            for s in sessions
        ]
        conn.executemany("""INSERT OR IGNORE INTO sessions (date, duration_min, activity, notes)
            VALUES (?, ?, ?, ?)""", rows)

        cursor = conn.execute("SELECT COUNT(*) FROM sessions")
        count_value_after = int(cursor.fetchone()[0])
        count_value = count_value_after - count_value_before
        return count_value
