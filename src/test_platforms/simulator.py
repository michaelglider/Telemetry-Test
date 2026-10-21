
from dataclasses import dataclass, asdict
import json
import time


@dataclass
class Telemetry:
    sequence: int
    timestamp_ms: int
    temperature_c: float
    voltage_v: float
    motor_current_a: float
    status: str


class DeviceSimulator:
    def __init__(self):
        self.started_at = time.monotonic()
        self.sequence = 0
        self.output_enabled = False
        self.fault = None

    def get_telemetry(self):
        self.sequence += 1

        # Deterministic nominal measurements make tests repeatable.
        temperature = 32.5
        voltage = 12.0
        current = 1.4 if self.output_enabled else 0.1
        status = "READY"

        if self.fault == "overtemperature":
            temperature = 95.0
        elif self.fault == "undervoltage":
            voltage = 8.0
        elif self.fault == "overcurrent":
            current = 12.0
        elif self.fault == "device_error":
            status = "ERROR"

        return Telemetry(
            sequence=self.sequence,
            timestamp_ms=int(
                (time.monotonic() - self.started_at) * 1000
            ),
            temperature_c=temperature,
            voltage_v=voltage,
            motor_current_a=current,
            status=status,
        )

    def handle_command(self, message):
        command = message.get("name")
        command_id = message.get("command_id", "unknown")

        if command == "GET_TELEMETRY":
            return {
                "type": "telemetry",
                **asdict(self.get_telemetry()),
            }

        if command == "SET_OUTPUT":
            value = message.get("value")

            if type(value) is not int or value not in (0, 1):
                return {
                    "type": "response",
                    "command_id": command_id,
                    "status": "INVALID_ARGUMENT",
                }

            self.output_enabled = bool(value)

            return {
                "type": "response",
                "command_id": command_id,
                "status": "OK",
            }

        if command == "INJECT_FAULT":
            allowed = {
                "overtemperature",
                "undervoltage",
                "overcurrent",
                "device_error",
            }
            fault = message.get("value")

            if fault not in allowed:
                return {
                    "type": "response",
                    "command_id": command_id,
                    "status": "INVALID_ARGUMENT",
                }

            self.fault = fault

            return {
                "type": "response",
                "command_id": command_id,
                "status": "OK",
            }

        if command == "RESET":
            self.output_enabled = False
            self.fault = None

            return {
                "type": "response",
                "command_id": command_id,
                "status": "OK",
            }

        return {
            "type": "response",
            "command_id": command_id,
            "status": "UNKNOWN_COMMAND",
        }


if __name__ == "__main__":
    device = DeviceSimulator()

    print("Simulated device ready. Enter a JSON command.")
    print('Example: {"name":"GET_TELEMETRY"}')
    print("Type quit to exit.")

    while True:
        try:
            line = input("> ")
            if line.strip().lower() == "quit":
                break

            message = json.loads(line)
            if not isinstance(message, dict):
                raise ValueError("Command must be a JSON object")

            result = device.handle_command(message)
            print(json.dumps(result))

        except (json.JSONDecodeError, ValueError) as exc:
            print(json.dumps({
                "type": "error",
                "message": str(exc),
            }))
