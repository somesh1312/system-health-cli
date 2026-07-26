import os
import psutil
from typing import Any

from syshealth.utils import get_status


def get_cpu_info() -> dict[str, Any]:
    """Collect CPU health information."""

    cpu_usage = psutil.cpu_percent(interval=1)

    logical_cores = psutil.cpu_count(logical=True)
    physical_cores = psutil.cpu_count(logical=False)

    try:
        load_average = os.getloadavg()
    except (AttributeError, OSError):
        load_average = (0.0, 0.0, 0.0)

    return {
        "usage_percent": cpu_usage,
        "logical_cores": logical_cores,
        "physical_cores": physical_cores,
        "load_average": load_average,
        "status": get_status(cpu_usage)
    }