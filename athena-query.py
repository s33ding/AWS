import sys
import os
from shared_func.athena_func import query_athena_to_df

database = "bronze"
query = """SELECT * FROM bronze.mcdonalds_sales LIMIT 10;"""
output_location = "s3://s33ding-kafka-output/athena-results/"
region_name = "us-east-1"

df = query_athena_to_df(query, database, output_location, region_name)

