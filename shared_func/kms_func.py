import boto3
import config

def enable_key_rotation(alias_name):
    """
    Enables automatic key rotation for the specified KMS key using its alias.

    Parameters:
        alias_name (str): The alias of the KMS key (e.g., 'alias/my-key').

    Returns:
        str: Success message if rotation is enabled, error message otherwise.
    """
    # Create a KMS client
    kms_client = boto3.client('kms')

    try:
        # Get the Key ID from the alias
        response = kms_client.describe_key(KeyId=alias_name)
        key_id = response['KeyMetadata']['KeyId']

        # Enable key rotation
        kms_client.enable_key_rotation(KeyId=key_id)
        return f"Key rotation enabled successfully for alias: {alias_name}"
    except ClientError as e:
        return f"Failed to enable key rotation for alias: {alias_name}. Error: {e}"

def encrypt_string(secret, key_alias=config.kms_key_alias):
    """
    Encrypts a string using AWS KMS and returns the encrypted secret.

    Parameters:
    - secret (str): The secret string to encrypt.
    - key_alias (str): The KMS key alias to use for encryption.

    Returns:
    - bytes: The encrypted secret.
    """
    # Initialize a boto3 using Amazon KMS
    kms_client = boto3.client('kms')

    # Encrypt the secret using a KMS key
    response = kms_client.encrypt(
        KeyId=f'alias/{key_alias}',
        Plaintext=secret.encode('utf-8')
    )

    # The encrypted secret
    encrypted_secret = response['CiphertextBlob']

    return encrypted_secret

def decrypt_string(encrypted_secret, key_alias=config.kms_key_alias):
    """
    Decrypts an encrypted string using AWS KMS and returns the decrypted secret.

    Parameters:
    - encrypted_secret (bytes): The encrypted secret to decrypt.
    - boto3 (boto3.boto3.Session): The boto3 boto3 to use.
    - key_alias (str): The KMS key alias used for decryption (not directly used in decryption but for context).

    Returns:
    - str: The decrypted secret.
    """
    # Initialize a boto3 using Amazon KMS
    kms_client = boto3.client('kms')

    # Decrypt the secret using KMS
    response = kms_client.decrypt(
        CiphertextBlob=encrypted_secret
    )

    # The decrypted secret
    decrypted_secret = response['Plaintext'].decode('utf-8')

    return decrypted_secret

def encrypt_file(file_path, output_path, key_alias=config.kms_key_alias):
    """
    Encrypts a file using AWS KMS and saves the encrypted content to an output file.

    Parameters:
    - file_path (str): The path to the file to encrypt.
    - output_path (str): The path to save the encrypted file.
    - key_alias (str): The KMS key alias to use for encryption.
    """
    # Initialize a boto3 using Amazon KMS
    kms_client = boto3.client('kms')

    # Read the file content
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # Encrypt the file content using a KMS key
    response = kms_client.encrypt(
        KeyId=f'alias/{key_alias}',
        Plaintext=file_content
    )

    # The encrypted content
    encrypted_content = response['CiphertextBlob']

    # Write the encrypted content to the output file
    with open(output_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_content)

def decrypt_file(encrypted_file_path, output_path):
    """
    Decrypts an encrypted file using AWS KMS and saves the decrypted content to an output file.

    Parameters:
    - encrypted_file_path (str): The path to the encrypted file.
    - output_path (str): The path to save the decrypted file.
    """
    # Initialize a boto3 using Amazon KMS
    kms_client = boto3.client('kms')

    # Read the encrypted file content
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_content = encrypted_file.read()

    # Decrypt the file content using KMS
    response = kms_client.decrypt(
        CiphertextBlob=encrypted_content
    )

    # The decrypted content
    decrypted_content = response['Plaintext']

    # Write the decrypted content to the output file
    with open(output_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_content)




def create_kms_key(description, alias_name, key_usage='ENCRYPT_DECRYPT', key_spec='SYMMETRIC_DEFAULT'):
    """
    Create a KMS key in AWS and set an alias for it.

    :param description: A description for the KMS key.
    :param alias_name: The alias to associate with the KMS key (e.g., "alias/my-key").
    :param key_usage: The key usage. Defaults to 'ENCRYPT_DECRYPT'.
    :param key_spec: The key specification. Defaults to 'SYMMETRIC_DEFAULT'.
    :return: The key ID of the created KMS key.
    """
    try:
        # Initialize a KMS client
        kms_client = boto3.client('kms')

        # Create the KMS key
        response = kms_client.create_key(
            Description=description,
            KeyUsage=key_usage,
            KeySpec=key_spec
        )

        # Extract the Key ID from the response
        key_id = response['KeyMetadata']['KeyId']
        print(f"KMS key created successfully with Key ID: {key_id}")

        # Create an alias for the key
        kms_client.create_alias(
            AliasName=alias_name,
            TargetKeyId=key_id
        )
        print(f"Alias '{alias_name}' created successfully for Key ID: {key_id}")

        return key_id
    except Exception as e:
        print(f"erro:",e)


def delete_kms_key(key_id):
    """
    Schedule the deletion of a KMS key.

    :param key_id: The ID of the KMS key to delete.
    :return: The deletion date of the KMS key.
    """
    try:
        # Initialize a KMS client
        kms_client = boto3.client('kms')

        # Schedule the deletion of the KMS key
        response = kms_client.schedule_key_deletion(
            KeyId=key_id,
            PendingWindowInDays=7  # Default to 7 days
        )

        # Extract the deletion date from the response
        deletion_date = response['DeletionDate']
        print(f"KMS key with Key ID {key_id} scheduled for deletion on {deletion_date}")

        return deletion_date

    except Exception as e:
        print(f"An error occurred while scheduling the deletion of the KMS key: {e}")
        raise

def list_kms_keys():
    """
    List all KMS keys with their names in the account.

    :return: A list of dictionaries with Key IDs and their aliases.
    """
    try:
        # Initialize a KMS client
        kms_client = boto3.client('kms')

        # List the KMS keys
        keys = []
        response = kms_client.list_keys()

        while True:
            for key in response['Keys']:
                key_id = key['KeyId']
                aliases_response = kms_client.list_aliases(KeyId=key_id)

                # Find the alias for the key
                alias_name = next((alias['AliasName'] for alias in aliases_response['Aliases'] if alias['AliasName'] != 'alias/aws/ebs'), None)
                keys.append({'KeyId': key_id, 'AliasName': alias_name})

            # Check if there are more keys to list
            if 'NextMarker' in response and response['Truncated']:
                response = kms_client.list_keys(Marker=response['NextMarker'])
            else:
                break

        print(f"Retrieved {len(keys)} KMS keys with their aliases.")
        return keys

    except Exception as e:
        print(f"An error occurred while listing the KMS keys with their aliases: {e}")
        raise
