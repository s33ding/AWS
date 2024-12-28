import json
import os
import subprocess
import config
import getpass

duration_mfa_sec = str(config.duration_mfa_sec)

def get_aws_key_choice():
    """Prompt the user to select an AWS key."""
    print("☁️  Select an AWS key:")
    print("  0) Work AWS key")
    print("  1) Personal AWS key")
    choice = input("> ")
    if choice == "0":
        return os.getenv("AWS_KEY_MAIN")
    elif choice == "1":
        return os.getenv("AWS_KEY2")
    else:
        print("Invalid choice. Exiting.")
        exit(1)

def read_aws_key_file(aws_key_path):
    """Read the AWS key file and return the parsed JSON data."""
    with open(aws_key_path, "r") as f:
        return json.load(f)

def write_credentials_file(id, secret, token=None):
    """Write AWS credentials to the ~/.aws/credentials file."""
    credentials_path = os.path.expanduser("~/.aws/credentials")
    os.makedirs(os.path.dirname(credentials_path), exist_ok=True)

    with open(credentials_path, "w") as f:
        f.write("[default]\n")
        f.write(f"aws_access_key_id = {id}\n")
        f.write(f"aws_secret_access_key = {secret}\n")
        if token:
            f.write(f"aws_session_token = {token}\n")

def get_temporary_credentials(arn, token):
    """Use AWS CLI to get temporary credentials."""
    cmd = [
        "aws",
        "sts",
        "get-session-token",
        "--duration-seconds", duration_mfa_sec,
        "--serial-number", arn,
        "--token-code", token,
        "--output", "json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error getting session token:", result.stderr)
        exit(1)

    return json.loads(result.stdout)

def write_temp_credentials_to_file(temp_credentials, file_path):
    """Write temporary credentials as JSON to a specified file."""
    with open(file_path, "w") as f:
        json.dump(temp_credentials, f, indent=2)

def main():
    """Main function to manage AWS credentials."""
    aws_key_path = get_aws_key_choice()
    aws_data = read_aws_key_file(aws_key_path)

    aws_id = aws_data.get("id")
    aws_secret = aws_data.get("secret")
    aws_arn = aws_data.get("arn")
    print(f"id: {aws_id}")

    # Write initial credentials
    write_credentials_file(aws_id, aws_secret)


    # Prompt for MFA token
    token = getpass.getpass('☁️  TOKEN: ')

    # Get temporary credentials
    temp_creds = get_temporary_credentials(aws_arn, token)

    temp_id = temp_creds["Credentials"]["AccessKeyId"]
    temp_secret = temp_creds["Credentials"]["SecretAccessKey"]
    temp_token = temp_creds["Credentials"]["SessionToken"]

    # Write temporary credentials to file
    temp_credentials_json = {
        "id": temp_id,
        "secret": temp_secret,
        "token": temp_token
    }
    temp_credentials_path = os.getenv("AWS_TEMP_CRED", "aws_temp_cred.json")
    write_temp_credentials_to_file(temp_credentials_json, temp_credentials_path)

    # Update the credentials file with temporary credentials
    write_credentials_file(temp_id, temp_secret, temp_token)

    # Display success message
    print("Access granted.")
    print("May the Python be with you! 🚀🐍🔥")

    # Use AWS CLI with temporary credentials
    subprocess.run(["aws", "s3", "ls"])

if __name__ == "__main__":
    main()

