import sys
import boto3
import json
import os
from shared_func.iam_func import *

# Define lambda functions to set default values if no arguments are provided
user_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter the User Name: "
)
username = user_name_func()


if __name__ == "__main__":
    #disable_aws_access_key(username)
    enable_aws_access_key(username)

