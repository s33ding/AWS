import sys
from shared_func.iam_func import create_iam_group


# Define lambda function to set default group name if not provided as an argument
group_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter IAM Group Name: "
)

# Get the group name using the lambda function
group_name = group_name_func()
create_iam_group(group_name)
