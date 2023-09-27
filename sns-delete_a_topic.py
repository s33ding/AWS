import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.sns_func import *

session = create_boto3_session()

# Define lambda function to set default user name if not provided as an argument
topic_arn_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter the arn name: "
)

# Get the user name using the lambda function
topic_arn = topic_arn_func()
delete_sns_topic(topic_arn)
