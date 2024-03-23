import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.dynamo_func import * 
import json
import os

# Initialize the Amazon DynamoDB client
session = create_boto3_session()


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
