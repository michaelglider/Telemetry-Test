
from src.test_platforms.simulator import DeviceSimulator


def test_nominal_telemetry():
    device = DeviceSimulator()

    telemetry = device.get_telemetry()

    assert telemetry.temperature_c == 32.5
    assert telemetry.voltage_v == 12.0
    assert telemetry.motor_current_a == 0.1
    assert telemetry.status == "READY"


def test_sequence_number_increments():
    device = DeviceSimulator()

    first = device.get_telemetry()
    second = device.get_telemetry()

    assert second.sequence == first.sequence + 1


def test_output_changes_current():
    device = DeviceSimulator()

    device.handle_command({
        "name": "SET_OUTPUT",
        "command_id": "cmd-001",
        "value": 1,
    })

    telemetry = device.get_telemetry()

    assert telemetry.motor_current_a == 1.4


def test_overtemperature_fault():
    device = DeviceSimulator()

    response = device.handle_command({
        "name": "INJECT_FAULT",
        "command_id": "cmd-002",
        "value": "overtemperature",
    })

    telemetry = device.get_telemetry()

    assert response["status"] == "OK"
    assert telemetry.temperature_c == 95.0


def test_undervoltage_fault():
    device = DeviceSimulator()

    device.handle_command({
        "name": "INJECT_FAULT",
        "command_id": "cmd-003",
        "value": "undervoltage",
    })

    telemetry = device.get_telemetry()

    assert telemetry.voltage_v == 8.0


def test_reset_clears_fault_and_output():
    device = DeviceSimulator()

    device.handle_command({
        "name": "SET_OUTPUT",
        "command_id": "cmd-004",
        "value": 1,
    })
    device.handle_command({
        "name": "INJECT_FAULT",
        "command_id": "cmd-005",
        "value": "overtemperature",
    })

    response = device.handle_command({
        "name": "RESET",
        "command_id": "cmd-006",
    })

    telemetry = device.get_telemetry()

    assert response["status"] == "OK"
    assert telemetry.temperature_c == 32.5
    assert telemetry.motor_current_a == 0.1


def test_invalid_output_command_is_rejected():
    device = DeviceSimulator()

    response = device.handle_command({
        "name": "SET_OUTPUT",
        "command_id": "cmd-007",
        "value": 5,
    })

    assert response["status"] == "INVALID_ARGUMENT"


def test_unknown_command_is_rejected():
    device = DeviceSimulator()

    response = device.handle_command({
        "name": "DO_SOMETHING_UNKNOWN",
        "command_id": "cmd-008",
    })

    assert response["status"] == "UNKNOWN_COMMAND"
