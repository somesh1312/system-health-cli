from typing import Any

import psutil


def get_process_info(limit: int = 5) -> dict[str, Any]:
    """Get process count and top memory-consuming processes."""

    processes: list[dict[str, Any]] = []

    for process in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_percent"]
    ):
        try:
            info = process.info

            processes.append({
                "pid": info["pid"],
                "name": info["name"] or "unknown",
                "cpu_percent": info["cpu_percent"] or 0.0,
                "memory_percent": round(
                    info["memory_percent"] or 0.0,
                    2
                )
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    processes.sort(
        key=lambda process: process["memory_percent"],
        reverse=True
    )

    return {
        "count": len(psutil.pids()),
        "top_processes": processes[:limit]
    }