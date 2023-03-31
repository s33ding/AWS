"""
This script demonstrates how to use the Amazon S3 client in boto3 with temporary AWS credentials.

The credentials are read from a JSON file that contains the following keys:
- id: The access key ID.
- secret: The secret access key.
- token: The session token.

The script prompts the user to enter the name of an S3 bucket and a string to search for. It then uses the S3 client to list all objects in the bucket and prints the key of each object that contains the specified string in its name to the console.

"""

import sys
import boto3
import pandas as pd
import json
import os

# Load AWS key from environment variable and read credentials from file
with open(os.environ['AWS_KEY'], 'r') as f:
    cred = json.load(f)

# Create S3 client object with temporary credentials
s3 = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id=cred.get('id'),
    aws_secret_access_key=cred.get('secret'),
    aws_session_token=cred.get('token')
)

def list_objects(bucket_nm: str, search_str: str):
    """
    Lists all objects in the specified bucket whose key contains the specified search string.
    """
    # Use S3 client object to list all objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_nm)

    # Extract the key of each object from the response and filter the objects whose key contains the specified search string
    files = [obj['Key'] for obj in response.get('Contents') if search_str in obj['Key']]

    return files

# Prompt user for bucket name and search string
bucket_nm = input('BUCKET: ')
search_str = input('SEARCH STRING: ')

# Call the list_objects function to get the list of filtered objects and print each object key to the console
files = list_objects(bucket_nm, search_str)
for key_obj in files:
    print(f'{key_obj}')
    #response = s3.delete_object(Bucket=bucket_nm, Key=key_obj)

