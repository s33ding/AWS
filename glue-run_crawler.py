import boto3
from botocore.exceptions import ClientError
import os
import json
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.glue_func import start_crawler
from shared_func.argv_parser import get_input

session = create_boto3_session()


crawler_name = get_input(message='Please enter a value: ')


start_crawler(crawler_name)
