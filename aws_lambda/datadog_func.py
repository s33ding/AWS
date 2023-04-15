import os
import json
from datadog import api
import datadog

def load_datadog_credentials():
    # Get the name of the DataDog credentials file from an environment variable
    credentials_file = os.environ.get('DATADOG_CRED')
    if not credentials_file:
        raise ValueError('DATADOG_CREDENTIALS_FILE environment variable not set')

    # Load the credentials from the JSON file
    with open(credentials_file, 'r') as f:
        credentials = json.load(f)

    # Return the credentials
    return credentials

def create_log_group(log_group_name):
    # Set up DataDog client
    credentials = load_datadog_credentials()
    print(credentials)
    datadog.api_key = credentials.get('api_key')
    datadog.app_key = credentials.get('app_key')
    datadog.initialize(api_key=credentials.get('api_key'), app_key=credentials.get('app_key'))
    # Create the log group
    result = datadog.api.Logs.create(
        logset_id='main',
        name=log_group_name,
        attributes={}
    )

    # Return the response
    return result
