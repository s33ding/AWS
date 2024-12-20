import sys
import boto3
import json
import os
from shared_func.iam_func import *

df = get_report()
print("df:")
print(df)
