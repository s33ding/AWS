import sys
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.iam_func import delete_user

def main():
    session = create_boto3_session()

    # Define lambda function to set default user name if not provided as an argument
    user_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
        "Enter IAM User Name: "
    )

    # Get the user name using the lambda function
    user_name = user_name_func()

    # Call delete_user with the obtained user name
    delete_user(user_name)

if __name__ == "__main__":
    main()
