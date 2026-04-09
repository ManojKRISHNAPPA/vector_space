#!/usr/bin/env python3
"""
Server CPU Utilization Monitor
Generates HTML email alerts when CPU usage exceeds threshold
"""

import psutil
import datetime
import socket
from pathlib import Path

class CPUMonitor:
    def __init__(self, threshold=80):
        self.threshold = threshold
        self.hostname = socket.gethostname()
        
    def get_cpu_info(self):
        """Get detailed CPU information"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Per-core usage
        per_core = psutil.cpu_percent(interval=1, percpu=True)
        
        # Memory info (additional useful metric)
        memory = psutil.virtual_memory()
        
        return {
            'total_percent': cpu_percent,
            'per_core': per_core,
            'cpu_count': cpu_count,
            'memory_percent': memory.percent,
            'memory_used': memory.used / (1024**3),  # GB
            'memory_total': memory.total / (1024**3),  # GB
            'timestamp': datetime.datetime.now()
        }
    
    def get_top_processes(self, count=5):
        """Get top CPU consuming processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:count]
    
    def generate_html_report(self):
        """Generate HTML email-friendly report"""
        cpu_info = self.get_cpu_info()
        top_processes = self.get_top_processes()
        alert_level = 'critical' if cpu_info['total_percent'] > 90 else 'warning'
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server CPU Alert</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 8px;
        }}
        
        .header p {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .alert-badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 12px;
            letter-spacing: 0.5px;
            margin-top: 12px;
        }}
        
        .alert-badge.critical {{
            background-color: #ff4757;
            color: white;
        }}
        
        .alert-badge.warning {{
            background-color: #ffa502;
            color: white;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .info-box {{
            background-color: #f8f9fa;
            padding: 15px;
            border-left: 4px solid #667eea;
            margin-bottom: 24px;
            border-radius: 4px;
        }}
        
        .info-box p {{
            margin: 6px 0;
            font-size: 13px;
            color: #555;
        }}
        
        .info-box strong {{
            color: #333;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 24px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 6px;
            text-align: center;
        }}
        
        .metric-card.memory {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        
        .metric-value {{
            font-size: 32px;
            font-weight: bold;
            margin: 8px 0;
        }}
        
        .metric-label {{
            font-size: 12px;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background-color: rgba(255, 255, 255, 0.3);
            border-radius: 4px;
            margin-top: 8px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background-color: white;
            border-radius: 4px;
            transition: width 0.3s ease;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 16px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
        }}
        
        .cpu-cores {{
            background-color: #f8f9fa;
            padding: 16px;
            border-radius: 6px;
            margin-bottom: 24px;
        }}
        
        .core-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            font-size: 13px;
        }}
        
        .core-item:last-child {{
            margin-bottom: 0;
        }}
        
        .core-bar {{
            flex: 1;
            height: 6px;
            background-color: #e0e0e0;
            border-radius: 3px;
            margin: 0 12px;
            overflow: hidden;
        }}
        
        .core-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }}
        
        .processes-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        
        .processes-table th {{
            background-color: #f0f0f0;
            font-weight: 600;
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #ddd;
        }}
        
        .processes-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #eee;
        }}
        
        .processes-table tr:hover {{
            background-color: #f8f9fa;
        }}
        
        .footer {{
            background-color: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            font-size: 12px;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}
        
        .timestamp {{
            color: #999;
            font-size: 11px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚠️ CPU Alert</h1>
            <p>Server: {self.hostname}</p>
            <span class="alert-badge {alert_level}">
                {alert_level.upper()} - {cpu_info['total_percent']:.1f}%
            </span>
        </div>
        
        <div class="content">
            <div class="info-box">
                <p><strong>Alert Time:</strong> {cpu_info['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Threshold:</strong> {self.threshold}%</p>
                <p><strong>Current Usage:</strong> {cpu_info['total_percent']:.1f}%</p>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">CPU Usage</div>
                    <div class="metric-value">{cpu_info['total_percent']:.1f}%</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {cpu_info['total_percent']}%"></div>
                    </div>
                </div>
                
                <div class="metric-card memory">
                    <div class="metric-label">Memory Usage</div>
                    <div class="metric-value">{cpu_info['memory_percent']:.1f}%</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {cpu_info['memory_percent']}%"></div>
                    </div>
                </div>
            </div>
            
            <div class="info-box">
                <p><strong>Memory:</strong> {cpu_info['memory_used']:.2f}GB / {cpu_info['memory_total']:.2f}GB</p>
                <p><strong>CPU Cores:</strong> {cpu_info['cpu_count']}</p>
            </div>
            
            <div class="section-title">Per-Core Usage</div>
            <div class="cpu-cores">
"""
        
        for idx, core_usage in enumerate(cpu_info['per_core']):
            html += f"""
                <div class="core-item">
                    <span>Core {idx}</span>
                    <div class="core-bar">
                        <div class="core-bar-fill" style="width: {core_usage}%"></div>
                    </div>
                    <span style="min-width: 40px; text-align: right;">{core_usage:.1f}%</span>
                </div>
"""
        
        html += """
            </div>
            
            <div class="section-title">Top Processes</div>
            <table class="processes-table">
                <thead>
                    <tr>
                        <th>Process Name</th>
                        <th>PID</th>
                        <th>CPU %</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for proc in top_processes:
            html += f"""
                    <tr>
                        <td>{proc['name']}</td>
                        <td>{proc['pid']}</td>
                        <td>{proc['cpu_percent']:.1f}%</td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p style="margin-bottom: 8px;">This is an automated alert from your monitoring system</p>
            <p class="timestamp">Generated at: """ + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def is_high_cpu(self):
        """Check if CPU usage exceeds threshold"""
        cpu_percent = psutil.cpu_percent(interval=1)
        return cpu_percent > self.threshold
    
    def save_html_report(self, filename='cpu_alert.html'):
        """Save HTML report to file"""
        html = self.generate_html_report()
        with open(filename, 'w') as f:
            f.write(html)
        print(f"Report saved to {filename}")
        return filename


if __name__ == "__main__":
    monitor = CPUMonitor(threshold=80)
    
    # Generate and save report
    report_file = monitor.save_html_report('cpu_alert.html')
    print(f"✓ HTML report generated: {report_file}")
    
    # Check CPU status
    if monitor.is_high_cpu():
        print("⚠️  High CPU usage detected!")
    else:
        print("✓ CPU usage is normal")
