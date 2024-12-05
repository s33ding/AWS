import sys
import boto3
import json
import os
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.iam_func import *


df = get_report()
