import boto3
import subprocess
from shared_func.ecr_func import *
from shared_func.create_boto3_session_from_json import *

# Example usage
region = 'us-east-1'
repository_name = input('repository_name:')

# Create an optional specific AWS session
session = boto3.Session()

# Create ECR repository
repo_uri = delete_ecr_repository(session, repository_name)
