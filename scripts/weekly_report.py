from __future__ import annotations

import argparse
from pathlib import Path
from de_learning_analytics.report import build_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--mode", "-m", default="week", choices=["week", "last7"])
    parser.add_argument("--output", type=str, default=None, help="Write report to file instead of stdout")
    args = parser.parse_args()

    report_text = build_report(args.db, args.mode)
    if args.output is None:
        print(report_text)
    else:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
