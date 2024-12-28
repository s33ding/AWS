import sys
import boto3
import json
import os
from shared_func.iam_func import *

# Define lambda functions to set default values if no arguments are provided
user_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter the User Name: "
)
username = user_name_func()

# Remove user from all groups
remove_user_from_all_groups(username)

# Attach user to a specific group
#attach_user_to_group(username, group_name)


