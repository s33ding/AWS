import boto3
import os
import time
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.argv_parser import get_input
from shared_func.cloudwatch_func import get_log_events

# Read the AWS credentials from the JSON file
session = create_boto3_session()

log_group_name = input("Please enter the name of the CloudWatch Logs log group: ")
log_stream_name = input("Please enter the name of the CloudWatch Logs log stream: ")

resp = get_log_events(log_group_name, log_stream_name)
print(resp)
