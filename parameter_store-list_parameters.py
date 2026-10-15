import sys
import boto3
import json
import os
from shared_func.argv_parser import get_input
from shared_func.parameter_store_func import list_ssm_parameters



# Prompt user for path or use command-line argument
path = get_input("parameter_path (default '/'): ") or '/'

# Use SSM client object to list parameters
parameters = list_ssm_parameters(path)

for param in parameters:
    print(param['Name'])
