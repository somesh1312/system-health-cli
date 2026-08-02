import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(
    log_level: str = "INFO",
    log_file: str = "logs/winze.log",
) -> None:
    """
    Configure centralized application logging.

    Logs are written to both the terminal and a rotating log file.

    Args:
        log_level: Minimum logging level, such as DEBUG or INFO.
        log_file: Path where application logs should be stored.

    Raises:
        ValueError: If an unsupported logging level is supplied.
    """

    numeric_level = getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError(
            f"Invalid logging level: '{log_level}'"
        )

    log_path = Path(log_file)

    try:
        log_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
    except OSError as error:
        raise RuntimeError(
            f"Unable to create log directory "
            f"'{log_path.parent}': {error}"
        ) from error

    root_logger = logging.getLogger()

    # Avoid adding duplicate handlers if setup_logging()
    # is called more than once.
    if root_logger.handlers:
        return

    root_logger.setLevel(numeric_level)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)

    try:
        file_handler = RotatingFileHandler(
            filename=log_path,
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
    except OSError as error:
        raise RuntimeError(
            f"Unable to initialize log file "
            f"'{log_path}': {error}"
        ) from error

    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)