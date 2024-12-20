import sys
from shared_func.sqs_func import *

queue_url = sys.argv[1] if len(sys.argv) > 1 else input("Enter the SQS Queue URL: ")
message_body = sys.argv[2] if len(sys.argv) > 2 else input("Enter the message body: ")

message_id = send_message_to_queue(queue_url, message_body)
print(f'Message sent with MessageId: {message_id}')
