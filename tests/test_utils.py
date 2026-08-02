from winze.utils import get_status,bytes_to_gb

import pytest


def test_get_status_returns_healthy() -> None:
    result = get_status(40, 70, 90)

    assert result == "HEALTHY"

def test_get_status_returns_warning() -> None:
    result = get_status(80, 70, 90)

    assert result == "WARNING"

def test_get_status_returns_critical() -> None:
    result = get_status(95, 70, 90)

    assert result == "CRITICAL"

def test_get_status_returns_threshold_mismatch() -> None:
    with pytest.raises(

        ValueError,

        match="Warning threshold must be lower than critical threshold."):

        get_status(50, 90, 70)

def test_bytes_to_gb_returns_one_gb() -> None:
    result = bytes_to_gb(1_073_741_824)

    assert result == 1.0

def test_get_status_rejects_negative_thresholds() -> None:
    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        get_status(
            percentage=50,
            warning=-1,
            critical=90,
        )