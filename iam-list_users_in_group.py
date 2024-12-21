import sys
from shared_func.iam_func import *


# Define lambda function to set default user name if not provided as an argument
group_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter IAM Group Name: "
)

def main():
    group_name = group_name_func()

    # Call list_users to list all IAM users
    list_users_in_group(group_name)

if __name__ == "__main__":
    main()
