import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.sns_func import *

session = create_boto3_session()

topic_arn_func= lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter the topic arn: "
)

topic_arn = topic_arn_func()
# List subscriptions for a topic
list_topic_subscriptions(topic_arn, sns_client=None)
