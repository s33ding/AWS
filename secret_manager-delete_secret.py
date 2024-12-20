from shared_func.argv_parser import get_input
from shared_func.secret_manager_func import delete_secret
import boto3
import json
import os


secret_name = get_input("secret_name: ")

res = delete_secret(secret_name)
print("Secret '{}' successfully deleted from Secrets Manager.".format(res))

