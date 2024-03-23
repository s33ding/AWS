import sys
import boto3
import json
import os
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.iam_func import *

session = create_boto3_session()

# Define lambda functions to set default values if no arguments are provided
role_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter IAM Role Name: "
)
policy_arn_func = lambda: sys.argv[2] if len(sys.argv) > 2 else input(
    "Enter the Policy ARN to attach: "
)

# Get values for role_name and policy_arn using lambda functions
role_name = role_name_func()
policy_arn = policy_arn_func()


if __name__ == "__main__":
    # Call attach_policy_to_role with the obtained values
    attach_policy_to_role(role_name, policy_arn)
