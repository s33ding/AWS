import boto3
from botocore.exceptions import ClientError
import os
import json
from shared_func.glue_func import start_crawler
from shared_func.argv_parser import get_input

crawler_name = get_input(message='Please enter a value: ')


start_crawler(crawler_name)
