import argparse
import sys
from syshealth.config import load_config
from syshealth.cpu import get_cpu_info
from syshealth.memory import get_memory_info
from syshealth.disk import get_disk_info
from syshealth.process import get_process_info
from syshealth.system import get_system_info


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="System health monitoring CLI"
    )

    parser.add_argument(
        "--disk",
        default="/",
        help="Filesystem path to monitor"
    )

    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of top processes to display"
    )

    parser.add_argument(
        "--output",
        help="Save health report to a file"
    )

    return parser


def generate_report(disk_path: str, top: int) -> str:
    config = load_config()
    system = get_system_info()
    cpu = get_cpu_info(
    warning=config["cpu"]["warning"],
    critical=config["cpu"]["critical"]
)
    memory = get_memory_info(
    warning=config["memory"]["warning"],
    critical=config["memory"]["critical"]
)
    disk = get_disk_info(
    path=disk_path,
    warning=config["disk"]["warning"],
    critical=config["disk"]["critical"]
)
    process_data = get_process_info(top)

    lines: list[str] = []

    lines.append("=" * 55)
    lines.append("SYSTEM HEALTH REPORT")
    lines.append("=" * 55)

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

    load = cpu["load_average"]

    lines.append(
        f"Load Average   : "
        f"{load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}"
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

    overall_status = calculate_overall_status(
        cpu["status"],
        memory["status"],
        disk["status"]
    )

    lines.append("")
    lines.append("=" * 55)
    lines.append(f"OVERALL STATUS: {overall_status}")
    lines.append("=" * 55)

    return "\n".join(lines)


def calculate_overall_status(*statuses: str) -> str:

    if "CRITICAL" in statuses:
        return "CRITICAL"

    if "WARNING" in statuses:
        return "WARNING"

    if "UNKNOWN" in statuses:
        return "UNKNOWN"

    return "HEALTHY"


def save_report(report: str, filename: str) -> None:

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(report)

    except PermissionError:
        print(
            f"Error: No permission to write to {filename}",
            file=sys.stderr
        )

        sys.exit(1)

    except OSError as error:
        print(
            f"Error writing report: {error}",
            file=sys.stderr
        )

        sys.exit(1)


def main() -> None:

    parser = create_parser()

    args = parser.parse_args()

    report = generate_report(
        disk_path=args.disk,
        top=args.top
    )

    print(report)

    if args.output:
        save_report(report, args.output)

        print(f"\nReport saved to {args.output}")


if __name__ == "__main__":
    main()