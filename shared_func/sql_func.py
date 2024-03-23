import sys
import os
import boto3
from time import sleep
import json
import pymysql
from os import environ
import mysql.connector
from secret_manager_func import *

def create_boto3_session(json_file_path = os.environ["AWS_KEY"]):
    """
    Creates a new Boto3 session using AWS credentials stored in a JSON file.

    Parameters:
    - json_file_path (str): The path to the JSON file containing the AWS credentials.

    Returns:
    - Boto3 session object.
    """
    aws_key, aws_secret, aws_token = read_aws_credentials(json_file_path)
    return boto3.Session(
        region_name='us-east-1',
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        aws_session_token=aws_token
    )

def read_aws_credentials(json_file_path):
    """
    Reads the AWS credentials from a JSON file.

    Parameters:
    - json_file_path (str): The path to the JSON file containing the AWS credentials.

    Returns:
    - Tuple containing the AWS access key ID, secret access key, and session token.
    """
    with open(json_file_path) as f:
        credentials = json.load(f)
        aws_key = credentials.get("id")
        aws_secret = credentials.get("secret")
        aws_token = credentials.get("token")
    return aws_key, aws_secret, aws_token

def write_sql_file_to_s3(bucket_name, key_name, sql_string):
    s3 = boto3.resource('s3')
    # Upload SQL string to S3 file
    s3.Object(bucket_name, key_name).put(Body=sql_string)

    # Return URL of the S3 file
    return f's3://{bucket_name}/{key_name}'

def download_sql_file(bucket_name, key_name):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=key_name)
    body = obj['Body'].read().decode('utf-8')
    return body


def get_database_credentials():
    try:
        json_file = environ['MYSQL_CRED']
    except KeyError:
        json_file = None

    if json_file is None:
        # Use environment variables directly
        db_cred = {
            "host" : environ['host'],
            "user" : environ['user'],
            "password" : environ['password']
        }
        sleep(1)
        print(f"connectings as: {environ['user']}.")

    else:
        # Get the database credentials from the JSON file
        with open(json_file, 'r') as f:
            db_cred = json.load(f)

    return db_cred

def get_master_database_credentials():
    try:
        json_file = environ['MYSQL_MASTER_CRED']
    except KeyError:
        json_file = None

    if json_file is None:
        db_cred = {
            "host" : environ['host'],
            "user" : environ['user'],
            "password" : environ['password']
        }

    else:
        # Get the database credentials from the JSON file
        with open(json_file, 'r') as f:
            db_cred = json.load(f)

    return db_cred 


def connect_to_database():
    """
    Connects to the database using the credentials in the JSON file or environment variables.
    """
    
    db_cred = get_master_database_credentials()
    connection = mysql.connector.connect(
        host=db_cred['host'],
        user=db_cred['user'],
        password=db_cred['password']
    )
    return connection


def query_mysql(query=None):
    if query is None:
        print("Query parameter is missing.")
        return None

    db_cred = get_database_credentials()

    # Connect to the database
    connection = pymysql.connect(
        host=db_cred['host'],
        user=db_cred['user'],
        password=db_cred['password'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

        # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

        # Close the connection and return the result
    connection.close()
    return result


def execute_sql_queries(queries):
    """
    Executes a list of SQL queries in a batch using transactions.
    """
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute("START TRANSACTION")
        for query in queries:
            print(query)
            cursor.execute(query)
        cursor.execute("COMMIT")
        print(f"Successfully executed {len(queries)} SQL queries.")
    except Exception as e:
        print("Error executing SQL queries:", e)
        cursor.execute("ROLLBACK")
        raise e
    finally:
        cursor.close()
        connection.close()

def record_exists(table_name, condition):
    # Establish a connection to the MySQL database
    db_cred = get_database_credentials()

    # Connect to the database
    connection = pymysql.connect(
        host=db_cred['host'],
        user=db_cred['user'],
        password=db_cred['password'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # Check if a record with the given condition already exists
            query = f"SELECT COUNT(*) FROM {table_name} WHERE {condition}"
            cursor.execute(query)
            result = cursor.fetchone()

            return result["COUNT(*)"] > 0
    finally:
        # Close the database connection
        connection.close()

def divide_into_sublists(data, max_size):
    """
    Divide a list into sublists of a maximum size.

    Args:
        data (list): The list to divide into sublists.
        max_size (int): The maximum size of each sublist.

    Returns:
        list: A list of sublists.
    """
    return [data[i:i+max_size] for i in range(0, len(data), max_size)]


def pd_query_mysql(query=None):
    if query is None:
        print("Query parameter is missing.")
        return None

    db_cred = get_database_credentials()

    # Connect to the database
    connection = pymysql.connect(
        host=db_cred['host'],
        user=db_cred['user'],
        password=db_cred['password'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    import pandas as pd 
    df = pd.read_sql(query, connection)
    return df



# Function to extract schema from AWS Glue
def get_glue_schema(database_name, table_name):
    # Set up AWS Glue client
    glue_client = boto3.client('glue')
    response = glue_client.get_table(
        DatabaseName=database_name,
        Name=table_name
    )
    schema = response['Table']['StorageDescriptor']['Columns']
    return schema

# Function to query MySQL using pandas and MySQL connector
def query_mysql_with_glue_schema(query):
    return pd.read_sql(query, con=mysql_connection)

def execute_stmt(stmt):
    """
    Executes a list of SQL queries in a batch using transactions.
    """
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute("STARTING")
        print(stmt)
        cursor.execute(stmt)
        cursor.execute("COMMITING")
        print(f"Successfully executed SQL stmt.")
    except Exception as e:
        print("Error executing SQL queries:", e)
        cursor.execute("ROLLBACK")
        raise e
    finally:
        cursor.close()
        connection.close()
