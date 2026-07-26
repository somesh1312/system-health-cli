from typing import Any

import psutil

from syshealth.utils import bytes_to_gb, get_status


def get_disk_info(path: str = "/") -> dict[str, Any]:
    """Collect disk usage information."""

    try:
        disk = psutil.disk_usage(path)

        return {
            "path": path,
            "total_gb": bytes_to_gb(disk.total),
            "used_gb": bytes_to_gb(disk.used),
            "free_gb": bytes_to_gb(disk.free),
            "usage_percent": disk.percent,
            "status": get_status(disk.percent)
        }

    except (PermissionError, FileNotFoundError) as error:
        return {
            "path": path,
            "error": str(error),
            "status": "UNKNOWN"
        }