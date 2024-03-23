import boto3
import os
import time
from shared_functions.create_boto3_session_from_json import create_boto3_session
from shared_functions.argv_parser import get_input

def delete_log_stream(log_group_name, log_stream_name):
    # create a CloudWatch Logs client
    client = boto3.client('logs')

    # delete the log stream
    response = client.delete_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)

    # return the response
    return response

# Get the path to the JSON file containing AWS credentials from an environment variable
json_file_path = os.environ["AWS_KEY"]

# Read the AWS credentials from the JSON file
session = create_boto3_session(json_file_path)

log_group_name = input("Please enter the name of the CloudWatch Logs log group: ")
log_stream_name = input("Please enter the name of the CloudWatch Logs log stream: ")

resp = delete_log_stream(log_group_name, log_stream_name)
print(resp)

# Use split(",") to split the log data into separate messages if needed. For example, if the input is "error, file not found, critical", splitting it into a list will give you ["error", "file not found", "critical"], which you can then send as separate log messages.
