import boto3
import pandas as pd
from io import BytesIO

def save_df_to_s3_parquet(df, bucket_name, key_name):
    """
    Save a pandas DataFrame as a Parquet file in an S3 bucket.

    Parameters:
    - df (pandas.DataFrame): the DataFrame to save
    - bucket_name (str): the name of the S3 bucket to save the file to
    - key_name (str): the S3 key (object name) to use when saving the file

    Returns:
    None
    """
    # Convert the DataFrame to Parquet format
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)

    # Upload the Parquet file to S3
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, key_name).put(Body=buffer.getvalue())
