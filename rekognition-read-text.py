import boto3
import json
import os

with open (os.environ['AWS_KEY2'], "r") as f:
    cred = json.load(f)

# Initialize the Amazon Recognition client
rekog = boto3.client('rekognition',
                 region_name='us-east-1',
                 aws_access_key_id=cred.get("id"),
                 aws_secret_access_key=cred.get("secret"))

# Initialize the Rekognition client

# Specify the S3 bucket and image file you want to analyze
bucket_name = 's33ding-rekognition'
image_file = 'rekognition-machine-tag.jpg'

# Define the parameters for text detection
params = {
    'Image': {
        'S3Object': {
            'Bucket': bucket_name,
            'Name': image_file
        }
    }
}

# Call the detect_text method to detect text in the image
response = rekog.detect_text(**params)

# Print the detected text
for text in response['TextDetections']:
    print(text['DetectedText'])
