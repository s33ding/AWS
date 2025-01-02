import sys
from shared_func.artifact_func import *

domain_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Domain: "
)

repo_func = lambda: sys.argv[2] if len(sys.argv) > 1 else input(
    "Repo name: "
)

domain = domain_func()
repo = repo_func()

list_packages(domain, repo)
