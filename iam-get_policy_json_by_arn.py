import sys
import boto3
import json
import os
from shared_func.iam_func import *

pd.set_option('display.max_colwidth', None)

# Define lambda functions to set default values if no arguments are provided
policy_arn_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "policy arn: "
)

# Define lambda functions to set default values if no arguments are provided
file_path_func = lambda: sys.argv[2] if len(sys.argv) > 2 else None

policy_arn = policy_arn_func()
file_path = file_path_func()

res = get_policy_json_by_arn(policy_arn , file_path)
