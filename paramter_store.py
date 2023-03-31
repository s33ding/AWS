import sys
import boto3
import json
import os

# Load AWS key from environment variable and read credentials from file
with open(os.environ['AWS_KEY'], 'r') as file:
    cred = json.load(file)

# Create SSM client object with temporary credentials
client = boto3.client(
    'ssm',
    region_name='us-east-1',
    aws_access_key_id=cred.get('usr'),
    aws_secret_access_key=cred.get('passwd'),
    aws_session_token=cred.get('token')
)

# Prompt user for parameter name or use command-line argument
try:
    parameter_name = sys.argv[1]
except:
    parameter_name = input('PARAMETER_NAME: ')

# Use SSM client object to get parameter value
response = client.get_parameter(Name=parameter_name, WithDecryption=True)
value = response['Parameter']['Value']
print(value)

