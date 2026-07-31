import logging
from typing import Any

import psutil

from syshealth.utils import (
    bytes_to_gb,
    get_status,
    log_health_status,
)


logger = logging.getLogger(__name__)


def get_memory_info(
    warning: float,
    critical: float,
) -> dict[str, Any]:
    """Collect system memory information."""

    logger.debug(
        "Collecting memory information with warning=%s and critical=%s",
        warning,
        critical,
    )

    memory = psutil.virtual_memory()

    status = get_status(
        memory.percent,
        warning,
        critical,
    )

    log_health_status(
        component="Memory",
        usage=memory.percent,
        status=status,
    )

    return {
        "total_gb": bytes_to_gb(memory.total),
        "used_gb": bytes_to_gb(memory.used),
        "available_gb": bytes_to_gb(memory.available),
        "usage_percent": memory.percent,
        "status": status,
    }