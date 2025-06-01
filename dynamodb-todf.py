import sys
from shared_func.dynamo_func import * 
import json
import os

# Define lambda function to set default user name if not provided as an argument
get_input = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Table name: "
)

# Get the user name using the lambda function
table_name = get_input()


df = dynamodb_to_dataframe(table_name)
print(df)
