import sys
import boto3
import pandas as pd
import json
import os

with open (os.environ['AWS_KEY'], "r") as f:
    cred = json.load(f)

s3 = boto3.client('s3', 
                 region_name='us-east-1',
                 aws_access_key_id=cred.get("id"), 
                 aws_session_token=cred.get('token'),
                 aws_secret_access_key=cred.get("secret"))

bucket_nm = input("BUCKET: ")
prefix_str = input("PREFIX: ")

response = s3.list_objects_v2(Bucket=bucket_nm, Prefix=prefix_str)

files = [obj['Key'] for obj in response.get("Contents")]

for key_obj in files:
    print(f"DELETING: {key_obj}")
    response = s3.delete_object(Bucket=bucket_nm,Key=key_obj)


