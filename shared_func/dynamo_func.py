import json
import os
import boto3
from botocore.exceptions import ClientError
<<<<<<< HEAD
=======
import pandas as pd
>>>>>>> 9a288f5 (saving)

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

def create_dynamodb_table(session, table_name, attribute_definitions, key_schema):
    dynamodb = session.client('dynamodb')
    print("creating the DynamoDB tbl")
    try:
        response = dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schema,
            #ProvisionedThroughput=provisioned_throughput
            BillingMode='PAY_PER_REQUEST'  # Use on-demand capacity mode
        )
        print("Table created successfully!")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Table already exists.")
        else:
            print("Error:", e)

## Define provisioned throughput

#    provisioned_throughput = {
#        'ReadCapacityUnits': 5,
#        'WriteCapacityUnits': 5
#    }

def list_keys_from_dynamodb(table_name):
    """
    List keys from a DynamoDB table.

    Args:
    - table_name (str): The name of the DynamoDB table.

    Returns:
    - list: A list of primary key values from the table.
    """
    # Initialize the DynamoDB client
    dynamodb = boto3.client('dynamodb')

    try:
        # Use the scan operation to list keys
        response = dynamodb.scan(TableName=table_name, Select='ALL_ATTRIBUTES')

        # Extract the keys from the response
#        keys = [item['YourPrimaryKeyName'] for item in response['Items']]

        return response

    except Exception as e:
        print(f"Error: {e}")
        return []

def query_dynamodb_columns(table_name, lst_cols):
    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')

    results = {}

    for column_name in lst_cols:
        # Define the query parameters for each column
        key_condition_expression = Key(column_name).exists()

        try:
            # Execute the query for the current column
            response = dynamodb.query(
                TableName=table_name,
                KeyConditionExpression=key_condition_expression
            )

            # Store the results for the current column
            results[column_name] = response.get('Items', [])
        except Exception as e:
            print(f"Error querying DynamoDB for column {column_name}: {e}")
            results[column_name] = []

    return results

<<<<<<< HEAD
import boto3
import pandas as pd
=======
>>>>>>> 9a288f5 (saving)

def dynamodb_to_dataframe(table_name):
    # Initialize a Boto3 DynamoDB client
    dynamodb = boto3.client('dynamodb', region_name="us-east-1")
    # Create an empty list to store the DynamoDB items
    items = []

    # Use a scan operation to retrieve all items from the table
    response = dynamodb.scan(TableName=table_name)

    # Continue scanning through the entire table if the response is paginated
    while 'LastEvaluatedKey' in response:
        items.extend(response['Items'])
        response = dynamodb.scan(TableName=table_name, ExclusiveStartKey=response['LastEvaluatedKey'])

    # Add the remaining items from the last response
    items.extend(response['Items'])

    # Extract just the values from the DynamoDB items
    extracted_data = []
    for item in items:
        extracted_item = {}
        for key, value in item.items():
            if 'S' in value:
                extracted_item[key] = value['S']
            elif 'N' in value:
                extracted_item[key] = float(value['N'])
        extracted_data.append(extracted_item)

    # Convert the extracted data to a Pandas DataFrame
    df = pd.DataFrame(extracted_data)

    return df
