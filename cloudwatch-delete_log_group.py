import boto3
import os
import time
from shared_functions.create_boto3_session_from_json import create_boto3_session
from shared_functions.argv_parser import get_input

def delete_log_group(log_group_name):
    # create a CloudWatch Logs client
    client = boto3.client('logs')

    # list all log streams within the log group
    response = client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy='LastEventTime',
        descending=True
    )
    log_streams = response.get('logStreams', [])

    # delete all log events within each log stream
    for log_stream in log_streams:
        client.delete_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream['logStreamName']
        )

    # delete the log group
    client.delete_log_group(logGroupName=log_group_name)

    # return the response
    return True

# Get the path to the JSON file containing AWS credentials from an environment variable
json_file_path = os.environ["AWS_KEY"]

# Read the AWS credentials from the JSON file
session = create_boto3_session(json_file_path)

log_group_name = get_input("log_group_name:")
resp = delete_log_group(log_group_name)
print(resp)
