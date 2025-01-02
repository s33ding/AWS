import sys
from shared_func.artifact_func import *

domain_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Domain: "
)

repo_func = lambda: sys.argv[2] if len(sys.argv) > 2 else input(
    "Repo name: "
)

external_connection_func = lambda: sys.argv[3] if len(sys.argv) > 3 else input(
    "External Connection: "
)

# Get the user inputs using the lambda functions
domain = domain_func()
repo = repo_func()
external_connection = external_connection_func()

# Associate the external connection
associate_external_connection(domain, repo, external_connection)

