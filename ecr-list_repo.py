import boto3
import subprocess
from shared_func.ecr_func import *
from shared_func.create_boto3_session_from_json import *

# Example usage
region = 'us-east-1'
repository_name = 'tst'
image_name = 'img-tst'

# Create an optional specific AWS session
session = create_boto3_session()

# Create ECR repository
res = list_ecr_repositories(session)