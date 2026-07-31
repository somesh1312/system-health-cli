import json
import logging
from typing import Any


logger = logging.getLogger(__name__)


def load_config(filename: str = "config.json") -> dict[str, Any]:
    """
    Load the application configuration from a JSON file.

    Args:
        filename: Path to the configuration file.

    Returns:
        Dictionary containing configuration values.

    Raises:
        RuntimeError: If the configuration file cannot be loaded.
    """

    logger.info("Loading configuration from '%s'", filename)

    try:
        with open(filename, "r", encoding="utf-8") as file:
            config = json.load(file)

        logger.info("Configuration loaded successfully")

        return config

    except FileNotFoundError as error:
        logger.error("Configuration file '%s' was not found", filename)

        raise RuntimeError(
            f"Configuration file '{filename}' was not found."
        ) from error

    except json.JSONDecodeError as error:
        logger.error(
            "Invalid JSON in '%s': %s",
            filename,
            error,
        )

        raise RuntimeError(
            f"Configuration file contains invalid JSON: {error}"
        ) from error

    except PermissionError as error:
        logger.error(
            "Permission denied while reading '%s'",
            filename,
        )

        raise RuntimeError(
            f"Permission denied while reading '{filename}'."
        ) from error

    except OSError as error:
        logger.error(
            "Unable to read configuration: %s",
            error,
        )

        raise RuntimeError(
            f"Unable to load configuration: {error}"
        ) from error