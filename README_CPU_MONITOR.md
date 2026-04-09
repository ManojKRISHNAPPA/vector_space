# Server CPU Monitoring & Alert System

A complete system for monitoring server CPU utilization and sending professional HTML email alerts.

## 📋 Project Files

### 1. **cpu_monitor.py** - Python CPU Monitor (Recommended)
Advanced monitoring script with detailed metrics and automatic HTML generation.

#### Features:
- Real-time CPU monitoring with per-core breakdown
- Memory usage tracking
- Top 5 CPU-consuming processes
- Professional HTML email template generation
- Customizable CPU threshold

#### Installation:
```bash
pip install psutil
```

#### Usage:
```bash
# Generate HTML report
python3 cpu_monitor.py

# This creates: cpu_alert.html

# Use with custom threshold (default is 80%)
python3 cpu_monitor.py --threshold 85
```

#### Example Integration - Cron Job:
```bash
# Add to crontab to check every 5 minutes
*/5 * * * * /usr/bin/python3 /path/to/cpu_monitor.py && if grep -q "critical" cpu_alert.html; then mail -s "🚨 CRITICAL: High CPU Alert" admin@example.com < cpu_alert.html; fi
```

---

### 2. **cpu_check.sh** - Bash CPU Checker (Simple)
Lightweight bash script for quick CPU checks.

#### Features:
- Minimal dependencies
- Quick CPU and memory overview
- Top 5 processes listing
- Optional email alerts
- No external dependencies (except mail utility)

#### Usage:
```bash
chmod +x cpu_check.sh

# Basic check (80% threshold)
./cpu_check.sh

# Custom threshold
./cpu_check.sh 85

# With email alerts (edit script to add email)
./cpu_check.sh 75
```

#### Example Cron Job:
```bash
# Every 10 minutes
*/10 * * * * /path/to/cpu_check.sh >> /var/log/cpu_monitor.log 2>&1
```

---

### 3. **cpu_alert_template.html** - Email Template
Standalone HTML email template with beautiful design. Use for manual customization or email service integration.

#### Features:
- Responsive design (works on all devices)
- Professional gradient styling
- Color-coded alerts (critical, warning, normal)
- Metrics dashboard
- Process listing table
- Recommendations section
- Email-safe CSS (no external dependencies)

#### Usage in Your Code:
```python
# Send via email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

html_content = open('cpu_alert_template.html').read()

msg = MIMEMultipart("alternative")
msg["Subject"] = "🚨 High CPU Alert"
msg["From"] = "monitor@example.com"
msg["To"] = "admin@example.com"

msg.attach(MIMEText(html_content, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login("your-email@gmail.com", "your-password")
    server.sendmail("monitor@example.com", "admin@example.com", msg.as_string())
```

---

## 🚀 Quick Start Guide

### Option 1: Using Python Monitor (Best)
```bash
# Install dependency
pip install psutil

# Run monitor
python3 cpu_monitor.py

# Check the generated HTML
open cpu_alert.html

# Set up continuous monitoring with cron
# Edit crontab:
crontab -e

# Add line:
*/5 * * * * python3 /path/to/cpu_monitor.py
```

### Option 2: Using Bash Script (Lightweight)
```bash
# Make executable
chmod +x cpu_check.sh

# Run directly
./cpu_check.sh 85

# For email alerts, edit the script and set EMAIL_TO variable
```

### Option 3: Using HTML Template (Custom)
- Edit `cpu_alert_template.html` with your server details
- Use in your alert system or email service
- See "Usage in Your Code" section above

---

## 📊 Alert Levels

| Level | CPU Range | Badge Color | Action |
|-------|-----------|-------------|--------|
| Normal | < 70% | Green | Monitor |
| Warning | 70-85% | Orange | Review |
| Critical | > 85% | Red | Immediate |

---

## 🔧 Advanced Configuration

### Combined Email System (Python):
```python
from cpu_monitor import CPUMonitor
import smtplib
from email.mime.text import MIMEText

monitor = CPUMonitor(threshold=80)

if monitor.is_high_cpu():
    html = monitor.generate_html_report()
    
    # Send email
    msg = MIMEText(html, 'html')
    msg['Subject'] = '⚠️ High CPU Alert'
    msg['From'] = 'alerts@your-domain.com'
    msg['To'] = 'admin@your-domain.com'
    
    server = smtplib.SMTP('localhost')
    server.send_message(msg)
    server.quit()
```

### Multiple Server Monitoring:
Create a wrapper script:
```bash
#!/bin/bash
SERVERS=("server1" "server2" "server3")
for server in "${SERVERS[@]}"; do
    ssh $server "python3 cpu_monitor.py"
done
```

---

## 📈 Monitoring with Cron

### Every 5 Minutes:
```bash
*/5 * * * * python3 /path/to/cpu_monitor.py >> /var/log/cpu_monitor.log 2>&1
```

### Every Hour:
```bash
0 * * * * /path/to/cpu_check.sh >> /var/log/cpu_check.log 2>&1
```

### During Business Hours Only:
```bash
0 8-18 * * MON-FRI python3 /path/to/cpu_monitor.py
```

---

## 🎨 HTML Email Customization

Edit these sections in the HTML template:

**Header Color** (Line ~67):
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**Alert Threshold**:
```html
<p><strong>Threshold:</strong> 80%</p>
```

**Server Name**:
```html
<p>Server: your-server-name</p>
```

---

## 📧 Email Integration Examples

### Gmail SMTP:
```python
import smtplib
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login('your-email@gmail.com', 'app-password')
    smtp.sendmail('from@gmail.com', 'to@example.com', message)
```

### SendGrid:
```bash
curl --request POST \
  --url https://api.sendgrid.com/v3/mail/send \
  --header "Authorization: Bearer YOUR_SENDGRID_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"personalizations":[{"to":[{"email":"admin@example.com"}]}],"from":{"email":"alerts@your-domain.com"},"subject":"CPU Alert","content":[{"type":"text/html","value":"<html>..."}]}'
```

---

## 🐛 Troubleshooting

### psutil not found:
```bash
pip install psutil
```

### Permission denied on bash script:
```bash
chmod +x cpu_check.sh
```

### Mail command not found:
```bash
# Ubuntu/Debian
sudo apt-get install mailutils

# macOS
brew install mailutils
```

### High false positives:
- Increase threshold in cpu_monitor.py or script
- Check for scheduled maintenance tasks
- Review application workload patterns

---

## 📝 License
Free to use and modify

---

## 💡 Pro Tips

1. **Test Before Deployment**: Run scripts manually to verify output
2. **Use Proper Error Handling**: Set up logs to track all alerts
3. **Archive Old Reports**: Keep historical data for trend analysis
4. **Slack Integration**: Use webhooks to send alerts to Slack instead of email
5. **Multiple Thresholds**: Set different thresholds for different servers
6. **Alerting**: Use tools like PagerDuty or OpsGenie for escalation

---

Created: 2024-01-15
Last Updated: 2024-01-15
