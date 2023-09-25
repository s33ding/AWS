import boto3

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
