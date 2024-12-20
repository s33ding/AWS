import sys
import boto3
import json
import os
from shared_func.iam_func import *

# Define lambda functions to set default values if no arguments are provided

# Define lambda functions to set default values if no arguments are provided
set_policy_name = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter IAM Policy Name: "
)
set_policy_document_file = lambda: sys.argv[2] if len(sys.argv) > 2 else input(
    "Enter the path to the JSON policy document file: "
)

# Set the variables using the lambda functions
policy_name = set_policy_name()
policy_document_file = set_policy_document_file()

# Ask for user input if any of the arguments is None
    
if policy_document_file is not None:
    arn = create_iam_policy(policy_name=policy_name, policy_document_file=policy_document_file)

    if arn:
        print(f"IAM policy created with ARN: {arn}")
