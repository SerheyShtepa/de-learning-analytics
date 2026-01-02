import argparse
import csv
import sys

from de_learning_analytics.db import init_db, insert_sessions
from de_learning_analytics.ingest import normalize_row, REQUIRED_COLUMNS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",
                        default="data/sessions_raw.csv",
                        help="Way to CSV (default: data/sessions_raw.csv)")
    parser.add_argument("--db",
                        default="data/sessions.db",
                        help="Way to DB (default: data/sessions.db)")
    return parser.parse_args()


def main():
    args = parse_args()
    input_path: str = args.input
    db_path: str = args.db

    sessions = []
    with open(input_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        fieldnames = reader.fieldnames or []
        missing = [c for c in REQUIRED_COLUMNS if c not in fieldnames]
        if missing:
            print(f"Missing required columns: {missing}", file=sys.stderr)
            sys.exit(2)
        for line_no, row in enumerate(reader, start=2):
            try:
                sessions.append(normalize_row(row))
            except ValueError as e:
                print(f"Row {line_no} invalid: {e}", file=sys.stderr)
                sys.exit(2)

    if sessions:
        init_db(db_path)
        inserted = insert_sessions(db_path, sessions)
        print(f"Inserted {inserted} rows into {db_path}")
    else:
        print(f"No sessions found", file=sys.stderr)


if __name__ == "__main__":
    main()
