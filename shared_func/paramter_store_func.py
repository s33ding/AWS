import boto3

def get_ssm_parameter(parameter_name):
    """
    Gets the value of the specified SSM parameter using the provided credentials
    
    Args:
    - parameter_name (str): the name of the SSM parameter to retrieve
    - usr (str): the AWS access key ID
    - passwd (str): the AWS secret access key
    - token (str): the temporary session token
    
    Returns:
    - value (str): the value of the specified SSM parameter
    """
    # Create SSM client object with temporary credentials
    ssm_client = boto3.client()

    # Use SSM client object to get parameter value
    response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
    value = response['Parameter']['Value']
    
    return value
