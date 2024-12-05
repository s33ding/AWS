import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.dynamo_func import * 
import json
import os
<<<<<<< HEAD
=======
import boto3
>>>>>>> 9a288f5 (saving)

# Initialize the Amazon DynamoDB client
session = create_boto3_session()

<<<<<<< HEAD

create_dynamodb_table(
        session=session, 
        table_name="FaceAnalysis", 
        attribute_definitions= [
            {
                'AttributeName': 'PersonName',  # Use 'PersonName' as the attribute name
                'AttributeType': 'S'  # S represents a string data type
            },
            {
                'AttributeName': 'RealAge',  # Add a new attribute for birthdate
                'AttributeType': 'N'  # S represents a string data type
            }
        ], 
        key_schema = [
                {
                    'AttributeName': 'PersonName',
                    'KeyType': 'HASH'  # HASH indicates the partition key
                },
                {
                    'AttributeName': 'RealAge',
                    'KeyType': 'RANGE'  # RANGE indicates the sort key
                }
            ]   
        )
=======
def create_boto3_session():
    # Initialize a session using Amazon DynamoDB
    session = boto3.Session()
    return session

def create_dynamodb_table(session, table_name, attribute_definitions, key_schema):
    dynamodb = session.client('dynamodb')

    request = {
        "TableName": table_name,
        "KeySchema": key_schema,
        "AttributeDefinitions": attribute_definitions,
        "BillingMode": "PAY_PER_REQUEST"  # Set to on-demand (serverless) mode
    }

    print("Create Table Request:", request)  # Debugging line

    response = dynamodb.create_table(**request)

    return response

def create_dynamodb_table2(session, table_name, attribute_definitions, key_schema):
    dynamodb = session.client('dynamodb')

    request = {
        "TableName": table_name,
        "KeySchema": key_schema,
        "AttributeDefinitions": attribute_definitions,
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 100
        }
    }

    print("Create Table Request:", request)  # Debugging line

    response = dynamodb.create_table(**request)

    return response

session = create_boto3_session()

response = create_dynamodb_table(
    session=session,
    table_name="rdqa-tbl-id",
    attribute_definitions=[
        {
            'AttributeName': 'proj-tbl-id',  # Attribute used as HASH key
            'AttributeType': 'S'  # S represents a string data type
        },
        {
            'AttributeName': 'proj',  # Attribute used as RANGE key
            'AttributeType': 'S'  # S represents a string data type
        }
    ],
    key_schema=[
        {
            'AttributeName': 'proj-tbl-id',
            'KeyType': 'HASH'  # HASH indicates the partition key
        },
        {
            'AttributeName': 'proj',
            'KeyType': 'RANGE'  # RANGE indicates the sort key
        }
    ]
)

print("Table status:", response['TableDescription']['TableStatus'])

>>>>>>> 9a288f5 (saving)
