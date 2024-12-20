from shared_func.argv_parser import get_input
from shared_func.secret_manager_func import get_secret
import boto3
import json
import os


secret_name = get_input("secret_name: ")
res = get_secret(secret_name)
# Use Secrets Manager client object to get secret value
print("res:",res)

