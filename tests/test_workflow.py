from de_learning_analytics.report import build_report
from de_learning_analytics.load import load_csv_to_sqlite


def test_workflow_load_and_report(tmp_path):
    db_path = tmp_path / "test.db"
    csv_path = tmp_path / "test.csv"
    str_db_path = str(db_path)
    str_csv_path = str(csv_path)
    csv_path.write_text(
        "date,duration_min,activity,notes\n"
        "2026-01-10,10,audio,Podcast\n"
        "2026-01-11,15,vocab_app,Unit 10\n",
        encoding="utf-8",
    )
    load_csv_to_sqlite(str_csv_path, str_db_path)
    report = build_report(str_db_path, mode="last7")
    assert report
    assert "total minutes:" in report
    assert any(a in report for a in ["audio", "vocab_app"])
