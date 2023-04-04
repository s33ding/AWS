def upload_pickle_to_s3(pickle_data, bucket, key):
    """
    Upload a pickle object to an S3 bucket.

    pickle_data: object
        The pickle object to upload.
    bucket_name: str
        The name of the S3 bucket to upload the pickle to.
    key: str
        The key to use when saving the pickle file in the S3 bucket.
    """
    # Create an S3 client
    s3 = boto3.client('s3')

    # Pickle the data
    pickled_data = pickle.dumps(pickle_data)

    # Upload the pickled data to S3
    s3.put_object(Bucket=bucket, Key=key, Body=pickled_data)
