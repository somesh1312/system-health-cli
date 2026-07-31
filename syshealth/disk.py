import logging
from typing import Any

import psutil

from syshealth.utils import (
    bytes_to_gb,
    get_status,
    log_health_status,
)


logger = logging.getLogger(__name__)


def get_disk_info(
    path: str,
    warning: float,
    critical: float,
) -> dict[str, Any]:
    """Collect disk usage information."""

    logger.debug(
        "Collecting disk information for path='%s' "
        "with warning=%s and critical=%s",
        path,
        warning,
        critical,
    )

    try:
        disk = psutil.disk_usage(path)

        status = get_status(
            disk.percent,
            warning,
            critical,
        )

        log_health_status(
            component=f"Disk ({path})",
            usage=disk.percent,
            status=status,
        )

        return {
            "path": path,
            "total_gb": bytes_to_gb(disk.total),
            "used_gb": bytes_to_gb(disk.used),
            "free_gb": bytes_to_gb(disk.free),
            "usage_percent": disk.percent,
            "status": status,
        }

    except (FileNotFoundError, PermissionError, OSError) as error:
        logger.error(
            "Unable to inspect disk path '%s': %s",
            path,
            error,
        )

        return {
            "path": path,
            "error": str(error),
            "status": "UNKNOWN",
        }