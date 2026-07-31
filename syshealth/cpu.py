import logging
import os
from typing import Any

import psutil

from syshealth.utils import get_status
from syshealth.utils import get_status, log_health_status

logger = logging.getLogger(__name__)


def get_cpu_info(
    warning: float,
    critical: float,
) -> dict[str, Any]:
    """Collect CPU usage and health information."""

    logger.debug(
        "Collecting CPU information with "
        "warning=%s and critical=%s",
        warning,
        critical,
    )

    cpu_usage = psutil.cpu_percent(interval=1)

    logical_cores = psutil.cpu_count(logical=True)
    physical_cores = psutil.cpu_count(logical=False)

    try:
        load_average = os.getloadavg()
    except (AttributeError, OSError):
        logger.warning(
            "CPU load average is unavailable "
            "on this operating system"
        )
        load_average = (0.0, 0.0, 0.0)

    status = get_status(
        cpu_usage,
        warning,
        critical,
    )

    log_health_status(
        component="CPU",
        usage=cpu_usage,
        status=status,
    )

    return {
        "usage_percent": cpu_usage,
        "logical_cores": logical_cores,
        "physical_cores": physical_cores,
        "load_average": load_average,
        "status": status,
    }