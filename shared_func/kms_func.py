import boto3
from shared_func.create_boto3_session_from_json import create_boto3_session
import config

session = create_boto3_session(
        json_file_path = config.path_boto3_cred
        )

def encrypt_string(secret, key_alias=config.kms_key_alias, session=session):
    """
    Encrypts a string using AWS KMS and returns the encrypted secret.

    Parameters:
    - secret (str): The secret string to encrypt.
    - key_alias (str): The KMS key alias to use for encryption.

    Returns:
    - bytes: The encrypted secret.
    """
    # Initialize a session using Amazon KMS
    kms_client = session.client('kms')

    # Encrypt the secret using a KMS key
    response = kms_client.encrypt(
        KeyId=f'alias/{key_alias}',
        Plaintext=secret.encode('utf-8')
    )

    # The encrypted secret
    encrypted_secret = response['CiphertextBlob']

    return encrypted_secret

def decrypt_string(encrypted_secret, session=session, key_alias=config.kms_key_alias):
    """
    Decrypts an encrypted string using AWS KMS and returns the decrypted secret.

    Parameters:
    - encrypted_secret (bytes): The encrypted secret to decrypt.
    - session (boto3.session.Session): The boto3 session to use.
    - key_alias (str): The KMS key alias used for decryption (not directly used in decryption but for context).

    Returns:
    - str: The decrypted secret.
    """
    # Initialize a session using Amazon KMS
    kms_client = session.client('kms')

    # Decrypt the secret using KMS
    response = kms_client.decrypt(
        CiphertextBlob=encrypted_secret
    )

    # The decrypted secret
    decrypted_secret = response['Plaintext'].decode('utf-8')

    return decrypted_secret

def encrypt_file(file_path, output_path, key_alias=config.kms_key_alias, session=session):
    """
    Encrypts a file using AWS KMS and saves the encrypted content to an output file.

    Parameters:
    - file_path (str): The path to the file to encrypt.
    - output_path (str): The path to save the encrypted file.
    - key_alias (str): The KMS key alias to use for encryption.
    - session (boto3.session.Session): The boto3 session to use. Defaults to session.
    """
    # Initialize a session using Amazon KMS
    kms_client = session.client('kms')

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

def decrypt_file(encrypted_file_path, output_path, session=session):
    """
    Decrypts an encrypted file using AWS KMS and saves the decrypted content to an output file.

    Parameters:
    - encrypted_file_path (str): The path to the encrypted file.
    - output_path (str): The path to save the decrypted file.
    - session (boto3.session.Session): The boto3 session to use. Defaults to session.
    """
    # Initialize a session using Amazon KMS
    kms_client = session.client('kms')

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

