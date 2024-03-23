import boto3
import json
import os

def analyze_image(bucket_name, image_file):
    # Initialize the Amazon Recognition client
    rekog = session.client('rekognition')

    try:
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

    except Exception as e:
        print('An error occurred:', str(e))


