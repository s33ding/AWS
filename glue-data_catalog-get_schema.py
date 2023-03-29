import boto3
from botocore.exceptions import ClientError
import os
import json

with open (os.environ['AWS_KEY'], "r") as f:
    credentials = json.load(f)

# Create a Boto3 session using the loaded credentials
session = boto3.Session(
    aws_access_key_id=credentials['id'],
    aws_secret_access_key=credentials['secret'],
    region_name='us-east-1'
)

def retrieves_table_details(database_name, table_name):
   glue_client = session.client('glue')
   try:
      response = glue_client.get_table(DatabaseName = database_name, Name = table_name)
      response = response["Table"]["StorageDescriptor"]["Columns"]
      return response
   except ClientError as e:
      raise Exception("boto3 client error in retrieves_table_details: " + e.__str__())
   except Exception as e:
      raise Exception("Unexpected error in retrieves_table_details: " + e.__str__())

database_name = input("database: ")
table_name = input("table: ")

tbl_schema = retrieves_table_details(database_name, table_name)
print(tbl_schema)

