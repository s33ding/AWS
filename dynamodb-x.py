import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.dynamo_func import * 
import json
import os

# Initialize the Amazon DynamoDB client
session = create_boto3_session()
table_name = sys.argv[1]
cols = [""]
res = list_keys_from_dynamodb(table_name)
print("res:",res)

