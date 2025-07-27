import os
from datetime import datetime
from dotenv import load_dotenv
import socket
import requests
import psutil
import time


load_dotenv()
# SUPABASE KEY
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
SUPABASE_URL: str =  os.getenv("SUPABASE_URL")


#AETHER SIEM SERVER LOCAL
AETHER_SIEM = "http://localhost:5000/log"

# Threshold
CPU_THRESHOLD = 50.0
MEM_THRESHOLD = 2000
SCAN_INTERVAL = 1

def create_alert(app_name, cpu_percent, mem, error):
    alert = {}
    if error == "cpu":
        #print(f"🚨 ALERT: {app_name}")
        #print(f"   CPU Usage: {cpu_percent:.2f}%")
        #print(f"   Memory: {mem:.2f} MB")
        #print("-" * 40)

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
        #print(f"🚨 ALERT: {app_name}")
        #print(f"   CPU Usage: {cpu_percent:.2f}%")
        #print(f"   Memory: {mem:.2f} MB")
        #print("-" * 40)

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
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": SUPABASE_KEY
    }

    # Send alert response to AETHER SIEM
    try:
        response = requests.post(AETHER_SIEM, json=alert, headers=headers)
        print(f"✔ Alert sent!")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

def watch_processes():
    app_usage = {}
    num_cores = psutil.cpu_count(logical=True)
    cnt = 0
    for process in psutil.process_iter(['pid', 'ppid', 'name', 'exe',
                                        'cpu_percent', 'memory_info']):
        cnt = cnt + 1
        try:
            # Process Details
            process_name = process.info['name'] or "Unknown"

            # CPU and Memory
            raw_cpu_percent = process.cpu_percent(interval=None)
            cpu_percent = raw_cpu_percent/num_cores
            mem = process.memory_info().rss / (1024 * 1024)

            if process_name not in app_usage:
                app_usage[process_name] = {"cpu": 0.0, "mem": 0.0}

            app_usage[process_name]["cpu"] += cpu_percent
            app_usage[process_name]["mem"] += mem

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


    # Evaluate all the apps/processes
    for app_name, usage in app_usage.items():
        if usage["cpu"] > CPU_THRESHOLD:
            alert = create_alert(app_name, usage["cpu"], usage["mem"], "cpu")
            send_alert(alert)

        elif usage["mem"] > MEM_THRESHOLD:
            alert = create_alert(app_name, usage["cpu"], usage["mem"], "mem")
            send_alert(alert)




def main():
    print("🦉 NightWatcher v1.0 is running... Press Ctrl+C to stop.\n")

    while True:
        watch_processes()
        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
