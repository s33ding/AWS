import sys
from shared_func.dynamo_func import * 
import json
import os

table_name = input('table_name:')


df = dynamodb_to_dataframe(table_name)
print(df)
