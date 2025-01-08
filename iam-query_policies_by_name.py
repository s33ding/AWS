import sys
import boto3
import json
import os
from shared_func.iam_func import *

pd.set_option('display.max_colwidth', None)

# Define lambda functions to set default values if no arguments are provided
policy_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "search term: "
)

search_term = policy_name_func()

# Call the function
df = query_policies_by_name(search_term)

# Display the filtered DataFrame
if not df.empty:
    print("\nMatched Policies:")
    print(df)
else:
    print("\nNo policies matched the search term.")
