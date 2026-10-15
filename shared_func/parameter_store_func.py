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
    ssm_client = boto3.client('ssm')


    # Additional parameters for get_parameter if version is specified
    params = {'Name': parameter_name, 'WithDecryption': True}

    # Use SSM client object to get parameter value
    response = ssm_client.get_parameter(**params)
    value = response['Parameter']['Value']
    return value


def get_ssm_parameter_history(parameter_name):
    # Create SSM client object with temporary credentials
    ssm_client = boto3.client('ssm')

    # Additional parameters for get_parameter if version is specified
    params = {'Name': parameter_name, 'WithDecryption': True}

    # Use SSM client object to get parameter value
    response = ssm_client.get_parameter(**params)
    return response['Parameter']

def create_ssm_parameter(parameter_name, parameter_value, parameter_type='SecureString', description='', overwrite=True):
    """
    Writes a new parameter to AWS Systems Manager Parameter Store

    Args:
    - parameter_name (str): the name of the parameter to create/update
    - parameter_value (str): the value of the parameter
    - parameter_type (str): the data type for the parameter value (default: 'String')
    - description (str): a description for the parameter (default: '')
    - overwrite (bool): whether to overwrite the parameter if it already exists (default: True)

    Returns:
    - response (dict): information about the newly created/updated parameter
    """
    # Create SSM client object with provided credentials
    ssm_client = boto3.client(
            'ssm'
            )

    # Additional parameters for put_parameter
    params = {
        'Name': parameter_name,
        'Value': parameter_value,
        'Type': parameter_type,
        'Description': description,
        'Overwrite': overwrite
    }

    # Use SSM client object to put parameter
    response = ssm_client.put_parameter(**params)
    return response

import boto3

def delete_ssm_parameter(parameter_name):
    """
    Deletes the specified parameter from AWS Systems Manager Parameter Store

    Args:
    - parameter_name (str): the name of the parameter to delete
    Returns:
    - response (dict): information about the deletion operation
    """
    # Create SSM client object with provided credentials
    ssm_client = boto3.client('ssm')

    # Additional parameters for delete_parameter
    params = {'Name': parameter_name}

    # Use SSM client object to delete parameter
    response = ssm_client.delete_parameter(**params)
    return response


def list_ssm_parameters(path='/'):
    """
    Lists custom parameters from AWS Systems Manager Parameter Store

    Args:
    - path (str): the parameter path to filter by (default: '/')

    Returns:
    - parameters (list): list of parameter names under the specified path
    """
    ssm_client = boto3.client('ssm')

    params = {'Path': path, 'Recursive': True, 'WithDecryption': False}
    parameters = []

    while True:
        response = ssm_client.get_parameters_by_path(**params)
        parameters.extend(response['Parameters'])
        if 'NextToken' in response:
            params['NextToken'] = response['NextToken']
        else:
            break

    return parameters
