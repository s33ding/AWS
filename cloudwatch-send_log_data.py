import boto3
import os
import time
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.argv_parser import get_input
from shared_func.cloudwatch_func import send_log_data

# Get the path to the JSON file containing AWS credentials from an environment variable
json_file_path = os.environ["AWS_KEY"]

# Read the AWS credentials from the JSON file
session = create_boto3_session(json_file_path)

log_group_name = input("Please enter the name of the CloudWatch Logs log group: ")
log_stream_name = input("Please enter the name of the CloudWatch Logs log stream: ")
log_data = input("Please enter the log data (separated by commas): ")

resp = send_log_data(log_group_name, log_stream_name, log_data)
print(resp)
