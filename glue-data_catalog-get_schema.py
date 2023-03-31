import boto3
from botocore.exceptions import ClientError
import os
import json

# Load credentials from environment variable
with open (os.environ['AWS_KEY'], "r") as f:
    credentials = json.load(f)

# Create a Boto3 session using the loaded credentials
session = boto3.Session(
    aws_access_key_id=credentials['id'],
    aws_secret_access_key=credentials['secret'],
    aws_session_token=credentials['token'],  # Add the temporary token
    region_name='us-east-1'
)

# Define a function to retrieve table details using Glue API
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

# Prompt user for database and table names
database_name = input("database: ")
table_name = input("table: ")

# Call the function to retrieve table schema and print it
tbl_schema = retrieves_table_details(database_name, table_name)
print(tbl_schema)

