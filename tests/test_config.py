import json
from pathlib import Path
from unittest.mock import patch

import pytest

from winze.config import load_config


def test_load_config_returns_configuration(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "config.json"

    expected_config = {
        "cpu": {
            "warning": 70,
            "critical": 90,
        },
        "memory": {
            "warning": 75,
            "critical": 90,
        },
        "disk": {
            "warning": 80,
            "critical": 90,
        },
    }

    config_file.write_text(
        json.dumps(expected_config),
        encoding="utf-8",
    )

    result = load_config(str(config_file))

    assert result == expected_config


def test_load_config_raises_error_for_missing_file(
    tmp_path: Path,
) -> None:
    missing_file = tmp_path / "missing.json"

    with pytest.raises(
        RuntimeError,
        match="was not found",
    ):
        load_config(str(missing_file))


def test_load_config_raises_error_for_invalid_json(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "config.json"

    config_file.write_text(
        '{"cpu": {"warning": 70,}}',
        encoding="utf-8",
    )

    with pytest.raises(
        RuntimeError,
        match="contains invalid JSON",
    ):
        load_config(str(config_file))


def test_load_config_raises_error_for_permission_denied() -> None:
    with (
        patch(
            "builtins.open",
            side_effect=PermissionError,
        ),
        pytest.raises(
            RuntimeError,
            match="Permission denied",
        ),
    ):
        load_config("config.json")

def test_load_config_raises_error_for_os_error() -> None:

    with (

        patch(

            "builtins.open",

            side_effect=OSError("filesystem unavailable"),

        ),

        pytest.raises(

            RuntimeError,

            match="Unable to read configuration file",

        ),

    ):

        load_config("config.json")