import boto3
import pandas as pd
import json
import os 
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.argv_parser import get_input

# Read the AWS credentials from the JSON file
session = create_boto3_session()

bucket_name =  input("BUCKET NAME:")
obj_key =  input("OBJECT KEY NAME:")

def s3_upload_file(bucket_name, file_name, obj_key):
    print("UPLOADING:", file_name)
    s3.upload_file(Bucket=bucket_name, Filename=file_name, Key=obj_key)

s3_upload_file(bucket_name, file_name, obj_key)
