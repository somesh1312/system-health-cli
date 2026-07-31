import logging

def setup_logger() -> logging.Logger:

    """Configure application logger."""

    logger = logging.getLogger("syshealth")

    logger.setLevel(logging.INFO)

    if logger.handlers:

        return logger

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(message)s"

    )

    file_handler = logging.FileHandler(

        "syshealth.log"

    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger