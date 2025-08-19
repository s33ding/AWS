#!/usr/bin/env python3
"""
Monitoring script for EKS scaling automation
"""

import boto3
import json
from datetime import datetime, timedelta
from typing import List, Dict

# Configuration
REGION = 'sa-east-1'
TABLE_NAME = 'eks-scaling-logs'
CLUSTER_NAME = 'sas-6881323-eks'

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb', region_name=REGION)
eks_client = boto3.client('eks', region_name=REGION)
cloudwatch = boto3.client('cloudwatch', region_name=REGION)

def get_recent_scaling_logs(days: int = 7) -> List[Dict]:
    """Get recent scaling logs from DynamoDB"""
    table = dynamodb.Table(TABLE_NAME)
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        response = table.scan(
            FilterExpression='#date BETWEEN :start_date AND :end_date',
            ExpressionAttributeNames={'#date': 'date'},
            ExpressionAttributeValues={
                ':start_date': start_date.strftime('%Y-%m-%d'),
                ':end_date': end_date.strftime('%Y-%m-%d')
            }
        )
        
        # Sort by timestamp
        items = sorted(response['Items'], key=lambda x: x['timestamp'], reverse=True)
        return items
        
    except Exception as e:
        print(f"Error fetching logs: {str(e)}")
        return []

def get_current_nodegroup_status():
    """Get current status of EKS node groups"""
    try:
        # List node groups
        nodegroups_response = eks_client.list_nodegroups(clusterName=CLUSTER_NAME)
        nodegroups = nodegroups_response['nodegroups']
        
        status = {}
        for ng_name in nodegroups:
            ng_details = eks_client.describe_nodegroup(
                clusterName=CLUSTER_NAME,
                nodegroupName=ng_name
            )
            
            ng_info = ng_details['nodegroup']
            status[ng_name] = {
                'status': ng_info['status'],
                'scaling': ng_info['scalingConfig'],
                'instance_types': ng_info['instanceTypes'],
                'capacity_type': ng_info['capacityType']
            }
        
        return status
        
    except Exception as e:
        print(f"Error fetching nodegroup status: {str(e)}")
        return {}

def display_current_status():
    """Display current EKS cluster status"""
    print("📊 Current EKS Cluster Status")
    print("=" * 50)
    
    status = get_current_nodegroup_status()
    
    for ng_name, ng_info in status.items():
        print(f"\n🔧 Node Group: {ng_name}")
        print(f"   Status: {ng_info['status']}")
        print(f"   Instance Types: {', '.join(ng_info['instance_types'])}")
        print(f"   Capacity Type: {ng_info['capacity_type']}")
        print(f"   Scaling Config:")
        print(f"     - Min Size: {ng_info['scaling']['minSize']}")
        print(f"     - Max Size: {ng_info['scaling']['maxSize']}")
        print(f"     - Desired Size: {ng_info['scaling']['desiredSize']}")

def display_recent_activity(days: int = 3):
    """Display recent scaling activity"""
    print(f"\n📈 Recent Scaling Activity (Last {days} days)")
    print("=" * 50)
    
    logs = get_recent_scaling_logs(days)
    
    if not logs:
        print("No recent scaling activity found.")
        return
    
    for log in logs[:10]:  # Show last 10 entries
        timestamp = datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00'))
        print(f"\n🕐 {timestamp.strftime('%Y-%m-%d %H:%M:%S')} ({log['weekday']})")
        print(f"   Type: {log['scaling_type']} - {log['description']}")
        
        # Show execution results
        if 'execution_result' in log:
            result = log['execution_result']
            for ng_type, ng_result in result.items():
                if ng_result['status'] == 'success':
                    scaling = ng_result['scaling']
                    print(f"   ✅ {ng_type}: {scaling['desired']} nodes (min:{scaling['min']}, max:{scaling['max']})")
                else:
                    print(f"   ❌ {ng_type}: {ng_result['error']}")

def get_cost_estimation():
    """Estimate cost savings from scaling"""
    print("\n💰 Cost Estimation")
    print("=" * 30)
    
    # Instance pricing (approximate, São Paulo region)
    pricing = {
        'm5.xlarge': 0.192,      # per hour
        'm5a.4xlarge': 0.688     # per hour
    }
    
    # Calculate daily costs for different scenarios
    scenarios = {
        'Always 3 big nodes': 3 * pricing['m5a.4xlarge'] * 24,
        'Always 1 big node': 1 * pricing['m5a.4xlarge'] * 24,
        'Current schedule': (
            # Sleep time (5.5h): 1 small node
            5.5 * pricing['m5.xlarge'] +
            # Tuesday peak (5h): 3 big nodes
            (5 * 3 * pricing['m5a.4xlarge']) / 7 +  # Only 1 day per week
            # Normal operation (13.5h): 1 big node
            13.5 * pricing['m5a.4xlarge']
        )
    }
    
    for scenario, daily_cost in scenarios.items():
        monthly_cost = daily_cost * 30
        print(f"{scenario}:")
        print(f"  Daily: ${daily_cost:.2f}")
        print(f"  Monthly: ${monthly_cost:.2f}")
    
    # Calculate savings
    always_big = scenarios['Always 1 big node']
    scheduled = scenarios['Current schedule']
    savings = always_big - scheduled
    
    print(f"\n💡 Estimated monthly savings: ${savings * 30:.2f}")
    print(f"   Percentage saved: {(savings / always_big) * 100:.1f}%")

def check_lambda_health():
    """Check Lambda function health"""
    print("\n🔍 Lambda Function Health")
    print("=" * 30)
    
    try:
        # Get CloudWatch metrics for Lambda function
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        
        # Get invocation count
        invocations = cloudwatch.get_metric_statistics(
            Namespace='AWS/Lambda',
            MetricName='Invocations',
            Dimensions=[
                {'Name': 'FunctionName', 'Value': 'eks-scaling-automation'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,  # 1 hour
            Statistics=['Sum']
        )
        
        # Get error count
        errors = cloudwatch.get_metric_statistics(
            Namespace='AWS/Lambda',
            MetricName='Errors',
            Dimensions=[
                {'Name': 'FunctionName', 'Value': 'eks-scaling-automation'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=['Sum']
        )
        
        total_invocations = sum(point['Sum'] for point in invocations['Datapoints'])
        total_errors = sum(point['Sum'] for point in errors['Datapoints'])
        
        print(f"Last 24 hours:")
        print(f"  Invocations: {int(total_invocations)}")
        print(f"  Errors: {int(total_errors)}")
        
        if total_invocations > 0:
            error_rate = (total_errors / total_invocations) * 100
            print(f"  Error Rate: {error_rate:.1f}%")
            
            if error_rate == 0:
                print("  Status: ✅ Healthy")
            elif error_rate < 5:
                print("  Status: ⚠️  Some errors")
            else:
                print("  Status: ❌ High error rate")
        else:
            print("  Status: ⚠️  No recent invocations")
            
    except Exception as e:
        print(f"❌ Error checking Lambda health: {str(e)}")

def main():
    """Main monitoring function"""
    print("🔍 EKS Scaling Automation Monitor")
    print("=" * 50)
    
    try:
        display_current_status()
        display_recent_activity()
        get_cost_estimation()
        check_lambda_health()
        
        print("\n" + "=" * 50)
        print("✅ Monitoring report completed")
        
    except Exception as e:
        print(f"❌ Error in monitoring: {str(e)}")

if __name__ == "__main__":
    main()
