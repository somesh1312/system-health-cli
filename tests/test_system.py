from datetime import timedelta
from unittest.mock import patch

from winze.system import format_uptime, get_system_info


def test_format_uptime_returns_readable_value() -> None:
    uptime = timedelta(
        days=2,
        hours=5,
        minutes=30,
    )

    result = format_uptime(uptime)

    assert result == "2 days, 5 hours, 30 minutes"


def test_get_system_info_returns_platform_information() -> None:
    with (
        patch(
            "winze.system.socket.gethostname",
            return_value="test-server",
        ),
        patch(
            "winze.system.platform.system",
            return_value="Linux",
        ),
        patch(
            "winze.system.platform.release",
            return_value="6.8.0",
        ),
        patch(
            "winze.system.platform.machine",
            return_value="x86_64",
        ),
        patch(
            "winze.system.platform.python_version",
            return_value="3.12.0",
        ),
    ):
        result = get_system_info()

    assert result["hostname"] == "test-server"
    assert result["os"] == "Linux"
    assert result["os_version"] == "6.8.0"
    assert result["architecture"] == "x86_64"
    assert result["python_version"] == "3.12.0"
    assert "uptime" in result