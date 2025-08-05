from flask import Flask, render_template_string
import json
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Load latest scan results
    data_file = "/tmp/scan_results.json"
    if os.path.exists(data_file):
        with open(data_file) as f:
            results = json.load(f)
    else:
        results = []
    # Render simple HTML
    html = "<h1>Ping Dashboard (Docker)</h1><table border='1'><tr><th>Name</th><th>IP</th><th>Status</th></tr>"
    for r in results:
        color = "green" if r['status']=="online" else "red"
        html += f"<tr><td>{r['name']}</td><td>{r['ip']}</td><td style='color:{color}'>{r['status']}</td></tr>"
    html += "</table>"
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
