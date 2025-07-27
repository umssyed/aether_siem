from datetime import datetime
import socket
import requests

import psutil
import time

#AETHER SIEM SERVER
AETHER_SIEM = "http://localhost:5000/log"

# Threshold
CPU_THRESHOLD = 50.0
MEM_THRESHOLD = 2000
SCAN_INTERVAL = 1

def create_alert(app_name, cpu_percent, mem, error):
    alert = {}
    if error == "cpu":
        print(f"🚨 ALERT: {app_name}")
        print(f"   CPU Usage: {cpu_percent:.2f}%")
        print(f"   Memory: {mem:.2f} MB")
        print("-" * 40)

        # Setup alert in JSON format to send off
        alert = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hostname": socket.gethostname(),
            "app_name": app_name,
            "cpu_percentage": cpu_percent,
            "memory": mem,
            "reason": "🖥️ High CPU usage"
        }
    elif error == "mem":
        print(f"🚨 ALERT: {app_name}")
        print(f"   CPU Usage: {cpu_percent:.2f}%")
        print(f"   Memory: {mem:.2f} MB")
        print("-" * 40)

        # Setup alert in JSON format to send off
        alert = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hostname": socket.gethostname(),
            "app_name": app_name,
            "cpu_percentage": cpu_percent,
            "memory": mem,
            "reason": "🔥 High memory usage"
        }
    return alert

def send_alert(alert):
    # Send alert response to AETHER SIEM
    try:
        response = requests.post(AETHER_SIEM, json=alert)
        print(f"✔ Alert sent!")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

def watch_processes(app_usage):
    num_cores = psutil.cpu_count(logical=True)
    cnt = 0
    for process in psutil.process_iter(['pid', 'ppid', 'name', 'exe',
                                        'cpu_percent', 'memory_info']):
        cnt = cnt + 1
        try:
            # Process Details
            process_name = process.info['name'] or "Unknown"
            process_pid = process.info['pid']
            process_ppid = process.info['ppid']
            process_path = process.info['exe'] or "Unknown"

            # CPU and Memory
            raw_cpu_percent = process.cpu_percent(interval=None)
            cpu_percent = raw_cpu_percent/num_cores
            mem = process.memory_info().rss / (1024 * 1024)

            if process_name not in app_usage:
                app_usage[process_name] = {"cpu": 0.0, "mem": 0.0, "updated": True}

            if cpu_percent > app_usage[process_name]["cpu"] or mem > app_usage[process_name]["mem"]:
                app_usage[process_name]["cpu"] = cpu_percent
                app_usage[process_name]["mem"] = mem
                app_usage[process_name]["updated"] = True

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


    # Evaluate all the apps/processes
    for app_name, usage in app_usage.items():

        if usage["updated"]:
            if usage["cpu"] > CPU_THRESHOLD:
                alert = create_alert(app_name, usage["cpu"], usage["mem"], "cpu")
                send_alert(alert)
                usage["updated"] = False
            elif usage["mem"] > MEM_THRESHOLD:
                alert = create_alert(app_name, usage["cpu"], usage["mem"], "mem")
                send_alert(alert)
                usage["updated"] = False



def main():
    print("🦉 NightWatcher v1.0 is running... Press Ctrl+C to stop.\n")
    app_usage = {}
    while True:
        watch_processes(app_usage)
        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
