import datetime
import socket
import requests

import psutil
import time

#AETHER SIEM SERVER
AETHER_SIEM = "http://localhost:5000/log"

# Threshold
CPU_THRESHOLD = 90.0
MEM_THRESHOLD = 300
SCAN_INTERVAL = 10


def initialize_cpu_tracking():
    for process in psutil.process_iter(['pid', 'name']):
        try:
            process.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


def watch_processes():
    for process in psutil.process_iter(['pid', 'name']):
        try:
            pid = process.info['pid']
            process_name = process.info['name']
            cpu_percent = process.cpu_percent(interval=None)
            mem = process.memory_info().rss / (1024 * 1024)

            if cpu_percent > CPU_THRESHOLD or mem > MEM_THRESHOLD:
                print(f"🚨 ALERT: {process_name} (PID: {pid})")
                print(f"   CPU Usage: {cpu_percent:.2f}%")
                print(f"   Memory: {mem:.2f} MB")
                print("-" * 40)

                # Setup alert in JSON format to send off
                alert = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "hostname": socket.gethostname(),
                    "pid": pid,
                    "processName": process_name,
                    "cpu_percentage": cpu_percent,
                    "memory": mem
                }

                # Send response to AETHER
                try:
                    response = requests.post(AETHER_SIEM, json=alert)
                except Exception as e:
                    print(f"❌ Failed to send alert: {e}")

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


def main():
    print("🦉 NightWatcher v1.0 is running... Press Ctrl+C to stop.\n")
    while True:
        initialize_cpu_tracking()
        time.sleep(10)

        watch_processes()
        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
