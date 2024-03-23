import sys
import boto3
import pandas as pd
import json
import os
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.s3_objects import *
from shared_func.argv_parser import get_input

# Read the AWS credentials from the JSON file
session = create_boto3_session()

bucket_name = input("BUCKET: ")
folder_name = input("FOLDER NAME(PREFIX): ")

delete_all_s3_files_in_folder(bucket_name, folder_name)
