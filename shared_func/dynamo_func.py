import json
import os
import boto3

def insert_into_dynamodb_batch(session, table_name, items):
    """
    Inserts multiple items into a DynamoDB table in batches.

    Parameters:
    - session (boto3.Session): The active AWS session.
    - table_name (str): The name of the DynamoDB table to insert the items into.
    - items (list): A list of dictionaries representing the items to insert.

    Returns:
    - None
    """
    # Create a DynamoDB client
    dynamodb = session.client('dynamodb')

    # Determine the maximum number of items per batch (25 items is the maximum allowed by DynamoDB)
    max_items_per_batch = 25

    # Split the items into batches
    batches = [items[i:i+max_items_per_batch] for i in range(0, len(items), max_items_per_batch)]

    # Perform batch write operations for each batch of items
    for batch in batches:
        # Create a batch write request
        batch_items = [{'PutRequest': {'Item': item}} for item in batch]
        request_items = {table_name: batch_items}

        # Batch write items to DynamoDB
        dynamodb.batch_write_item(RequestItems=request_items)

def insert_into_dynamodb(session,table_name, dct):
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

def list_dynamodb_tables(session):
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
    # Create a Boto3 session using the loaded credentials
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.get_item(Key=key)
    return response.get('Item')

def create_dynamodb_table(table_name, attribute_definitions, key_schema, provisioned_throughput):
    dynamodb = boto3.client('dynamodb')
    
    try:
        response = dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schema,
            ProvisionedThroughput=provisioned_throughput
        )
        print("Table created successfully!")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Table already exists.")
        else:
            print("Error:", e)
