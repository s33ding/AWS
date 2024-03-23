import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.dynamo_func import * 
import json
import os
from decimal import Decimal

# Initialize the Amazon DynamoDB client
session = create_boto3_session()

sample_data = {
    'PersonName': 'John Doe',
    'RealAge': Decimal('33'),  # Convert to Decimal
    'Gender': 'Male',
    'Smile': Decimal('0'),  # Convert to Decimal
    'EyesOpen': Decimal('1'),  # Convert to Decimal
    'Beard': Decimal('1'),  # Convert to Decimal
    'Mustache': Decimal('0'),  # Convert to Decimal
    'Sunglasses': Decimal('0'),  # Convert to Decimal
    'CALM': Decimal('65.53168487548828'),  # Convert to Decimal
    'SURPRISED': Decimal('15.469156265258789'),  # Convert to Decimal
    'ANGRY': Decimal('10.675048828125'),  # Convert to Decimal
    'CONFUSED': Decimal('2.57720947265625'),  # Convert to Decimal
    'SAD': Decimal('1.1749267578125'),  # Convert to Decimal
    'DISGUSTED': Decimal('0.2277374267578125'),  # Convert to Decimal
    'FEAR': Decimal('0.040531158447265625'),  # Convert to Decimal
    'HAPPY': Decimal('0.012008348479866982')  # Convert to Decimal
}

# Insert the sample data into the DynamoDB table
insert_into_dynamodb(session = session, table_name="FaceAnalysisTable", dct=sample_data)
