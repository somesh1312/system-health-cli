from typing import Any

import psutil

from syshealth.utils import bytes_to_gb, get_status


def get_memory_info() -> dict[str, Any]:
    """Collect system memory information."""

    memory = psutil.virtual_memory()

    return {
        "total_gb": bytes_to_gb(memory.total),
        "used_gb": bytes_to_gb(memory.used),
        "available_gb": bytes_to_gb(memory.available),
        "usage_percent": memory.percent,
        "status": get_status(memory.percent)
    }