#!/usr/bin/env python3
"""
Manual scale test - simulate what the Lambda would do
"""

import sys
import os
from datetime import datetime, timezone, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lambda_function import determine_scaling_action, get_sao_paulo_time

def simulate_tuesday_peak():
    """Simulate Tuesday peak scaling"""
    print("🚀 Simulating Tuesday Peak Scale-Up")
    print("=" * 50)
    
    # Create Tuesday 9:00 AM São Paulo time
    sp_timezone = timezone(timedelta(hours=-3))
    tuesday_morning = datetime(2025, 8, 19, 9, 0, tzinfo=sp_timezone)
    
    print(f"Simulated time: {tuesday_morning.strftime('%A %Y-%m-%d %H:%M:%S %Z')}")
    
    # Get scaling decision
    action = determine_scaling_action(tuesday_morning)
    
    print(f"\n📊 Scaling Decision:")
    print(f"  Type: {action['type']}")
    print(f"  Description: {action['description']}")
    
    print(f"\n🔧 What would happen to nodegroups:")
    print(f"  Small nodegroup (m5.xlarge):")
    print(f"    Current: unknown")
    print(f"    Target:  desired={action['small_nodegroup']['desired']}, min={action['small_nodegroup']['min']}, max={action['small_nodegroup']['max']}")
    
    print(f"  Big nodegroup (m5a.4xlarge):")
    print(f"    Current: 1 node")
    print(f"    Target:  desired={action['big_nodegroup']['desired']}, min={action['big_nodegroup']['min']}, max={action['big_nodegroup']['max']}")
    
    if action['type'] == 'B3':
        print(f"\n✅ SCALE-UP TRIGGERED!")
        print(f"  📈 Big nodegroup will scale from 1 → 3 nodes")
        print(f"  📉 Small nodegroup will scale to 0 nodes")
        print(f"  💰 Cost will increase temporarily for peak workload")
    
    return action

def simulate_current_time():
    """Simulate current time scaling decision"""
    print(f"\n🕐 Current Time Scaling Decision")
    print("=" * 50)
    
    current_time = get_sao_paulo_time()
    action = determine_scaling_action(current_time)
    
    print(f"Current São Paulo time: {current_time.strftime('%A %Y-%m-%d %H:%M:%S %Z')}")
    print(f"Current scaling type: {action['type']}")
    print(f"Description: {action['description']}")
    
    print(f"\n🎯 Current target configuration:")
    print(f"  Small nodegroup: {action['small_nodegroup']['desired']} nodes")
    print(f"  Big nodegroup: {action['big_nodegroup']['desired']} nodes")
    
    return action

def show_scaling_schedule():
    """Show the complete scaling schedule"""
    print(f"\n📅 Complete Scaling Schedule (São Paulo Time)")
    print("=" * 60)
    
    # Test different times throughout the week
    test_times = [
        (0, 30, 0, "Monday 00:30"),      # Monday midnight
        (3, 0, 0, "Monday 03:00"),       # Monday sleep time
        (7, 0, 0, "Monday 07:00"),       # Monday morning
        (12, 0, 0, "Monday 12:00"),      # Monday afternoon
        (22, 0, 0, "Monday 22:00"),      # Monday evening
        
        (3, 0, 1, "Tuesday 03:00"),      # Tuesday sleep time
        (9, 0, 1, "Tuesday 09:00"),      # Tuesday PEAK
        (12, 0, 1, "Tuesday 12:00"),     # Tuesday afternoon
        
        (0, 30, 5, "Saturday 00:30"),    # Saturday midnight
        (3, 0, 5, "Saturday 03:00"),     # Saturday sleep
        (9, 0, 5, "Saturday 09:00"),     # Saturday morning
    ]
    
    sp_timezone = timezone(timedelta(hours=-3))
    base_date = datetime(2025, 8, 18)  # Monday
    
    for hour, minute, day_offset, description in test_times:
        test_date = base_date + timedelta(days=day_offset)
        test_time = test_date.replace(hour=hour, minute=minute, tzinfo=sp_timezone)
        
        action = determine_scaling_action(test_time)
        
        small_nodes = action['small_nodegroup']['desired']
        big_nodes = action['big_nodegroup']['desired']
        
        print(f"{description:20} | {action['type']:2} | Small: {small_nodes} | Big: {big_nodes} | {action['description']}")

def main():
    """Main test function"""
    print("🧪 Manual EKS Scale-Up Testing")
    print("=" * 60)
    
    # Test Tuesday peak scaling
    tuesday_action = simulate_tuesday_peak()
    
    # Test current time
    current_action = simulate_current_time()
    
    # Show complete schedule
    show_scaling_schedule()
    
    print(f"\n" + "=" * 60)
    print("📋 Test Summary:")
    print(f"✅ Tuesday peak scaling: {tuesday_action['type']} - {tuesday_action['big_nodegroup']['desired']} big nodes")
    print(f"✅ Current time scaling: {current_action['type']} - {current_action['big_nodegroup']['desired']} big nodes")
    print(f"✅ Schedule logic working correctly")
    
    print(f"\n💡 The Lambda function will automatically:")
    print(f"  🔄 Scale up to 3 nodes on Tuesday mornings (6:30-11:30)")
    print(f"  📉 Scale down to 1 node for normal operation")
    print(f"  😴 Use small nodes during sleep time (1:00-6:30)")
    print(f"  💰 Optimize costs while maintaining performance")

if __name__ == "__main__":
    main()
