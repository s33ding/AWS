#!/usr/bin/env python3
"""
Test scale-up functionality for EKS Lambda automation
Simulates Tuesday morning peak time scaling
"""

import json
import sys
import os
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lambda_function import (
    lambda_handler, 
    determine_scaling_action, 
    execute_scaling,
    update_nodegroup_scaling,
    log_scaling_action
)

def test_tuesday_peak_scaling():
    """Test Tuesday morning peak scaling (B3 scenario)"""
    print("🚀 Testing Tuesday Peak Scale-Up (B3)")
    print("=" * 50)
    
    # Create Tuesday 9:00 AM São Paulo time
    sp_timezone = timezone(timedelta(hours=-3))
    tuesday_morning = datetime(2025, 8, 19, 9, 0, tzinfo=sp_timezone)  # Tuesday 9:00 AM
    
    print(f"Test time: {tuesday_morning.strftime('%A %Y-%m-%d %H:%M:%S %Z')}")
    print(f"Weekday: {tuesday_morning.weekday()} (1=Tuesday)")
    
    # Get scaling action
    scaling_action = determine_scaling_action(tuesday_morning)
    
    print(f"\n📊 Scaling Decision:")
    print(f"Type: {scaling_action['type']}")
    print(f"Description: {scaling_action['description']}")
    print(f"Small nodegroup config: {scaling_action['small_nodegroup']}")
    print(f"Big nodegroup config: {scaling_action['big_nodegroup']}")
    
    # Verify it's the correct B3 scenario
    assert scaling_action['type'] == 'B3', f"Expected B3, got {scaling_action['type']}"
    assert scaling_action['big_nodegroup']['desired'] == 3, "Should scale to 3 big nodes"
    assert scaling_action['small_nodegroup']['desired'] == 0, "Should scale small nodes to 0"
    
    print("\n✅ Tuesday peak scaling logic: PASSED")
    return scaling_action

def test_normal_operation_scaling():
    """Test normal operation scaling (B1 scenario)"""
    print("\n🔄 Testing Normal Operation Scaling (B1)")
    print("=" * 50)
    
    # Create Monday 9:00 AM São Paulo time
    sp_timezone = timezone(timedelta(hours=-3))
    monday_morning = datetime(2025, 8, 18, 9, 0, tzinfo=sp_timezone)  # Monday 9:00 AM
    
    print(f"Test time: {monday_morning.strftime('%A %Y-%m-%d %H:%M:%S %Z')}")
    
    # Get scaling action
    scaling_action = determine_scaling_action(monday_morning)
    
    print(f"\n📊 Scaling Decision:")
    print(f"Type: {scaling_action['type']}")
    print(f"Description: {scaling_action['description']}")
    print(f"Small nodegroup config: {scaling_action['small_nodegroup']}")
    print(f"Big nodegroup config: {scaling_action['big_nodegroup']}")
    
    # Verify it's the correct B1 scenario
    assert scaling_action['type'] == 'B1', f"Expected B1, got {scaling_action['type']}"
    assert scaling_action['big_nodegroup']['desired'] == 1, "Should scale to 1 big node"
    assert scaling_action['small_nodegroup']['desired'] == 0, "Should scale small nodes to 0"
    
    print("\n✅ Normal operation scaling logic: PASSED")
    return scaling_action

def test_sleep_time_scaling():
    """Test sleep time scaling (S1 scenario)"""
    print("\n😴 Testing Sleep Time Scaling (S1)")
    print("=" * 50)
    
    # Create 3:00 AM São Paulo time
    sp_timezone = timezone(timedelta(hours=-3))
    sleep_time = datetime(2025, 8, 18, 3, 0, tzinfo=sp_timezone)  # 3:00 AM
    
    print(f"Test time: {sleep_time.strftime('%A %Y-%m-%d %H:%M:%S %Z')}")
    
    # Get scaling action
    scaling_action = determine_scaling_action(sleep_time)
    
    print(f"\n📊 Scaling Decision:")
    print(f"Type: {scaling_action['type']}")
    print(f"Description: {scaling_action['description']}")
    print(f"Small nodegroup config: {scaling_action['small_nodegroup']}")
    print(f"Big nodegroup config: {scaling_action['big_nodegroup']}")
    
    # Verify it's the correct S1 scenario
    assert scaling_action['type'] == 'S1', f"Expected S1, got {scaling_action['type']}"
    assert scaling_action['small_nodegroup']['desired'] == 1, "Should scale to 1 small node"
    assert scaling_action['big_nodegroup']['desired'] == 0, "Should scale big nodes to 0"
    
    print("\n✅ Sleep time scaling logic: PASSED")
    return scaling_action

def mock_eks_scaling_test():
    """Test the actual scaling execution with mocked AWS calls"""
    print("\n🔧 Testing EKS Scaling Execution (Mocked)")
    print("=" * 50)
    
    # Mock AWS EKS client responses
    mock_update_response = {
        'update': {
            'id': 'test-update-id-12345',
            'status': 'InProgress',
            'type': 'ConfigUpdate'
        }
    }
    
    # Test Tuesday peak scaling
    sp_timezone = timezone(timedelta(hours=-3))
    tuesday_morning = datetime(2025, 8, 19, 9, 0, tzinfo=sp_timezone)
    scaling_action = determine_scaling_action(tuesday_morning)
    
    # Mock the EKS client
    with patch('lambda_function.eks_client') as mock_eks:
        mock_eks.update_nodegroup_config.return_value = mock_update_response
        
        # Test scaling execution
        result = execute_scaling(scaling_action, tuesday_morning)
        
        print("📋 Scaling Execution Results:")
        print(json.dumps(result, indent=2))
        
        # Verify EKS calls were made correctly
        assert mock_eks.update_nodegroup_config.call_count == 2, "Should call update for both nodegroups"
        
        # Check the calls
        calls = mock_eks.update_nodegroup_config.call_args_list
        
        # First call should be for small nodegroup (scale to 0)
        small_call = calls[0]
        assert small_call[1]['nodegroupName'] == 'default-20250319191255393900000026'
        assert small_call[1]['scalingConfig']['desiredSize'] == 0
        
        # Second call should be for big nodegroup (scale to 3)
        big_call = calls[1]
        assert big_call[1]['nodegroupName'] == 'new-m5a4xlarge-v4'
        assert big_call[1]['scalingConfig']['desiredSize'] == 3
        
        print("\n✅ EKS scaling execution: PASSED")
        print("✅ Small nodegroup scaled to 0")
        print("✅ Big nodegroup scaled to 3")

def mock_dynamodb_logging_test():
    """Test DynamoDB logging with mocked calls"""
    print("\n📝 Testing DynamoDB Logging (Mocked)")
    print("=" * 50)
    
    sp_timezone = timezone(timedelta(hours=-3))
    tuesday_morning = datetime(2025, 8, 19, 9, 0, tzinfo=sp_timezone)
    scaling_action = determine_scaling_action(tuesday_morning)
    
    mock_result = {
        'small_nodegroup': {'status': 'success', 'update_id': 'test-small-123'},
        'big_nodegroup': {'status': 'success', 'update_id': 'test-big-456'}
    }
    
    # Mock DynamoDB table
    with patch('lambda_function.dynamodb') as mock_dynamodb:
        mock_table = Mock()
        mock_dynamodb.Table.return_value = mock_table
        
        # Test logging
        log_scaling_action(scaling_action, mock_result, tuesday_morning)
        
        # Verify DynamoDB call
        assert mock_table.put_item.called, "Should call put_item on DynamoDB table"
        
        # Check the logged item
        logged_item = mock_table.put_item.call_args[1]['Item']
        
        print("📋 Logged Item Structure:")
        print(f"  Timestamp: {logged_item['timestamp']}")
        print(f"  Date: {logged_item['date']}")
        print(f"  Weekday: {logged_item['weekday']}")
        print(f"  Scaling Type: {logged_item['scaling_type']}")
        print(f"  Description: {logged_item['description']}")
        
        assert logged_item['scaling_type'] == 'B3'
        assert logged_item['weekday'] == 'Tuesday'
        assert logged_item['cluster_name'] == 'sas-6881323-eks'
        
        print("\n✅ DynamoDB logging: PASSED")

def test_full_lambda_handler():
    """Test the complete Lambda handler with mocks"""
    print("\n🎯 Testing Complete Lambda Handler (Mocked)")
    print("=" * 50)
    
    # Mock event and context
    event = {'trigger': 'scale_up_test'}
    
    class MockContext:
        def __init__(self):
            self.function_name = 'eks-scaling-automation'
            self.aws_request_id = 'test-request-123'
    
    context = MockContext()
    
    # Mock all AWS services
    mock_update_response = {
        'update': {
            'id': 'test-update-id-12345',
            'status': 'InProgress',
            'type': 'ConfigUpdate'
        }
    }
    
    with patch('lambda_function.eks_client') as mock_eks, \
         patch('lambda_function.dynamodb') as mock_dynamodb:
        
        # Setup mocks
        mock_eks.update_nodegroup_config.return_value = mock_update_response
        mock_table = Mock()
        mock_dynamodb.Table.return_value = mock_table
        
        # Override time to Tuesday morning for testing
        with patch('lambda_function.get_sao_paulo_time') as mock_time:
            sp_timezone = timezone(timedelta(hours=-3))
            tuesday_morning = datetime(2025, 8, 19, 9, 0, tzinfo=sp_timezone)
            mock_time.return_value = tuesday_morning
            
            # Execute Lambda handler
            response = lambda_handler(event, context)
            
            print("📋 Lambda Response:")
            print(json.dumps(json.loads(response['body']), indent=2))
            
            # Verify response
            assert response['statusCode'] == 200
            body = json.loads(response['body'])
            assert body['action']['type'] == 'B3'
            assert 'Tuesday peak time' in body['action']['description']
            
            print("\n✅ Complete Lambda handler: PASSED")

def main():
    """Run all scale-up tests"""
    print("🧪 EKS Lambda Scale-Up Testing Suite")
    print("=" * 60)
    
    try:
        # Test scaling logic
        test_tuesday_peak_scaling()
        test_normal_operation_scaling()
        test_sleep_time_scaling()
        
        # Test execution with mocks
        mock_eks_scaling_test()
        mock_dynamodb_logging_test()
        test_full_lambda_handler()
        
        print("\n" + "=" * 60)
        print("🎉 ALL SCALE-UP TESTS PASSED!")
        print("✅ Scaling logic working correctly")
        print("✅ EKS API calls properly formatted")
        print("✅ DynamoDB logging functional")
        print("✅ Complete Lambda handler working")
        print("\n💡 The Lambda function is ready for deployment!")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
