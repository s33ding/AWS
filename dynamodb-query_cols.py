import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.dynamo_func import * 
import json
import os

# Initialize the Amazon DynamoDB client
session = create_boto3_session()
table_name = "FaceAnalysisTable"
lst_cols = ["RealAge", "AgeRange"]
res = query_dynamodb_columns(table_name, lst_cols)
print("res:",res)

