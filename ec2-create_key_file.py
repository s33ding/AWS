import boto3
import os
import subprocess
import sys
from shared_func.ec2_func import *


# Define lambda functions to set default values if no arguments are provided
key_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter the name for your new key pair: "
)
save_path_func = lambda: sys.argv[2] if len(sys.argv) > 2 else input(
    "Enter the directory to save the key file (default: current directory): "
)

# Get values for key_name and save_path using lambda functions
key_name = key_name_func()
save_path = save_path_func()
if not save_path:
    save_path = os.getcwd()  

create_key_pair(key_name, save_path)
