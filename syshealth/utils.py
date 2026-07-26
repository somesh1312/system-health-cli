from typing import Union


Number = Union[int, float]


def bytes_to_gb(value: Number) -> float:
    """Convert bytes to gigabytes."""
    return round(value / (1024 ** 3), 2)


def get_status(
    percentage: float,
    warning: float = 70.0,
    critical: float = 90.0
) -> str:
    """Return health status based on resource usage."""

    if percentage >= critical:
        return "CRITICAL"

    if percentage >= warning:
        return "WARNING"

    return "HEALTHY"