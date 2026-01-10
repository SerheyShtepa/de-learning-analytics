from de_learning_analytics.db import init_db, insert_sessions
from de_learning_analytics.report import build_report


def test_empty_db(tmp_path):
    db_path = tmp_path / "test.db"
    str_db_path = str(db_path)
    init_db(str_db_path)
    text = build_report(str_db_path, "last7")
    assert "No sessions found" in text


def test_small_dataset(tmp_path):
    db_path = tmp_path / "test.db"
    str_db_path = str(db_path)
    sessions = [
        {"date": "2026-01-01", "duration_min": 30, "activity": "audio", "notes": "Podcast"},
        {"date": "2026-01-01", "duration_min": 15, "activity": "vocab_app", "notes": None},
        {"date": "2026-01-02", "duration_min": 45, "activity": "new_lesson_app", "notes": "Unit 10"},
        {"date": "2026-01-02", "duration_min": 20, "activity": "grammar_gpt", "notes": "Verbs"},
        {"date": "2026-01-01", "duration_min": 30, "activity": "audio", "notes": "Podcast 2"},
    ]

    init_db(str_db_path)
    inserted = insert_sessions(str_db_path, sessions)
    assert inserted == len(sessions)
    text = build_report(str_db_path, "last7")
    assert "total minutes: 140" in text
    assert "audio" in text
    assert "vocab_app" in text
    assert "new_lesson_app" in text
