from types import SimpleNamespace
from unittest.mock import patch

from syshealth.disk import get_disk_info

def test_get_disk_info_returns_healthy_status() -> None:
    path = "/"
    fake_disk = SimpleNamespace(
        total = 512*1024 ** 3,
        used=124*1024**3,
        free=400*1024**3,
        percent=30.0,
    )
    with patch(
        "syshealth.disk.psutil.disk_usage",
        return_value =fake_disk
    ):
        result = get_disk_info(
            path=path,
            warning=75,
            critical=90
        )
    assert result["path"]== path
    assert result["total_gb"] == 512.0
    assert result["used_gb"] == 124.0
    assert result["free_gb"] == 400.0
    assert result["usage_percent"] == 30.0
    assert result["status"] == 'HEALTHY'

def test_get_disk_info_returns_unknown_for_missing_path() -> None:
    with patch(
        "syshealth.disk.psutil.disk_usage",
        side_effect=FileNotFoundError("path not found"),
    ):
        result = get_disk_info(
            path="/missing",
            warning=75,
            critical=90,
        )

    assert result["path"] == "/missing"
    assert result["status"] == "UNKNOWN"
    assert "error" in result