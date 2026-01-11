markdown
## How to run

### Input data:
data/sessions_raw.csv is expected to exist locally,
the file is gitignored,
for quick start - copy or rename sessions_raw_example.csv

### 1. Load CSV into SQLite

```bash
python scripts/load_sqlite.py --input data/sessions_raw.csv --db data/sessions.db
```
### 2. Generate report (stdout)
```bash
python scripts/weekly_report.py --db data/sessions.db --mode last7
```
### 3. Generate report (file)
```bash
python scripts/weekly_report.py --db data/sessions.db --mode last7 --output reports/last7.txt
```
### Quality checks
```bash
ruff check .
pytest -q
```

