import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.s3_objects  import *
from shared_func.argv_parser import get_input

# Read the AWS credentials from the JSON file
session = create_boto3_session()

# Prompt user for bucket name and search string
bucket_name = input('BUCKET: ')
folder_name_s3 = input('FOLDER: ')
search_str = input('SEARCH STRING: ')

res = list_objects(bucket_name, folder_name_s3, search_str)
# Call the list_objects function to get the list of filtered objects and print each object key to the console
print("res:")
for i,key_obj in enumerate(res):
    print(f'=================')
    print(f'index: {i}')
    print(f'object: {key_obj}')

