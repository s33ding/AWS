#!/usr/bin/env python3

import subprocess
import json
import time
import logging
import sys
from datetime import datetime, timedelta, timezone
import os

# Configure logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
)

def monitor_rds_cpu():
    """Monitor RDS CPU metrics using AWS CLI"""
    
    # RDS resource identifier
    resource_id = os.environ.get("RDS_ID", "db-FF3NLYWVAU47T6D3LFG5NCMRPI")
    
    try:
        # Get current time and 1 minute ago
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=1)
        
        # Format timestamps for AWS CLI
        start_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # CPU metrics to query (all metrics from working config)
        cpu_metrics = [
            "os.cpuUtilization.user.avg",
            "os.cpuUtilization.system.avg",
            "os.cpuUtilization.nice.avg",
            "os.cpuUtilization.wait.avg"
        ]
        
        # Build AWS metric query payload
        metric_queries = [{"Metric": metric} for metric in cpu_metrics]
        metric_queries_json = json.dumps(metric_queries)
        
        # AWS CLI command
        command = [
            "aws", "pi", "get-resource-metrics",
            "--service-type", "RDS",
            "--identifier", resource_id,
            "--metric-queries", metric_queries_json,
            "--start-time", start_str,
            "--end-time", end_str,
            "--period-in-seconds", "60",
            "--region", "us-east-1"
        ]
        
        # Run command
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Handle errors
        if result.returncode != 0:
            logging.error(f"AWS CLI command failed: {result.stderr}")
            return
        
        if not result.stdout.strip():
            logging.error("No output from AWS CLI")
            return
        
        # Parse response
        try:
            output = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing error: {e}")
            return
        
        # Sum CPU usage for the most recent timestamp
        metric_data = output.get("MetricList", [])
        cpu_sum = 0
        latest_time = None
        breakdown = {}
        
        for metric in metric_data:
            metric_name = metric["Key"]["Metric"]
            if metric["DataPoints"]:
                latest_dp = sorted(metric["DataPoints"], key=lambda d: d["Timestamp"])[-1]
                timestamp = latest_dp["Timestamp"]
                value = latest_dp["Value"]
                breakdown[metric_name] = value
                cpu_sum += value
                latest_time = timestamp
        
        # Output
        if latest_time:
            logging.info(f"Real-time CPU utilization at {latest_time}: {cpu_sum:.2f}%")
            for k, v in breakdown.items():
                logging.info(f"  {k}: {v:.2f}%")
        else:
            logging.warning("No data returned for the last minute")
                
    except Exception as e:
        logging.error(f"Error monitoring CPU: {e}")

def main():
    """Main monitoring loop"""
    logging.info("Starting RDS CPU monitoring")
    
    while True:
        monitor_rds_cpu()
        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    main()
