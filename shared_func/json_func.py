import boto3 
import json 

def get_json_from_s3(bucket_name, key_name):
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=key_name)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        return data
    except Exception as e:
        raise Exception("Error while retrieving JSON from S3: " + e.__str__())

def upload_json_to_s3(json_data, bucket_name, key_name):
    # Create an S3 client
    s3 = boto3.client('s3')

    # Convert the JSON data to a string
    json_string = json.dumps(json_data)

    # Upload the JSON file to S3
    s3.put_object(Bucket=bucket_name, Key=key_name, Body=json_string.encode('utf-8'))

    # Print a success message
    print(f"JSON file {key_name} uploaded to S3 bucket {bucket_name}")
