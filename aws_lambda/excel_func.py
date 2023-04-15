import boto3
import io
import pandas as pd

def read_excel_from_s3(bucket_name, key_name):
    # Create an S3 client
    s3 = boto3.client('s3')

    # Use the S3 client to get the file contents
    object = s3.get_object(Bucket=bucket_name, Key=key_name)

    # Read the contents of the file into a Pandas dataframe
    body = object['Body']
    excel_file = io.BytesIO(body.read())
    df = pd.read_excel(excel_file)

    return df
  
def upload_excel_to_s3(bucket_name, key_name, df):
    # Create an S3 client
    s3 = boto3.client('s3')

    # Save the Pandas dataframe to an in-memory buffer
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)

    # Upload the buffer to S3
    buffer.seek(0)
    s3.upload_fileobj(buffer, bucket_name, key_name)

    return True
