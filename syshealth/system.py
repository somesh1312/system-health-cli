import platform
import socket
from datetime import datetime, timedelta
from typing import Any

import psutil


def get_system_info() -> dict[str, Any]:
    """Return general system information."""

    boot_timestamp = psutil.boot_time()

    boot_time = datetime.fromtimestamp(boot_timestamp)

    uptime = datetime.now() - boot_time

    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "uptime": format_uptime(uptime)
    }


def format_uptime(uptime: timedelta) -> str:
    days = uptime.days

    hours, remainder = divmod(uptime.seconds, 3600)

    minutes = remainder // 60

    return f"{days} days, {hours} hours, {minutes} minutes"