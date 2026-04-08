import boto3
import subprocess
from shared_func.ecr_func import *

# Example usage
region = 'us-east-1'
repository_name = input('repository_name:')


# Create ECR repository
repo_uri = delete_ecr_repository(session, repository_name)
