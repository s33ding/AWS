import boto3
import json

def read_aws_credentials(json_file_path):
    """
    Reads the AWS credentials from a JSON file.

    Parameters:
    - json_file_path (str): The path to the JSON file containing the AWS credentials.

    Returns:
    - Tuple containing the AWS access key ID, secret access key, and session token.
    """
    with open(json_file_path) as f:
        credentials = json.load(f)
        aws_key = credentials.get("id")
        aws_secret = credentials.get("secret")
        aws_token = credentials.get("token")
    return aws_key, aws_secret, aws_token

def create_boto3_session(json_file_path):
    """
    Creates a new Boto3 session using AWS credentials stored in a JSON file.

    Parameters:
    - json_file_path (str): The path to the JSON file containing the AWS credentials.

    Returns:
    - Boto3 session object.
    """
    aws_key, aws_secret, aws_token = read_aws_credentials(json_file_path)
    return boto3.Session(
        region_name='us-east-1',
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        aws_session_token=aws_token
    )

def simulate_lambda_locally(filename):
    if "AWS_KEY" in os.environ:
        # Get the path to the JSON file containing AWS credentials from an environment variable
        json_file_path = os.environ["AWS_KEY"]
        # Read the AWS credentials from the JSON file
        session = boto3.Session(profile_name='default')
        
        # Read the contents of the JSON file
        with open(filename, "r") as f:
            event = json.load(f)
            
        # Do something with the event object
        print(event)
    else:
        print("AWS_KEY environment variable not set")
    
    return event, session
