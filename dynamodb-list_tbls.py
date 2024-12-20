import sys
from shared_func.dynamo_func import * 
import json
import os

res = list_dynamodb_tables()
print("res:",res)

