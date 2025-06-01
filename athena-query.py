import sys
import os
from shared_func.athena_func import query_athena_to_df

database = "tisaude_empresa"
query = """SELECT cliente FROM "tisaude_empresa"."clientes" """
output_location = "s3://athena-output-teste/"
region_name = "us-east-1"

df = query_athena_to_df(query, database, output_location, region_name)

