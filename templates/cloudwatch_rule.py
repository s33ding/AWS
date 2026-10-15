import os
import boto3
import sys
import subprocess
aws_lambda = sys.path.append(os.environ['AWS_SHARED_FUNC'])
from create_boto3_session_from_json import *

session = create_boto3_session(json_file_path = os.environ["AWS_KEY"])

def create_cloudwatch_rule(rule_name, target_lambda_arn, delay_seconds):
    # Calculate the minute mark
    minute_mark = delay_seconds // 60

    # Create the CloudWatch Events rule using AWS CLI
    try:
        aws_command = f"aws events put-rule --name {rule_name} --schedule-expression 'cron(* * * * ? {minute_mark} *)' --state ENABLED"
        subprocess.run(aws_command, shell=True, check=True)
        print(f"Rule '{rule_name}' created successfully with a {delay_seconds} second delay.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating rule: {e}")

    # Add the Lambda function as a target to the rule
    try:
        aws_command = f"aws events put-targets --rule {rule_name} --targets Id=1,Arn={target_lambda_arn}"
        subprocess.run(aws_command, shell=True, check=True)
        print(f"Lambda function '{target_lambda_arn}' added as a target to rule '{rule_name}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error adding target: {e}")

if __name__ == "__main__":
    # Build the Lambda ARN from the current (default) AWS identity
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()['Account']
    region = boto3.session.Session().region_name or 'us-east-1'
    function_name = 'dados_disponibilidade_porto_rdqa'
    target_lambda_arn = f'arn:aws:lambda:{region}:{account_id}:function:{function_name}'
    rule_name = 'DelayedInvocationRule'
    delay_seconds = 200  
    create_cloudwatch_rule(rule_name, target_lambda_arn, delay_seconds)

