import sys
import boto3
import json
import os

with open(os.environ["AWS_KEY"]) as file:
    cred = json.load(file)


client = boto3.client('ssm', 
                      region_name='us-east-1', 
                      aws_access_key_id=cred.get('usr'), 
                      aws_secret_access_key=cred.get('passwd')
                      )

try:
    paramter_name = sys.argv[1]
except:
    paramter_name = input("PARAMTER_NAME: ") 
request = client.get_parameter(Name = paramter_name, WithDecryption=True)
result = request['Parameter']['Value']
print(result)
