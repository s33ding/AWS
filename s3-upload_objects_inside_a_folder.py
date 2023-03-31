import boto3
import pandas as pd
import json
import os 

with open (os.environ["AWS_KEY"], "r") as f:
    cred = json.load(f)

s3 = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id=cred.get('id'),
    aws_secret_access_key=cred.get('secret'),
    aws_session_token=cred.get('token')
)

bucket_name =  input("BUCKET NAME:")
obj_key =  input("OBJECT KEY NAME:")

def s3_upload_file(bucket_name, file_name, obj_key):
    print("UPLOADING:", file_name)
    s3.upload_file(Bucket=bucket_name, Filename=file_name, Key=obj_key)

s3_upload_file(bucket_name, file_name, obj_key)
