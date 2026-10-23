
import json
from pathlib import Path
from datetime import datetime, timezone


def save_test_report(result, output_dir="reports"):
    report_dir = Path(output_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )
    filename = f"test_report_{timestamp}.json"
    report_path = report_dir / filename

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)

    return report_path
