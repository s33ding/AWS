import os 
import json 

with open(os.environ['AWS_TEMP_CRED'],'r') as f:
    dt=json.load(f)

aws = dt.get('Credentials')

os.system("touch ~/.aws/credentials")
with open(os.environ['AWS_CRED'],'w') as f:
    f.write(f"[default]\n")
    f.write(f"aws_access_key_id = {aws['AccessKeyId']}\n")
    f.write(f"aws_secret_access_key = {aws['SecretAccessKey']}\n")
    f.write(f"aws_security_token = {aws['SessionToken']}\n")
