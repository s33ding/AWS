import boto3
import botocore
import os
import json


def get_s3_client():
    # Load AWS credentials from JSON file
    with open(os.environ['AWS_KEY'], "r") as f:
        credentials = json.load(f)

    # Create a Boto3 session using the loaded credentials
    session = boto3.Session(
        aws_access_key_id=credentials['id'],
        aws_secret_access_key=credentials['secret'],
        aws_session_token=credentials['token'],
        region_name='us-east-1')

    # Create an S3 client using the session
    s3_client = session.client('s3')

    return s3_client


def check_file_exists_s3(bucket_name, key):
    # Get an S3 client
    s3_client = get_s3_client()

    try:
        # Check if the object exists in S3
        s3_client.head_object(Bucket=bucket_name, Key=key)
    except botocore.exceptions.ClientError as e:
        # If the object does not exist, return False
        if e.response['Error']['Code'] == "404":
            return False
        # Otherwise, raise the error
        else:
            raise e

    # If the object exists, return True
    return True


if __name__ == '__main__':
    bucket_name = input("Enter the name of the S3 bucket: ")
    key = input("Enter the key or path of the file to check: ")

    if check_file_exists_s3(bucket_name, key):
        print(f"The file '{key}' exists in the '{bucket_name}' bucket.")
    else:
        print(f"The file '{key}' does not exist in the '{bucket_name}' bucket.")

