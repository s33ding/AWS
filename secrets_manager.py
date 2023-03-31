"""
This script demonstrates how to create a boto3 Secrets Manager client using temporary AWS credentials.

The credentials are read from a JSON file that contains the following keys:
- id: The access key ID.
- secret: The secret access key.
- token: The session token.

The script prompts the user to enter the ID of the secret to retrieve, and creates a client object using the provided credentials.

"""

import boto3
import json
import os

# Load AWS key from environment variable and read credentials from file
with open(os.environ['AWS_KEY'], 'r') as f:
    cred = json.load(f)

# Create Secrets Manager client object with temporary credentials
session = boto3.session.Session()
client = boto3.client(
    'secretsmanager',
    region_name='us-east-1',
    aws_access_key_id=cred.get('id'),
    aws_secret_access_key=cred.get('secret'),
    aws_session_token=cred.get('token')
)

# Prompt user for input or use command-line argument to specify the ID of the secret to retrieve
try:
    secret_id = sys.argv[1]
except:
    secret_id = input('SECRET_ID: ')

# Use Secrets Manager client object to get secret value
get_secret_value_response = client.get_secret_value(SecretId=secret_id)
dct = json.loads(get_secret_value_response['SecretString'])
print(dct)

