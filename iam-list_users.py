import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.iam_func import list_users

def main():
    session = create_boto3_session()

    # Call list_users to list all IAM users
    list_users()

if __name__ == "__main__":
    main()
  
