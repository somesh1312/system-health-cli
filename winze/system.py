import logging
import platform
import socket
from datetime import datetime, timedelta
from typing import Any

import psutil


logger = logging.getLogger(__name__)


def get_system_info() -> dict[str, Any]:
    """Return general system information."""

    logger.debug(
        "Collecting operating-system information"
    )

    boot_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_timestamp)
    uptime = datetime.now() - boot_time

    hostname = socket.gethostname()

    system_info = {
        "hostname": hostname,
        "os": platform.system(),
        "os_version": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "uptime": format_uptime(uptime),
    }

    logger.info(
        "System information collected for host '%s'",
        hostname,
    )

    return system_info


def format_uptime(uptime: timedelta) -> str:
    """Convert a timedelta into a readable uptime string."""

    days = uptime.days

    hours, remainder = divmod(
        uptime.seconds,
        3600,
    )

    minutes = remainder // 60

    return (
        f"{days} days, "
        f"{hours} hours, "
        f"{minutes} minutes"
    )