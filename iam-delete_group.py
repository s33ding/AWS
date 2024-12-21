import sys
from shared_func.iam_func import *



# Define lambda function to set default user name if not provided as an argument
group_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter IAM Group Name: "
)
gp_nm = group_name_func()


delete_iam_group(gp_nm)

