
import json

from src.test_platforms.simulator import DeviceSimulator
from src.test_platforms.executor import run_test


def load_test_plan():
    with open("config/nominal_tests.json") as file:
        return json.load(file)


def test_nominal_plan_passes():
    result = run_test(DeviceSimulator(), load_test_plan())

    assert result["verdict"] == "PASS"
    assert all(
        step["verdict"] == "PASS"
        for step in result["steps"]
    )


def test_overtemperature_causes_failure():
    device = DeviceSimulator()
    device.fault = "overtemperature"

    result = run_test(device, load_test_plan())

    assert result["verdict"] == "FAIL"
