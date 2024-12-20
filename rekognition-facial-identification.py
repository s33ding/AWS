import boto3
import json
import os

client = boto3.client('rekognition')

# Specify the S3 bucket and image files for the two faces you want to compare
bucket_name = 's33ding-recognition'
face1_file = 'rekognition-am-i-roberto.jpg'
face2_file = 'rekognition-roberto-facial-id.jpg'

# Define the parameters for face comparison
params = {
    'SimilarityThreshold': 80,
    'SourceImage': {
        'S3Object': {
            'Bucket': 's33ding-rekognition',
            'Name': face1_file
        }
    },
    'TargetImage': {
        'S3Object': {
            'Bucket': 's33ding-rekognition',
            'Name': face2_file
        }
    }
}

# Call the compare_faces method to compare the two faces
response = client.compare_faces(**params)

# Check if the faces match and print the result
if len(response['FaceMatches']) > 0:
    print(f"The two faces match with a similarity score of {response['FaceMatches'][0]['Similarity']}%")
else:
    print("The two faces do not match")
