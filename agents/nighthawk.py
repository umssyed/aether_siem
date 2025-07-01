import psutil
import time

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

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


def main():
    print("🦉 NightWatcher v1.0 is running... Press Ctrl+C to stop.\n")
    while True:
        initialize_cpu_tracking()
        time.sleep(0.1)

        watch_processes()
        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
