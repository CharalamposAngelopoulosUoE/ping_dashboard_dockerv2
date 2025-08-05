import subprocess
import platform
import json
import os

# Path to IP list file
IP_FILE = os.path.join("data", "IP_list")

def load_ips():
    ips = []
    if not os.path.exists(IP_FILE):
        print(f"IP list file not found: {IP_FILE}")
        return ips

    with open(IP_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # skip empty lines or comments
            try:
                name, ip = line.split(",")
                ips.append({"name": name.strip(), "ip": ip.strip()})
            except ValueError:
                print(f"Invalid line in IP list: {line}")
    return ips

def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def run_scan():
    ips = load_ips()
    results = []
    for item in ips:
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
