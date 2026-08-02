import logging


logger = logging.getLogger(__name__)


def bytes_to_gb(value: int) -> float:
    """Convert bytes to gigabytes."""

    return round(value / (1024 ** 3), 2)


def get_status(
    percentage: float,
    warning: float,
    critical: float,
) -> str:
    """Determine health status from usage thresholds."""

    if warning < 0 or critical < 0:
        raise ValueError(
            "Health thresholds cannot be negative."
        )

    if warning >= critical:
        raise ValueError(
            "Warning threshold must be lower than critical threshold."
        )

    if percentage >= critical:
        return "CRITICAL"

    if percentage >= warning:
        return "WARNING"

    return "HEALTHY"


def log_health_status(
    component: str,
    usage: float,
    status: str,
) -> None:
    """Log component health using the appropriate severity."""

    message = "%s usage is %.2f%% with status %s"

    if status == "CRITICAL":
        logger.critical(
            message,
            component,
            usage,
            status,
        )

    elif status == "WARNING":
        logger.warning(
            message,
            component,
            usage,
            status,
        )

    elif status == "UNKNOWN":
        logger.error(
            message,
            component,
            usage,
            status,
        )

    else:
        logger.info(
            message,
            component,
            usage,
            status,
        )