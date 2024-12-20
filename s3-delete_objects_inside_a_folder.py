import sys
import boto3
import pandas as pd
import json
import os
from shared_func.s3_func import *
from shared_func.argv_parser import get_input


bucket_name = input("BUCKET: ")
folder_name = input("FOLDER NAME(PREFIX): ")

delete_all_s3_files_in_folder(bucket_name, folder_name)
