from flask import Flask, jsonify, Response
import psutil
import threading
import socket
import platform
import datetime

app = Flask(__name__)

# =========================
# SYSTEM METRICS API
# =========================
@app.route("/metrics")
def metrics():

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()

    return jsonify({
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "cpu": cpu,
        "memory": memory.percent,
        "disk": disk.percent,
        "threads": threading.active_count(),
        "processes": len(psutil.pids()),
        "upload": net.bytes_sent // (1024*1024),
        "download": net.bytes_recv // (1024*1024)
    })


# =========================
# DASHBOARD UI
# =========================
@app.route("/")
def dashboard():

    html = """
<!DOCTYPE html>
<html>
<head>
<title>🚀 Jenkins Production Monitoring</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{
background:#020617;
color:white;
font-family:Arial;
margin:0;
}

header{
background:#0f172a;
padding:15px;
text-align:center;
font-size:24px;
font-weight:bold;
color:#38bdf8;
}

.grid{
display:grid;
grid-template-columns:repeat(3,1fr);
gap:20px;
padding:20px;
}

.card{
background:#0f172a;
padding:20px;
border-radius:12px;
box-shadow:0 0 10px #000;
}

h3{margin-top:0;}

canvas{height:220px;}

.info{
padding:15px;
text-align:center;
font-size:18px;
}

</style>
</head>

<body>

<header>🚀 Jenkins Live System Monitoring Dashboard</header>

<div class="info" id="sysinfo">Loading...</div>

<div class="grid">

<div class="card">
<h3>CPU Usage</h3>
<canvas id="cpu"></canvas>
</div>

<div class="card">
<h3>Memory Usage</h3>
<canvas id="memory"></canvas>
</div>

<div class="card">
<h3>Disk Usage</h3>
<canvas id="disk"></canvas>
</div>

<div class="card">
<h3>Active Threads</h3>
<canvas id="threads"></canvas>
</div>

<div class="card">
<h3>Network Traffic</h3>
<canvas id="network"></canvas>
</div>

<div class="card">
<h3>Running Processes</h3>
<canvas id="process"></canvas>
</div>

</div>

<script>

const cpuChart=new Chart(document.getElementById("cpu"),{
type:"line",
data:{labels:[],datasets:[{label:"CPU %",data:[]}]}
});

const memoryChart=new Chart(document.getElementById("memory"),{
type:"bar",
data:{labels:["Memory"],datasets:[{data:[0]}]}
});

const diskChart=new Chart(document.getElementById("disk"),{
type:"doughnut",
data:{labels:["Used","Free"],datasets:[{data:[0,100]}]}
});

const threadChart=new Chart(document.getElementById("threads"),{
type:"bar",
data:{labels:["Threads"],datasets:[{data:[0]}]}
});

const networkChart=new Chart(document.getElementById("network"),{
type:"line",
data:{labels:[],datasets:[
{label:"Upload(MB)"},
{label:"Download(MB)"}
]}
});

const processChart=new Chart(document.getElementById("process"),{
type:"pie",
data:{labels:["Processes"],datasets:[{data:[0]}]}
});

async function fetchMetrics(){

let res=await fetch("/metrics");
let d=await res.json();

document.getElementById("sysinfo").innerHTML=
`Host: ${d.hostname} | OS: ${d.os} | Time: ${d.time}`;

/* CPU */
cpuChart.data.labels.push("");
cpuChart.data.datasets[0].data.push(d.cpu);
if(cpuChart.data.labels.length>15){
cpuChart.data.labels.shift();
cpuChart.data.datasets[0].data.shift();
}
cpuChart.update();

/* Memory */
memoryChart.data.datasets[0].data=[d.memory];
memoryChart.update();

/* Disk */
diskChart.data.datasets[0].data=[d.disk,100-d.disk];
diskChart.update();

/* Threads */
threadChart.data.datasets[0].data=[d.threads];
threadChart.update();

/* Network */
networkChart.data.labels.push("");
networkChart.data.datasets[0].data.push(d.upload);
networkChart.data.datasets[1].data.push(d.download);

if(networkChart.data.labels.length>15){
networkChart.data.labels.shift();
networkChart.data.datasets[0].data.shift();
networkChart.data.datasets[1].data.shift();
}
networkChart.update();

/* Processes */
processChart.data.datasets[0].data=[d.processes];
processChart.update();

}

setInterval(fetchMetrics,2000);

</script>

</body>
</html>
"""
    return Response(html, mimetype="text/html")


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)