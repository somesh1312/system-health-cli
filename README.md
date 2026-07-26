# SysHealth CLI

A lightweight Python CLI for monitoring Linux system health.

## Features

- CPU utilization and load averages
- Physical and logical CPU information
- Memory monitoring
- Disk utilization
- Process monitoring
- Top memory-consuming processes
- Health thresholds
- File report generation
- CLI arguments
- Exception handling

## Installation

Clone the repository:

git clone ...

Create virtual environment:

python3 -m venv .venv

Activate:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

## Usage

python main.py

python main.py --top 10

python main.py --disk /var

python main.py --output health-report.txt

## Technologies

- Python
- psutil
- Linux
- argparse
- Git