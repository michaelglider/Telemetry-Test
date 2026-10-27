
from abc import ABC, abstractmethod
from typing import Any


class DeviceInterface(ABC):
    """Common interface for simulated and physical test devices."""

    @abstractmethod
    def handle_command(self, message: dict[str, Any]) -> dict[str, Any]:
        """Send a command to the device and return its response."""
        raise NotImplementedError
