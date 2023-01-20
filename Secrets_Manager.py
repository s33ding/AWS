#source: https://www.youtube.com/watch?v=l0tTbavDb7g

import boto3
import mysql.connector
import json
import os

with open (os.environ["AWS_CRED"], "r") as f:
    cred = json.load(f)

session = boto3.session.Session()
client = boto3.client('secretsmanager', region_name='us-east-1',
                      aws_access_key_id=cred.get("id"),
                      aws_secret_access_key=cred.get("secret"))

try:
    secret_id = sys.argv[1]
except:
    secret_id = input("SECRET_ID: ")
get_secret_value_response = client.get_secret_value(SecretId=secret_id)
dct = json.loads(get_secret_value_response['SecretString'])
print(dct)
