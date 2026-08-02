# Testing Strategy

SysHealth uses `pytest` for automated testing.

The test suite focuses on verifying application behavior without depending on the current machine's real CPU, memory, disk, process, or operating-system state.

System-level dependencies are mocked where necessary so tests remain:

- deterministic
- repeatable
- fast
- independent of the host operating system
- suitable for local development and CI/CD pipelines

---

## utils.py

### Purpose

Verify that shared helper functions produce correct and predictable results.

### Functions Tested

- `get_status()`
- `bytes_to_gb()`
- `log_health_status()` where applicable

### Behaviors Verified

- Usage below the warning threshold returns `HEALTHY`.
- Usage at or above the warning threshold returns `WARNING`.
- Usage at or above the critical threshold returns `CRITICAL`.
- Invalid threshold combinations raise `ValueError`.
- Byte values are converted correctly into gigabytes.

### Why These Tests Matter

These helper functions are reused by CPU, memory, and disk modules. A defect in this logic could produce incorrect health classifications across the entire application.

---

## memory.py

### Purpose

Verify that memory information is collected, converted, and classified correctly.

### External Dependency

- `psutil.virtual_memory()`

### Mocking Strategy

`psutil.virtual_memory()` is patched to return a controlled fake memory object.

Example fake values:

- total memory
- used memory
- available memory
- usage percentage

### Behaviors Verified

- Byte values are converted correctly into gigabytes.
- Memory usage percentage is returned correctly.
- Health status is calculated using configured warning and critical thresholds.
- The result contains all expected fields.

### Why Mocking Is Required

Real memory usage changes continuously and differs between systems. A unit test should not fail because the developer opened another application or because the test runs on a machine with different RAM capacity.

---

## cpu.py

### Purpose

Verify that CPU usage, core counts, load averages, and health status are collected correctly.

### External Dependencies

- `psutil.cpu_percent()`
- `psutil.cpu_count()`
- `os.getloadavg()`

### Mocking Strategy

Each external function is patched with predictable values.

`psutil.cpu_count()` is called twice:

- once for logical cores
- once for physical cores

A mock `side_effect` is used to return different values for each call.

### Behaviors Verified

- CPU usage percentage is returned correctly.
- Logical core count is returned correctly.
- Physical core count is returned correctly.
- Load averages are returned correctly.
- CPU health status is calculated from configured thresholds.
- High CPU usage produces a `CRITICAL` status where tested.

### Why Mocking Is Required

CPU utilization and system load change constantly. Tests must use controlled values so results are consistent on every machine and in CI/CD environments.

---

## disk.py

### Purpose

Verify that disk information is collected, converted, and classified correctly.

### External Dependency

- `psutil.disk_usage()`

### Mocking Strategy

`psutil.disk_usage()` is patched to return a fake disk object containing:

- total bytes
- used bytes
- free bytes
- usage percentage

### Behaviors Verified

- Disk size values are converted correctly into gigabytes.
- The monitored path is included in the result.
- Disk usage percentage is returned correctly.
- Health status is calculated correctly.
- Invalid or inaccessible paths return `UNKNOWN` instead of crashing the application.

### Why Mocking Is Required

Disk capacity and utilization differ across machines. Some paths may also be unavailable depending on operating-system permissions and filesystem structure.

---

## process.py

### Purpose

Verify that process information is collected, sorted, limited, and handled safely.

### External Dependencies

- `psutil.process_iter()`
- `psutil.pids()`

### Mocking Strategy

Fake process objects are created with controlled `info` dictionaries containing:

- PID
- process name
- CPU percentage
- memory percentage

Special fake process classes are used to raise operating-system-related exceptions when their `info` property is accessed.

### Behaviors Verified

- Total process count is returned correctly.
- Processes are sorted by memory usage in descending order.
- Only the requested number of top processes is returned.
- Processes that raise `AccessDenied` are skipped.
- Zombie processes are skipped.
- One inaccessible process does not terminate the entire health check.

### Special Cases

- `psutil.AccessDenied`
- `psutil.ZombieProcess`
- `psutil.NoSuchProcess`, where applicable

### Why These Tests Matter

Processes can disappear or become inaccessible while the system is being inspected. The collector must continue safely instead of failing the complete report.

---

## system.py

### Purpose

Verify that operating-system information and uptime formatting are returned correctly.

### Functions Tested

- `get_system_info()`
- `format_uptime()`

### External Dependencies

- `socket.gethostname()`
- `platform.system()`
- `platform.release()`
- `platform.machine()`
- `platform.python_version()`
- `psutil.boot_time()`
- `datetime.now()`

### Mocking Strategy

Platform and hostname functions are patched with predictable values.

The uptime formatting function is tested separately using a known `timedelta`.

### Behaviors Verified

- Hostname is returned correctly.
- Operating-system name is returned correctly.
- Operating-system version is returned correctly.
- Architecture is returned correctly.
- Python version is returned correctly.
- Uptime is converted into a readable string containing days, hours, and minutes.

### Why Mocking Is Required

System details vary between Linux, macOS, Windows, local machines, and CI/CD runners. Controlled values keep the tests platform-independent.

---

## config.py

### Purpose

Verify that application configuration is loaded correctly and common file-related failures are handled safely.

### External Dependencies

- Filesystem access through `open()`
- JSON parsing through `json.load()`

### Testing Strategy

Real temporary files are created with pytest's `tmp_path` fixture for valid and malformed configuration tests.

`open()` is mocked for permission-related tests.

### Behaviors Verified

- Valid JSON configuration is loaded and returned.
- Missing configuration files raise a controlled `RuntimeError`.
- Invalid JSON raises a controlled `RuntimeError`.
- Permission errors raise a controlled `RuntimeError`.
- Low-level exceptions are translated into meaningful application errors.

### Why Temporary Files Are Used

Temporary files test the real file-reading and JSON-parsing behavior without creating permanent files inside the repository.

---

## Test Organization

Tests are stored in the `tests/` directory.

```text
tests/
├── test_config.py
├── test_cpu.py
├── test_disk.py
├── test_memory.py
├── test_process.py
├── test_system.py
└── test_utils.py