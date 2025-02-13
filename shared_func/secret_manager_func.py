import boto3
import json
from botocore.exceptions import ClientError

def get_secret(secret_name):
    """
    Retrieves the value of the specified AWS Secrets Manager secret using the provided boto3 object
    
    Args:
    - secret_name (str): the name of the AWS Secrets Manager secret to retrieve
    
    Returns:
    - dct (dict): a dictionary containing the values in the specified secret
    """
    # Initialize the Secrets Manager client using the boto3
    client = boto3.client('secretsmanager')
    
    # Use Secrets Manager client object to get secret value
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    
    # Extract the values from the secret
    dct = json.loads(get_secret_value_response['SecretString'])
    
    return dct

def list_secrets(region_name='us-east-1', verbose=True):
    """
    List secrets in AWS Secrets Manager.

    Args:
    region_name (str): AWS region where the secrets manager is located. Default is 'us-east-1'.

    Returns:
    list: List of secret names.
    """
    # Initialize the Secrets Manager client
    client = boto3.client('secretsmanager', region_name=region_name)

    # Call the list_secrets API
    response = client.list_secrets()

    # Extract secret names from the response
    secret_names = [secret['Name'] for secret in response['SecretList']]
    if verbose:
        for v in secret_names:
            print(v)

    return secret_names


def create_secret(secret_name, json_path):
    """
    Create or overwrite a secret in AWS Secrets Manager using a JSON file.

    Args:
    secret_name (str): Name of the secret.
    json_path (str): Path to the JSON file containing the secret values.

    Returns:
    dict: Response from the Secrets Manager API.
    """
    # Read and load JSON data from file
    try:
        with open(json_path, "r") as json_file:
            secret_value_json = json.load(json_file)
    except FileNotFoundError:
        print(f"❌ Error: File '{json_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON format in '{json_path}'.")
        return None

    # Convert JSON object to string
    secret_value_str = json.dumps(secret_value_json)

    # Initialize the Secrets Manager client
    client = boto3.client('secretsmanager')

    try:
        # Try to create the secret
        response = client.create_secret(
            Name=secret_name,
            SecretString=secret_value_str
        )
        print(f"✅ Secret '{secret_name}' created successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceExistsException':
            # Overwrite the existing secret
            try:
                response = client.update_secret(
                    SecretId=secret_name,
                    SecretString=secret_value_str
                )
                print(f"🔄 Secret '{secret_name}' updated successfully (overwrite enabled).")
            except ClientError as update_error:
                print(f"❌ Failed to overwrite secret '{secret_name}': {update_error}")
                return None
        else:
            print(f"❌ Error creating secret '{secret_name}': {e}")
            return None

    return response

def delete_secret(secret_name, region_name='us-east-1'):
    """
    Delete a secret from AWS Secrets Manager.

    Args:
    secret_name (str): Name of the secret to delete.
    region_name (str): AWS region where the secrets manager is located. Default is 'us-east-1'.

    Returns:
    dict: Response from the Secrets Manager API.
    """
    # Initialize the Secrets Manager client
    client = boto3.client('secretsmanager', region_name=region_name)

    # Call the delete_secret API
    response = client.delete_secret(
        SecretId=secret_name,
        ForceDeleteWithoutRecovery=True  # Set to True to delete the secret immediately without recovery
    )

    return response
