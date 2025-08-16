#!/usr/bin/env python3
"""
REAL EKS node scaling test - Actually scales nodes in AWS
WARNING: This will modify your actual EKS cluster!
"""

import boto3
import json
import time
from datetime import datetime

# Configuration
REGION = 'sa-east-1'
CLUSTER_NAME = 'sas-6881323-eks'
BIG_NODEGROUP = 'new-m5a4xlarge-v4'

def get_current_nodegroup_status():
    """Get current nodegroup status"""
    eks_client = boto3.client('eks', region_name=REGION)
    
    response = eks_client.describe_nodegroup(
        clusterName=CLUSTER_NAME,
        nodegroupName=BIG_NODEGROUP
    )
    
    scaling = response['nodegroup']['scalingConfig']
    status = response['nodegroup']['status']
    
    return {
        'min': scaling['minSize'],
        'max': scaling['maxSize'], 
        'desired': scaling['desiredSize'],
        'status': status
    }

def scale_nodegroup_to_3():
    """Actually scale the big nodegroup to 3 nodes"""
    print("🚀 REAL SCALING TEST - Scaling to 3 nodes")
    print("=" * 50)
    
    eks_client = boto3.client('eks', region_name=REGION)
    
    # Get current status
    current = get_current_nodegroup_status()
    print(f"Current status: {current}")
    
    if current['desired'] == 3:
        print("✅ Already at 3 nodes, no scaling needed")
        return current
    
    print(f"📈 Scaling from {current['desired']} to 3 nodes...")
    
    # Scale to 3 nodes
    response = eks_client.update_nodegroup_config(
        clusterName=CLUSTER_NAME,
        nodegroupName=BIG_NODEGROUP,
        scalingConfig={
            'minSize': 1,
            'maxSize': 3,
            'desiredSize': 3
        }
    )
    
    update_id = response['update']['id']
    print(f"✅ Scaling initiated! Update ID: {update_id}")
    
    return response

def monitor_scaling_progress(update_id):
    """Monitor the scaling progress"""
    print(f"\n🔍 Monitoring scaling progress...")
    print("=" * 50)
    
    eks_client = boto3.client('eks', region_name=REGION)
    
    while True:
        # Check update status
        update_response = eks_client.describe_update(
            name=CLUSTER_NAME,
            updateId=update_id
        )
        
        update_status = update_response['update']['status']
        print(f"Update status: {update_status}")
        
        # Check nodegroup status
        current = get_current_nodegroup_status()
        print(f"Nodegroup: desired={current['desired']}, status={current['status']}")
        
        if update_status in ['Successful', 'Failed', 'Cancelled']:
            break
            
        print("⏳ Waiting 30 seconds...")
        time.sleep(30)
    
    return update_status

def scale_back_to_1():
    """Scale back to 1 node after test"""
    print(f"\n📉 Scaling back to 1 node...")
    print("=" * 50)
    
    eks_client = boto3.client('eks', region_name=REGION)
    
    response = eks_client.update_nodegroup_config(
        clusterName=CLUSTER_NAME,
        nodegroupName=BIG_NODEGROUP,
        scalingConfig={
            'minSize': 1,
            'maxSize': 3,
            'desiredSize': 1
        }
    )
    
    update_id = response['update']['id']
    print(f"✅ Scale-down initiated! Update ID: {update_id}")
    
    return response

def main():
    """Main real scaling test"""
    print("⚠️  REAL EKS NODE SCALING TEST")
    print("=" * 60)
    print("WARNING: This will actually modify your EKS cluster!")
    print("This test will:")
    print("1. Scale your big nodegroup to 3 nodes")
    print("2. Wait for scaling to complete")
    print("3. Scale back down to 1 node")
    print("=" * 60)
    
    # Ask for confirmation
    confirm = input("Do you want to proceed with REAL scaling? (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ Test cancelled by user")
        return
    
    try:
        # Step 1: Scale up to 3 nodes
        scale_response = scale_nodegroup_to_3()
        
        if 'update' in scale_response:
            update_id = scale_response['update']['id']
            
            # Step 2: Monitor progress
            final_status = monitor_scaling_progress(update_id)
            
            if final_status == 'Successful':
                print(f"\n🎉 SCALE-UP SUCCESSFUL!")
                
                # Show final status
                final_status = get_current_nodegroup_status()
                print(f"Final status: {final_status}")
                
                # Wait a bit to see the nodes
                print(f"\n⏳ Waiting 60 seconds to let you see the 3 nodes...")
                time.sleep(60)
                
                # Step 3: Scale back down
                scale_back_response = scale_back_to_1()
                scale_back_id = scale_back_response['update']['id']
                
                print(f"\n📉 Scaling back down...")
                monitor_scaling_progress(scale_back_id)
                
                print(f"\n✅ REAL SCALING TEST COMPLETED!")
                print(f"✅ Successfully scaled up to 3 nodes")
                print(f"✅ Successfully scaled back to 1 node")
                
            else:
                print(f"❌ Scaling failed with status: {final_status}")
        
    except Exception as e:
        print(f"❌ Error during real scaling test: {str(e)}")

if __name__ == "__main__":
    main()
