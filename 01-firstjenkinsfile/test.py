#!/usr/bin/env python3

import os
import json
import psutil
import socket
from datetime import datetime

print("Current Working Directory:", os.getcwd())
print("Script Location:", os.path.abspath(__file__))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REPORT_FILE = os.path.join(BASE_DIR, "status_report.html")
HISTORY_FILE = os.path.join(BASE_DIR, "status_history.json")


def get_metrics():
    return {
        "time": datetime.utcnow().strftime("%H:%M:%S"),
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "host": socket.gethostname(),
        "build": os.getenv("BUILD_NUMBER", "local"),
        "job": os.getenv("JOB_NAME", "dev")
    }


def load_history():
    if os.path.exists(HISTORY_FILE):
        return json.load(open(HISTORY_FILE))
    return []


def save_history(data):
    json.dump(data[-200:], open(HISTORY_FILE, "w"), indent=2)


def generate_dashboard(history):

    labels = [x["time"] for x in history]
    cpu = [x["cpu"] for x in history]
    mem = [x["memory"] for x in history]
    disk = [x["disk"] for x in history]

    html = f"""
<html>
<head>
<title>Jenkins Live Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<meta http-equiv="refresh" content="10">

<style>
body {{
background:#0f172a;
color:white;
font-family:Arial;
padding:30px;
}}

.card {{
background:#111827;
padding:20px;
border-radius:12px;
margin-bottom:20px;
}}

h1 {{color:#38bdf8}}
</style>
</head>

<body>

<h1>🚀 Jenkins Live Monitoring Dashboard</h1>

<div class="card">
Host: {history[-1]["host"]} |
Job: {history[-1]["job"]} |
Build: {history[-1]["build"]}
</div>

<canvas id="cpu"></canvas>
<canvas id="mem"></canvas>
<canvas id="disk"></canvas>

<script>

const labels = {labels};

new Chart(document.getElementById("cpu"), {{
type:"line",
data:{{labels:labels,datasets:[{{label:"CPU %",data:{cpu}}}]}}
}});

new Chart(document.getElementById("mem"), {{
type:"line",
data:{{labels:labels,datasets:[{{label:"Memory %",data:{mem}}}]}}
}});

new Chart(document.getElementById("disk"), {{
type:"line",
data:{{labels:labels,datasets:[{{label:"Disk %",data:{disk}}}]}}
}});

</script>

</body>
</html>
"""

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("Dashboard generated:", REPORT_FILE)


def main():
    history = load_history()

    metrics = get_metrics()
    history.append(metrics)

    save_history(history)
    generate_dashboard(history)


if __name__ == "__main__":
    main()