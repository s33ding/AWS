import boto3
import pandas as pd
import json
import os

# Load the AWS credentials from a JSON file
with open (os.environ['AWS_KEY'], "r") as f:
    credentials = json.load(f)

# Create a Boto3 session using the loaded credentials
session = boto3.Session(
    aws_access_key_id=credentials['id'],
    aws_secret_access_key=credentials['secret'],
    region_name='us-east-1'
)

# Initialize the Amazon Recognition client
rekog = session.client('rekognition')

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

