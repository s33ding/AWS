from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.argv_parser import get_input
from shared_func.secret_manager_func import list_secrets
import boto3
import json
import os

# Read the AWS credentials from the JSON file
session = create_boto3_session()

lst = list_secrets()
