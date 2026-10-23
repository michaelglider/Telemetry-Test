
import json

from src.test_platforms.results import save_test_report


def test_save_test_report(tmp_path):
    result = {
        "test_name": "Controller Functional Test",
        "verdict": "PASS",
        "started_at": "2026-10-22T10:00:00+00:00",
        "completed_at": "2026-10-22T10:00:01+00:00",
        "steps": [
            {
                "step": "Temperature Check",
                "measurement": "temperature_c",
                "actual": 32.5,
                "minimum": 0,
                "maximum": 80,
                "verdict": "PASS"
            }
        ]
    }

    path = save_test_report(result, output_dir=tmp_path)

    assert path.exists()

    with path.open(encoding="utf-8") as file:
        saved_result = json.load(file)

    assert saved_result["verdict"] == "PASS"
    assert saved_result["steps"][0]["actual"] == 32.5
