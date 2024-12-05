import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.ses_func import *

# Define lambda function to set default user name if not provided as an argument
email = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter the topic name: "
)

verify_email(email)
