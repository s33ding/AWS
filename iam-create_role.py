import sys
import boto3
import json
import os
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.iam_func import *

# Read the AWS credentials from the JSON file
session = create_boto3_session()

# Define lambda functions to set default values if no arguments are provided
role_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter IAM Policy Name: "
)
policy_file_func = lambda: sys.argv[2] if len(sys.argv) > 2 else input(
    "Enter the path to the JSON policy document file: "
)
description_func = lambda: sys.argv[3] if len(sys.argv) > 3 else input(
    "Enter Description (default: Lambda Role): "
)

# another_script.py
if __name__ == "__main__":

    role_name = role_name_func()
    policy_file = policy_file_func()
    description = description_func()

    create_iam_role(
        role_name=role_name, 
        policy_file=None, 
        description=description
    )

    # Call create_iam_role with the obtained values
    arn = create_iam_role(
        role_name=role_name,
        policy_file=policy_file,
        description=description
    )

    if arn:
        print(f"IAM Role created with ARN: {arn}")
