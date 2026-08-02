import logging
from pathlib import Path

from syshealth.logging_config import setup_logging
import pytest

def test_setup_logging_adds_console_and_file_handlers(
    tmp_path: Path,
) -> None:
    root_logger = logging.getLogger()

    original_handlers = root_logger.handlers.copy()

    try:
        root_logger.handlers.clear()

        log_file = tmp_path / "syshealth.log"

        setup_logging(
            log_level="DEBUG",
            log_file=str(log_file),
        )

        assert root_logger.level == logging.DEBUG
        assert len(root_logger.handlers) == 2

        logger = logging.getLogger("test")
        logger.info("test message")

        assert log_file.exists()

    finally:
        for handler in root_logger.handlers:
            handler.close()

        root_logger.handlers.clear()
        root_logger.handlers.extend(original_handlers)



def test_setup_logging_rejects_invalid_log_level() -> None:

    with pytest.raises(

        ValueError,

        match="Invalid logging level",

    ):

        setup_logging(log_level="INVALID")