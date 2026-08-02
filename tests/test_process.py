from types import SimpleNamespace
from unittest.mock import patch

import psutil
from syshealth.process import get_process_info


def test_get_process_info_returns_top_processes() -> None:
    fake_processes = [
        SimpleNamespace(
            info={
                "pid": 101,
                "name": "Google Chrome",
                "cpu_percent": 20.0,
                "memory_percent": 12.5,
            }
        ),
        SimpleNamespace(
            info={
                "pid": 202,
                "name": "Python",
                "cpu_percent": 10.0,
                "memory_percent": 25.0,
            }
        ),
        SimpleNamespace(
            info={
                "pid": 303,
                "name": "Docker",
                "cpu_percent": 5.0,
                "memory_percent": 8.0,
            }
        ),
    ]

    with (
        patch(
            "syshealth.process.psutil.process_iter",
            return_value=fake_processes,
        ),
        patch(
            "syshealth.process.psutil.pids",
            return_value=[101, 202, 303],
        ),
    ):
        result = get_process_info(limit=2)

    assert result["count"] == 3
    assert len(result["top_processes"]) == 2
    assert result["top_processes"][0]["name"] == "Python"
    assert result["top_processes"][0]["memory_percent"] == 25.0
    assert result["top_processes"][1]["name"] == "Google Chrome"

class AccessDeniedProcess:

    @property

    def info(self) -> dict:

        raise psutil.AccessDenied(pid=999)

def test_get_process_info_skips_access_denied_processes() -> None:

    fake_processes = [

        SimpleNamespace(

            info={

                "pid": 102,

                "name": "Google Chrome",

                "cpu_percent": 30.0,

                "memory_percent": 22.5,

            }

        ),

        AccessDeniedProcess(),

        SimpleNamespace(

            info={

                "pid": 305,

                "name": "Docker",

                "cpu_percent": 50.0,

                "memory_percent": 80.0,

            }

        ),

    ]

    with (

        patch(

            "syshealth.process.psutil.process_iter",

            return_value=fake_processes,

        ),

        patch(

            "syshealth.process.psutil.pids",

            return_value=[102, 204, 305],

        ),

    ):

        result = get_process_info(limit=5)

    assert result["count"] == 3

    assert len(result["top_processes"]) == 2

    assert result["top_processes"][0]["name"] == "Docker"

    assert result["top_processes"][1]["name"] == "Google Chrome"

class ZombieProcess:
    @property
    def info(self) -> dict:
        raise psutil.ZombieProcess(pid=888)

class MissingProcess:
    @property
    def info(self) -> dict:
        raise psutil.NoSuchProcess(pid=777)

def test_get_process_info_skips_zombie_processes() -> None:
    fake_processes = [
        ZombieProcess(),
        SimpleNamespace(
            info={
                "pid": 401,
                "name": "Python",
                "cpu_percent": 15.0,
                "memory_percent": 10.0,
            }
        ),
    ]

    with (
        patch(
            "syshealth.process.psutil.process_iter",
            return_value=fake_processes,
        ),
        patch(
            "syshealth.process.psutil.pids",
            return_value=[888, 401],
        ),
    ):
        result = get_process_info(limit=5)

    assert result["count"] == 2
    assert len(result["top_processes"]) == 1
    assert result["top_processes"][0]["name"] == "Python"