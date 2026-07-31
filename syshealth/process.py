import logging
from typing import Any

import psutil


logger = logging.getLogger(__name__)


def get_process_info(limit: int = 5) -> dict[str, Any]:
    """Get process count and top memory-consuming processes."""

    logger.debug(
        "Collecting top %s processes",
        limit,
    )

    processes: list[dict[str, Any]] = []

    for process in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_percent"]
    ):
        try:
            info = process.info

            processes.append(
                {
                    "pid": info["pid"],
                    "name": info["name"] or "unknown",
                    "cpu_percent": info["cpu_percent"] or 0.0,
                    "memory_percent": round(
                        info["memory_percent"] or 0.0,
                        2,
                    ),
                }
            )

        except psutil.NoSuchProcess:
            logger.debug(
                "Process disappeared while collecting information"
            )

        except psutil.AccessDenied:
            logger.debug(
                "Access denied while inspecting a process"
            )

        except psutil.ZombieProcess:
            logger.debug(
                "Zombie process skipped"
            )

    processes.sort(
        key=lambda process: process["memory_percent"],
        reverse=True,
    )

    total_processes = len(psutil.pids())
    top_processes = processes[:limit]

    logger.info(
        "Collected process information: total=%s, displayed=%s",
        total_processes,
        len(top_processes),
    )

    return {
        "count": total_processes,
        "top_processes": top_processes,
    }