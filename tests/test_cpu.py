from unittest.mock import patch

from winze.cpu import get_cpu_info


def test_get_cpu_info_returns_healthy_status() -> None:
    with (
        patch(
            "winze.cpu.psutil.cpu_percent",
            return_value=35.0,
        ),
        patch(
            "winze.cpu.psutil.cpu_count",
            side_effect=[16, 8],
        ),
        patch(
            "winze.cpu.os.getloadavg",
            return_value=(0.80, 0.75, 0.60),
        ),
    ):
        result = get_cpu_info(
            warning=70,
            critical=90,
        )

    assert result["usage_percent"] == 35.0
    assert result["logical_cores"] == 16
    assert result["physical_cores"] == 8
    assert result["load_average"] == (0.80, 0.75, 0.60)
    assert result["status"] == "HEALTHY"


def test_get_cpu_info_uses_default_when_load_average_unavailable() -> None:
    with (
        patch(
            "winze.cpu.psutil.cpu_percent",
            return_value=35.0,
        ),
        patch(
            "winze.cpu.psutil.cpu_count",
            side_effect=[16, 8],
        ),
        patch(
            "winze.cpu.os.getloadavg",
            side_effect=OSError,
        ),
    ):
        result = get_cpu_info(
            warning=70,
            critical=90,
        )

    assert result["load_average"] == (0.0, 0.0, 0.0)
    assert result["status"] == "HEALTHY"