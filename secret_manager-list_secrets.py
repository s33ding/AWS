from shared_func.argv_parser import get_input
from shared_func.secret_manager_func import list_secrets
import boto3
import json
import os

lst = list_secrets()
