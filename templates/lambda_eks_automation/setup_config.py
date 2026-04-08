#!/usr/bin/env python3
"""
Setup and manage EKS scaling configuration in DynamoDB
"""

import boto3
import json
from datetime import datetime

# Configuration
REGION = 'sa-east-1'
CONFIG_TABLE_NAME = 'eks-scaling-config'

def create_config_table():
    """Create DynamoDB configuration table"""
    print("🔧 Creating configuration table...")
    
    dynamodb = boto3.client('dynamodb', region_name=REGION)
    
    try:
        response = dynamodb.create_table(
            TableName=CONFIG_TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'config_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'config_id',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST',
            Tags=[
                {
                    'Key': 'Project',
                    'Value': 'EKS-Scaling-Automation'
                },
                {
                    'Key': 'Environment',
                    'Value': 'Production'
                }
            ]
        )
        
        print(f"✅ Configuration table created: {CONFIG_TABLE_NAME}")
        return response['TableDescription']['TableArn']
        
    except dynamodb.exceptions.ResourceInUseException:
        print("⚠️  Configuration table already exists")
        table_arn = dynamodb.describe_table(TableName=CONFIG_TABLE_NAME)['Table']['TableArn']
        return table_arn

def get_default_configuration():
    """Get the default scaling configuration"""
    return {
        'config_id': 'active',
        'cluster_name': 'sas-6881323-eks',
        'small_nodegroup': 'default-20250319191255393900000026',
        'big_nodegroup': 'new-m5a4xlarge-v4',
        'schedules': {
            'sleep_time': {
                'start_hour': 1,
                'start_minute': 0,
                'end_hour': 6,
                'end_minute': 30,
                'small_nodes': 1,
                'big_nodes': 0,
                'description': 'Sleep time - small nodegroup'
            },
            'tuesday_peak': {
                'start_hour': 6,
                'start_minute': 30,
                'end_hour': 11,
                'end_minute': 30,
                'weekday': 1,  # Tuesday
                'small_nodes': 0,
                'big_nodes': 3,
                'description': 'Tuesday peak time - 3 big nodes'
            },
            'normal_operation': {
                'small_nodes': 0,
                'big_nodes': 1,
                'description': 'Normal operation - 1 big node'
            },
            'weekend_midnight': {
                'start_hour': 0,
                'end_hour': 1,
                'weekdays': [5, 6],  # Saturday, Sunday
                'small_nodes': 1,
                'big_nodes': 0,
                'description': 'Weekend sleep time'
            }
        },
        'nodegroup_limits': {
            'small_nodegroup': {
                'min_size': 0,
                'max_size': 1
            },
            'big_nodegroup': {
                'min_size': 0,
                'max_size': 3
            }
        },
        'enabled': True,
        'last_updated': datetime.now().isoformat(),
        'created_by': 'setup_script',
        'version': '1.0'
    }

def save_configuration(config):
    """Save configuration to DynamoDB"""
    print("💾 Saving configuration to DynamoDB...")
    
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(CONFIG_TABLE_NAME)
    
    try:
        table.put_item(Item=config)
        print("✅ Configuration saved successfully")
        return True
    except Exception as e:
        print(f"❌ Error saving configuration: {str(e)}")
        return False

def load_configuration():
    """Load current configuration from DynamoDB"""
    print("📖 Loading current configuration...")
    
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(CONFIG_TABLE_NAME)
    
    try:
        response = table.get_item(Key={'config_id': 'active'})
        if 'Item' in response:
            print("✅ Configuration loaded successfully")
            return response['Item']
        else:
            print("⚠️  No configuration found")
            return None
    except Exception as e:
        print(f"❌ Error loading configuration: {str(e)}")
        return None

def display_configuration(config):
    """Display configuration in a readable format"""
    print("\n📋 Current EKS Scaling Configuration")
    print("=" * 60)
    
    print(f"🔧 Basic Settings:")
    print(f"  Cluster: {config['cluster_name']}")
    print(f"  Small Nodegroup: {config['small_nodegroup']}")
    print(f"  Big Nodegroup: {config['big_nodegroup']}")
    print(f"  Enabled: {config['enabled']}")
    print(f"  Last Updated: {config['last_updated']}")
    
    print(f"\n⏰ Schedules:")
    schedules = config['schedules']
    
    # Sleep time
    sleep = schedules['sleep_time']
    print(f"  Sleep Time: {sleep['start_hour']:02d}:{sleep['start_minute']:02d} - {sleep['end_hour']:02d}:{sleep['end_minute']:02d}")
    print(f"    Small nodes: {sleep['small_nodes']}, Big nodes: {sleep['big_nodes']}")
    
    # Tuesday peak
    tuesday = schedules['tuesday_peak']
    print(f"  Tuesday Peak: {tuesday['start_hour']:02d}:{tuesday['start_minute']:02d} - {tuesday['end_hour']:02d}:{tuesday['end_minute']:02d}")
    print(f"    Small nodes: {tuesday['small_nodes']}, Big nodes: {tuesday['big_nodes']}")
    
    # Normal operation
    normal = schedules['normal_operation']
    print(f"  Normal Operation: Default")
    print(f"    Small nodes: {normal['small_nodes']}, Big nodes: {normal['big_nodes']}")
    
    # Weekend midnight
    weekend = schedules['weekend_midnight']
    print(f"  Weekend Midnight: {weekend['start_hour']:02d}:00 - {weekend['end_hour']:02d}:00 (Sat/Sun)")
    print(f"    Small nodes: {weekend['small_nodes']}, Big nodes: {weekend['big_nodes']}")
    
    print(f"\n🔒 Node Limits:")
    limits = config['nodegroup_limits']
    print(f"  Small Nodegroup: min={limits['small_nodegroup']['min_size']}, max={limits['small_nodegroup']['max_size']}")
    print(f"  Big Nodegroup: min={limits['big_nodegroup']['min_size']}, max={limits['big_nodegroup']['max_size']}")

def update_schedule(schedule_name, **kwargs):
    """Update a specific schedule"""
    print(f"🔄 Updating {schedule_name} schedule...")
    
    config = load_configuration()
    if not config:
        print("❌ No configuration found to update")
        return False
    
    if schedule_name not in config['schedules']:
        print(f"❌ Schedule '{schedule_name}' not found")
        return False
    
    # Update the schedule
    for key, value in kwargs.items():
        config['schedules'][schedule_name][key] = value
    
    config['last_updated'] = datetime.now().isoformat()
    
    return save_configuration(config)

def enable_disable_scaling(enabled: bool):
    """Enable or disable scaling"""
    action = "Enabling" if enabled else "Disabling"
    print(f"🔄 {action} EKS scaling...")
    
    config = load_configuration()
    if not config:
        print("❌ No configuration found to update")
        return False
    
    config['enabled'] = enabled
    config['last_updated'] = datetime.now().isoformat()
    
    return save_configuration(config)

def main():
    """Main configuration setup"""
    print("🚀 EKS Scaling Configuration Setup")
    print("=" * 50)
    
    # Create table
    create_config_table()
    
    # Check if configuration exists
    existing_config = load_configuration()
    
    if existing_config:
        print("\n📋 Existing configuration found:")
        display_configuration(existing_config)
        
        update = input("\nDo you want to update the configuration? (yes/no): ")
        if update.lower() != 'yes':
            print("✅ Using existing configuration")
            return
    
    # Save default configuration
    default_config = get_default_configuration()
    
    if save_configuration(default_config):
        print("\n✅ Configuration setup completed!")
        display_configuration(default_config)
        
        print(f"\n💡 You can now modify the configuration by:")
        print(f"  1. Editing the DynamoDB table directly")
        print(f"  2. Using this script's update functions")
        print(f"  3. Creating a web interface")
        
        print(f"\n🔗 DynamoDB Console:")
        print(f"  https://console.aws.amazon.com/dynamodbv2/home?region={REGION}#table?name={CONFIG_TABLE_NAME}")
    else:
        print("❌ Configuration setup failed")

if __name__ == "__main__":
    main()
