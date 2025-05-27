import boto3
import time
import pandas as pd
import io

athena_client = boto3.client('athena', region_name='us-east-1')  # Adjust the region as necessary

# Function to wait for query completion
def wait_for_query_to_finish(query_execution_id):
    while True:
        result = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = result['QueryExecution']['Status']['State']
        
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            return status
        time.sleep(5)

def list_tables_in_database(database_name, s3_output_location=None):
    # Define the query to list the tables
    sql_query = f"SHOW TABLES IN {database_name}"

    # Set up query execution parameters
    query_params = {
        'QueryString': sql_query,
        'QueryExecutionContext': {'Database': database_name}
    }

    # If S3 output location is provided, include it in the query parameters
    if s3_output_location:
        query_params['ResultConfiguration'] = {'OutputLocation': s3_output_location}
    else:
        # Set a default S3 output location if none is provided
        default_output_location = 's3://your-default-bucket/output/'
        query_params['ResultConfiguration'] = {'OutputLocation': default_output_location}

    # Start the query execution
    response = athena_client.start_query_execution(**query_params)

    # Get the QueryExecutionId
    query_execution_id = response['QueryExecutionId'] 
    print(f"Query Execution ID: {query_execution_id}")

    # Wait for the query to finish and check its status
    status = wait_for_query_to_finish(query_execution_id)

    # If the query was successful, fetch the results
    if status == 'SUCCEEDED':
        result = athena_client.get_query_results(QueryExecutionId=query_execution_id)
        
        # Extract table names from the result
        table_names = [row['Data'][0]['VarCharValue'] for row in result['ResultSet']['Rows']]
        
        return table_names
    else:
        print(f"Query failed with status: {status}")
        return []


def create_view_for_table(table, database_name, s3_output_location, view_name, select_clause='*', where_clause=None):
    """
    Create or replace a view for a specified table.
    
    Args:
        table (str): The name of the table to create a view for.
        database_name (str): The Athena database where the query will run.
        s3_output_location (str): The S3 location to store query results.
        view_name (str): The name of the view to be created or replaced.
        select_clause (str, optional): The SELECT clause (columns) to be used in the query. Defaults to '*'.
        where_clause (str, optional): The condition(s) to apply in the WHERE clause. Defaults to None.
    
    Returns:
        str: The query execution status.
    """
    # Construct the SQL query with dynamic SELECT clause
    sql_query = f"""
    CREATE OR REPLACE VIEW {view_name} AS
    SELECT {select_clause}
    FROM "{database_name}".{table}
    """

    # Append the WHERE clause if provided
    if where_clause:
        sql_query += f" WHERE {where_clause};"
    else:
        sql_query += ";"

    print(sql_query)

    # Start the query execution
    response = athena_client.start_query_execution(
        QueryString=sql_query,
        QueryExecutionContext={
            'Database': database_name,
            'Catalog': 'AwsDataCatalog'  # Add this line
        },
        ResultConfiguration={'OutputLocation': s3_output_location}
    )

    query_execution_id = response['QueryExecutionId']

    # Wait for the query to finish and check its status
    status = wait_for_query_to_finish(query_execution_id)
    return status


def query_athena_to_df(query, database, output_location, region_name='us-east-1'):
    """
    Executes a query on AWS Athena and returns the results as a pandas DataFrame.

    Parameters:
        query (str): SQL query to execute.
        database (str): Athena database to query.
        output_location (str): S3 location where query results are stored, e.g. 's3://your-bucket/folder/'.
        region_name (str): AWS region where Athena is hosted.

    Returns:
        pd.DataFrame: Query results as a DataFrame.
    """
    client = boto3.client('athena', region_name=region_name)

    # Start query execution
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': output_location}
    )
    query_execution_id = response['QueryExecutionId']

    # Wait for the query to finish
    while True:
        status = client.get_query_execution(QueryExecutionId=query_execution_id)
        state = status['QueryExecution']['Status']['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(1)

    if state != 'SUCCEEDED':
        raise Exception(f"Query failed or was cancelled: {state}")

    # Get result file from S3
    result_file = f"{output_location}{query_execution_id}.csv"
    s3 = boto3.client('s3')
    parsed = boto3.session.Session().resource('s3')
    bucket_name = result_file.split('/')[2]
    key = '/'.join(result_file.split('/')[3:])
    obj = parsed.Object(bucket_name, key)
    data = obj.get()['Body'].read().decode('utf-8')

    # Load CSV into pandas DataFrame
    return pd.read_csv(io.StringIO(data))

