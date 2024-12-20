import boto3
import json
import os
import sys
import boto3
import pandas as pd
import json
import os

rekog = boto3.client('rekognition')
def facial_analyzis(bucket_name, image_file):

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


