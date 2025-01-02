import sys
from shared_func.artifact_func import *

domain_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Domain: "
)

# Define lambda function to set default user name if not provided as an argument
repo_func = lambda: sys.argv[2] if len(sys.argv) > 1 else input(
    "Repo name: "
)

# Get the user name using the lambda function
domain = domain_func()
repo = repo_func()

create_codeartifact_repository(domain, repo)
