import sys
import boto3
from shared_func.iam_func import enable_login_profile


# Define lambda function to set default user name if not provided as an argument
user_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter IAM User Name: "
)

# Get the user name using the lambda function
user_name = user_name_func()

# Call create_iam_user with the obtained user name
password, login_url = enable_login_profile(user_name)
print(f"Password: '{password}'")
print(f"login_url: '{login_url}'")
