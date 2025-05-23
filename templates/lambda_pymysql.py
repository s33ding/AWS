import json
import pymysql
from os import environ

def exec_stmt(cmd):
    conn = pymysql.connect(host=environ['host'],user=environ['user'], passwd=environ['password'], connect_timeout=10)
    cur = conn.cursor()
    cur.execute(cmd)
    conn.close()

def lambda_handler(event, context): 
    cmd = s3_get_data(bucket_name= 'inserts', object_key='file.sql')
    try:
        exec_stmt(cmd)
    except Exception as e:
        print(f"ERRO: {e}, STMT: '{cmd}';")
    
    return {'statusCode': 200,'body': json.dumps("ok")}
