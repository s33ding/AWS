import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.sqs_func import *

session = create_boto3_session()

list_sqs_queues()
