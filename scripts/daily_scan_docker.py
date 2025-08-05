import subprocess
import platform
import json
import os
import pandas as pd

# Path to Excel IP list file
IP_FILE = os.path.join("data", "IP_List.xlsx")

def load_ips():
    if not os.path.exists(IP_FILE):
        raise FileNotFoundError(f"IP list file not found: {IP_FILE}")

    try:
        df = pd.read_excel(IP_FILE)
        # Normalize column names
        df.columns = [c.strip().lower() for c in df.columns]

        # Detect name and IP columns
        name_col = None
        ip_col = None
        for col in df.columns:
            if "name" in col:
                name_col = col
            if "ip" in col:
                ip_col = col

        if not name_col or not ip_col:
            raise ValueError(f"Expected columns containing 'Name' and 'IP' in {IP_FILE}")

        ips = []
        for _, row in df.iterrows():
            name = str(row[name_col]).strip()
            ip = str(row[ip_col]).strip()
            if name and ip:
                ips.append({"name": name, "ip": ip})

        if not ips:
            raise ValueError(f"No valid IPs found in {IP_FILE}")

        return ips
    except Exception as e:
        raise ValueError(f"Error reading IP list from {IP_FILE}: {e}")

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

    with open("/tmp/scan_results.json", "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    run_scan()
