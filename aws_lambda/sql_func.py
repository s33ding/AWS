import boto3
import json
import pymysql
from os import environ

def write_sql_file_to_s3(bucket_name, key_name, sql_string):
    s3 = boto3.resource('s3')
    # Upload SQL string to S3 file
    s3.Object(bucket_name, key_name).put(Body=sql_string)

    # Return URL of the S3 file
    return f's3://{bucket_name}/{key_name}'

def download_sql_file(bucket_name, key_name):
    obj = s3.get_object(Bucket=bucket_name, Key=key_name)
    body = obj['Body'].read().decode('utf-8')
    return body

def exec_stmt(cmd):
    conn = pymysql.connect(host=environ['host'],user=environ['user'], passwd=environ['password'], connect_timeout=10)
    cur = conn.cursor()
    cur.execute(cmd)
    conn.close()
