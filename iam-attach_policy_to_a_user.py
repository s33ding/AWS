import sys
import boto3
import json
import os
from shared_func.iam_func import *

# Define lambda functions to set default values if no arguments are provided
user_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter IAM User Name: "
)
policy_arn_func = lambda: sys.argv[2] if len(sys.argv) > 2 else input(
    "Enter the Policy ARN to attach: "
)

# Get values for user_name and policy_arn using lambda functions
user_name = user_name_func()
policy_arn = policy_arn_func()

if __name__ == "__main__":
    # Call attach_policy_to_user with the obtained values
    attach_policy_to_user(user_name, policy_arn)
