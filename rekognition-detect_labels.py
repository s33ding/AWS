import sys
import boto3
import pandas as pd
import json
import os

with open (os.environ['AWS_KEY2'], "r") as f:
    cred = json.load(f)

rekog = boto3.client('rekognition', 
                 region_name='us-east-1',
                 aws_access_key_id=cred.get("id"), 
                 aws_secret_access_key=cred.get("secret"))

def rekog_detect_labels(image_file_path=""):
    if len(sys.argv) > 1:
        image_file_path = sys.argv[1]

    if image_file_path == "":
        image_file_path = input("image_file_path:") 

    # Read the image file into memory
    with open(image_file_path, "rb") as image:
        image_binary = image.read()

    # Call the Amazon Rekognition detect_labels function
    response = rekog.detect_labels(Image={'Bytes': image_binary})

    return response

res = rekog_detect_labels()
print(res)
