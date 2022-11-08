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