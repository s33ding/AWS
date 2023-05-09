import boto3
from time import sleep
import json
import pymysql
from os import environ
from secret_manager_func import *


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
