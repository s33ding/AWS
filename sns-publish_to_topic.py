import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.sns_func import *

session = create_boto3_session()

# Define lambda function to set default user name if not provided as an argument
topic_arn_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter the topic arn: "
)

message_func = lambda: sys.argv[2] if len(sys.argv) > 2 else input(
    "Enter the message: "
)

# Get the user name using the lambda function
topic_arn = topic_arn_func()
message = message_func()
    
publish_to_topic(topic_arn, message, sns_client=None)
