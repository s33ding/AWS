import awswrangler as wr
import pandas as pd

def read_data_from_file(file_path):
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == 'csv':
        return wr.s3.read_csv(file_path)
    elif file_extension == 'xlsx':
        return wr.s3.read_excel(file_path)
    elif file_extension == 'pkl':
        return wr.s3.read_pickle(file_path)
    elif file_extension == 'parquet':
        return wr.s3.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def write_data_to_file(df, s3_bucket, key_name):
    file_extension = key_name.split('.')[-1].lower()

    if file_extension == 'csv':
        wr.s3.to_csv(df, f's3://{s3_bucket}/{key_name}', index=False)
    elif file_extension == 'xlsx':
        wr.s3.to_excel(df, f's3://{s3_bucket}/{key_name}', index=False)
    elif file_extension == 'pkl':
        wr.s3.to_pickle(df, f's3://{s3_bucket}/{key_name}')
    elif file_extension == 'parquet':
        wr.s3.to_parquet(df, f's3://{s3_bucket}/{key_name}')
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
