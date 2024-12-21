import sys
from shared_func.iam_func import *

if __name__ == "__main__":
    user_name = input("user:")
    group_name = input("group:")
    attach_user_to_group(user_name, group_name)
