import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.lambda_func import list_functions

def main():
    session = create_boto3_session()

    # Call list_users to list all IAM users
    list_functions()

if __name__ == "__main__":
    main()
  
