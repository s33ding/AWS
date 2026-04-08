import sys
import subprocess
from shared_func.artifact_func import *

# Lambda functions to get inputs for domain, repo, and tool
domain_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input("Domain: ")
repo_func = lambda: sys.argv[2] if len(sys.argv) > 2 else input("Repo name: ")
tool_func = lambda: sys.argv[3] if len(sys.argv) > 3 else input("Tool (npm/pip/maven): ").lower()

# Get the user inputs using the lambda functions
domain = domain_func()
repo = repo_func()
tool = tool_func()

# Call the function to configure the tool
configure_codeartifact_tool(domain, repo, tool)

