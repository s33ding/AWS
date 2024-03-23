import boto3

# Function to check if an object exists in an S3 bucket
def check_object_exists(bucket_name, key_name):
    try:
        s3 = boto3.client('s3')
        s3.head_object(Bucket=bucket_name, Key=key_name)
        ret:q1:—urn True
    except:
        return False

def copy_s3_object_to_folder(bucket_name_src, key_name_src, bucket_name_dest, key_name_dest):
    # Create S3 resource object
    s3 = boto3.resource('s3')

    # Specify copy source and destination
    copy_source = {
        'Bucket': bucket_name_src, 
        'Key': key_name_src
    }

    # Copy object to destination folder in destination bucket
    destination_bucket = s3.Bucket(bucket_name_dest)
    destination_bucket.copy(copy_source, key_name_dest)
    
def delete_all_s3_files_in_folder(bucket_name, folder_name):
    """
    Deletes all files in the specified S3 folder using the provided session object
    
    Args:
    - bucket_name (str): the name of the S3 bucket containing the folder to delete files from
    - folder_name (str): the name of the folder to delete files from
    - session (boto3.Session): the session object for initializing the S3 client
    
    Returns:
    - None
    """
    # Initialize the S3 client using the session
    s3 = session.client('s3')
    
    # List all objects in the specified folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{folder_name}/")
    files = [obj['Key'] for obj in response.get("Contents")]
    
    # Delete each file in the specified folder
    for key_obj in files:
        print(f"DELETING: {key_obj}")
        response = s3.delete_object(Bucket=bucket_name,Key=key_obj)
    
    print("Deletion complete.")

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
def check_object_exists(bucket_name, key_name):
    try:
        s3 = boto3.client('s3')
        s3.head_object(Bucket=bucket_name, Key=key_name)
        return True
    except:
        return False

def put_string_in_s3_object(bucket_name, key_name, string):
    # Create an object key using the folder name and file name
    object_key = f'{folder_name}/{file_name}'

    # Create an S3 resource
    s3 = boto3.resource('s3')

    # Upload the string to the S3 bucket as an object
    res = s3.Bucket(bucket_name).put_object(Key=key_name, Body=string)

    # Return the result of the upload operation
    return res

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = session.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_all_s3_files_in_folder(bucket_name, folder_name):
    """
    Deletes all files in the specified S3 folder using the provided session object
    
    Args:
    - bucket_name (str): the name of the S3 bucket containing the folder to delete files from
    - folder_name (str): the name of the folder to delete files from
    - session (boto3.Session): the session object for initializing the S3 client
    
    Returns:
    - None
    """
    # Initialize the S3 client using the session
    s3 = session.client('s3')
    
    # List all objects in the specified folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{folder_name}/")
    files = [obj['Key'] for obj in response.get("Contents")]
    
    # Delete each file in the specified folder
    for key_obj in files:
        print(f"DELETING: {key_obj}")
        response = s3.delete_object(Bucket=bucket_name,Key=key_obj)
    
    print("Deletion complete.")


def download_file_from_s3(bucket_name, file_key, destination_path):
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, file_key, destination_path)
        print(f"File downloaded successfully to: {destination_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")
