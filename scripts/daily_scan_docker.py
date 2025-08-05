import subprocess
import platform
import json

# List of IPs (could also be imported from config)
IPS = [
    {"name": "Server1", "ip": "192.168.1.10"},
    {"name": "Server2", "ip": "192.168.1.20"}
]

def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def run_scan():
    results = []
    for item in IPS:
        status = "online" if ping(item["ip"]) else "offline"
        results.append({
            "name": item["name"],
            "ip": item["ip"],
            "status": status
        })
    # Save to temporary json (used by monitor.py)
    with open("/tmp/scan_results.json", "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    run_scan()
