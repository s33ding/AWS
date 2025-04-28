import sys
import os
from shared_func.athena_func import list_tables_in_database


# Define lambda function to set default user name if not provided as an argument
input_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter the DB name: "
)


# Define lambda function to set default user name if not provided as an argument
input_func2 = lambda: sys.argv[2] if len(sys.argv) > 2 else os.environ["ATHENA_S3_OUTPUT"]

# Get the user name using the lambda function
database_name = input_func()
output_s3 = input_func2()
lst_tbl = list_tables_in_database(database_name,output_s3)
print("-------------------------------------")
for tbl in lst_tbl:
    print(tbl)
print("-------------------------------------")
