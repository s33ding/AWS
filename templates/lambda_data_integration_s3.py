import os
import boto3
import pandas as pd

def lambda_handler(event, context):
    bucket = event['bucket']
    folder = event['folder']
    output_folder = event['output_folder']
    output_format = event.get('output_format', 'parquet')  # default is parquet

    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')

    df = pd.DataFrame()
    for object_summary in s3.Bucket(bucket).objects.filter(Prefix=f"{folder}/"):
        file_path = object_summary.key
        file_name = os.path.split(file_path)[1]
        file_extension = os.path.splitext(file_name)[1]
        local_path = "/tmp/" + file_name

        # Download the file to /tmp
        s3_client.download_file(bucket, file_path, local_path)

        if file_extension == ".parquet":
            temp_df = pd.read_parquet(local_path)
        elif file_extension == ".csv":
            temp_df = pd.read_csv(local_path)
        elif file_extension == ".xlsx":
            temp_df = pd.read_excel(local_path, engine='openpyxl')
        elif file_extension in [".pkl", ".pickle"]:
            temp_df = pd.read_pickle(local_path)
        else:
            continue

        df = pd.concat([df, temp_df])

    # Save the combined data to a new file in /tmp
    combined_file_path = "/tmp/combined_file." + output_format

    if output_format == 'parquet':
        df.to_parquet(combined_file_path)
    elif output_format == 'csv':
        df.to_csv(combined_file_path, index=False)
    elif output_format == 'xlsx':
        df.to_excel(combined_file_path, index=False)

    # Upload the combined file to S3
    s3_client.upload_file(combined_file_path, bucket, f'{output_folder}/combined_file.{output_format}')

    return {
        'statusCode': 200,
        'body': f"Files combined successfully in: {output_folder}/combined_file.{output_format}"
    }

