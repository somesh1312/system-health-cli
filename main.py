import argparse
import sys
from datetime import datetime

from syshealth.config import load_config
from syshealth.cpu import get_cpu_info
from syshealth.disk import get_disk_info
from syshealth.logging import setup_logger
from syshealth.memory import get_memory_info
from syshealth.process import get_process_info
from syshealth.system import get_system_info


logger = setup_logger()


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description="Monitor system CPU, memory, disk, and process health."
    )

    parser.add_argument(
        "--disk",
        default="/",
        help="Filesystem path to monitor. Default: /",
    )

    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of top processes to display. Default: 5",
    )

    parser.add_argument(
        "--output",
        help="Optional file path where the health report will be saved.",
    )

    return parser


def calculate_overall_status(*statuses: str) -> str:
    """Return the most severe status from all health checks."""

    if "CRITICAL" in statuses:
        return "CRITICAL"

    if "WARNING" in statuses:
        return "WARNING"

    if "UNKNOWN" in statuses:
        return "UNKNOWN"

    return "HEALTHY"


def get_exit_code(status: str) -> int:
    """Convert a health status into a process exit code."""

    exit_codes = {
        "HEALTHY": 0,
        "WARNING": 1,
        "CRITICAL": 2,
        "UNKNOWN": 3,
    }

    return exit_codes.get(status, 3)


def generate_report(
    disk_path: str,
    top: int,
) -> tuple[str, str]:
    """Collect system information and generate a formatted health report."""

    logger.info("Loading application configuration")
    config = load_config()

    logger.info("Collecting system health metrics")

    system = get_system_info()

    cpu = get_cpu_info(
        warning=config["cpu"]["warning"],
        critical=config["cpu"]["critical"],
    )

    memory = get_memory_info(
        warning=config["memory"]["warning"],
        critical=config["memory"]["critical"],
    )

    disk = get_disk_info(
        path=disk_path,
        warning=config["disk"]["warning"],
        critical=config["disk"]["critical"],
    )

    process_data = get_process_info(top)

    overall_status = calculate_overall_status(
        cpu["status"],
        memory["status"],
        disk["status"],
    )

    lines: list[str] = []

    lines.append("=" * 55)
    lines.append("SYSTEM HEALTH REPORT")
    lines.append("=" * 55)
    lines.append(
        f"Generated At   : "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    lines.append("")
    lines.append("SYSTEM")
    lines.append("-" * 55)
    lines.append(f"Hostname       : {system['hostname']}")
    lines.append(f"OS             : {system['os']} {system['os_version']}")
    lines.append(f"Architecture   : {system['architecture']}")
    lines.append(f"Python         : {system['python_version']}")
    lines.append(f"Uptime         : {system['uptime']}")

    lines.append("")
    lines.append("CPU")
    lines.append("-" * 55)
    lines.append(f"Usage          : {cpu['usage_percent']}%")
    lines.append(f"Physical Cores : {cpu['physical_cores']}")
    lines.append(f"Logical Cores  : {cpu['logical_cores']}")

    load_average = cpu["load_average"]

    lines.append(
        f"Load Average   : "
        f"{load_average[0]:.2f}, "
        f"{load_average[1]:.2f}, "
        f"{load_average[2]:.2f}"
    )

    lines.append(f"Status         : {cpu['status']}")

    lines.append("")
    lines.append("MEMORY")
    lines.append("-" * 55)
    lines.append(f"Total          : {memory['total_gb']} GB")
    lines.append(f"Used           : {memory['used_gb']} GB")
    lines.append(f"Available      : {memory['available_gb']} GB")
    lines.append(f"Usage          : {memory['usage_percent']}%")
    lines.append(f"Status         : {memory['status']}")

    lines.append("")
    lines.append("DISK")
    lines.append("-" * 55)

    if "error" in disk:
        lines.append(f"Path           : {disk_path}")
        lines.append(f"Error          : {disk['error']}")
    else:
        lines.append(f"Path           : {disk['path']}")
        lines.append(f"Total          : {disk['total_gb']} GB")
        lines.append(f"Used           : {disk['used_gb']} GB")
        lines.append(f"Free           : {disk['free_gb']} GB")
        lines.append(f"Usage          : {disk['usage_percent']}%")

    lines.append(f"Status         : {disk['status']}")

    lines.append("")
    lines.append("PROCESSES")
    lines.append("-" * 55)
    lines.append(f"Total Processes: {process_data['count']}")

    lines.append("")
    lines.append(
        f"{'PID':<10}"
        f"{'NAME':<25}"
        f"{'CPU %':<10}"
        f"{'MEM %':<10}"
    )

    for process in process_data["top_processes"]:
        lines.append(
            f"{process['pid']:<10}"
            f"{process['name'][:23]:<25}"
            f"{process['cpu_percent']:<10}"
            f"{process['memory_percent']:<10}"
        )

    lines.append("")
    lines.append("=" * 55)
    lines.append(f"OVERALL STATUS: {overall_status}")
    lines.append("=" * 55)

    report = "\n".join(lines)

    return report, overall_status


def save_report(report: str, filename: str) -> None:
    """Save the generated health report to a file."""

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(report)

    except PermissionError as error:
        raise RuntimeError(
            f"No permission to write report to '{filename}'."
        ) from error

    except OSError as error:
        raise RuntimeError(
            f"Unable to write report to '{filename}': {error}"
        ) from error


def main() -> None:
    """Run the system health command-line application."""

    parser = create_parser()
    args = parser.parse_args()

    if args.top < 1:
        parser.error("--top must be greater than zero")

    logger.info(
        "System health check started: disk=%s, top=%s",
        args.disk,
        args.top,
    )

    try:
        report, overall_status = generate_report(
            disk_path=args.disk,
            top=args.top,
        )

        print(report)

        if args.output:
            save_report(
                report=report,
                filename=args.output,
            )

            logger.info(
                "Health report saved to %s",
                args.output,
            )

            print(f"\nReport saved to {args.output}")

        exit_code = get_exit_code(overall_status)

        logger.info(
            "System health check completed: status=%s, exit_code=%s",
            overall_status,
            exit_code,
        )

        sys.exit(exit_code)

    except RuntimeError as error:
        logger.error(
            "System health check failed: %s",
            error,
        )

        print(
            f"Error: {error}",
            file=sys.stderr,
        )

        sys.exit(3)

    except KeyboardInterrupt:
        logger.warning("System health check interrupted by user")

        print(
            "\nSystem health check interrupted.",
            file=sys.stderr,
        )

        sys.exit(130)


if __name__ == "__main__":
    main()