import boto3

def s3_get_data(bucket_name, object_key):
    s3_client = boto3.client('s3')
    s3_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    return  s3_response["Body"].read().decode('utf')
    
def s3_upload_file(bucket_name, folder_name, file_name, string):
    object_key =  f'{folder_name}/{file_name}'
    s3 = boto3.resource("s3")
    res = s3.Bucket(bucket_name).put_object(Key=object_key, Body=string)
    return res

def list_objects(bucket, folder_name_s3, search_strings):
    """
    List the objects inside an S3 folder that contain the specified search strings in their filename.

    Args:
    - bucket_name: str, the name of the S3 bucket
    - folder_name: str, the name of the S3 folder
    - search_strings: list of str, the list of search strings to look for in the filenames

    Returns:
    - A list of objects that match the search strings in their filename
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    objects = bucket.objects.filter(Prefix=folder_name_s3)
    matches = []
    for obj in objects:
        if any(search_string in obj.key for search_string in search_strings):
            matches.append(obj.key)
            
    lst_files = [x.split("/")[-1] for x in matches]
    return lst_files

# Function to invoke another Lambda function
def invoke_lamb(my_payload, lambda_name, invocation_type):
    client = boto3.client("lambda")
    response = client.invoke(
      FunctionName = lambda_name,
      InvocationType = invocation_type, # best options: RequestResponse or Event
      Payload = json.dumps(my_payload))
    return response

def extract_response_value_from_lambda(lambda_response):
    response_body = json.loads(lambda_response['Payload'].read().decode())
    data_cleaned = json.loads(response_body['body'])
    return data_cleaned

def read_pickle_file_from_s3(bucket, key):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    body = obj.get()['Body'].read()
    return pickle.loads(body)

def get_json_from_s3(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        return data
    except Exception as e:
        raise Exception("Error while retrieving JSON from S3: " + e.__str__())
