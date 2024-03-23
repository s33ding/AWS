import boto3
import os
import time
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.argv_parser import get_input
from shared_func.cloudwatch_func import delete_log_group

session = create_boto3_session()

log_group_name = get_input("log_group_name:")
resp = delete_log_group(log_group_name)
print(resp)
