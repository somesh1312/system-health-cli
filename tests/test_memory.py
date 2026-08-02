from types import SimpleNamespace
from unittest.mock import patch

from winze.memory import get_memory_info

def test_get_memory_info_returns_healthy_status() -> None:
    fake_memory = SimpleNamespace(
        total = 16*1024 ** 3,
        used=8*1024**3,
        available=8*1024**3,
        percent=50.0,
    )
    with patch(
        "winze.memory.psutil.virtual_memory",
        return_value =fake_memory
    ):
        
        result = get_memory_info(
            warning =75,
            critical=90,
        )
    assert result["total_gb"] == 16.0
    assert result["used_gb"] == 8.0
    assert result["available_gb"] == 8.0
    assert result["usage_percent"] == 50.0
    assert result["status"] == "HEALTHY"
