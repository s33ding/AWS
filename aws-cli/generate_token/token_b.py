import os 
import json 

with open(os.environ['AWS_KEY'],'r') as f:
    aws=json.load(f)

os.system("touch ~/.aws/credentials")
with open(os.environ['AWS_CRED'],'w') as f:
    f.write(f"[default]\n")
    f.write(f"aws_access_key_id = {aws['id']}\n")
    f.write(f"aws_secret_access_key = {aws['secret']}\n")
