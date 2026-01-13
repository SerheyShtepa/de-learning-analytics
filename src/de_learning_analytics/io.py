from pathlib import Path


def emit_report(report_text: str, output: str | None) -> None:
    if output is None:
        print(report_text)
    else:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report_text, encoding="utf-8")
