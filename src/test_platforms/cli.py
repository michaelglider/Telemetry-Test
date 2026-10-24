
import argparse
import json
from pathlib import Path

from src.test_platforms.simulator import DeviceSimulator
from src.test_platforms.executor import run_test
from src.test_platforms.results import save_test_report


def main():
    parser = argparse.ArgumentParser(
        description="Hardware Test and Telemetry Platform"
    )
    parser.add_argument(
        "--fault",
        choices=[
            "overtemperature",
            "undervoltage",
            "overcurrent",
            "device_error",
        ],
        help="Inject a simulated device fault",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]
    plan_path = project_root / "config" / "nominal_tests.json"

    with plan_path.open(encoding="utf-8") as file:
        test_plan = json.load(file)

    device = DeviceSimulator()

    
    if args.fault:
        response = device.handle_command({
            "name": "INJECT_FAULT",
            "value": args.fault,
        })

        if response["status"] != "OK":
            raise RuntimeError(
                f"Fault injection failed: {response}"
            )


    result = run_test(device, test_plan)

    report_path = save_test_report(
        result,
        output_dir=project_root / "reports",
    )

    print(f"Test: {result['test_name']}")
    print(f"Overall verdict: {result['verdict']}")
    print(f"Fault injected: {args.fault or 'None'}")
    print(f"Report saved to: {report_path}")

    for step in result["steps"]:
        print(
            f"{step['verdict']}: {step['step']} — "
            f"actual={step['actual']}, "
            f"limits=[{step['minimum']}, {step['maximum']}]"
        )


if __name__ == "__main__":
    main()

