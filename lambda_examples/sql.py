import boto3

def write_sql_file_to_s3(bucket_name, sql_string, filename):
    s3 = boto3.resource('s3')
    # Upload SQL string to S3 file
    s3.Object(bucket_name, filename).put(Body=sql_string)

    # Return URL of the S3 file
    return f's3://{bucket_name}/{filename}'

