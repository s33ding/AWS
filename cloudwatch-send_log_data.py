import boto3
import os
import time
from shared_functions.create_boto3_session_from_json import create_boto3_session
from shared_functions.argv_parser import get_input

def send_log_data(log_group_name, log_stream_name, log_data):
    # create a CloudWatch Logs client
    client = boto3.client('logs')

    # create a new log stream
    response = client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)

    # put log events to the new log stream
    log_events = []
    for data in log_data:
        log_events.append({
            'timestamp': int(time.time() * 1000),
            'message': data
        })

    response = client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=log_events)
    
    # return the response
    return response

# Get the path to the JSON file containing AWS credentials from an environment variable
json_file_path = os.environ["AWS_KEY"]

# Read the AWS credentials from the JSON file
session = create_boto3_session(json_file_path)

log_group_name = input("Please enter the name of the CloudWatch Logs log group: ")
log_stream_name = input("Please enter the name of the CloudWatch Logs log stream: ")
log_data = input("Please enter the log data (separated by commas): ")

resp = send_log_data(log_group_name, log_stream_name, log_data)
print(resp)

# Use split(",") to split the log data into separate messages if needed. For example, if the input is "error, file not found, critical", splitting it into a list will give you ["error", "file not found", "critical"], which you can then send as separate log messages.
