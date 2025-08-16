#!/usr/bin/env python3
"""
Update EventBridge rules to match the agreed schedule exactly:
- 01:00-06:30: Small node (sleep)
- 06:30-11:30: Tuesday=3 big nodes, Other days=1 big node  
- 11:30-01:00: 1 big node (normal)
"""

import boto3
import json

# Configuration
REGION = 'sa-east-1'
FUNCTION_NAME = 'eks-scaling-automation'

def delete_old_rules():
    """Delete the current 4 rules"""
    print("🗑️  Deleting old EventBridge rules...")
    
    events = boto3.client('events', region_name=REGION)
    
    old_rules = [
        'eks-scaling-sleep-start',
        'eks-scaling-morning-start', 
        'eks-scaling-afternoon-start',
        'eks-scaling-midnight-weekend'
    ]
    
    for rule_name in old_rules:
        try:
            # Remove targets first
            events.remove_targets(Rule=rule_name, Ids=['1'])
            # Delete rule
            events.delete_rule(Name=rule_name)
            print(f"✅ Deleted rule: {rule_name}")
        except Exception as e:
            print(f"⚠️  Rule {rule_name} not found or already deleted: {str(e)}")

def create_new_rules():
    """Create the 3 new rules matching the agreed schedule"""
    print("\n🔧 Creating new EventBridge rules for agreed schedule...")
    
    events = boto3.client('events', region_name=REGION)
    lambda_client = boto3.client('lambda', region_name=REGION)
    
    # Get account ID for permissions
    account_id = boto3.client('sts').get_caller_identity()['Account']
    
    # New schedule rules (São Paulo time -> UTC conversion: SP + 3 hours)
    new_rules = [
        {
            'name': 'eks-scaling-sleep-period',
            'description': 'Sleep period: 01:00-06:30 SP (04:00-09:30 UTC)',
            'schedule': 'cron(0 4 * * ? *)',  # 01:00 SP = 04:00 UTC
            'input': {'trigger': 'sleep_period', 'period': 'sleep'}
        },
        {
            'name': 'eks-scaling-morning-period', 
            'description': 'Morning period: 06:30-11:30 SP (09:30-14:30 UTC)',
            'schedule': 'cron(30 9 * * ? *)',  # 06:30 SP = 09:30 UTC
            'input': {'trigger': 'morning_period', 'period': 'morning'}
        },
        {
            'name': 'eks-scaling-afternoon-period',
            'description': 'Afternoon period: 11:30-01:00 SP (14:30-04:00 UTC)',
            'schedule': 'cron(30 14 * * ? *)',  # 11:30 SP = 14:30 UTC
            'input': {'trigger': 'afternoon_period', 'period': 'afternoon'}
        }
    ]
    
    for rule_config in new_rules:
        try:
            # Create rule
            events.put_rule(
                Name=rule_config['name'],
                ScheduleExpression=rule_config['schedule'],
                Description=rule_config['description'],
                State='ENABLED'
            )
            
            # Add Lambda target
            events.put_targets(
                Rule=rule_config['name'],
                Targets=[
                    {
                        'Id': '1',
                        'Arn': f"arn:aws:lambda:{REGION}:{account_id}:function:{FUNCTION_NAME}",
                        'Input': json.dumps(rule_config['input'])
                    }
                ]
            )
            
            # Add permission for EventBridge to invoke Lambda
            try:
                lambda_client.add_permission(
                    FunctionName=FUNCTION_NAME,
                    StatementId=f"allow-eventbridge-{rule_config['name']}",
                    Action='lambda:InvokeFunction',
                    Principal='events.amazonaws.com',
                    SourceArn=f"arn:aws:events:{REGION}:{account_id}:rule/{rule_config['name']}"
                )
            except lambda_client.exceptions.ResourceConflictException:
                pass  # Permission already exists
            
            print(f"✅ Created rule: {rule_config['name']}")
            print(f"   Schedule: {rule_config['schedule']}")
            print(f"   Description: {rule_config['description']}")
            
        except Exception as e:
            print(f"❌ Error creating rule {rule_config['name']}: {str(e)}")

def show_new_schedule():
    """Show the new schedule"""
    print(f"\n📅 NEW CRON SCHEDULE (Acordo Original)")
    print("=" * 60)
    print("🕐 Cronograma (São Paulo):")
    print("• 01:00-06:30: Node pequeno (sono) 😴")
    print("• 06:30-11:30:")
    print("  - Terça: 3 nodes grandes 🚀") 
    print("  - Outros dias: 1 node grande")
    print("• 11:30-01:00: 1 node grande (normal)")
    
    print(f"\n⏰ EventBridge Rules (UTC):")
    print("• 04:00 UTC (01:00 SP): Trigger sleep period")
    print("• 09:30 UTC (06:30 SP): Trigger morning period") 
    print("• 14:30 UTC (11:30 SP): Trigger afternoon period")
    
    print(f"\n🎯 Lambda Logic:")
    print("• Sleep period: Always 1 small node")
    print("• Morning period: Check if Tuesday -> 3 big nodes, else 1 big node")
    print("• Afternoon period: Always 1 big node")

def verify_rules():
    """Verify the new rules are created correctly"""
    print(f"\n🔍 Verifying new rules...")
    
    events = boto3.client('events', region_name=REGION)
    
    try:
        response = events.list_rules(NamePrefix='eks-scaling')
        rules = response['Rules']
        
        print(f"✅ Found {len(rules)} EKS scaling rules:")
        for rule in rules:
            print(f"  • {rule['Name']}: {rule['State']} - {rule['ScheduleExpression']}")
            
        return len(rules) == 3
        
    except Exception as e:
        print(f"❌ Error verifying rules: {str(e)}")
        return False

def main():
    """Update cron schedule to match the agreement"""
    print("🔄 UPDATING CRON SCHEDULE TO MATCH AGREEMENT")
    print("=" * 60)
    
    # Show what we're changing to
    show_new_schedule()
    
    # Ask for confirmation
    confirm = input(f"\nProceed with updating the cron schedule? (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ Update cancelled")
        return
    
    try:
        # Delete old rules
        delete_old_rules()
        
        # Create new rules
        create_new_rules()
        
        # Verify
        if verify_rules():
            print(f"\n🎉 CRON SCHEDULE UPDATED SUCCESSFULLY!")
            print("✅ 3 rules created matching the agreed schedule")
            print("✅ Lambda will now follow the exact agreement")
            
            print(f"\n📱 WhatsApp Update:")
            print("✅ CRON ATUALIZADO CONFORME ACORDO! ⏰")
            print("• 01h-06h30: Node pequeno 😴")
            print("• 06h30-11h30: Terça=3 nodes, Outros=1 node 🚀") 
            print("• 11h30-01h: 1 node grande (normal)")
            print("Sistema agora segue exatamente o acordo! 🎯")
            
        else:
            print("❌ Verification failed - please check manually")
            
    except Exception as e:
        print(f"❌ Update failed: {str(e)}")

if __name__ == "__main__":
    main()
