# Create the new sd-vehicle-data bucket
s3.create_bucket(Bucket='sd-vehicle-data')

# List the buckets in S3
for bucket_info in s3.list_buckets()['Buckets']:
    
    # Get the bucket_name
    bucket_name = bucket_info['Name']
    
    # Generate bucket ARN.
    arn = "arn:aws:s3:::{}".format(bucket_name)
    
    # Print the ARN
    print(arn)