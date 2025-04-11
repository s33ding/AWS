import json
import os
import boto3
from botocore.exceptions import ClientError
import pandas as pd

def insert_into_dynamodb_batch(table_name, items):
    """
    Inserts multiple items into a DynamoDB table in batches.

    Parameters:
    - table_name (str): The name of the DynamoDB table to insert the items into.
    - items (list): A list of dictionaries representing the items to insert.

    Returns:
    - None
    """
    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')

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
    dynamodb = boto3.resource('dynamodb')
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
    dynamodb = boto3.client('dynamodb')
    # Call the list_tables method to retrieve a list of table names
    table_list = dynamodb.list_tables()['TableNames']
    # Return the list of table names
    return table_list

def retrieve_from_dynamodb(table_name, key):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.get_item(Key=key)
    return response.get('Item')

def create_dynamodb_table(table_name, attribute_definitions, key_schema):
    dynamodb = boto3.client('dynamodb')
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

def empty_dynamodb_table(table_name, region_name='us-east-1'):
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table(table_name)

    print(f"Scanning table '{table_name}'...")

    # Scan the table and collect all items
    response = table.scan()
    data = response.get('Items', [])
    print(f"Scanned {len(data)} items.")

    # Continue scanning if there are more pages
    page = 1
    while 'LastEvaluatedKey' in response:
        print(f"Fetching page {page + 1}...")
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        scanned_items = response.get('Items', [])
        data.extend(scanned_items)
        print(f"Scanned {len(scanned_items)} more items (total so far: {len(data)}).")
        page += 1

    print(f"Starting deletion of {len(data)} items...")

    # Delete each item
    with table.batch_writer() as batch:
        for idx, item in enumerate(data, start=1):
            key = {k['AttributeName']: item[k['AttributeName']] for k in table.key_schema}
            batch.delete_item(Key=key)
            print(f"[{idx}/{len(data)}] Deleted item with key: {key}")

    print(f"\n✅ All {len(data)} items deleted from '{table_name}'.")





