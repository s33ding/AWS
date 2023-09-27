import boto3
import json

def list_functions():
    # Initialize a Boto3 Lambda client
    lambda_client = boto3.client('lambda')

    # List Lambda functions
    try:
        response = lambda_client.list_functions()
        functions = response['Functions']
        
        if functions:
            print("Lambda Functions:")
            for function in functions:
                print(f"Function Name: {function['FunctionName']}")
                print(f"Function ARN: {function['FunctionArn']}")
                print("-" * 30)
        else:
            print("No Lambda functions found.")
    
    except Exception as e:

        print(f"An error occurred: {str(e)}")

def make_aws_authenticated_request(credential_file_path, host_name, payload, region_name='us-east-1'):

    import requests
    from aws_requests_auth.aws_auth import AWSRequestsAuth

    with open(credential_file_path, 'r') as f:
        cred = json.load(f)

    auth = AWSRequestsAuth(
        aws_access_key=cred['id'],
        aws_secret_access_key=cred['secret'],
        aws_token=cred['token'],
        aws_host=host_name,
        aws_region=region_name,
        aws_service='execute-api'
    )

    url = f'https://{host_name}'
    response = requests.post(url, auth=auth, json=payload)

    return json.loads(response.content)

def create_lambda_function_and_return_arn(
    zip_file_path,
    handler,
    role_arn,
    function_name="my-lambda",
    runtime="python3.9",
    memory_size=128,
    timeout=60  # Default timeout of 60 seconds
):

    # Initialize the AWS Lambda client
    lambda_client = boto3.client("lambda")

    # Create the Lambda function
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime=runtime,
        Role=role_arn,
        Handler=handler,
        Code={
            "ZipFile": open(zip_file_path, "rb").read(),
        },
        MemorySize=memory_size,
        Timeout=timeout,  # Set the Timeout parameter
    )

    # Return the ARN of the created Lambda function
    return response["FunctionArn"]
