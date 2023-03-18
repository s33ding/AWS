import sys
import boto3
import pandas as pd
import json
import os

with open (os.environ['AWS_CRED'], "r") as f:
    cred = json.load(f)

# Initialize the Amazon Recognition client
rekog = boto3.client('rekognition', 
                 region_name='us-east-1',
                 aws_access_key_id=cred.get("id"), 
                 aws_secret_access_key=cred.get("secret"))

print('Specify the S3 bucket and image file you want to analyze')
bucket_name = input('BUCKET: ')
image_file = input('IMG: ')

# Call the DetectFaces API to analyze the image for facial features
response = rekog.detect_faces(
    Image={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': image_file,
        }
    },
    Attributes=['ALL']
)

# Print the results of the facial analysis
for face_detail in response['FaceDetails']:
    print('The detected face is between ' + str(face_detail['AgeRange']['Low']) + ' and ' + str(face_detail['AgeRange']['High']) + ' years old')
    print('The detected gender is ' + str(face_detail['Gender']['Value']))
    print('The detected emotion is ' + str(face_detail['Emotions'][0]['Type']))
