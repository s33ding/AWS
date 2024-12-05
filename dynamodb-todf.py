import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.dynamo_func import * 
import json
import os

# Initialize the Amazon DynamoDB client
session = create_boto3_session()

# Example usage:
<<<<<<< HEAD
table_name = 'FaceAnalysis'
=======
table_name = 'disponibilidade'
>>>>>>> 9a288f5 (saving)

df = dynamodb_to_dataframe(table_name)
print(df)
