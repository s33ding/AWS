import boto3
import subprocess
from shared_func.ecr_func import *
from shared_func.create_boto3_session_from_json import *

# Create ECR repository
res = list_ecr_repositories()
