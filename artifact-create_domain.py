import sys
from shared_func.artifact_func import *

# Define lambda function to set default user name if not provided as an argument
domain_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter the domain name: "
)

# Get the user name using the lambda function
domain_name = domain_name_func()
create_codeartifact_domain(domain_name)
