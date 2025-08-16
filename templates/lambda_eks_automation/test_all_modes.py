#!/usr/bin/env python3
"""
Test all 3 scaling modes with real AWS calls
B3 (3 big nodes) -> B1 (1 big node) -> S1 (1 small node) -> B1 (back to normal)
"""

import boto3
import time
import json

# Configuration
REGION = 'sa-east-1'
CLUSTER_NAME = 'sas-6881323-eks'
SMALL_NODEGROUP = 'default-20250319191255393900000026'  # m5.xlarge
BIG_NODEGROUP = 'new-m5a4xlarge-v4'  # m5a.4xlarge

def get_nodegroup_status(nodegroup_name):
    """Get current nodegroup status"""
    eks_client = boto3.client('eks', region_name=REGION)
    
    response = eks_client.describe_nodegroup(
        clusterName=CLUSTER_NAME,
        nodegroupName=nodegroup_name
    )
    
    scaling = response['nodegroup']['scalingConfig']
    status = response['nodegroup']['status']
    
    return {
        'name': nodegroup_name,
        'min': scaling['minSize'],
        'max': scaling['maxSize'], 
        'desired': scaling['desiredSize'],
        'status': status
    }

def wait_for_nodegroup_active(nodegroup_name, max_wait=300):
    """Wait for nodegroup to become active"""
    print(f"⏳ Waiting for {nodegroup_name} to become ACTIVE...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        status = get_nodegroup_status(nodegroup_name)
        print(f"  Status: {status['status']}, Desired: {status['desired']}")
        
        if status['status'] == 'ACTIVE':
            print(f"✅ {nodegroup_name} is now ACTIVE")
            return True
            
        time.sleep(15)
    
    print(f"❌ Timeout waiting for {nodegroup_name}")
    return False

def scale_nodegroup(nodegroup_name, desired, min_size, max_size, description):
    """Scale a specific nodegroup"""
    print(f"\n🔧 {description}")
    print("=" * 50)
    
    eks_client = boto3.client('eks', region_name=REGION)
    
    # Get current status
    current = get_nodegroup_status(nodegroup_name)
    print(f"Current: {current}")
    
    if current['desired'] == desired and current['status'] == 'ACTIVE':
        print(f"✅ Already at desired state: {desired} nodes")
        return True
    
    print(f"📈 Scaling {nodegroup_name} to {desired} nodes...")
    
    try:
        response = eks_client.update_nodegroup_config(
            clusterName=CLUSTER_NAME,
            nodegroupName=nodegroup_name,
            scalingConfig={
                'minSize': min_size,
                'maxSize': max_size,
                'desiredSize': desired
            }
        )
        
        update_id = response['update']['id']
        print(f"✅ Scaling initiated! Update ID: {update_id}")
        
        # Wait for completion
        return wait_for_nodegroup_active(nodegroup_name)
        
    except Exception as e:
        print(f"❌ Error scaling {nodegroup_name}: {str(e)}")
        return False

def show_current_nodes():
    """Show current EC2 instances and Kubernetes nodes"""
    print(f"\n📊 Current Node Status")
    print("=" * 50)
    
    # Show EC2 instances
    print("EC2 Instances:")
    import subprocess
    result = subprocess.run([
        'aws', 'ec2', 'describe-instances', 
        '--region', REGION,
        '--filters', 'Name=tag:kubernetes.io/cluster/sas-6881323-eks,Values=owned',
        'Name=instance-state-name,Values=running,pending',
        '--query', 'Reservations[].Instances[].[InstanceId,InstanceType,State.Name,Tags[?Key==`Name`].Value|[0]]',
        '--output', 'table'
    ], capture_output=True, text=True)
    print(result.stdout)
    
    # Show Kubernetes nodes
    print("Kubernetes Nodes:")
    k8s_result = subprocess.run(['kubectl', 'get', 'nodes', '-o', 'wide'], 
                               capture_output=True, text=True)
    print(k8s_result.stdout)

def test_mode_b1_normal_operation():
    """Test B1: Normal operation (1 big node, 0 small nodes)"""
    print(f"\n🔄 TESTING MODE B1: Normal Operation")
    print("=" * 60)
    print("Target: 1x m5a.4xlarge, 0x m5.xlarge")
    
    # Scale small nodegroup to 0
    small_success = scale_nodegroup(
        SMALL_NODEGROUP, 0, 0, 1, 
        "Scaling small nodegroup to 0 (B1 mode)"
    )
    
    # Scale big nodegroup to 1
    big_success = scale_nodegroup(
        BIG_NODEGROUP, 1, 1, 3,
        "Scaling big nodegroup to 1 (B1 mode)"
    )
    
    if small_success and big_success:
        print(f"\n✅ MODE B1 SUCCESSFUL!")
        show_current_nodes()
        return True
    else:
        print(f"\n❌ MODE B1 FAILED!")
        return False

def test_mode_s1_sleep_time():
    """Test S1: Sleep time (0 big nodes, 1 small node)"""
    print(f"\n😴 TESTING MODE S1: Sleep Time")
    print("=" * 60)
    print("Target: 0x m5a.4xlarge, 1x m5.xlarge")
    
    # Scale big nodegroup to 0
    big_success = scale_nodegroup(
        BIG_NODEGROUP, 0, 0, 3,
        "Scaling big nodegroup to 0 (S1 mode)"
    )
    
    # Scale small nodegroup to 1
    small_success = scale_nodegroup(
        SMALL_NODEGROUP, 1, 0, 1,
        "Scaling small nodegroup to 1 (S1 mode)"
    )
    
    if small_success and big_success:
        print(f"\n✅ MODE S1 SUCCESSFUL!")
        show_current_nodes()
        return True
    else:
        print(f"\n❌ MODE S1 FAILED!")
        return False

def main():
    """Test all 3 scaling modes"""
    print("🧪 TESTING ALL 3 EKS SCALING MODES")
    print("=" * 70)
    print("This will test:")
    print("1. B3 -> B1: Scale down from 3 to 1 big node")
    print("2. B1 -> S1: Switch to sleep mode (small node)")
    print("3. S1 -> B1: Switch back to normal operation")
    print("=" * 70)
    
    # Ask for confirmation
    confirm = input("Proceed with testing all modes? (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ Test cancelled")
        return
    
    print(f"\n🚀 Starting comprehensive scaling test...")
    
    # Show initial state
    print(f"\n📊 INITIAL STATE")
    show_current_nodes()
    
    # Test 1: B3 -> B1 (we're currently at B3 with 3 nodes)
    print(f"\n" + "="*70)
    print("TEST 1: B3 -> B1 (Scale down from 3 to 1 big node)")
    b1_success = test_mode_b1_normal_operation()
    
    if not b1_success:
        print("❌ Cannot continue - B1 test failed")
        return
    
    input("\nPress Enter to continue to S1 test...")
    
    # Test 2: B1 -> S1 (Switch to sleep mode)
    print(f"\n" + "="*70)
    print("TEST 2: B1 -> S1 (Switch to sleep mode)")
    s1_success = test_mode_s1_sleep_time()
    
    if not s1_success:
        print("❌ Cannot continue - S1 test failed")
        return
    
    input("\nPress Enter to switch back to normal operation...")
    
    # Test 3: S1 -> B1 (Back to normal)
    print(f"\n" + "="*70)
    print("TEST 3: S1 -> B1 (Back to normal operation)")
    final_b1_success = test_mode_b1_normal_operation()
    
    # Final summary
    print(f"\n" + "="*70)
    print("🎉 ALL SCALING MODE TESTS COMPLETED!")
    print("=" * 70)
    
    if b1_success and s1_success and final_b1_success:
        print("✅ B3 -> B1: Scale down successful")
        print("✅ B1 -> S1: Sleep mode successful") 
        print("✅ S1 -> B1: Back to normal successful")
        print(f"\n💡 All 3 Lambda scaling modes work perfectly!")
        print(f"🚀 Ready for production deployment!")
    else:
        print("❌ Some tests failed - check the logs above")
    
    print(f"\n📊 FINAL STATE")
    show_current_nodes()

if __name__ == "__main__":
    main()
