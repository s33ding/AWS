import boto3
from botocore.exceptions import ClientError
import os
import json
from shared_func.glue_func import glue_retrieves_table_details
from shared_func.argv_parser import get_input


# Prompt user for database and table names
database_name = input("database: ")
table_name = input("table: ")

# Call the function to retrieve table schema and print it
tbl_schema = glue_retrieves_table_details(database_name, table_name)
print(tbl_schema)

