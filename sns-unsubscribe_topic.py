import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.sns_func import *

# Define lambda function to set default user name if not provided as an argument
subscribe_arn_func= lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter the subscribe arn: "
)

# Example usage of protocol_func
subscription_arn = subscribe_arn_func()
unsubscribe_from_topic(subscription_arn)
