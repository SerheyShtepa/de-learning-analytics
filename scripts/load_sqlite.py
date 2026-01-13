import argparse
import sys

from de_learning_analytics.load import load_csv_to_sqlite


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
    try:
        inserted = load_csv_to_sqlite(input_path, db_path)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(2)
    if inserted:
        print(f"{inserted} rows inserted")
    else:
        print("0 new rows inserted (already loaded)")


if __name__ == "__main__":
    main()
