from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.argv_parser import get_input
from shared_func.secret_manager_func import create_secret
import boto3
import json
import os

# Read the AWS credentials from the JSON file
session = create_boto3_session()

new_secret_name = "template"

secret = dict()
secret["template"]=""

response = create_secret(new_secret_name, secret)
print("New secret successfully added to Secrets Manager.")
