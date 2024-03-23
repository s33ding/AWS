import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
import json

with open('SOURCE/credential.json','r') as f:
    cred = json.load(f) 

regionName = 'us-east-1'
serviceName = 'execute-api'
hostName = f"xxxxxxxxxx.{serviceName}.{regionName}.amazonaws.com"
projectName = "my-script"

auth = AWSRequestsAuth(
                       aws_access_key=cred['id'],
                       aws_secret_access_key=cred['secret'],
                       aws_token=cred['token'],
                       aws_host=hostName,
                       aws_region=regionName,
                       aws_service=serviceName)

response = requests.post(f'https://{hostName}/{projectName}-xxxx', auth=auth, json=payload)

json.loads(response.content)
