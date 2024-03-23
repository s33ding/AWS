"""
This script demonstrates how to use the Amazon Rekognition client in boto3 with temporary AWS credentials.

The credentials are read from a JSON file that contains the following keys:
- id: The access key ID.
- secret: The secret access key.
- token: The session token.

The script prompts the user to enter the path to an image file, and uses the Rekognition client to detect labels in the image.

"""

import sys
import boto3
import pandas as pd
import json
import os

# Load AWS key from environment variable and read credentials from file
with open(os.environ['AWS_KEY'], 'r') as f:
    cred = json.load(f)

# Create Rekognition client object with temporary credentials
rekog = boto3.client(
    'rekognition',
    region_name='us-east-1',
    aws_access_key_id=cred.get('id'),
    aws_secret_access_key=cred.get('secret'),
    aws_session_token=cred.get('token')
)

def rekog_detect_labels(image_file_path=''):
    if len(sys.argv) > 1:
        image_file_path = sys.argv[1]

    if image_file_path == '':
        image_file_path = input('image_file_path: ')

    # Read the image file into memory
    with open(image_file_path, 'rb') as image:
        image_binary = image.read()

    # Call the Amazon Rekognition detect_labels function
    response = rekog.detect_labels(Image={'Bytes': image_binary})

    return response

# Call the rekog_detect_labels function and print the response
res = rekog_detect_labels()
print(res)

