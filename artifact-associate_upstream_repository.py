import sys
from shared_func.artifact_func import *

domain_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Domain: "
)

repo_func = lambda: sys.argv[2] if len(sys.argv) > 2 else input(
    "Repo name: "
)

upstream_repo_func = lambda: sys.argv[3] if len(sys.argv) > 3 else input(
    "upstream_repo: "
)

# Get the user inputs using the lambda functions
domain = domain_func()
repo = repo_func()
upstream_repo =  upstream_repo_func()

# Associate the external connection
associate_upstream_repository(domain, repo, upstream_repo)

