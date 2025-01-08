import subprocess
import json
import boto3
import string
import secrets
import qrcode
from io import BytesIO
import pandas as pd
from botocore.exceptions import ClientError

def create_iam_role(role_name=None, policy_file=None, description=None):

    # AWS CLI command to create the IAM role
    command = [
        "aws", "iam", "create-role",
        "--role-name", role_name,
        "--description", description,
        "--assume-role-policy-document", f"file://{policy_file}"
    ]

    # Execute the AWS CLI command and capture the output
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
        # Parse the JSON output to extract the ARN
        role_info = json.loads(output)
        role_arn = role_info["Role"]["Arn"]
        return role_arn
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def create_iam_policy(policy_name=None, policy_document_file=None):

    # AWS CLI command to create the IAM policy
    command = [
        "aws", "iam", "create-policy",
        "--policy-name", policy_name,
        "--policy-document", f"file://{policy_document_file}"
    ]

    # Execute the AWS CLI command and capture the output
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
        # Parse the JSON output to extract the ARN
        policy_info = json.loads(output)
        policy_arn = policy_info["Policy"]["Arn"]
        return policy_arn

    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def attach_policy_to_role(role_name, policy_arn):
    # AWS CLI command to attach a policy to an IAM role
    command = [
        "aws", "iam", "attach-role-policy",
        "--role-name", role_name,
        "--policy-arn", policy_arn
    ]

    # Execute the AWS CLI command
    try:
        subprocess.run(command, check=True)
        print(f"Policy ARN '{policy_arn}' attached to IAM Role '{role_name}' successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")

def attach_policy_to_user(user_name, policy_arn):
    # AWS CLI command to attach a policy to an IAM user
    command = [
        "aws", "iam", "attach-user-policy",
        "--user-name", user_name,
        "--policy-arn", policy_arn
    ]

    # Execute the AWS CLI command
    try:
        subprocess.run(command, check=True)
        print(f"Policy ARN '{policy_arn}' attached to IAM User '{user_name}' successfully.")
        return user_name
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def create_iam_group(group_name):
    """
    Create a group in AWS IAM.

    :param group_name: Name of the group to create.
    :return: Response from the create_group API call or an error message.
    """
    # Initialize the IAM client
    iam_client = boto3.client('iam')

    # Create the group
    response = iam_client.create_group(
        GroupName=group_name
    )
    print("Group created successfully.")
    return response

def create_iam_policy(policy_name=None, policy_document_file=None):

    # AWS CLI command to create the IAM policy
    command = [
        "aws", "iam", "create-policy",
        "--policy-name", policy_name,
        "--policy-document", f"file://{policy_document_file}"
    ]

    # Execute the AWS CLI command and capture the output
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
        # Parse the JSON output to extract the ARN
        policy_info = json.loads(output)
        policy_arn = policy_info["Policy"]["Arn"]
        return policy_arn

    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def attach_policy_to_role(role_name, policy_arn):
    # AWS CLI command to attach a policy to an IAM role
    command = [
        "aws", "iam", "attach-role-policy",
        "--role-name", role_name,
        "--policy-arn", policy_arn
    ]

    # Execute the AWS CLI command
    try:
        subprocess.run(command, check=True)
        print(f"Policy ARN '{policy_arn}' attached to IAM Role '{role_name}' successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")

def attach_policy_to_user(user_name, policy_arn):
    # AWS CLI command to attach a policy to an IAM user
    command = [
        "aws", "iam", "attach-user-policy",
        "--user-name", user_name,
        "--policy-arn", policy_arn
    ]

    # Execute the AWS CLI command
    try:
        subprocess.run(command, check=True)
        print(f"Policy ARN '{policy_arn}' attached to IAM User '{user_name}' successfully.")
        return user_name
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def create_iam_user(username):
    # Create an IAM client
    iam = boto3.client('iam')

    # Create the IAM user
    iam.create_user(UserName=username)
    print(f"IAM User '{username}' created.")


def get_report():
    # Create IAM client
    iam = boto3.client('iam')

    # Get list of all users
    response = iam.list_users()

    # Extract user details
    users = response['Users']

    # Collect user details in a list
    user_data = []
    for user in users:
        # Get user's access keys
        access_keys_response = iam.list_access_keys(UserName=user['UserName'])
        access_keys = access_keys_response['AccessKeyMetadata']

        # Include multiple access keys if they exist
        for access_key in access_keys:
            user_info = {
                'UserName': user['UserName'],
                'UserId': user['UserId'],
                'Arn': user['Arn'],
                'CreateDate': user['CreateDate'],
                'AccessKeyId': access_key['AccessKeyId'],
                'AccessKeyStatus': access_key['Status'],
                'AccessKeyCreateDate': access_key['CreateDate']
            }
            user_data.append(user_info)

    # Convert to DataFrame
    df = pd.DataFrame(user_data)
    return df

def generate_random_password(length=20):
    # Define the character set for the password
    password_chars = string.ascii_letters + string.digits + string.punctuation  # Add special characters

    # Ensure at least one special character in the password
    special_char = secrets.choice(string.punctuation)
    
    # Generate the remaining part of the password
    remaining_length = length - 1  # Subtract 1 for the special character
    password = special_char + ''.join(secrets.choice(password_chars) for i in range(remaining_length))

    return password

def enable_login_profile(username):
    # Create an IAM client
    iam = boto3.client('iam')

    # Generate a random password
    password = generate_random_password()

    # Check if the login profile already exists
    try:
        existing_profile = iam.get_login_profile(UserName=username)
        print(f"Login profile for '{username}' already exists.")
        
        # Get the AWS account ID
        account_id = boto3.client('sts').get_caller_identity()['Account']
        
        # Provide a link to the AWS Management Console login page
        login_url = f"https://{account_id}.signin.aws.amazon.com/console"
        
        iam.update_login_profile(UserName=username, Password=password, PasswordResetRequired=False)
        print(f"Login profile for '{username}' updated with a new random password.")
        return password, login_url
    except iam.exceptions.NoSuchEntityException:
        pass  # Continue to create a new login profile


    # Create or update the login profile with the random password
    try:
        iam.create_login_profile(UserName=username, Password=password, PasswordResetRequired=True)
        print(f"Login profile for '{username}' enabled with a random password.")
        
        # Get the AWS account ID
        account_id = boto3.client('sts').get_caller_identity()['Account']
        
        # Provide a link to the AWS Management Console login page
        login_url = f"https://{account_id}.signin.aws.amazon.com/console"
        
    except iam.exceptions.EntityAlreadyExistsException:
        iam.update_login_profile(UserName=username, Password=password, PasswordResetRequired=False)
        print(f"Login profile for '{username}' updated with a random password.")
        
        # Get the AWS account ID
        account_id = boto3.client('sts').get_caller_identity()['Account']
        
        # Provide a link to the AWS Management Console login page
        login_url = f"https://{account_id}.signin.aws.amazon.com/console"

    return password, login_url


def delete_user(username):
    # Create an IAM client
    iam = boto3.client('iam')

    # List attached policies for the IAM user
    try:
        attached_policies = iam.list_attached_user_policies(UserName=username)['AttachedPolicies']
        for policy in attached_policies:
            # Detach each policy from the user
            iam.detach_user_policy(UserName=username, PolicyArn=policy['PolicyArn'])
            print(f"Detached policy '{policy['PolicyName']}' from '{username}' successfully.")
    except iam.exceptions.NoSuchEntityException:
        print(f"IAM user '{username}' does not exist or has no attached policies.")

    # Delete the login profile
    try:
        iam.delete_login_profile(UserName=username)
        print(f"Login profile for '{username}' deleted successfully.")
    except iam.exceptions.NoSuchEntityException:
        print(f"Login profile for '{username}' does not exist.")

    # Delete the IAM user
    try:
        iam.delete_user(UserName=username)
        print(f"IAM user '{username}' deleted successfully.")
    except iam.exceptions.NoSuchEntityException:
        print(f"IAM user '{username}' does not exist.")

def list_users():
    # Create an IAM client
    iam = boto3.client('iam')

    # List all IAM users
    response = iam.list_users()

    # Extract and print user names
    if 'Users' in response:
        users = response['Users']
        if users:
            print("IAM Users:")
            for user in users:
                print(user['UserName'])
        else:
            print("No IAM users found.")
    else:
        print("No IAM users found.")

def get_account_id():
    sts = boto3.client('sts')
    response = sts.get_caller_identity()
    return response['Account']

def list_roles():
    # Initialize a Boto3 IAM client
    iam_client = boto3.client('iam')

    # List all IAM roles
    try:
        response = iam_client.list_roles()
        roles = response['Roles']
        
        if roles:
            print("IAM Roles:")
            for role in roles:
                print(f"Role Name: {role['RoleName']}")
                print(f"Role ARN: {role['Arn']}")
                print("-" * 30)

        else:
            print("No IAM roles found.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def enforce_mfa_access(username):
    try:
        # Initialize the IAM client
        iam = boto3.client('iam')

        # Get the AWS account ID
        account_id = iam.get_user()["User"]["Arn"].split(":")[4]

        # Create an IAM policy JSON document to enforce MFA
        mfa_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Deny",
                    "Action": "*",
                    "Resource": "*",
                    "Condition": {
                        "BoolIfExists": {
                            "aws:MultiFactorAuthPresent": "false"
                        }
                    }
                },
                {
                    "Effect": "Allow",
                    "Action": "*",
                    "Resource": "*"
                }
            ]
        }

        # Create the IAM policy or update it if it already exists
        policy_name = f'{username}_MFA_Policy'
        policy_document = json.dumps(mfa_policy)

        # Check if the policy exists
        policy_exists = False
        for policy in iam.list_policies(Scope='Local')['Policies']:
            if policy['PolicyName'] == policy_name:
                policy_exists = True
                break

        # Initialize version_id to None
        version_id = None

        if policy_exists:
            # Get the policy's version ID
            policy_versions = iam.list_policy_versions(PolicyArn=f'arn:aws:iam::{account_id}:policy/{policy_name}')
            for version in policy_versions['Versions']:
                if version['IsDefaultVersion'] is False:
                    version_id = version['VersionId']
                    break

            # Delete the existing policy
            iam.delete_policy_version(PolicyArn=f'arn:aws:iam::{account_id}:policy/{policy_name}', VersionId=version_id)

            # Create a new version of the policy
            iam.create_policy_version(PolicyArn=f'arn:aws:iam::{account_id}:policy/{policy_name}',
                                      PolicyDocument=policy_document, SetAsDefault=True)
            print(f"An updated version of IAM Policy '{policy_name}' has been created and attached to IAM user '{username}' to enforce MFA access.")
        else:
            # If the policy doesn't exist, create it
            iam.create_policy(PolicyName=policy_name, PolicyDocument=policy_document)
            print(f"IAM Policy '{policy_name}' has been created and attached to IAM user '{username}' to enforce MFA access.")

        # Attach the policy to the IAM user
        iam.attach_user_policy(UserName=username, PolicyArn=f'arn:aws:iam::{account_id}:policy/{policy_name}')

    except Exception as e:
        print(f"Error enforcing MFA access for IAM user '{username}': {str(e)}")


def list_iam_groups():
    """
    List all groups in AWS IAM.

    :return: List of IAM groups.
    """
    # Initialize the IAM client
    iam_client = boto3.client('iam')

    # List the groups
    response = iam_client.list_groups()
    groups = response.get('Groups', [])
    print("IAM Groups:")
    for group in groups:
        print(f"- {group['GroupName']}")
    return groups

def delete_iam_group(group_name):
    """
    Delete a specified IAM group.

    :param group_name: Name of the group to delete.
    :return: Response from the delete_group API call.
    """
    # Initialize the IAM client
    iam_client = boto3.client('iam')

    # Delete the group
    response = iam_client.delete_group(
        GroupName=group_name
    )
    print(f"Group '{group_name}' deleted successfully.")
    return response

def delete_iam_group(group_name):
    """
    Delete a specified IAM group.

    :param group_name: Name of the group to delete.
    :return: Response from the delete_group API call.
    """
    # Initialize the IAM client
    iam_client = boto3.client('iam')

    # Delete the group
    response = iam_client.delete_group(
        GroupName=group_name
    )
    print(f"Group '{group_name}' deleted successfully.")
    return response

def list_users_in_group(group_name):
    """
    List all users in a specified IAM group.

    :param group_name: Name of the group to list users from.
    :return: List of users in the group.
    """
    # Initialize the IAM client
    iam_client = boto3.client('iam')

    # List the users in the group
    response = iam_client.get_group(
        GroupName=group_name
    )
    users = response.get('Users', [])
    print(f"Users in group '{group_name}':")
    for user in users:
        print(f"- {user['UserName']}")
    return users

def attach_user_to_group(user_name, group_name):
    """
    Attach a user to an IAM group.

    :param user_name: The name of the IAM user
    :param group_name: The name of the IAM group
    :return: None
    """
    # Create an IAM client
    iam = boto3.client('iam')

    try:
        # Add the user to the group
        iam.add_user_to_group(GroupName=group_name, UserName=user_name)
        print(f"User '{user_name}' successfully added to group '{group_name}'.")
    except ClientError as error:
        print(f"Error adding user '{user_name}' to group '{group_name}': {error}")


def remove_user_from_group(user_name, group_name):
    """
    Remove a user from an IAM group.

    :param user_name: The name of the IAM user
    :param group_name: The name of the IAM group
    :return: None
    """
    # Create an IAM client
    iam = boto3.client('iam')

    try:
        # Remove the user from the group
        iam.remove_user_from_group(GroupName=group_name, UserName=user_name)
        print(f"User '{user_name}' successfully removed from group '{group_name}'.")
    except ClientError as error:
        print(f"Error removing user '{user_name}' from group '{group_name}': {error}")

def remove_user_from_all_groups(username):
    """
    Remove the given IAM user from all the groups they are a member of.

    :param username: The username of the IAM user to remove from all groups.
    """
    # Create an IAM client
    iam_client = boto3.client('iam')

    try:
        # List groups the user is a member of
        response = iam_client.list_groups_for_user(UserName=username)
        groups = response['Groups']

        if not groups:
            print(f"The user '{username}' is not a member of any groups.")
            return

        # Remove the user from each group
        for group in groups:
            group_name = group['GroupName']
            iam_client.remove_user_from_group(GroupName=group_name, UserName=username)
            print(f"Removed user '{username}' from group '{group_name}'.")

    except Exception as e:
        print(f"An error occurred while removing the user from groups: {e}")


def attach_user_to_group(username, group_name):
    """
    Attach the given IAM user to a specific group.

    :param username: The username of the IAM user to attach to the group.
    :param group_name: The name of the IAM group to attach the user to.
    """
    # Create an IAM client
    iam_client = boto3.client('iam')

    try:
        # Add the user to the specified group
        iam_client.add_user_to_group(GroupName=group_name, UserName=username)
        print(f"Added user '{username}' to group '{group_name}'.")

    except Exception as e:
        print(f"An error occurred while adding the user to the group: {e}")


def disable_aws_access_key(username):
    """
    Disable all active access keys of a given IAM user.

    :param username: The username of the IAM user whose access keys need to be disabled.
    """
    # Create an IAM client
    iam_client = boto3.client('iam')

    try:
        # List access keys for the specified user
        response = iam_client.list_access_keys(UserName=username)
        access_keys = response['AccessKeyMetadata']

        if not access_keys:
            print(f"No access keys found for user: {username}")
            return

        # Loop through all access keys and disable any that are active
        for key in access_keys:
            key_id = key['AccessKeyId']
            status = key['Status']

            if status == 'Active':
                # Disable the access key
                iam_client.update_access_key(
                    UserName=username,
                    AccessKeyId=key_id,
                    Status='Inactive'
                )
                print(f"Disabled access key: {key_id} for user: {username}")
            else:
                print(f"Access key: {key_id} is already inactive for user: {username}")

    except Exception as e:
        print(f"An error occurred: {e}")

def enable_aws_access_key(username):
    """
    Enable all inactive access keys of a given IAM user.

    :param username: The username of the IAM user whose access keys need to be enabled.
    """
    # Create an IAM client
    iam_client = boto3.client('iam')

    try:
        # List access keys for the specified user
        response = iam_client.list_access_keys(UserName=username)
        access_keys = response['AccessKeyMetadata']

        if not access_keys:
            print(f"No access keys found for user: {username}")
            return

        # Loop through all access keys and enable any that are inactive
        for key in access_keys:
            key_id = key['AccessKeyId']
            status = key['Status']

            if status == 'Inactive':
                # Enable the access key
                iam_client.update_access_key(
                    UserName=username,
                    AccessKeyId=key_id,
                    Status='Active'
                )
                print(f"Enabled access key: {key_id} for user: {username}")
            else:
                print(f"Access key: {key_id} is already active for user: {username}")

    except Exception as e:
        print(f"An error occurred: {e}")


def get_customer_managed_policies():
    # Initialize the IAM client
    iam = boto3.client('iam')

    # List Customer Managed Policies
    policies_data = []
    paginator = iam.get_paginator('list_policies')
    response_iterator = paginator.paginate(Scope='Local')

    try:
        for page in response_iterator:
            for policy in page['Policies']:
                # Fetch policy metadata
                policy_name = policy['PolicyName']
                policy_arn = policy['Arn']
                default_version_id = policy['DefaultVersionId']
                create_date = policy['CreateDate']
                update_date = policy['UpdateDate']
                attachment_count = policy['AttachmentCount']

                # Fetch policy document
                version_response = iam.get_policy_version(
                    PolicyArn=policy_arn,
                    VersionId=default_version_id
                )
                policy_document = json.dumps(version_response['PolicyVersion']['Document'], indent=4)

                # Add data to the list
                policies_data.append({
                    "PolicyName": policy_name,
                    "PolicyArn": policy_arn,
#                    "DefaultVersionId": default_version_id,
#                    "CreateDate": create_date,
                    "UpdateDate": update_date,
#                    "AttachmentCount": attachment_count,
#                    "PolicyDocument": policy_document
                })

    except Exception as e:
        print(f"Error retrieving policies: {e}")

    # Convert to Pandas DataFrame
    df = pd.DataFrame(policies_data)
    return df

import boto3
import pandas as pd
import json


def get_all_policies():
    """
    Fetch all policies (Customer Managed and AWS Managed)
    and return as a Pandas DataFrame.
    """
    iam = boto3.client('iam')

    policies_data = []
    paginator = iam.get_paginator('list_policies')

    # Fetch both AWS Managed and Customer Managed Policies
    for scope in ['AWS', 'Local']:
        response_iterator = paginator.paginate(Scope=scope)
        for page in response_iterator:
            for policy in page['Policies']:
                policies_data.append({
                    "PolicyName": policy['PolicyName'],
                    "PolicyArn": policy['Arn'],
#                    "DefaultVersionId": policy['DefaultVersionId'],
                    "Scope": scope,
#                    "CreateDate": policy['CreateDate'],
                    "UpdateDate": policy['UpdateDate'],
#                    "AttachmentCount": policy['AttachmentCount']
                })

    # Convert to Pandas DataFrame
    df = pd.DataFrame(policies_data)
    return df


def query_policies_by_name(partial_name):
    """
    Query policies by part of their name (case-insensitive).
    Returns a Pandas DataFrame of matched policies.
    """
    # Fetch all policies
    df = get_all_policies()

    # Filter policies by partial name (case-insensitive)
    filtered_df = df[df['PolicyName'].str.contains(partial_name, case=False, na=False)]

    return filtered_df

def get_policy_json_by_arn(policy_arn, file_path=None):
    """
    Fetch and display/save the JSON document of a policy by its ARN.

    :param policy_arn: The ARN of the policy.
    :param file_path: Optional file path to save the policy JSON document.
    """
    # Initialize the IAM client
    iam = boto3.client('iam')

    try:
        # Get policy details to retrieve the default version ID
        policy_details = iam.get_policy(PolicyArn=policy_arn)
        default_version_id = policy_details['Policy']['DefaultVersionId']

        # Fetch the policy document of the default version
        version_response = iam.get_policy_version(
            PolicyArn=policy_arn,
            VersionId=default_version_id
        )
        policy_document = version_response['PolicyVersion']['Document']

        # Print the policy JSON document
        print("\nPolicy JSON Document:")
        print(json.dumps(policy_document, indent=4))

        # Save the policy JSON document to a file if file_path is provided
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(policy_document, file, indent=4)
            print(f"\nPolicy JSON has been saved to '{file_path}'")

        # Optionally return the JSON document
        return policy_document

    except Exception as e:
        print(f"Error retrieving policy JSON: {e}")
        return None

