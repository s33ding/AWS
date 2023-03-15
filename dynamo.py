import boto3
import json
import os

def read_credentials_from_file(file_path):
    with open(file_path) as f:
        cred = json.load(f)
        return cred.get("id"), cred.get("secret")

def insert_into_dynamodb(table_name, dct):
    """
    Inserts an item into a DynamoDB table with a primary key.

    Parameters:
    - table_name (str): The name of the DynamoDB table to insert the item into.
    - dct (dict): A dictionary representing the item to insert, including the primary key.

    Returns:
    - None
    """
    # Create a DynamoDB resource
    dynamodb = session.resource('dynamodb')
    # Retrieve the specified table
    table = dynamodb.Table(table_name)
    # Insert the item into the table
    table.put_item(Item=dct, ConditionExpression='attribute_not_exists(PK)') # The ConditionExpression is used to ensure that the primary key attribute does not already exist.

def list_dynamodb_tables():
    """
    Lists all of the existing DynamoDB tables in the current region.

    Parameters:
    - None

    Returns:
    - List of strings representing the names of the DynamoDB tables.
    """
    # Create a DynamoDB client
    dynamodb = session.client('dynamodb')
    # Call the list_tables method to retrieve a list of table names
    table_list = dynamodb.list_tables()['TableNames']
    # Return the list of table names
    return table_list

def retrieve_from_dynamodb(table_name, key):
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.get_item(Key=key)
    return response.get('Item')

aws_key, aws_secret = read_credentials_from_file(os.environ["AWS_KEY"])

session = boto3.Session(region_name='us-east-1', aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)

table_list = list_dynamodb_tables()
print(table_list)
