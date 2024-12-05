from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.argv_parser import get_input
from shared_func.secret_manager_func import delete_secret
import boto3
import json
import os

# Read the AWS credentials from the JSON file
session = create_boto3_session()

secret_name = get_input("secret_name: ")

res = delete_secret(secret_name)
print("Secret '{}' successfully deleted from Secrets Manager.".format(res))

