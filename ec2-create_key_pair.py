import boto3
import subprocess
from shared_func.ec2_func import *
import sys

# Define lambda functions to set default values if no arguments are provided
key_name_func = lambda: sys.argv[1] if len(sys.argv) > 1 else input("Enter the name for your new key pair: ")
save_to_file_func = lambda: sys.argv[2] if len(sys.argv) > 2 else input("Enter the file name to save the private key (leave empty to skip saving): ").strip()

key_name = key_name_func()
file_name = save_to_file_func()

# Create the key pair
create_key_pair(key_name, file_name)
