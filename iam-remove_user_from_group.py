import sys
from shared_func.iam_func import *

def main():

    # Define lambda function to set default user name if not provided as an argument
    user_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
        "Enter IAM User Name: "
    )

    # Define lambda function to set default user name if not provided as an argument
    group_name_func = lambda: sys.argv[2] if len(sys.argv) > 1 else input(
        "Enter IAM Group Name: "
    )

    # Get the user name using the lambda function
    user_name = user_name_func()
    group_name = group_name_func()

    # Call delete_user with the obtained user name
    remove_user_from_group(user_name, group_name)


if __name__ == "__main__":
    main()
