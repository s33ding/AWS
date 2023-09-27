import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.sqs_func import *

session = create_boto3_session()

if len(sys.argv) != 2:
    queue_arn = input("Enter the name of the SQS arn: ")
else:
    queue_arn = sys.argv[1]

delete_sqs_queue(queue_arn)

print(f"Deleted SQS queue with name: {queue_arn}")
