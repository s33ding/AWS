import sys
from shared_func.dynamo_func import * 
import json
import os

table_name = input('table_name:')

df = empty_dynamodb_table(table_name)
print(df)
