#!/bin/bash
# Simple CPU Monitoring Script
# Usage: ./cpu_check.sh [threshold]

THRESHOLD=${1:-80}
EMAIL_TO=""  # Add email address if you want to send alerts

# Get CPU usage
CPU_USAGE=$(top -bn1 | grep "CPU usage" | sed "s/.* \([0-9.]*\)%% user.*/\1/" | awk '{print int($1)}')

# Get memory usage
MEMORY_USAGE=$(vm_stat | grep "Pages active" | awk '{print $3}' | sed 's/\.//')

# Get hostname
HOSTNAME=$(hostname)

# Get timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Get top 5 processes
TOP_PROCESSES=$(ps aux --sort=-%cpu | head -6 | tail -5)

# Check if CPU exceeds threshold
if [ "$CPU_USAGE" -gt "$THRESHOLD" ]; then
    echo "⚠️  HIGH CPU ALERT - $CPU_USAGE%"
    echo "Server: $HOSTNAME"
    echo "Time: $TIMESTAMP"
    echo ""
    echo "Top Processes:"
    echo "$TOP_PROCESSES"
    echo ""
    
    # Optional: Send email alert
    if [ ! -z "$EMAIL_TO" ]; then
        echo "Alert: CPU at $CPU_USAGE% on $HOSTNAME" | mail -s "⚠️  High CPU Alert" "$EMAIL_TO"
    fi
else
    echo "✓ CPU Usage Normal: $CPU_USAGE% (Threshold: $THRESHOLD%)"
fi

echo ""
echo "Current Status:"
echo "  CPU:      $CPU_USAGE%"
echo "  Memory:   $MEMORY_USAGE"
echo "  Hostname: $HOSTNAME"
echo "  Time:     $TIMESTAMP"
