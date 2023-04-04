# Function to retrieve table schema information from an AWS Glue catalog
def glue_retrieves_table_details(database_name, table_name):
    try:
        glue_client = boto3.client('glue')
        response = glue_client.get_table(DatabaseName=database_name, Name=table_name)
        response = response["Table"]["StorageDescriptor"]["Columns"]
        return response
    except ClientError as e:
        raise Exception("boto3 client error in retrieves_table_details: " + e.__str__())
    except Exception as e:
        raise Exception("Unexpected error in retrieves_table_details: " + e.__str__())
# Lambda handler function
def lambda_handler(event, context):
    
    # Set the AWS Glue catalog database name
    database_glue_catalog = ""
    
    # Generate the AWS Glue catalog table name
    glue_tbl = f""
        
    # retrieve the table schema information
    schema = glue_retrieves_table_details(database_name=database_glue_catalog, table_name=glue_tbl)
