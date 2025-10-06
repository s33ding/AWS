#!/usr/bin/env python3

import subprocess
import json
import time
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
from collections import deque
import os

# Data storage
timestamps = deque(maxlen=30)
cpu_totals = deque(maxlen=30)
cpu_user = deque(maxlen=30)
cpu_system = deque(maxlen=30)
cpu_nice = deque(maxlen=30)
cpu_wait = deque(maxlen=30)

def get_cpu_data():
    """Fetch CPU data from RDS Performance Insights or generate fake data"""
    resource_id = os.environ.get("RDS_ID", None)
    
    # Generate fake data if no RDS_ID is set
    if not resource_id:
        import random
        return {
            "os.cpuUtilization.user.avg": random.uniform(10, 40),
            "os.cpuUtilization.system.avg": random.uniform(5, 20),
            "os.cpuUtilization.nice.avg": random.uniform(0, 5),
            "os.cpuUtilization.wait.avg": random.uniform(0, 15)
        }
    
    # Get time window
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=1)
    start_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # CPU metrics
    cpu_metrics = [
        "os.cpuUtilization.user.avg",
        "os.cpuUtilization.system.avg",
        "os.cpuUtilization.nice.avg",
        "os.cpuUtilization.wait.avg"
    ]
    
    # AWS CLI command
    metric_queries = [{"Metric": metric} for metric in cpu_metrics]
    command = [
        "aws", "pi", "get-resource-metrics",
        "--service-type", "RDS",
        "--identifier", resource_id,
        "--metric-queries", json.dumps(metric_queries),
        "--start-time", start_str,
        "--end-time", end_str,
        "--period-in-seconds", "60",
        "--region", "us-east-1"
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return None
            
        output = json.loads(result.stdout)
        metric_data = output.get("MetricList", [])
        
        breakdown = {}
        for metric in metric_data:
            metric_name = metric["Key"]["Metric"]
            if metric["DataPoints"]:
                latest_dp = sorted(metric["DataPoints"], key=lambda d: d["Timestamp"])[-1]
                value = latest_dp["Value"]
                breakdown[metric_name] = value
        
        return breakdown
    except:
        return None

def update_data():
    """Update data collections with new CPU metrics"""
    data = get_cpu_data()
    if not data:
        return False
        
    current_time = datetime.now().strftime("%H:%M:%S")
    timestamps.append(current_time)
    
    user = data.get("os.cpuUtilization.user.avg", 0)
    system = data.get("os.cpuUtilization.system.avg", 0)
    nice = data.get("os.cpuUtilization.nice.avg", 0)
    wait = data.get("os.cpuUtilization.wait.avg", 0)
    
    cpu_user.append(user)
    cpu_system.append(system)
    cpu_nice.append(nice)
    cpu_wait.append(wait)
    cpu_totals.append(user + system + nice + wait)
    
    return True

def plot_data():
    """Create live plot of CPU data"""
    plt.clf()
    
    if not timestamps:
        plt.text(0.5, 0.5, 'Waiting for data...', ha='center', va='center')
        return
    
    # Create subplots
    plt.subplot(2, 1, 1)
    plt.plot(list(timestamps), list(cpu_totals), 'b-', linewidth=2, label='Total CPU')
    plt.title('RDS CPU Usage - Total')
    plt.ylabel('CPU %')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    
    plt.subplot(2, 1, 2)
    plt.plot(list(timestamps), list(cpu_user), 'r-', label='User', linewidth=1.5)
    plt.plot(list(timestamps), list(cpu_system), 'g-', label='System', linewidth=1.5)
    plt.plot(list(timestamps), list(cpu_nice), 'orange', label='Nice', linewidth=1.5)
    plt.plot(list(timestamps), list(cpu_wait), 'purple', label='Wait', linewidth=1.5)
    plt.title('RDS CPU Usage - Breakdown')
    plt.ylabel('CPU %')
    plt.xlabel('Time')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    
    plt.tight_layout()

def main():
    """Main plotting loop"""
    plt.ion()
    fig = plt.figure(figsize=(12, 8))
    
    print("Starting RDS CPU live plotting...")
    
    while True:
        if update_data():
            plot_data()
            plt.draw()
            plt.pause(0.1)
        
        time.sleep(60)

if __name__ == "__main__":
    main()
