import os
import time
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.cloudwatch_func import create_log_group
from shared_func.argv_parser import get_input

# Read the AWS credentials from the JSON file
session = create_boto3_session()

log_group_name = get_input("log_group_name:")
resp = create_log_group(log_group_name)
print(resp)
