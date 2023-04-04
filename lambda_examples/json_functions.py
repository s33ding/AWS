def get_json_from_s3(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        return data
    except Exception as e:
        raise Exception("Error while retrieving JSON from S3: " + e.__str__())

def s3_get_data(bucket_name, object_key):
    s3_client = boto3.client('s3')
    s3_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    return  s3_response["Body"].read().decode('utf')
    
def s3_create_folder(bucket_name, object_key):
    s3_client = boto3.client('s3')
    s3_response =  s3_client.put_object(Bucket=bucket_name,  Key=object_key)
    return s3_response
    
def s3_upload_file(bucket_name, folder_name, file_name, string):
    object_key =  f'{folder_name}/{file_name}'
    s3 = boto3.resource("s3")
    res = s3.Bucket(bucket_name).put_object(Key=object_key, Body=string)
    return res

# Lambda function handler
def lambda_handler(event, context):
    
    dct = json.loads(event['body'])
    
    # Upload dictionary to S3 bucket
    s3_upload_file(
    bucket_name=bucket_name, 
    folder_name = folder_name,
    file_name='file.json', 
    string=json.dumps(dct, indent=4))
