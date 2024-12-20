import os 

repo_name=os.environ["ECR_REPO_NAME"]
path_boto3_cred = os.environ["AWS_TEMP_CRED"]
kms_key_alias = os.environ["KMS_KEY_DEFAULT"]
