import boto3
import os
import time
from shared_functions.create_boto3_session_from_json import create_boto3_session
from shared_functions.argv_parser import get_input

def create_log_group(log_group_name):
    # create a CloudWatch Logs client
    client = boto3.client('logs')

    # create the log group
    response = client.create_log_group(logGroupName=log_group_name)

    # print the response
    print(response)

    # return the response
    return response

# Get the path to the JSON file containing AWS credentials from an environment variable
json_file_path = os.environ["AWS_KEY"]

# Read the AWS credentials from the JSON file
session = create_boto3_session(json_file_path)

log_group_name = get_input("log_group_name:")
resp = create_log_group(log_group_name)
print(resp)
