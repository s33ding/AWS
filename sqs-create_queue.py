import sys
from shared_func.sqs_func import create_sqs_queue

if len(sys.argv) != 2:
    queue_name = input("Enter the name of the SQS Queue: ")
else:
    queue_name = sys.argv[1]

create_sqs_queue(queue_name)

print(f"Created SQS queue with name: {queue_name}")
