import json
from typing import Any


def load_config(filename: str = "config.json") -> dict[str, Any]:
    """Load system health configuration."""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            config = json.load(file)

        return config

    except FileNotFoundError:
        raise RuntimeError(
            f"Configuration file '{filename}' was not found."
        )

    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Configuration file contains invalid JSON: {error}"
        )

    except PermissionError:
        raise RuntimeError(
            f"Permission denied while reading '{filename}'."
        )

