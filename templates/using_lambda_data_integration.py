import pandas as pd
import os
import mysql.connector
import boto3
import sys
import json
import s3fs
from s3fs import S3FileSystem
import pyarrow.parquet as pq

def pd_mysql_con(query):
    with open(os.environ["MYSQL_CRED"], 'r') as f:
        db_ms = json.load(f)
    try:
        with mysql.connector.connect(host=db_ms['host'], user=db_ms["user"], password=db_ms["password"]) as engine_ms:
            return pd.read_sql(query, engine_ms)
    except mysql.connector.Error as e:
        return f"Error connecting to MySQL: {e}"

def get_secret(secret_name, session):
    client = session.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    return json.loads(get_secret_value_response['SecretString'])

def create_boto3_session(credentials_file, region='us-east-1'):
    with open(credentials_file, "r") as f:
        aws_credentials = json.load(f)
    return boto3.Session(region_name=region, aws_access_key_id=aws_credentials.get("usr"), aws_secret_access_key=aws_credentials.get("passwd"))

# Function to invoke another Lambda function
def invoke_lambda(my_payload, lambda_name, invocation_type):
  client = boto3.client("lambda")
  response = client.invoke(
      FunctionName = lambda_name,
      InvocationType = invocation_type, # best options: RequestResponse or Event
      Payload = json.dumps(my_payload))
  return response

def read_single_parquet(bucket, file_path):
    s3_filesystem = s3fs.S3FileSystem()
    with s3_filesystem.open(f'{bucket}/{file_path}') as f:
        df = pd.read_parquet(f)
    return df

session = create_boto3_session(credentials_file="b3.json")
dataset = sys.argv[1]
bucket_name = ""
lamb_arn = ""

my_payload = {
  "bucket":bucket_name ,
  "folder": dataset,
  "output_folder": f"{dataset}_integrated"
}


invoke_lambda(my_payload, lambda_name=lamb_arn, invocation_type="RequestResponse")

df = read_single_parquet(bucket=bucket_name, file_path = f'{dataset}_integrated/combined_file.parquet')

