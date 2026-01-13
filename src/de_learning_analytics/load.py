import csv

from de_learning_analytics.ingest import normalize_row, REQUIRED_COLUMNS
from de_learning_analytics.db import init_db, insert_sessions


def _inserted_sessions(sessions: list, db_path: str) -> int:
    init_db(db_path)
    inserted = insert_sessions(db_path, sessions)
    return inserted


def _load_sessions_from_csv(input_path: str) -> list[dict]:
    sessions = []
    with open(input_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames or []
        missing = [c for c in REQUIRED_COLUMNS if c not in fieldnames]
        if missing:
            raise ValueError("Missing required columns: {}".format(missing))
        for line_no, row in enumerate(reader, start=2):
            try:
                sessions.append(normalize_row(row))
            except ValueError as e:
                raise ValueError(f"Row {line_no} invalid: {e}") from e
    return sessions


def load_csv_to_sqlite(input_path: str, db_path: str) -> int:
    sessions = _load_sessions_from_csv(input_path)
    inserted = _inserted_sessions(sessions, db_path)
    return inserted
