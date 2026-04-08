#!/usr/bin/env python3
"""
Deploy EKS Scaling Automation Infrastructure
Creates Lambda function, DynamoDB table, IAM roles, and EventBridge rules
"""

import boto3
import json
import zipfile
import os
from datetime import datetime

# Configuration
REGION = 'sa-east-1'
FUNCTION_NAME = 'eks-scaling-automation'
TABLE_NAME = 'eks-scaling-logs'
ROLE_NAME = 'eks-scaling-lambda-role'
POLICY_NAME = 'eks-scaling-lambda-policy'

# Initialize AWS clients
iam = boto3.client('iam', region_name=REGION)
lambda_client = boto3.client('lambda', region_name=REGION)
dynamodb = boto3.client('dynamodb', region_name=REGION)
events = boto3.client('events', region_name=REGION)

def create_iam_role():
    """Create IAM role for Lambda function"""
    print("Creating IAM role...")
    
    # Trust policy for Lambda
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    # Lambda execution policy
    lambda_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "arn:aws:logs:*:*:*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "eks:DescribeCluster",
                    "eks:DescribeNodegroup",
                    "eks:UpdateNodegroupConfig",
                    "eks:ListNodegroups"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:PutItem",
                    "dynamodb:GetItem",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:UpdateItem"
                ],
                "Resource": [
                    f"arn:aws:dynamodb:{REGION}:*:table/{TABLE_NAME}",
                    f"arn:aws:dynamodb:{REGION}:*:table/eks-scaling-config"
                ]
            }
        ]
    }
    
    try:
        # Create role
        role_response = iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role for EKS scaling automation Lambda function'
        )
        
        # Create and attach policy
        iam.create_policy(
            PolicyName=POLICY_NAME,
            PolicyDocument=json.dumps(lambda_policy),
            Description='Policy for EKS scaling automation'
        )
        
        # Attach policy to role
        iam.attach_role_policy(
            RoleName=ROLE_NAME,
            PolicyArn=f"arn:aws:iam::{boto3.client('sts').get_caller_identity()['Account']}:policy/{POLICY_NAME}"
        )
        
        print(f"✅ IAM role created: {role_response['Role']['Arn']}")
        return role_response['Role']['Arn']
        
    except iam.exceptions.EntityAlreadyExistsException:
        print("⚠️  IAM role already exists, using existing role")
        role_arn = iam.get_role(RoleName=ROLE_NAME)['Role']['Arn']
        return role_arn

def create_dynamodb_table():
    """Create DynamoDB table for logging"""
    print("Creating DynamoDB table...")
    
    try:
        response = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'date',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'date-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'date',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    }
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
        
        print(f"✅ DynamoDB table created: {TABLE_NAME}")
        return response['TableDescription']['TableArn']
        
    except dynamodb.exceptions.ResourceInUseException:
        print("⚠️  DynamoDB table already exists")
        table_arn = dynamodb.describe_table(TableName=TABLE_NAME)['Table']['TableArn']
        return table_arn

def create_lambda_function(role_arn):
    """Create Lambda function"""
    print("Creating Lambda function...")
    
    # Create deployment package
    zip_filename = 'lambda_deployment.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        zip_file.write('lambda_function.py')
    
    # Read the zip file
    with open(zip_filename, 'rb') as zip_file:
        zip_content = zip_file.read()
    
    try:
        response = lambda_client.create_function(
            FunctionName=FUNCTION_NAME,
            Runtime='python3.11',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_content},
            Description='EKS node scaling automation based on schedule',
            Timeout=300,
            MemorySize=256,
            Environment={
                'Variables': {
                    'CLUSTER_NAME': 'sas-6881323-eks',
                    'REGION': REGION,
                    'TABLE_NAME': TABLE_NAME
                }
            },
            Tags={
                'Project': 'EKS-Scaling-Automation',
                'Environment': 'Production'
            }
        )
        
        print(f"✅ Lambda function created: {response['FunctionArn']}")
        
    except lambda_client.exceptions.ResourceConflictException:
        print("⚠️  Lambda function already exists, updating code...")
        lambda_client.update_function_code(
            FunctionName=FUNCTION_NAME,
            ZipFile=zip_content
        )
        print("✅ Lambda function code updated")
    
    # Clean up zip file
    os.remove(zip_filename)
    
    return lambda_client.get_function(FunctionName=FUNCTION_NAME)['Configuration']['FunctionArn']

def create_eventbridge_rules(function_arn):
    """Create EventBridge rules for scheduling"""
    print("Creating EventBridge rules...")
    
    # Get account ID for Lambda ARN
    account_id = boto3.client('sts').get_caller_identity()['Account']
    
    # Schedule rules (all times in UTC, converted from São Paulo time UTC-3)
    schedules = [
        {
            'name': 'eks-scaling-sleep-start',
            'description': 'Start sleep mode (01:00 SP = 04:00 UTC)',
            'schedule': 'cron(0 4 * * ? *)',  # Daily at 04:00 UTC
            'input': {'trigger': 'sleep_start'}
        },
        {
            'name': 'eks-scaling-morning-start',
            'description': 'Start morning operation (06:30 SP = 09:30 UTC)',
            'schedule': 'cron(30 9 * * ? *)',  # Daily at 09:30 UTC
            'input': {'trigger': 'morning_start'}
        },
        {
            'name': 'eks-scaling-afternoon-start',
            'description': 'Start afternoon operation (11:30 SP = 14:30 UTC)',
            'schedule': 'cron(30 14 * * ? *)',  # Daily at 14:30 UTC
            'input': {'trigger': 'afternoon_start'}
        },
        {
            'name': 'eks-scaling-midnight-weekend',
            'description': 'Weekend midnight check (00:00 SP = 03:00 UTC)',
            'schedule': 'cron(0 3 ? * SAT,SUN *)',  # Saturday and Sunday at 03:00 UTC
            'input': {'trigger': 'weekend_midnight'}
        }
    ]
    
    for rule_config in schedules:
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
                        'Arn': function_arn,
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
            
            print(f"✅ EventBridge rule created: {rule_config['name']}")
            
        except Exception as e:
            print(f"❌ Error creating rule {rule_config['name']}: {str(e)}")

def main():
    """Main deployment function"""
    print("🚀 Starting EKS Scaling Automation deployment...")
    print(f"Region: {REGION}")
    print(f"Function: {FUNCTION_NAME}")
    print(f"Table: {TABLE_NAME}")
    print("-" * 50)
    
    try:
        # Create IAM role
        role_arn = create_iam_role()
        
        # Create DynamoDB table
        table_arn = create_dynamodb_table()
        
        # Wait a bit for IAM role to propagate
        print("⏳ Waiting for IAM role to propagate...")
        import time
        time.sleep(10)
        
        # Create Lambda function
        function_arn = create_lambda_function(role_arn)
        
        # Create EventBridge rules
        create_eventbridge_rules(function_arn)
        
        print("-" * 50)
        print("🎉 Deployment completed successfully!")
        print(f"📊 Monitor logs: https://console.aws.amazon.com/cloudwatch/home?region={REGION}#logsV2:log-groups/log-group/$252Faws$252Flambda$252F{FUNCTION_NAME}")
        print(f"📋 DynamoDB table: https://console.aws.amazon.com/dynamodbv2/home?region={REGION}#table?name={TABLE_NAME}")
        print(f"⚡ Lambda function: https://console.aws.amazon.com/lambda/home?region={REGION}#/functions/{FUNCTION_NAME}")
        
    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
