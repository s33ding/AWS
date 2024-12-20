import sys
import boto3
import pandas as pd
import json
import os


# Create Rekognition client object with temporary credentials
rekog = boto3.client('rekognition')

def rekog_detect_labels(image_file_path=''):
    if len(sys.argv) > 1:
        image_file_path = sys.argv[1]

    if image_file_path == '':
        image_file_path = input('image_file_path: ')

    # Read the image file into memory
    with open(image_file_path, 'rb') as image:
        image_binary = image.read()

    # Call the Amazon Rekognition detect_labels function
    response = rekog.detect_labels(Image={'Bytes': image_binary})

    return response

# Call the rekog_detect_labels function and print the response
res = rekog_detect_labels()
print(res)

