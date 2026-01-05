import sqlite3 as sql

from de_learning_analytics.db import init_db, insert_sessions


def test_loader_idempotent(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    str_db_path = str(db_path)

    sessions = [
        {"date": "2026-01-01", "duration_min": 30, "activity": "audio", "notes": "Podcast"},
        {"date": "2026-01-01", "duration_min": 15, "activity": "vocab_app", "notes": None},
        {"date": "2026-01-02", "duration_min": 45, "activity": "new_lesson_app", "notes": "Unit 10"},
        {"date": "2026-01-02", "duration_min": 20, "activity": "grammar_gpt", "notes": "Verbs"},
    ]

    init_db(str_db_path)
    first_insert = insert_sessions(str_db_path, sessions)
    second_insert = insert_sessions(str_db_path, sessions)

    with sql.connect(str_db_path) as conn:
        cur = conn.execute("SELECT COUNT(*) FROM sessions")
        total_rows = cur.fetchone()[0]

    assert first_insert == 4
    assert second_insert == 0
    assert total_rows == 4
