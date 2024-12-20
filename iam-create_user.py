import sys
from shared_func.iam_func import create_iam_user


# Define lambda function to set default user name if not provided as an argument
user_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter IAM User Name: "
)

# Get the user name using the lambda function
user_name = user_name_func()
create_iam_user(user_name)
