import boto3

def list_objects(bucket_name, folder_name_s3, search_strings):
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
    bucket = s3.Bucket(bucket_name)
    objects = bucket.objects.filter(Prefix=folder_name_s3)
    matches = []
    for obj in objects:
        if any(search_string in obj.key for search_string in search_strings):
            matches.append(obj.key)
    lst_files = [x.split("/")[-1] for x in matches]
    return lst_files

# Function to check if an object exists in an S3 bucket
def check_object_exists(bucket, key):
    try:
        s3 = boto3.client('s3')
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except:
        return False
