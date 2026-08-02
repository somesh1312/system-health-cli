import json
import logging
from typing import Any


logger = logging.getLogger(__name__)


def load_config(filename: str = "config.json") -> dict[str, Any]:
    """
    Load the application configuration from a JSON file.

    Args:
        filename: Path to the JSON configuration file.

    Returns:
        Dictionary containing the configuration values.

    Raises:
        RuntimeError: If the file cannot be loaded or parsed.
    """

    logger.debug(
        "Attempting to load configuration from '%s'",
        filename,
    )

    try:
        with open(filename, "r", encoding="utf-8") as file:
            config = json.load(file)

    except FileNotFoundError as error:
        logger.error(
            "Configuration file not found: %s",
            filename,
        )

        raise RuntimeError(
            f"Configuration file '{filename}' was not found."
        ) from error

    except json.JSONDecodeError as error:
        logger.error(
            "Invalid JSON in configuration file '%s': %s",
            filename,
            error,
        )

        raise RuntimeError(
            f"Configuration file contains invalid JSON: {error}"
        ) from error

    except PermissionError as error:
        logger.error(
            "Permission denied while reading configuration: %s",
            filename,
        )

        raise RuntimeError(
            f"Permission denied while reading '{filename}'."
        ) from error

    except OSError as error:
        logger.error(
            "Operating-system error while reading '%s': %s",
            filename,
            error,
        )

        raise RuntimeError(
            f"Unable to read configuration file "
            f"'{filename}': {error}"
        ) from error

    logger.info(
        "Configuration loaded successfully from '%s'",
        filename,
    )

    return config