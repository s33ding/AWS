import boto3
from botocore.exceptions import ClientError
import os
import json
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.glue_data_catalog import glue_retrieves_table_details
from shared_func.argv_parser import get_input

session = create_boto3_session()

# Prompt user for database and table names
database_name = input("database: ")
table_name = input("table: ")

# Call the function to retrieve table schema and print it
tbl_schema = glue_retrieves_table_details(database_name, table_name)
print(tbl_schema)

