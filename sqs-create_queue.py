import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.sqs_func import create_sqs_queue

session = create_boto3_session()

if len(sys.argv) != 2:
    queue_name = input("Enter the name of the SQS Queue: ")
else:
    queue_name = sys.argv[1]

create_sqs_queue(queue_name)

print(f"Created SQS queue with name: {queue_name}")
