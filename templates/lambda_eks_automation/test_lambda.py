#!/usr/bin/env python3
"""
Test script for EKS scaling Lambda function
"""

import json
import sys
import os
from datetime import datetime, timezone, timedelta

# Add current directory to path to import lambda_function
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lambda_function import determine_scaling_action, get_sao_paulo_time

def test_scheduling_logic():
    """Test the scheduling logic with different times"""
    print("🧪 Testing EKS Scaling Logic")
    print("=" * 50)
    
    # Test cases: (hour, minute, weekday, expected_type)
    test_cases = [
        # Sleep time (01:00-06:30)
        (2, 0, 0, 'S1', 'Monday 02:00 - Sleep time'),
        (5, 30, 1, 'S1', 'Tuesday 05:30 - Sleep time'),
        (6, 0, 2, 'S1', 'Wednesday 06:00 - Sleep time'),
        
        # Morning time (06:30-11:30)
        (7, 0, 0, 'B1', 'Monday 07:00 - Normal morning'),
        (9, 0, 1, 'B3', 'Tuesday 09:00 - Peak morning'),
        (10, 30, 2, 'B1', 'Wednesday 10:30 - Normal morning'),
        
        # Afternoon/Evening (11:30-01:00)
        (12, 0, 0, 'B1', 'Monday 12:00 - Normal operation'),
        (15, 30, 1, 'B1', 'Tuesday 15:30 - Normal operation'),
        (22, 0, 2, 'B1', 'Wednesday 22:00 - Normal operation'),
        
        # Weekend midnight exception
        (0, 30, 5, 'S1', 'Saturday 00:30 - Weekend sleep'),
        (0, 45, 6, 'S1', 'Sunday 00:45 - Weekend sleep'),
    ]
    
    for hour, minute, weekday, expected_type, description in test_cases:
        # Create test datetime - use a base date and add weekday offset
        base_date = datetime(2025, 8, 18)  # This is a Monday
        test_date = base_date + timedelta(days=weekday)
        
        sp_timezone = timezone(timedelta(hours=-3))
        test_time = test_date.replace(hour=hour, minute=minute, tzinfo=sp_timezone)
        
        # Get scaling action
        action = determine_scaling_action(test_time)
        
        # Check result
        status = "✅" if action['type'] == expected_type else "❌"
        print(f"{status} {description}")
        print(f"   Expected: {expected_type}, Got: {action['type']}")
        print(f"   Description: {action['description']}")
        
        if action['type'] != expected_type:
            print(f"   ⚠️  MISMATCH! Expected {expected_type}, got {action['type']}")
        
        print()

def test_current_time():
    """Test with current São Paulo time"""
    print("🕐 Current Time Test")
    print("=" * 30)
    
    sp_time = get_sao_paulo_time()
    action = determine_scaling_action(sp_time)
    
    print(f"Current São Paulo time: {sp_time.strftime('%Y-%m-%d %H:%M:%S %A')}")
    print(f"Scaling action: {action['type']}")
    print(f"Description: {action['description']}")
    print(f"Small nodegroup: {action['small_nodegroup']}")
    print(f"Big nodegroup: {action['big_nodegroup']}")

def simulate_lambda_event():
    """Simulate a Lambda event"""
    print("\n🚀 Lambda Event Simulation")
    print("=" * 30)
    
    # Mock event and context
    event = {'trigger': 'test'}
    
    class MockContext:
        def __init__(self):
            self.function_name = 'test-function'
            self.aws_request_id = 'test-request-id'
    
    context = MockContext()
    
    # Import and test lambda handler (without AWS calls)
    try:
        # This would normally call AWS services, so we'll just test the logic
        sp_time = get_sao_paulo_time()
        action = determine_scaling_action(sp_time)
        
        result = {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Test completed successfully',
                'action': action,
                'timestamp': sp_time.isoformat()
            }, indent=2)
        }
        
        print("Lambda simulation result:")
        print(result['body'])
        
    except Exception as e:
        print(f"❌ Error in simulation: {str(e)}")

if __name__ == "__main__":
    test_scheduling_logic()
    test_current_time()
    simulate_lambda_event()
