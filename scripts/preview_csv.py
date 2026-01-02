from __future__ import annotations

from de_learning_analytics.ingest import die, REQUIRED_COLUMNS, normalize_row

import csv
import sys
from pathlib import Path



def main() -> int:
    if len(sys.argv) != 2:
        return die("Usage: python scripts/preview_csv.py <path-to-csv>")

    path = Path(sys.argv[1])
    if not path.exists():
        return die(f"File not found: {path}")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        if fieldnames is None:
            return die("CSV has no header row.")

        missing = [c for c in REQUIRED_COLUMNS if c not in fieldnames]
        if missing:
            return die(f"Missing required columns: {missing}\n"
                       f"Found columns: {fieldnames}")

        raw_rows = list(enumerate(reader, start=2))
        normalized_rows =[]
        for lin_no, row in raw_rows:
            try:
                clean_row = normalize_row(row)
                normalized_rows.append(clean_row)
            except ValueError as e:
                return die(f"Row {lin_no-1} (CSV line {lin_no}) invalid: {e}")


        first_3 = "\n".join(str(row) for row in normalized_rows[:3])
        return die(f"OK. Rows read: {len(normalized_rows)}\n"
                   f"First 3 rows:\n"
                   f"{first_3}", 0)

if __name__ == "__main__":
    raise SystemExit(main())
