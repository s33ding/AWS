import boto3
import subprocess
from shared_func.cloudformation_func import *
import sys

stacks = list_cloudformation_stacks()

for stack in stacks:
    print(stack)
