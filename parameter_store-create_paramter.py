import sys
import boto3
import json
import os
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.argv_parser import get_input
from shared_func.parameter_store_func import create_ssm_parameter

# Read the AWS credentials from the JSON file
session = create_boto3_session()


# Prompt user for parameter name or use command-line argument
parameter_name = get_input("parameter_name: ")

# Prompt user for parameter name or use command-line argument
parameter_value = get_input("parameter_value: ")

res = create_ssm_parameter(
        parameter_name = parameter_name, 
        parameter_value = parameter_value
        )

print(res)

