import subprocess
import json
import boto3

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

def create_iam_user(username):
    # Create an IAM client
    iam = boto3.client('iam')

    # Create the IAM user
    iam.create_user(UserName=username)
    print(f"IAM User '{username}' created.")

def generate_random_password(length=12):
    # Define the character set for the password
    password_chars = string.ascii_letters + string.digits + string.punctuation

    # Generate a random password
    password = ''.join(secrets.choice(password_chars) for i in range(length))

    print(f"Generated random password: {password}")

    return password

def enable_login_profile(username):
    # Create an IAM client
    iam = boto3.client('iam')

    # Generate a random password
    password = generate_random_password()

    # Create the login profile with the random password
    iam.create_login_profile(UserName=username, Password=password)
    print(f"Login profile for '{username}' enabled with a random password.")

    return password

