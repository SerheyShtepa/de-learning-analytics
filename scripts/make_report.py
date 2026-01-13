import argparse

from de_learning_analytics.report import build_report
from de_learning_analytics.io import emit_report
from de_learning_analytics.load import load_csv_to_sqlite


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/sessions.db", help="Database path (default: data/sessions.db)")
    parser.add_argument("--mode", "-m", default="week", choices=["week", "last7"])
    parser.add_argument("--output", type=str, default=None, help="Write report to file instead of stdout")
    parser.add_argument("--input", required=True, help="Path to sessions_raw.csv")
    args = parser.parse_args()
    db_path = args.db
    load_csv_to_sqlite(args.input, db_path)
    text = build_report(db_path, args.mode)
    emit_report(text, args.output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
